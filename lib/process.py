#!/usr/bin/env python3
"""
Data processing utilities for calculating energy shares.
"""

from datetime import datetime, timedelta
from collections import defaultdict
from typing import Dict, List, Tuple, Any


# Fuel technology categories
FOSSILS = [
    'gas_recip', 'gas_ocgt', 'gas_ccgt', 'gas_steam', 
    'gas_lfg', 'gas_wcmg', 'distillate', 'coal_brown', 'coal_black'
]

RENEWABLES = [
    'solar_utility', 'solar_rooftop', 'wind', 'hydro', 
    'bioenergy_biomass', 'bioenergy_biogas'
]


def parse_date(date_str: str) -> Tuple[int, int]:
    """
    Parse date string to (year, month) tuple.
    
    Args:
        date_str: ISO format date string
    
    Returns:
        Tuple of (year, month)
    """
    dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    return (dt.year, dt.month)


def format_date(year: int, month: int) -> str:
    """
    Format date as YYYY-MM.
    
    Args:
        year: Year
        month: Month
    
    Returns:
        Formatted date string
    """
    return f"{year:04d}-{month:02d}"


def extract_energy_data(api_response: Dict[str, Any], interval: str = 'month') -> Dict[Any, Dict[str, float]]:
    """
    Extract energy data by fuel technology from API response.
    
    Args:
        api_response: Raw API response (with 'data' field containing list of series)
        interval: 'month' or 'day' to determine date key format
    
    Returns:
        Dictionary mapping date keys to fuel tech energy values
        - For monthly: keys are (year, month) tuples
        - For daily: keys are 'YYYY-MM-DD' strings
    """
    from datetime import timedelta
    
    energy_data = defaultdict(lambda: defaultdict(float))
    
    print(f"Processing {interval}ly fuel technology data...")
    
    # Handle wrapped API response
    if isinstance(api_response, dict) and 'data' in api_response:
        data_series = api_response['data']
    else:
        data_series = api_response if isinstance(api_response, list) else []
    
    # Process each series
    for series in data_series:
        if not isinstance(series, dict):
            continue
            
        # Extract fuel_tech from id (format: au.nem.fuel_tech.{fuel_tech}.energy)
        series_id = series.get('id', '')
        parts = series_id.split('.')
        
        # Only process energy data (not emissions or market_value)
        if len(parts) >= 5 and parts[2] == 'fuel_tech' and parts[4] == 'energy':
            fuel_tech = parts[3]
            
            # Exclude pumps and battery_charging (they're consumption, not generation)
            if fuel_tech in ['pumps', 'battery_charging']:
                continue
            
            # Get history data
            history = series.get('history', {})
            
            # Handle array format with start date
            if isinstance(history, dict) and 'data' in history and 'start' in history:
                start_date = datetime.fromisoformat(history['start'].replace('Z', '+00:00'))
                data_array = history['data']
                data_interval = history.get('interval', '1M' if interval == 'month' else '1D')
                
                # Process each data point
                for i, value in enumerate(data_array):
                    if value is not None:  # Skip null values
                        # Calculate the date for this data point
                        if data_interval == '1M' or interval == 'month':
                            # Monthly intervals
                            month_offset = start_date.month + i
                            year_offset = (month_offset - 1) // 12
                            month = ((month_offset - 1) % 12) + 1
                            year = start_date.year + year_offset
                            date_key = (year, month)
                        else:
                            # Daily intervals
                            current_date = start_date + timedelta(days=i)
                            date_key = current_date.strftime('%Y-%m-%d')
                        
                        energy_data[date_key][fuel_tech] = value
    
    return energy_data


def extract_monthly_data(api_response: Dict[str, Any]) -> Dict[Tuple[int, int], Dict[str, float]]:
    """
    Extract monthly energy data by fuel technology from API response.
    Wrapper for backward compatibility.
    """
    return extract_energy_data(api_response, interval='month')


def calculate_monthly_rolling_averages(
    monthly_data: Dict[Tuple[int, int], Dict[str, float]], 
    window_size: int = 12
) -> Tuple[List[str], List[float], List[float]]:
    """
    Calculate monthly rolling averages for fossil and renewable energy shares.
    
    Args:
        monthly_data: Monthly energy data by fuel technology
        window_size: Size of rolling window in months (default 12)
    
    Returns:
        Tuple of (dates, fossil_shares, renewable_shares) as lists
    """
    # Sort dates
    sorted_dates = sorted(monthly_data.keys())
    
    if not sorted_dates:
        print("Warning: No data found to process")
        return [], [], []
    
    print(f"Found data for {len(sorted_dates)} months from {format_date(*sorted_dates[0])} to {format_date(*sorted_dates[-1])}")
    
    dates = []
    fossil_shares = []
    renewable_shares = []
    
    # Need at least window_size months of data for rolling average
    for i in range(window_size - 1, len(sorted_dates)):
        # Get window of data
        window_dates = sorted_dates[i - window_size + 1:i + 1]
        
        fossil_sum = 0
        renewable_sum = 0
        total_sum = 0
        
        for date in window_dates:
            month_data = monthly_data[date]
            
            # Sum ALL generation for total
            for fuel_tech, value in month_data.items():
                total_sum += value
                
                # Also categorize into fossil/renewable
                if fuel_tech in FOSSILS:
                    fossil_sum += value
                elif fuel_tech in RENEWABLES:
                    renewable_sum += value
        
        # Calculate shares as percentage of TOTAL generation (including batteries, etc.)
        if total_sum > 0:
            fossil_share = (fossil_sum / total_sum) * 100
            renewable_share = (renewable_sum / total_sum) * 100
            
            # Format date
            year, month = sorted_dates[i]
            date_str = format_date(year, month)
            
            # Append to lists
            dates.append(date_str)
            fossil_shares.append(fossil_share)
            renewable_shares.append(renewable_share)
    
    print(f"Calculated shares for {len(dates)} months")
    
    return dates, fossil_shares, renewable_shares


def calculate_last_year_average() -> Tuple[float, float]:
    """
    Fetch daily data and calculate fossil/renewable shares for 
    the last full year (ending yesterday). Handles leap years automatically.
    
    Returns:
        Tuple of (fossil_share, renewable_share) as percentages
    """
    from lib.read import fetch_daily_energy_data
    from datetime import date, timedelta
    
    # Calculate date range: one year ago through yesterday
    yesterday = date.today() - timedelta(days=1)
    # Go back exactly one year from yesterday, then add one day to get the start
    # This gives us a full year including yesterday
    one_year_ago = yesterday.replace(year=yesterday.year - 1)
    start_date = one_year_ago + timedelta(days=1)
    
    # Get years we need to fetch
    years_needed = set([start_date.year, yesterday.year])
    
    print(f"Fetching daily data for years: {', '.join(map(str, sorted(years_needed)))}")
    
    # Fetch data for all needed years
    all_daily_data = {}
    for year in years_needed:
        data = fetch_daily_energy_data(year)
        daily_data = extract_energy_data(data, interval='day')
        all_daily_data.update(daily_data)
    
    # Filter to our exact date range
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = yesterday.strftime('%Y-%m-%d')
    
    window_dates = [
        date_str for date_str in sorted(all_daily_data.keys())
        if start_date_str <= date_str <= end_date_str
    ]
    
    print(f"Using {len(window_dates)} days from {window_dates[0]} to {window_dates[-1]}")
    
    # Calculate totals for the window
    fossil_sum = 0
    renewable_sum = 0
    total_sum = 0
    
    for date in window_dates:
        date_data = all_daily_data[date]
        
        # Sum ALL generation for total
        for fuel_tech, value in date_data.items():
            total_sum += value
            
            # Also categorize into fossil/renewable
            if fuel_tech in FOSSILS:
                fossil_sum += value
            elif fuel_tech in RENEWABLES:
                renewable_sum += value
    
    # Calculate shares as percentage of TOTAL generation
    if total_sum > 0:
        fossil_share = (fossil_sum / total_sum) * 100
        renewable_share = (renewable_sum / total_sum) * 100
        
        print(f"\nOne-year totals ({len(window_dates)} days):")
        print(f"  Fossil:     {fossil_sum:,.2f} GWh")
        print(f"  Renewable:  {renewable_sum:,.2f} GWh")
        print(f"  Total:      {total_sum:,.2f} GWh")
        print(f"\nOne-year shares:")
        print(f"  Fossil:     {fossil_share:.4f}%")
        print(f"  Renewable:  {renewable_share:.4f}%")
        print(f"  Sum:        {fossil_share + renewable_share:.2f}% (of total generation)")
        
        return fossil_share, renewable_share
    
    return 0, 0


def process_monthly_energy_data(data: Dict[str, Any], window_size: int = 12) -> Tuple[List[str], List[float], List[float]]:
    """
    Process monthly energy data to calculate rolling average energy shares.
    
    Args:
        data: Raw monthly API response data
        window_size: Rolling average window size in months
    
    Returns:
        Tuple of (dates, fossil_shares, renewable_shares) as lists
    """
    # Extract monthly data
    monthly_data = extract_monthly_data(data)
    
    # Calculate monthly rolling averages
    return calculate_monthly_rolling_averages(monthly_data, window_size)
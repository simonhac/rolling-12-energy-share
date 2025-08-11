#!/usr/bin/env python3
"""
OpenNEM API v4 compliant output formatter
Based on specification from https://github.com/opennem/opennem/issues/446
"""

import math
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Union


def format_precision(value: float, min_sig_figs: int = 4) -> Union[int, float]:
    """
    Format number according to OpenNEM precision rules:
    - Maintain minimum significant figures (default 4)
    - Preserve all digits left of decimal point
    - Include decimals only when precision is needed
    - Remove trailing zeros after decimal place
    
    Examples:
    - 1234.5678 → 1235
    - 123.456 → 123.5
    - 1000.0 → 1000
    - 12.3456 → 12.35
    - 0.123456 → 0.1235
    """
    if value == 0:
        return 0
    
    # Calculate the order of magnitude
    magnitude = math.floor(math.log10(abs(value)))
    
    # Round to specified significant figures
    rounded = round(value, -int(magnitude) + min_sig_figs - 1)
    
    # If it's an integer, return as int
    if rounded == int(rounded):
        return int(rounded)
    
    # Format with appropriate decimal places, removing trailing zeros
    str_val = f"{rounded:.10f}".rstrip('0').rstrip('.')
    return float(str_val)


def format_date_precision(date: Union[str, datetime], precision: str = "month") -> str:
    """
    Format date according to OpenNEM ISO8601 reduced precision format.
    
    Args:
        date: Date string or datetime object
        precision: One of "year", "month", "day", "hour", "minute"
    
    Returns:
        ISO8601 formatted string with reduced precision
    """
    if isinstance(date, str):
        # Parse various date formats
        if len(date) == 4:  # YYYY
            dt = datetime.strptime(date, "%Y")
        elif len(date) == 7:  # YYYY-MM
            dt = datetime.strptime(date, "%Y-%m")
        elif len(date) == 10:  # YYYY-MM-DD
            dt = datetime.strptime(date, "%Y-%m-%d")
        else:
            # Try ISO format with timezone
            try:
                dt = datetime.fromisoformat(date.replace('Z', '+00:00'))
            except ValueError:
                # Fallback to parsing common formats
                for fmt in ["%Y-%m-%d", "%Y-%m", "%Y"]:
                    try:
                        dt = datetime.strptime(date, fmt)
                        break
                    except ValueError:
                        continue
                else:
                    raise ValueError(f"Unable to parse date: {date}")
    else:
        dt = date
    
    if precision == "year":
        return f"{dt.year:04d}"
    elif precision == "month":
        return f"{dt.year:04d}-{dt.month:02d}"
    elif precision == "day":
        return f"{dt.year:04d}-{dt.month:02d}-{dt.day:02d}"
    elif precision == "hour":
        return f"{dt.year:04d}-{dt.month:02d}-{dt.day:02d}T{dt.hour:02d}"
    elif precision == "minute":
        return f"{dt.year:04d}-{dt.month:02d}-{dt.day:02d}T{dt.hour:02d}:{dt.minute:02d}"
    else:
        # Full ISO format
        return dt.isoformat()


def create_data_series(
    series_id: str,
    dates: List[str],
    values: List[Union[int, float]],
    data_type: str = "history",
    units: Optional[str] = None,
    interval: str = "1M",
    network: str = "NEM",
    **kwargs
) -> Dict[str, Any]:
    """
    Create a data series in OpenNEM v4 format with array structure.
    
    Args:
        series_id: Unique identifier for the series
        dates: List of date strings
        values: List of numeric values
        data_type: Type of data (e.g., "history", "forecast")
        units: Unit of measurement (e.g., "MW", "MWh", "%")
        interval: Data interval (e.g., "1M" for monthly, "1D" for daily)
        network: Network code (default "NEM")
        **kwargs: Additional metadata fields
    
    Returns:
        Dictionary in OpenNEM v4 format with array structure
    """
    # Format values with proper precision
    formatted_values = [
        format_precision(v) if isinstance(v, (int, float)) else v 
        for v in values
    ]
    
    # Get start and last dates
    start_date = dates[0] if dates else None
    last_date = dates[-1] if dates else None
    
    # Build the series object with OpenNEM v4 format
    series = {
        "id": series_id,
        "type": data_type,
        "units": units,
        "history": {
            "start": start_date,
            "last": last_date,
            "interval": interval,
            "data": formatted_values
        }
    }
    
    # Add optional fields
    if network:
        series["network"] = network
    
    # Add any additional metadata
    for key, value in kwargs.items():
        if value is not None:
            series[key] = value
    
    return series


def create_opennem_response(
    data_series: List[Dict[str, Any]],
    response_type: str = "energy",
    version: str = "v4",
    network: str = "NEM",
    created_at: Optional[datetime] = None,
    **metadata
) -> Dict[str, Any]:
    """
    Create a complete OpenNEM API v4 response.
    
    Args:
        data_series: List of data series objects
        response_type: Type of response (e.g., "energy", "power")
        version: API version
        network: Network code
        created_at: Response creation timestamp
        **metadata: Additional metadata fields
    
    Returns:
        Complete OpenNEM v4 API response
    """
    if created_at is None:
        # Use +10 timezone (Australian Eastern Standard Time)
        tz_plus10 = timezone(timedelta(hours=10))
        created_at = datetime.now(tz_plus10)
    
    response = {
        "type": response_type,
        "version": version,
        "network": network,
        "created_at": created_at.replace(microsecond=0).isoformat(),
        "data": data_series
    }
    
    # Add any additional metadata
    for key, value in metadata.items():
        if value is not None:
            response[key] = value
    
    return response
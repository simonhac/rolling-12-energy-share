#!/usr/bin/env python3
"""
Main script to process Australian electricity data and calculate 
fossil vs renewable energy shares using 12-month rolling averages.
"""

from datetime import date
from lib.read import fetch_monthly_energy_data, save_raw_data
from lib.process import process_monthly_energy_data, calculate_last_year_average
from lib.write import ensure_output_directory, save_processed_data, print_summary


def main():
    """Main orchestration function."""
    
    # Ensure output directory exists
    ensure_output_directory()
    
    # Step 1: Read - Fetch monthly data from API
    print("Step 1: Fetching monthly data from OpenElectricity API...")
    data = fetch_monthly_energy_data(region="_all")
    
    # Save raw data
    raw_filepath = "output/raw.json"
    save_raw_data(data, raw_filepath)
    
    # Step 2: Process - Calculate rolling averages
    print("\nStep 2: Processing monthly data...")
    dates, fossil_shares, renewable_shares = process_monthly_energy_data(data, window_size=12)
    
    if not dates:
        print("Error: No data was processed. Please check the API response structure.")
        return
    
    # Step 2b: Add current month estimate based on last year of daily data
    print("\nStep 2b: Calculating current month estimate from daily data...")
    fossil_ytd, renewable_ytd = calculate_last_year_average()
    
    # Add current month to the data
    current_month = f"{date.today().year:04d}-{date.today().month:02d}"
    dates.append(current_month)
    fossil_shares.append(fossil_ytd)
    renewable_shares.append(renewable_ytd)
    
    print(f"Added estimate for {current_month}: Fossil {fossil_ytd:.2f}%, Renewable {renewable_ytd:.2f}%")
    
    # Step 3: Write - Save processed data
    print("\nStep 3: Writing output...")
    processed_filepath = "output/processed.json"
    notes = f"Shares calculated as percentage of total generation including all sources. Last value ({current_month}) is an estimate based on 12 months to yesterday"
    save_processed_data(
        dates, 
        fossil_shares, 
        renewable_shares, 
        processed_filepath,
        fossil_description="12-month rolling average of fossil fuel share of total generation",
        renewable_description="12-month rolling average of renewable energy share of total generation",
        source="nemweb",
        data_type="energy_share",
        notes=notes
    )
    
    # Print summary
    print_summary(dates, fossil_shares, renewable_shares)
    
    print("\n✅ Processing complete!")
    print(f"   Raw data: {raw_filepath}")
    print(f"   Processed data: {processed_filepath}")


if __name__ == "__main__":
    main()
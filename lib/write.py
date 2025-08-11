#!/usr/bin/env python3
"""
Data writing and output utilities.
"""

import json
import os
from typing import Dict, List, Any

from .format import create_data_series, create_opennem_response


def ensure_output_directory(directory: str = "output") -> None:
    """
    Ensure the output directory exists.
    
    Args:
        directory: Name of the output directory
    """
    os.makedirs(directory, exist_ok=True)
    print(f"Output directory '{directory}' is ready")


def save_processed_data(
    dates: List[str],
    fossil_shares: List[float],
    renewable_shares: List[float],
    filepath: str,
    fossil_description: str,
    renewable_description: str,
    source: str,
    data_type: str,
    notes: str = None
) -> None:
    """
    Save processed energy share data in OpenNEM format.
    
    Args:
        dates: List of date strings
        fossil_shares: List of fossil share percentages
        renewable_shares: List of renewable share percentages
        filepath: Path to save the output file
        fossil_description: Description for fossil series
        renewable_description: Description for renewable series
        source: Data source
        data_type: Type for the data series (e.g., "energy_share")
        notes: Optional notes about the data
    """
    # Prepare note text if provided
    combined_note = notes if notes else None
    
    # Create data series for fossils
    fossil_series = create_data_series(
        series_id="au.nem.fuel_tech_group.fossils.energy_share",
        dates=dates,
        values=fossil_shares,
        units="%",
        interval="1M",  # OpenNEM format for monthly interval
        network="NEM",
        data_type=data_type,
        source=source,
        description=fossil_description,
        note=combined_note
    )
    
    # Create data series for renewables
    renewable_series = create_data_series(
        series_id="au.nem.fuel_tech_group.renewables.energy_share",
        dates=dates,
        values=renewable_shares,
        units="%",
        interval="1M",  # OpenNEM format for monthly interval
        network="NEM",
        data_type=data_type,
        source=source,
        description=renewable_description,
        note=combined_note
    )
    
    # Create complete OpenNEM response
    response = create_opennem_response(
        data_series=[fossil_series, renewable_series],
        response_type="energy_share",
        version="v4",
        network="NEM"
    )
    
    # Save to file with compact data arrays
    # First convert to JSON with indentation
    json_str = json.dumps(response, indent=2)
    
    # Then compact the data arrays to single lines
    import re
    
    # Find and replace only the numerical data arrays inside "history" objects
    # This pattern specifically looks for "data" arrays that come after "interval"
    # which is a reliable indicator that this is the numerical data array
    def compact_numerical_array(match):
        # Keep everything before the array content
        prefix = match.group(1)
        # Get the array content
        array_content = match.group(2)
        # Remove whitespace and newlines within the numerical array
        compacted = re.sub(r'\s+', ' ', array_content.strip())
        return f'{prefix}[{compacted}]'
    
    # Match pattern: find "data": [ ... ] that appears after "interval": 
    # This ensures we only match the numerical data arrays inside history objects
    pattern = r'("interval":[^}]*?"data":\s*)\[([\d\s,.\-]+)\]'
    json_str = re.sub(pattern, compact_numerical_array, json_str, flags=re.DOTALL)
    
    # Write the formatted JSON
    with open(filepath, 'w') as f:
        f.write(json_str)
    
    print(f"Processed data saved to {filepath}")


def print_summary(dates: List[str], fossil_shares: List[float], renewable_shares: List[float]) -> None:
    """
    Print a summary of the processed data.
    
    Args:
        dates: List of date strings
        fossil_shares: List of fossil share percentages
        renewable_shares: List of renewable share percentages
    """
    print("\n" + "="*60)
    print("Sample data (first 5 and last 5 months):")
    print("="*60)
    
    # First 5 months
    for i in range(min(5, len(dates))):
        total = fossil_shares[i] + renewable_shares[i]
        print(f"{dates[i]}: Fossil {fossil_shares[i]:.2f}%, Renewable {renewable_shares[i]:.2f}%, Sum {total:.1f}%")
    
    # Last 5 months if we have more than 10 total
    if len(dates) > 10:
        print("...")
        for i in range(-5, 0):
            total = fossil_shares[i] + renewable_shares[i]
            print(f"{dates[i]}: Fossil {fossil_shares[i]:.2f}%, Renewable {renewable_shares[i]:.2f}%, Sum {total:.1f}%")
    
    # Note about percentages
    print("\n" + "="*60)
    print("Note: Fossil + Renewable shares sum to 100% of (fossil + renewable) generation.")
    print("This excludes storage, imports/exports, and other sources.")
    print("="*60)
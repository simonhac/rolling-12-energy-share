#!/usr/bin/env python3
"""
Data reading and fetching utilities.
"""

import json
import requests
from typing import Dict, Any


def fetch_monthly_energy_data(region: str = "_all") -> Dict[str, Any]:
    """
    Fetch monthly energy data from OpenElectricity API.
    
    Args:
        region: Region to fetch data for (default "_all" for all regions)
    
    Returns:
        Dictionary containing the API response
    """
    url = f"https://openelectricity.org.au/api/energy?region={region}"
    return fetch_from_url(url)


def fetch_daily_energy_data(year: int) -> Dict[str, Any]:
    """
    Fetch daily energy data for a specific year from OpenElectricity API.
    
    Args:
        year: Year to fetch data for (e.g., 2024, 2025)
    
    Returns:
        Dictionary containing the API response
    """
    url = f"https://data.openelectricity.org.au/v4/stats/au/NEM/energy/{year}.json"
    return fetch_from_url(url)


def fetch_from_url(url: str) -> Dict[str, Any]:
    """
    Fetch data from a given URL.
    
    Args:
        url: URL to fetch from
    
    Returns:
        Dictionary containing the API response
    """
    print(f"Fetching data from {url}")
    
    response = requests.get(url)
    response.raise_for_status()
    
    data = response.json()
    if isinstance(data, dict):
        data_count = len(data.get('data', data))
        print(f"Data fetched successfully. Found {data_count} series.")
    else:
        print(f"Data fetched successfully.")
    
    return data


def save_raw_data(data: Dict[str, Any], filepath: str) -> None:
    """
    Save raw API data to a JSON file.
    
    Args:
        data: Data dictionary to save
        filepath: Path to save the file to
    """
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"Raw data saved to {filepath}")


def load_raw_data(filepath: str) -> Dict[str, Any]:
    """
    Load raw data from a JSON file.
    
    Args:
        filepath: Path to the JSON file
    
    Returns:
        Dictionary containing the loaded data
    """
    with open(filepath, 'r') as f:
        data = json.load(f)
    print(f"Raw data loaded from {filepath}")
    return data
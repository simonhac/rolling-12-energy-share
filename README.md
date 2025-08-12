# Rolling Share Calculator for Australia's National Electricity Market

A reference implementation for calculating 12-month rolling averages of fossil fuel vs renewable energy shares in Australia's National Electricity Market (NEM).

## Purpose

This is a toy script created as a reference implementation for [opennem/opennem#447](https://github.com/opennem/opennem/issues/447). It demonstrates one approach to calculating rolling averages for energy generation shares, combining monthly historical data with current daily data to provide up-to-date estimates.

## Features

- Fetches monthly and daily electricity generation data from OpenElectricity API
- Calculates 12-month rolling average energy shares as a percentage for fossil fuel vs renewable energy generation
- Calculates current month estimate based on last-year-to-date daily data
- Outputs both monthly source (`raw.json`) and final output (`processed.json`) data in JSON format

## Usage

Run the main script:
```bash
python main.py
```

This will:
1. Fetch monthly energy data from OpenElectricity API and save to `output/raw.json`
2. Calculate 12-month rolling averages of energy share
3. Fetch daily data for current and previous year
4. Calcuate rolling averages of energy share for last 12 months
5. Create OpenNEM v4 style output data structure
6. Save result to `output/processed.json`

## Output

The script generates two JSON files in the `output/` directory:
- `raw.json`: Raw data from the API
- `processed.json`: Calculated rolling averages

## Data Source

Data is sourced from [OpenElectricity](https://openelectricity.org.au/) using the JSONs used by the UI, not from the API, avoiding the need for an API key.

## Project Structure

```
rolling-share/
├── main.py              # Main orchestration script
├── lib/
│   ├── __init__.py
│   ├── read.py         # Data fetching utilities
│   ├── process.py      # Data processing and calculations
│   ├── write.py        # Output formatting and saving
│   └── format.py       # Data formatting utilities
└── output/             # Generated output files
    ├── raw.json
    └── processed.json
```

## Sample Output

The `processed.json` file contains the calculated 12-month rolling averages in OpenNEM v4 format:

```json
{
  "type": "energy_share",
  "version": "v4",
  "network": "NEM",
  "created_at": "2025-08-12T11:08:45+10:00",
  "data": [
    {
      "id": "au.nem.fuel_tech_group.fossils.energy_share",
      "type": "energy_share",
      "units": "%",
      "history": {
        "start": "1999-11",
        "last": "2025-08",
        "interval": "1M",
        "data": [96.04, 96.14, 96.26, 96.23, 96.2, 96.23, 96.24, 96.16, 96.08, 95.97, 95.85, 95.8, 95.89, 95.97, 96.01, 96.13, 96.23, 96.29, 96.2, 96.23, 96.37, 96.56, 96.67, 96.69, 96.66, 96.6, 96.63, 96.61, 96.68, 96.78, 96.93, 97.01, 96.98, 96.99, 96.98, 97.01, 97.05, 97.09, 96.98, 96.92, 96.8, 96.69, 96.63, 96.58, 96.51, 96.34, 96.26, 96.21, 96.13, 96.11, 96.33, 96.45, 96.6, 96.67, 96.77, 96.9, 97.09, 97.29, 97.31, 97.31, 97.37, 97.45, 97.32, 97.25, 97.19, 97.06, 96.73, 96.24, 95.72, 95.24, 94.87, 94.53, 94.17, 93.7, 93.35, 93.05, 92.74, 92.45, 92.28, 92.2, 92.13, 92.19, 92.36, 92.56, 92.71, 92.96, 93.12, 93.25, 93.35, 93.41, 93.54, 93.51, 93.74, 93.87, 93.88, 93.81, 93.88, 93.86, 93.91, 94.02, 94.05, 94.13, 94.14, 94.33, 94.25, 94.21, 94.19, 94.2, 94.21, 94.24, 94.15, 94.06, 94.13, 94.15, 94.19, 94.21, 93.96, 93.56, 93.23, 93.08, 92.87, 92.66, 92.56, 92.41, 92.25, 92.05, 91.81, 91.56, 91.57, 91.46, 91.32, 91.03, 90.64, 90.21, 90.11, 89.98, 89.83, 89.84, 89.81, 89.68, 89.51, 89.66, 89.75, 89.98, 90.23, 90.54, 90.54, 90.67, 90.55, 90.42, 90.39, 90.27, 90.04, 89.61, 89.32, 89.02, 88.91, 88.71, 88.51, 88.18, 88.06, 87.87, 87.55, 87.56, 87.43, 87.29, 87.18, 86.84, 86.54, 86.26, 86.2, 86.28, 86.41, 86.48, 86.48, 86.2, 86.27, 86.72, 87.03, 87.45, 87.81, 88.22, 88.26, 88.32, 88.25, 88.16, 88.05, 88.2, 88.15, 87.74, 87.55, 87.36, 86.89, 86.25, 85.61, 85.1, 84.71, 84.51, 84.12, 83.72, 83.31, 83.2, 83.01, 82.24, 81.87, 81.78, 82.19, 82.34, 82.56, 82.72, 83.03, 83.46, 83.6, 83.5, 83.17, 83.55, 83.94, 84.17, 83.93, 83.78, 83.36, 82.9, 82.58, 82, 81.61, 81.08, 80.97, 80.84, 80.3, 79.71, 79.41, 79.16, 79.12, 78.95, 78.77, 78.62, 78.52, 78.53, 78.3, 77.98, 77.59, 77.26, 76.89, 76.62, 76.01, 75.58, 75.18, 75.02, 75.12, 74.97, 74.57, 74.08, 73.79, 73.41, 72.81, 72.29, 71.97, 71.78, 71.62, 71.29, 70.71, 70.27, 69.88, 69.45, 69.09, 68.57, 68.23, 67.76, 67.52, 67.32, 67.05, 66.58, 66.39, 66.1, 66.01, 65.94, 65.38, 64.91, 64.52, 64.29, 64.02, 63.66, 63.44, 63.11, 62.59, 62.37, 61.89, 61.22, 61.24, 61.21, 61.15, 61.08, 60.8, 60.8, 61, 61.67, 61.93, 61.82, 61.56, 61.36, 61.09, 60.82, 60.37, 59.95, 59.81, 59.53, 59.02, 58.43, 58, 57.85]
      },
      "network": "NEM",
      "source": "nemweb",
      "description": "12-month rolling average of fossil fuel share of total generation",
      "note": "Shares calculated as percentage of total generation including all sources. Last value (2025-08) is an estimate based on 12 months to yesterday"
    },
    {
      "id": "au.nem.fuel_tech_group.renewables.energy_share",
      "type": "energy_share",
      "units": "%",
      "history": {
        "start": "1999-11",
        "last": "2025-08",
        "interval": "1M",
        "data": [3.961, 3.864, 3.743, 3.769, 3.804, 3.77, 3.76, 3.835, 3.918, 4.031, 4.15, 4.202, 4.114, 4.027, 3.993, 3.866, 3.773, 3.714, 3.797, 3.769, 3.626, 3.443, 3.33, 3.312, 3.341, 3.399, 3.372, 3.392, 3.317, 3.223, 3.071, 2.988, 3.019, 3.013, 3.023, 2.994, 2.948, 2.909, 3.02, 3.077, 3.204, 3.311, 3.372, 3.424, 3.487, 3.662, 3.739, 3.786, 3.872, 3.885, 3.667, 3.547, 3.395, 3.333, 3.227, 3.096, 2.913, 2.714, 2.69, 2.686, 2.633, 2.548, 2.68, 2.748, 2.815, 2.941, 3.274, 3.761, 4.279, 4.763, 5.133, 5.466, 5.835, 6.303, 6.649, 6.953, 7.263, 7.547, 7.725, 7.804, 7.868, 7.805, 7.643, 7.442, 7.29, 7.036, 6.876, 6.745, 6.655, 6.595, 6.462, 6.49, 6.264, 6.127, 6.116, 6.186, 6.124, 6.142, 6.087, 5.983, 5.951, 5.87, 5.86, 5.668, 5.755, 5.794, 5.814, 5.797, 5.791, 5.759, 5.854, 5.941, 5.873, 5.851, 5.808, 5.791, 6.037, 6.438, 6.765, 6.919, 7.133, 7.336, 7.437, 7.592, 7.753, 7.953, 8.186, 8.445, 8.43, 8.54, 8.678, 8.971, 9.363, 9.792, 9.891, 10.02, 10.17, 10.16, 10.19, 10.32, 10.49, 10.34, 10.25, 10.02, 9.768, 9.462, 9.455, 9.328, 9.455, 9.58, 9.607, 9.733, 9.957, 10.39, 10.68, 10.98, 11.09, 11.29, 11.49, 11.82, 11.94, 12.13, 12.45, 12.44, 12.57, 12.71, 12.82, 13.16, 13.46, 13.74, 13.8, 13.72, 13.59, 13.52, 13.52, 13.8, 13.73, 13.28, 12.97, 12.55, 12.19, 11.78, 11.74, 11.68, 11.75, 11.84, 11.95, 11.8, 11.85, 12.26, 12.45, 12.64, 13.11, 13.75, 14.39, 14.9, 15.29, 15.49, 15.88, 16.28, 16.69, 16.8, 16.99, 17.76, 18.13, 18.22, 17.81, 17.66, 17.44, 17.28, 16.97, 16.54, 16.4, 16.5, 16.83, 16.45, 16.06, 15.83, 16.07, 16.21, 16.64, 17.1, 17.41, 17.99, 18.38, 18.9, 19.02, 19.15, 19.68, 20.27, 20.57, 20.82, 20.86, 21.03, 21.21, 21.35, 21.45, 21.44, 21.67, 21.99, 22.38, 22.71, 23.07, 23.35, 23.96, 24.39, 24.78, 24.95, 24.84, 25, 25.4, 25.88, 26.17, 26.55, 27.14, 27.67, 27.98, 28.17, 28.33, 28.66, 29.23, 29.67, 30.06, 30.49, 30.85, 31.37, 31.71, 32.17, 32.41, 32.6, 32.86, 33.32, 33.51, 33.78, 33.86, 33.93, 34.49, 34.96, 35.35, 35.58, 35.85, 36.21, 36.43, 36.76, 37.27, 37.49, 37.96, 38.63, 38.6, 38.62, 38.67, 38.73, 39, 38.99, 38.78, 38.09, 37.82, 37.92, 38.18, 38.36, 38.62, 38.88, 39.31, 39.71, 39.84, 40.1, 40.58, 41.13, 41.53, 41.68]
      },
      "network": "NEM",
      "source": "nemweb",
      "description": "12-month rolling average of renewable energy share of total generation",
      "note": "Shares calculated as percentage of total generation including all sources. Last value (2025-08) is an estimate based on 12 months to yesterday"
    }
  ]
}
```

Current 12-month rolling average (as of August 2025):
- **Fossil fuels: 57.85%**
- **Renewables: 41.68%**

## Note

This is a reference implementation intended to demonstrate the calculation methodology. Not intended for production!

## License

MIT License - see [LICENSE](LICENSE) file for details
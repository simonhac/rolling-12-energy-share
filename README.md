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

## Note

This is a reference implementation intended to demonstrate the calculation methodology. Not intended for production!

## License

MIT License - see [LICENSE](LICENSE) file for details
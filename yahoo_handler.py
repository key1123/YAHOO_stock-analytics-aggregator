"""
======================================
How This Code Works: Yahoo Finance Data Handler
======================================

This codebase includes two files: `yahoo_handler.py` and `main.py`.

1. **yahoo_handler.py**:
   - Loads a list of stock symbols from a CSV file.
   - Uses the `yfinance` library to fetch detailed data for each symbol:
     - Company fundamentals (e.g., market cap, sector)
     - Historical prices
     - Corporate actions (splits, dividends)
     - Analyst recommendations
   - Returns a nested dictionary with all this data for each symbol.

2. **main.py**:
   - Calls `load_csv` to get tickers from `top30.csv`.
   - Calls `fetch_all_data` to retrieve full market data from Yahoo Finance.
   - Saves the result as `top30_data.json`.

This setup enables easy downstream analysis, such as feeding data into financial models, analytics engines, or dashboards.
"""

# yahoo_handler.py
import csv
import yfinance as yf

def load_csv(csv_path):
    """
    Load ticker symbols from a CSV file.

    Expects:
        A CSV with a column named 'symbol'.

    Args:
        csv_path (str): Path to the CSV file.

    Returns:
        List[str]: List of uppercase ticker symbols.
    """
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        return [row["symbol"].strip().upper() for row in reader if row.get("symbol")]

def fetch_all_data(tickers):
    """
    Fetch Yahoo Finance data for a list of tickers.

    For each ticker, retrieves:
        - info: Company profile and fundamentals
        - history: Daily price history
        - actions: Corporate actions (splits/dividends)
        - recommendations: Analyst ratings
        - dividends: Historical dividends
        - splits: Historical stock splits

    Args:
        tickers (List[str]): List of stock ticker symbols.

    Returns:
        Dict[str, Dict]: Mapping of ticker symbol to its full data dictionary.
    """
    output = {}
    for t in tickers:
        tk = yf.Ticker(t)
        data = {
            "info": tk.info,
            "history": tk.history(period="max", auto_adjust=False),
            "actions": tk.actions,
            "recommendations": tk.recommendations,
            "dividends": tk.dividends,
            "splits": tk.splits
        }
        output[t] = data
    return output


# main.py
from yahoo_handler import load_csv, fetch_all_data
import json

def main():
    """
    Entry point for retrieving and saving Yahoo Finance data.

    Steps:
        1. Load symbols from top30.csv.
        2. Fetch all available Yahoo Finance data.
        3. Save it to a JSON file.
    """
    tickers = load_csv("top30.csv")
    print(f"Loaded {len(tickers)} tickers:", tickers)

    data = fetch_all_data(tickers)
    print("Fetched data for all tickers.")

    # Save to JSON file
    with open("top30_data.json", "w") as f:
        json.dump(data, f, default=str, indent=2)

    print("Saved combined data to 'top30_data.json'")

if __name__ == "__main__":
    main()


# top30.csv (example CSV content as string)
# symbol
# AAPL
# MSFT
# TSLA
# AMZN
# GOOGL
# NVDA
# META
# AMD
# INTC
# BAC
# F
# GE
# T
# XOM
# WFC
# WMT
# KO
# PEP
# PFE
# JNJ
# DIS
# NFLX
# CRM
# V
# MA
# CSCO
# ADBE
# ORCL
# NIO
# UBER

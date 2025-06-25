# main.py
import pandas as pd
import json
import csv
import time
from yahoo_handler import load_csv, fetch_all_data

"""
How This Code Works:

1. Loads tickers from top30.csv.
2. Fetches raw data using Yahoo Finance API handler.
3. Cleans the data to include only OHLC + analysis-needed fields.
4. Saves the raw data (optional) and cleaned data to separate tables.
5. Performs analysis calculations like mark price, % change, etc.
6. Saves results of analysis to its own table.

Outputs:
- top30_raw.json       → Raw unfiltered data
- top30_data.csv       → Cleaned data with OHLC + required fields
- top30_analysis.csv   → Table with calculated metrics per ticker
"""

NEEDED_KEYS = {
    "open", "high", "low", "close",
    "regularMarketOpen", "regularMarketDayHigh", "regularMarketDayLow", "regularMarketPrice",
    "previousClose", "regularMarketPreviousClose", "regularMarketVolume",
    "bid", "ask", "lastPrice", "optionPrice",
    "strikePrice", "expirationDate", "dividendYield", "impliedVolatility", "inTheMoney",
    "marketCap", "currency"
}

def clean_data(data):
    cleaned = {}
    for ticker, entry in data.items():
        if not entry or not isinstance(entry, dict):
            continue

        # Look for the nested 'info' dict (most Yahoo/finance libs use this)
        info = entry.get("info", {})
        if not info:
            print(f"[WARN] No 'info' field for {ticker}. Sample keys: {list(entry.keys())[:5]}")
            continue

        cleaned_info = {}
        for key in NEEDED_KEYS:
            value = info.get(key)
            if value is None or (isinstance(value, str) and value.strip() == ""):
                continue
            if isinstance(value, (pd.DataFrame, pd.Series)):
                if value.empty:
                    continue
                value = value.to_dict()
            try:
                json.dumps(value)
                cleaned_info[key] = value
            except (TypeError, OverflowError):
                cleaned_info[key] = str(value)
        if cleaned_info:
            cleaned[ticker] = cleaned_info
        else:
            print(f"[WARN] No NEEDED_KEYS found for {ticker} in info. Sample: {list(info.keys())[:5]}")
    return cleaned


def export_to_csv(data_dict, filename):
    if not data_dict:
        print(f"No data to export for {filename}")
        return

    # Union of all keys found
    all_keys = set()
    for item in data_dict.values():
        all_keys.update(item.keys())
    headers = ["Ticker"] + sorted(all_keys)

    with open(filename, mode='w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for ticker, info in data_dict.items():
            row = {"Ticker": ticker}
            row.update(info)
            writer.writerow(row)

def analyze_data(data):
    analysis = []
    for ticker, info in data.items():
        row = {"Ticker": ticker}

        try:
            bid = float(info.get("bid", 0) or 0)
            ask = float(info.get("ask", 0) or 0)
            mark_price = round((bid + ask) / 2, 4) if bid and ask else None

            last = float(info.get("regularMarketPrice", 0) or 0)
            close = float(info.get("regularMarketPreviousClose", 0) or 0)

            net_change = last - close if last and close else None
            percent_change = ((net_change / close) * 100) if close else None

            row["Mark Price"] = round(mark_price, 4) if mark_price is not None else "N/A"
            row["Net Change"] = round(net_change, 4) if net_change is not None else "N/A"
            row["% Change"] = round(percent_change, 2) if percent_change is not None else "N/A"
            row["Last Price"] = last if last else "N/A"
            row["Previous Close"] = close if close else "N/A"
            row["Volume"] = info.get("regularMarketVolume", "N/A")
        except Exception as e:
            print(f"[ERROR] Analysis failed for {ticker}: {e}")

        analysis.append(row)
    return analysis

def export_analysis(data, filename):
    if not data:
        print(f"No analysis data for {filename}")
        return
    headers = data[0].keys()
    with open(filename, "w", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def save_json(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2, default=str)

def main():
    start_time = time.time()
    
    print("Loading tickers...")
    tickers = load_csv("top30.csv")
    print(f"Loaded {len(tickers)} tickers")

    print("Fetching raw data...")
    raw_data = fetch_all_data(tickers)
    save_json(raw_data, "top30_raw.json")
    print("Saved raw data → top30_raw.json")

    print("Cleaning data...")
    cleaned = clean_data(raw_data)
    # Print a sample cleaned ticker for inspection
    if cleaned:
        sample_ticker = next(iter(cleaned))
        print(f"Sample cleaned for {sample_ticker}: {cleaned[sample_ticker]}")
    export_to_csv(cleaned, "top30_data.csv")
    print("Saved cleaned data → top30_data.csv")
    print(json.dumps(raw_data["AAPL"]["info"], indent=2))
    print("Analyzing data...")
    analysis = analyze_data(cleaned)
    export_analysis(analysis, "top30_analysis.csv")
    print("Saved analysis → top30_analysis.csv")

    print(f"\n✅ Completed in {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main()

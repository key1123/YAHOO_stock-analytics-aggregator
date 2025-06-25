
---

### `INFO.md`

```markdown
# Project Info & Usage

## Purpose

This project automates the collection, cleaning, and analytics of key stock market data using Yahoo Finance.
Intended for traders, analysts, and students who need streamlined batch metrics and customizable analytics.

## Main Components

- **Data Fetching**: Uses `yahoo_handler.py` to pull info, history, and corporate actions for each ticker in `top30.csv`
- **Cleaning & Export**: `main.py` extracts only the required fields for further analysis
- **Analytics & Risk**: `combinedanalysisaggregator.py` computes advanced analytics, such as risk, volatility, P/E ratio, and trade signals

## Typical Workflow

1. Place your tickers in `top30.csv` (one per line, under header `symbol`)
2. Run `main.py`
   - This will fetch data, save raw/cleaned tables, and run calculations
3. Check outputs in CSV and JSON format for further exploration

## Extending

- To add more analytics: Extend classes in `combinedanalysisaggregator.py`
- To add more symbols: Edit `top30.csv`
- To use in Jupyter or dashboards: Import the aggregator classes directly

## Requirements

- `pandas`
- `numpy`
- `yfinance`

Install with:
```bash
pip install pandas numpy yfinance

# Stock Analytics Aggregator

A Python project to batch-analyze top-traded stocks using Yahoo Finance data and custom financial analytics.

**Features:**
- Fetches and cleans stock data for the top 30 traded tickers
- Calculates mark price, net change, % change, option analytics, risk scores, and more
- Exports results to CSV and JSON for further analysis

## Project Structure

- `main.py`: Main script to load tickers, fetch and clean data, run analysis, and save results
- `yahoo_handler.py`: Handles data loading from Yahoo Finance and CSV files
- `combinedanalysisaggregator.py`: Contains calculation logic for risk scores, analytics, options, volatility, etc.
- `top30.csv`: List of ticker symbols to analyze

## Quickstart

```bash
pip install pandas numpy yfinance
python main.py

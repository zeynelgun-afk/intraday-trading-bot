---
title: Financial Modeling Prep (FMP) API Guide
description: Comprehensive guide to the Financial Modeling Prep (FMP) API, covering Stock Quotes, Fundamentals, Analyst Ratings, Market Performance, and Bulk Data fetching.
---

# Financial Modeling Prep (FMP) API Guide

This document is a complete reference for integrating with the Financial Modeling Prep API within this project. It covers authentication, rate limits, and detailed endpoint documentation.

## 🔑 Authentication
- **Base URL:** `https://financialmodelingprep.com/stable`
- **Query Param:** Append `?apikey=YOUR_API_KEY` to all requests.
- **Environment Variable:** Ensure `FMP_API_KEY` is set in your `.env` file.

## 🚀 Best Practices
1.  **Use Bulk/Batch Endpoints:** For fetching data for multiple symbols, ALWAYS use the batch or bulk endpoints.
2.  **Caching:** Implement caching (e.g., Redis or in-memory) for fundamental data to safe API credits.
3.  **Error Handling:** Check for empty arrays `[]` in responses.

---

## 📚 API Endpoints Reference

### 1. Company Search & Identifiers
| Feature | Endpoint | Description |
| :--- | :--- | :--- |
| **Symbol Search** | `/search-symbol?query=AAPL` | Search ticker across global markets. |
| **Name Search** | `/search-name?query=Apple` | Search by company name. |
| **CIK Search** | `/search-cik?cik=...` | Get ticker from CIK. |
| **CUSIP Search** | `/search-cusip?cusip=...` | Get ticker from CUSIP. |
| **ISIN Search** | `/search-isin?isin=...` | Get ticker from ISIN. |
| **Screener** | `/company-screener` | Filter stocks by market cap, sector, price, etc. |
| **Exchange Variants** | `/search-exchange-variants?symbol=...` | Find listing on multiple exchanges. |

### 2. Stock Directory
| Feature | Endpoint | Description |
| :--- | :--- | :--- |
| **Symbol List** | `/stock-list` | List of all available symbols. |
| **Statement Symbols**| `/financial-statement-symbol-list` | Companies with financial statements. |
| **CIK List** | `/cik-list` | List of all CIKs. |
| **ETF List** | `/etf-list` | List of all ETFs. |
| **Actively Trading** | `/actively-trading-list` | Currently active stocks. |
| **Symbol Changes** | `/symbol-change` | Mergers, acquisitions, split history. |

### 3. Company Information
| Feature | Endpoint | Description |
| :--- | :--- | :--- |
| **Profile** | `/profile?symbol=...` | Detailed company profile (Market Cap, CEO, Description). |
| **Market Cap** | `/market-capitalization?symbol=...` | Current market cap. |
| **Batch Market Cap** | `/market-capitalization-batch?symbols=...` | Batch market cap. |
| **Shares Float** | `/shares-float?symbol=...` | Publicly traded shares count. |
| **Executives** | `/key-executives?symbol=...` | Company executives list. |
| **Compensation** | `/governance-executive-compensation?symbol=...` | Executive detailed compensation. |
| **Peers** | `/stock-peers?symbol=...` | Competitors in same sector/mkt cap. |
| **Delisted** | `/delisted-companies` | List of delisted companies. |

### 4. Stock Quotes (Real-Time)
| Feature | Endpoint | Description |
| :--- | :--- | :--- |
| **Quote** | `/quote?symbol=...` | Full quote (Price, Change, Vol, Mkt Cap). |
| **Quote Short** | `/quote-short?symbol=...` | Lightweight quote. |
| **Batch Quote** | `/batch-quote?symbols=...` | Multiple full quotes. |
| **Batch Short** | `/batch-quote-short?symbols=...` | Multiple short quotes. |
| **Aftermarket** | `/aftermarket-quote?symbol=...` | Post-market quote. |
| **Price Change** | `/stock-price-change?symbol=...` | Change over various timeframes (1D, 5D, 1M, etc). |

### 5. Financial Statements
| Feature | Endpoint | Description |
| :--- | :--- | :--- |
| **Income Statement** | `/income-statement?symbol=...` | Revenue, Expenses, EPS. |
| **Balance Sheet** | `/balance-sheet-statement?symbol=...` | Assets, Liabilities, Equity. |
| **Cash Flow** | `/cash-flow-statement?symbol=...` | Operating, Investing, Financing. |
| **Key Metrics** | `/key-metrics?symbol=...` | ROE, Debt/Equity, etc. |
| **Ratios** | `/ratios?symbol=...` | P/E, P/B, Current Ratio. |
| **Scores** | `/financial-scores?symbol=...` | Altman Z-Score, Piotroski. |
| **Enterprise Value** | `/enterprise-values?symbol=...` | EV breakdown. |
| **Growth** | `/[statement]-growth?symbol=...` | Growth metrics for statements. |
| **SEC 10-K** | `/financial-reports-json?symbol=...` | Full 10-K as JSON. |
| **Revenue Segments** | `/revenue-product-segmentation?symbol=...` | Revenue by product/geo. |

### 6. Charts & Historical Data
| Feature | Endpoint | Description |
| :--- | :--- | :--- |
| **EOD Full** | `/historical-price-eod/full?symbol=...` | Full history (OHLCV). |
| **Dividend Adj** | `/historical-price-eod/dividend-adjusted?symbol=...` | Adjusted for dividends. |
| **Intraday** | `/historical-chart/[interval]?symbol=...` | Intervals: 1min, 5min, 15min, 30min, 1hour, 4hour. |

### 7. Analyst & Estimates
| Feature | Endpoint | Description |
| :--- | :--- | :--- |
| **Estimates** | `/analyst-estimates?symbol=...` | Annual/Quarterly EPS/Rev estimates. |
| **Ratings** | `/rating?symbol=...` | Overall rating (Buy/Sell). |
| **Price Targets** | `/price-target-consensus?symbol=...` | High/Low/Median target. |
| **Upgrades/Down** | `/upgrades-downgrades-consensus?symbol=...` | Analyst sentiment. |

### 8. Market Performance
| Feature | Endpoint | Description |
| :--- | :--- | :--- |
| **Gainers/Losers** | `/biggest-gainers`, `/biggest-losers` | Top movers. |
| **Most Active** | `/most-actives` | High volume symbols. |
| **Sector Perf** | `/sector-performance-snapshot` | Real-time sector gains/losses. |

### 9. News & Sentiment
| Feature | Endpoint | Description |
| :--- | :--- | :--- |
| **Stock News** | `/news/stock?symbols=...` | News specific to tickers. |
| **Press Releases** | `/news/press-releases?symbols=...` | Official PRs. |
| **Earnings Transcripts** | `/earning-call-transcript?symbol=...` | Text transcripts of calls. |
| **Social Sentiment** | `/social-sentiment?symbol=...` | (If available in plan). |

### 10. Earnings & Dividends
| Feature | Endpoint | Description |
| :--- | :--- | :--- |
| **Earnings Calendar**| `/earnings-calendar` | Upcoming earnings. |
| **Dividends** | `/dividends?symbol=...` | Dividend history. |
| **Splits** | `/splits?symbol=...` | Stock split history. |

### 11. Institutional & Insider
| Feature | Endpoint | Description |
| :--- | :--- | :--- |
| **Insider Trading** | `/insider-trading/search?symbol=...` | Insider buys/sells. |
| **Institutional** | `/institutional-ownership/symbol-positions-summary?symbol=...` | Major holders. |

### 12. Economics
| Feature | Endpoint | Description |
| :--- | :--- | :--- |
| **Treasury Rates** | `/treasury-rates` | Yield curve data. |
| **Indicators** | `/economic-indicators?name=GDP` | GDP, CPI, Unemployment. |
| **Calendar** | `/economic-calendar` | Upcoming economic events. |

### 13. Commodities, Forex, Crypto
| Feature | Endpoint | Description |
| :--- | :--- | :--- |
| **Commodities** | `/batch-commodity-quotes` | Gold, Oil, etc. |
| **Forex** | `/batch-forex-quotes` | EURUSD, etc. |
| **Crypto** | `/batch-crypto-quotes` | BTCUSD, etc. |

### 14. Bulk (Batch) Data
*Efficient for initializing databases.*
| Feature | Endpoint | Description |
| :--- | :--- | :--- |
| **Bulk Profile** | `/profile-bulk` | |
| **Bulk Ratings** | `/rating-bulk` | |
| **Bulk EOD** | `/eod-bulk?date=...` | |
| **Bulk Ratios** | `/ratios-ttm-bulk` | |
| **Bulk Metrics** | `/key-metrics-ttm-bulk` | |

---

## 💻 Code Examples

### Standard Fetch (Python)
```python
import requests
import os

FMP_API_KEY = os.getenv("FMP_API_KEY")

def get_ratios(symbol: str):
    url = f"https://financialmodelingprep.com/stable/ratios?symbol={symbol}&period=quarter&apikey={FMP_API_KEY}"
    response = requests.get(url)
    return response.json()[0] if response.status_code == 200 else []
```

### Batch Fetch (Python)
```python
def get_batch_quotes(symbols: list):
    symbol_str = ",".join(symbols)
    url = f"https://financialmodelingprep.com/stable/batch-quote?symbols={symbol_str}&apikey={FMP_API_KEY}"
    response = requests.get(url)
    return response.json()
```

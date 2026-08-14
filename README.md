# Volume Scanner

Scans the **S&P 500**, **Nasdaq Composite**, and a fixed **ETF watchlist**
for the tickers with the highest trailing average daily volume over the
last **50** and **100** trading sessions.

## How it works

- `scripts/scan_volume.py` builds the three ticker universes:
  - S&P 500 — scraped from the Wikipedia constituents table.
  - Nasdaq Composite — all non-test, non-ETF common symbols from Nasdaq
    Trader's official symbol directory.
  - ETFs — a fixed watchlist: `XLE, XLF, GLD, TLT, XLB, SPY, EEM, QQQ, SLV,
    XLRE` (edit `FIXED_ETFS` in the script to change it).
- Pulls ~9 months of daily volume history per ticker from Yahoo Finance
  (`yfinance`), in chunks, with basic retry/backoff.
- Computes trailing 50-day and 100-day average daily volume per ticker.
- Writes a Markdown report to `reports/volume_report_<date>.md` and updates
  `reports/latest.md`.

## Schedule

`.github/workflows/volume-scan.yml` runs this every **weekday at 22:00 UTC**
(after the US market close) via GitHub Actions and commits the updated
report back to the repo. It also supports manual runs via the "Run
workflow" button (`workflow_dispatch`).

**Note:** scheduled (`cron`) workflows on GitHub only fire from the
repository's default branch. This branch (`claude/volume-tickers-sp500-nasdaq-e9tusw`)
is currently the repo's default branch (the repo had no commits before this
change), so the schedule is active as-is.

## Configuration

Environment variables (set in the workflow file or when running locally):

- `TOP_N` — how many tickers to list per universe/window (default `25`).
- `CHUNK_SIZE` — how many tickers to request from Yahoo Finance per batch
  (default `150`). Lower this if you hit rate-limiting (HTTP 429) errors.

## Running locally

```bash
pip install -r requirements.txt
python scripts/scan_volume.py
```

Requires normal internet access to `en.wikipedia.org`, `nasdaqtrader.com`,
and Yahoo Finance.

## Known limitations

- Yahoo Finance's unofficial API can rate-limit large scans. The S&P 500 +
  Nasdaq Composite combined is still ~3,500-4,000 tickers, so if runs start
  failing partway through, reduce `CHUNK_SIZE` and/or increase the delay
  between chunks in `scan_volume.py`.

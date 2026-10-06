# Quality Dip Backtest — 2026-10-06

Month-end signals from 2004-12 to 2026-10 across 571 stocks (547 with SEC financials): today's S&P 500 and Nasdaq-100 (lists from the NIBII repo) plus this repo's watchlist. S&P 500 stocks only count from the date they joined the index. A signal = month-end close within 15% of the trailing 52-week low; a *quality* signal also passed revenue growth ≥ 5%, net margin ≥ 10%, positive FCF, and net cash or net debt ≤ 1.5x EBITDA, using only the latest 10-K filed by that date. After a signal, that ticker is skipped for 12 months. Returns include dividends.

## Results

| Group | Horizon | Signals | Avg return | Median return | % positive | Avg SPY same window | Avg excess vs SPY | % beat SPY |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| A. All near-low signals (2004+) | 1y | 4,215 | +14.3% | +11.8% | 68% | +13.1% | +1.3% | 49% |
| A. All near-low signals (2004+) | 3y | 3,705 | +51.1% | +39.3% | 78% | +45.1% | +6.0% | 47% |
| A'. All near-low signals (2010+) | 1y | 3,122 | +16.1% | +12.7% | 70% | +15.9% | +0.1% | 47% |
| A'. All near-low signals (2010+) | 3y | 2,632 | +57.3% | +45.8% | 84% | +55.2% | +2.1% | 44% |
| B. Near low + quality (2010+) | 1y | 501 | +16.1% | +12.5% | 67% | +15.2% | +0.9% | 48% |
| B. Near low + quality (2010+) | 3y | 431 | +62.1% | +52.4% | 83% | +55.6% | +6.5% | 49% |
| C. Near low, failed quality (2010+) | 1y | 2,621 | +16.1% | +12.8% | 71% | +16.1% | +0.0% | 47% |
| C. Near low, failed quality (2010+) | 3y | 2,201 | +56.4% | +44.9% | 84% | +55.2% | +1.2% | 43% |

Compare B with C to see whether the quality checks help. A' covers the same years as B and C, so it's the fair price-only comparison.

## As a portfolio

Since 2011-01-03. Every quality signal bought at its month-end close, equal weight, held 1 or 3 years.

| Portfolio | Total | Per year | Worst drop | $10k became |
|---|---:|---:|---:|---:|
| Quality dips, hold 1y | +894% | +15.7% | -34% | $99,370 |
| Quality dips, hold 3y | +1,171% | +17.5% | -35% | $127,070 |
| SPY | +708% | +14.2% | -34% | $80,785 |

| Year | Quality dips, hold 1y | Quality dips, hold 3y | SPY |
|---|---:|---:|---:|
| 2011 | +23% | +24% | +1% |
| 2012 | +25% | +25% | +16% |
| 2013 | +28% | +33% | +32% |
| 2014 | +23% | +22% | +13% |
| 2015 | -2% | -1% | +1% |
| 2016 | +20% | +19% | +12% |
| 2017 | +29% | +30% | +22% |
| 2018 | -5% | -5% | -5% |
| 2019 | +41% | +37% | +31% |
| 2020 | +34% | +36% | +18% |
| 2021 | +20% | +33% | +29% |
| 2022 | -16% | -16% | -18% |
| 2023 | +23% | +28% | +26% |
| 2024 | +15% | +12% | +25% |
| 2025 | +5% | +7% | +18% |
| 2026 | +1% | +8% | +15% |

## By signal year (3-year forward returns)

| Signal year | Quality signals | Avg 3y | vs SPY | Failed-quality signals | Avg 3y | vs SPY |
|---|---:|---:|---:|---:|---:|---:|
| 2010 | 4 | +143.5% | +81.2% | 104 | +65.6% | +4.5% |
| 2011 | 37 | +99.9% | +25.2% | 154 | +91.5% | +18.0% |
| 2012 | 35 | +75.8% | +18.6% | 86 | +86.2% | +30.2% |
| 2013 | 15 | +47.8% | +11.4% | 62 | +44.0% | +8.0% |
| 2014 | 22 | +54.3% | +18.9% | 137 | +50.2% | +15.1% |
| 2015 | 36 | +60.5% | +15.7% | 200 | +49.0% | +4.6% |
| 2016 | 22 | +65.9% | +17.7% | 135 | +71.3% | +21.9% |
| 2017 | 15 | +38.0% | +1.4% | 130 | +26.3% | -10.6% |
| 2018 | 36 | +107.9% | +38.5% | 276 | +62.6% | -5.4% |
| 2019 | 19 | +83.2% | +31.2% | 114 | +54.9% | +6.1% |
| 2020 | 24 | +42.7% | -4.2% | 164 | +57.7% | +14.0% |
| 2021 | 18 | +41.6% | +6.4% | 134 | +32.5% | -3.3% |
| 2022 | 102 | +44.6% | -7.3% | 264 | +43.2% | -14.7% |
| 2023 | 46 | +42.2% | -42.1% | 241 | +60.2% | -22.5% |

## Best and worst quality signals (3-year forward return)

| Ticker | Signal date | 3y return | SPY same window |
|---|---|---:|---:|
| NVDA | 2022-06-30 | +943.7% | +70.9% |
| GILD | 2011-11-30 | +403.5% | +76.4% |
| NVDA | 2018-10-31 | +388.6% | +78.9% |
| MELI | 2018-12-31 | +360.4% | +99.9% |
| APH | 2023-10-31 | +350.5% | +93.2% |
| ANET | 2022-06-30 | +336.6% | +70.9% |
| GILD | 2010-11-30 | +309.9% | +62.6% |
| MKTX | 2014-06-30 | +281.6% | +31.3% |
| SNPS | 2018-10-31 | +272.1% | +78.9% |
| LRCX | 2018-08-31 | +269.5% | +64.2% |
| EL | 2022-02-28 | -74.5% | +42.2% |
| ETSY | 2022-01-31 | -65.0% | +39.8% |
| CSGP | 2023-10-31 | -62.4% | +93.2% |
| ENPH | 2023-05-31 | -60.7% | +88.1% |
| MKTX | 2021-04-30 | -57.9% | +25.7% |
| BF-B | 2022-09-30 | -56.9% | +94.3% |
| PAYC | 2023-02-28 | -55.6% | +80.1% |
| PYPL | 2021-11-30 | -53.1% | +38.2% |
| QRVO | 2021-11-30 | -52.8% | +38.2% |
| INTC | 2021-10-29 | -52.3% | +29.4% |

## Caveats

- **Survivorship bias:** the universe is *today's* S&P 500 / Nasdaq-100 + watchlist. Companies that collapsed and left the index aren't here, so every group looks better than it would have in real time — the price-only group (A) most of all, since failing companies are exactly the ones that sit near lows.
- Financials come from SEC XBRL filings, which start around 2009–2011, so quality results cover fewer years.
- Missing XBRL data counts as failing quality, so banks/insurers and companies with unusual tags rarely qualify.
- Signals overlap in time (many stocks dip together in a crash), so they are not independent bets. Not financial advice.

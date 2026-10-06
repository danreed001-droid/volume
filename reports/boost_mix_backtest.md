# Boost + Quality Dips Mix, with Leverage

NIBII's **Auto + News boost** plan mixed with this repo's **quality dips (hold 3y)** portfolio. Weights are rebalanced weekly; anything above 100% of the account is borrowed at the margin rate shown, charged daily (NIBII's `backtest_leverage.run`). Same universe for both: today's S&P 500 (from each stock's join date) + Nasdaq-100, so survivorship bias flatters all of it.

## Borrowing at 6% a year

### Since 2011-01-03 (quality data starts ~2010)

| Plan | Per year | Worst drop | Worst calendar year | $10k became | COVID Feb-Mar 2020 | 2022 bear market | Feb-Apr 2025 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Boost alone x1 | +43% | -36% | -12% | $2,831,175 | -29% | -4% | -30% |
| Boost alone x1.25 | +52% | -43% | -17% | $7,514,589 | -35% | -7% | -36% |
| Boost alone x1.5 | +61% | -50% | -22% | $18,437,316 | -41% | -11% | -42% |
| Boost alone x2 | +78% | -63% | -33% | $87,724,983 | -52% | -19% | -53% |
| 70/30 Boost/quality x1 | +36% | -33% | -2% | $1,227,289 | -31% | -10% | -27% |
| 70/30 Boost/quality x1.25 | +43% | -40% | -5% | $2,816,919 | -37% | -14% | -32% |
| 70/30 Boost/quality x1.5 | +50% | -47% | -8% | $6,126,173 | -44% | -18% | -38% |
| 70/30 Boost/quality x2 | +64% | -58% | -15% | $24,648,110 | -55% | -27% | -48% |
| 50/50 Boost/quality x1 | +31% | -32% | -1% | $671,999 | -32% | -14% | -25% |
| 50/50 Boost/quality x1.25 | +37% | -39% | -4% | $1,365,619 | -39% | -19% | -30% |
| 50/50 Boost/quality x1.5 | +43% | -46% | -7% | $2,658,975 | -45% | -24% | -35% |
| 50/50 Boost/quality x2 | +54% | -57% | -14% | $8,861,356 | -56% | -33% | -45% |
| Quality dips alone x1 | +18% | -35% | -16% | $127,070 | -35% | -24% | -19% |
| Quality dips alone x1.25 | +20% | -42% | -22% | $174,343 | -42% | -31% | -24% |
| Quality dips alone x1.5 | +22% | -49% | -28% | $231,226 | -49% | -37% | -28% |
| Quality dips alone x2 | +26% | -61% | -38% | $366,700 | -61% | -48% | -36% |

### Boost alone since 2000-01-03 (includes the dot-com crash and 2008)

| Plan | Per year | Worst drop | Worst calendar year | $10k became | Dot-com Mar 2000-Oct 2002 | 2008 crisis Oct 2007-Mar 2009 | COVID Feb-Mar 2020 | 2022 bear market | Feb-Apr 2025 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Boost alone x1 | +32% | -62% | -43% | $16,314,608 | -45% | -58% | -29% | -4% | -30% |
| Boost alone x1.25 | +37% | -73% | -52% | $47,623,174 | -56% | -68% | -35% | -7% | -36% |
| Boost alone x1.5 | +42% | -81% | -60% | $119,512,710 | -67% | -76% | -41% | -11% | -42% |
| Boost alone x2 | +50% | -91% | -73% | $475,736,579 | -82% | -87% | -52% | -19% | -53% |
| SPY | +8% | -55% | -37% | $85,702 | -48% | -55% | -34% | -24% | -19% |

## Borrowing at 8% a year

### Since 2011-01-03 (quality data starts ~2010)

| Plan | Per year | Worst drop | Worst calendar year | $10k became | COVID Feb-Mar 2020 | 2022 bear market | Feb-Apr 2025 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Boost alone x1 | +43% | -36% | -12% | $2,831,175 | -29% | -4% | -30% |
| Boost alone x1.25 | +52% | -44% | -17% | $6,949,587 | -35% | -8% | -36% |
| Boost alone x1.5 | +60% | -51% | -23% | $15,770,292 | -41% | -11% | -42% |
| Boost alone x2 | +75% | -63% | -34% | $64,189,959 | -52% | -20% | -53% |
| 70/30 Boost/quality x1 | +36% | -33% | -2% | $1,227,289 | -31% | -10% | -27% |
| 70/30 Boost/quality x1.25 | +42% | -40% | -5% | $2,604,954 | -37% | -15% | -33% |
| 70/30 Boost/quality x1.5 | +49% | -47% | -9% | $5,239,337 | -44% | -19% | -38% |
| 70/30 Boost/quality x2 | +61% | -58% | -17% | $18,032,088 | -55% | -28% | -48% |
| 50/50 Boost/quality x1 | +31% | -32% | -1% | $671,999 | -32% | -14% | -25% |
| 50/50 Boost/quality x1.25 | +36% | -39% | -5% | $1,262,789 | -39% | -19% | -30% |
| 50/50 Boost/quality x1.5 | +41% | -46% | -8% | $2,273,779 | -45% | -24% | -35% |
| 50/50 Boost/quality x2 | +51% | -57% | -16% | $6,481,120 | -57% | -34% | -45% |
| Quality dips alone x1 | +18% | -35% | -16% | $127,070 | -35% | -24% | -19% |
| Quality dips alone x1.25 | +19% | -42% | -22% | $161,185 | -42% | -31% | -24% |
| Quality dips alone x1.5 | +21% | -49% | -28% | $197,642 | -49% | -37% | -28% |
| Quality dips alone x2 | +23% | -61% | -40% | $267,900 | -61% | -49% | -36% |

### Boost alone since 2000-01-03 (includes the dot-com crash and 2008)

| Plan | Per year | Worst drop | Worst calendar year | $10k became | Dot-com Mar 2000-Oct 2002 | 2008 crisis Oct 2007-Mar 2009 | COVID Feb-Mar 2020 | 2022 bear market | Feb-Apr 2025 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Boost alone x1 | +32% | -62% | -43% | $16,314,608 | -45% | -58% | -29% | -4% | -30% |
| Boost alone x1.25 | +37% | -73% | -52% | $41,690,557 | -57% | -68% | -35% | -8% | -36% |
| Boost alone x1.5 | +41% | -81% | -61% | $91,590,773 | -67% | -76% | -41% | -11% | -42% |
| Boost alone x2 | +47% | -92% | -74% | $279,304,714 | -83% | -87% | -52% | -20% | -53% |
| SPY | +8% | -55% | -37% | $85,702 | -48% | -55% | -34% | -24% | -19% |

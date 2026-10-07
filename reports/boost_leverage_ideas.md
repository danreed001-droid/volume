# Levering Auto + News Boost — 2026-10-07

Built on NIBII's Auto + News boost curve (`backtest_long_history.build(boost=True)`). Leverage is decided at the Friday close; 'uptrend' = SPY above its 200-day average. Borrowed money pays 6% a year. Put hedge = 3-month SPY puts 10% out of the money on the full levered exposure, rolled monthly, Black-Scholes at VIX + 4 points, 2% paid each way. Survivorship bias (today's index lists) flatters every line.

## 2000-01-03 to 2026-10-06

| Plan | Per year | Worst drop | Worst year | Dot-com | 2008 | Flash 2011 | Q4 2018 | COVID | 2022 | 2025 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Boost 1x (today) | +32% | -62% | -43% | -45% | -58% | -18% | -19% | -29% | -4% | -30% |
| Boost 1.5x constant | +42% | -80% | -61% | -66% | -77% | -28% | -28% | -41% | -11% | -42% |
| Boost 2x constant | +48% | -91% | -75% | -80% | -88% | -37% | -36% | -52% | -20% | -53% |
| 1.5x in uptrend, 1x otherwise | +40% | -70% | -44% | -57% | -61% | -25% | -26% | -33% | -4% | -39% |
| 2x in uptrend, 1x otherwise | +47% | -78% | -45% | -68% | -63% | -31% | -32% | -37% | -4% | -47% |
| 1.5x in uptrend, 0.6x otherwise | +37% | -62% | -29% | -53% | -44% | -22% | -24% | -26% | -0% | -36% |
| 1.25x in uptrend, 0.6x otherwise | +34% | -57% | -28% | -47% | -43% | -19% | -21% | -24% | -0% | -31% |
| 2x in uptrend, 0.6x otherwise | +44% | -71% | -31% | -65% | -48% | -29% | -30% | -30% | -0% | -44% |
| 2x in uptrend, cash otherwise | +38% | -67% | -35% | -62% | -20% | -27% | -28% | -20% | +3% | -40% |
| 1x + SPY put hedge | +29% | -58% | -35% | -43% | -48% | -12% | -11% | -11% | +0% | -22% |
| 2x constant + SPY put hedge | +44% | -88% | -64% | -78% | -79% | -26% | -23% | -20% | -12% | -42% |
| 1.5x in uptrend / 0.6x + put hedge | +33% | -60% | -24% | -52% | -37% | -17% | -12% | -13% | +9% | -31% |
| 2x in uptrend / 0.6x + put hedge | +39% | -70% | -34% | -64% | -41% | -23% | -16% | -17% | +12% | -40% |
| SPY buy & hold | +8% | -55% | -37% | -48% | -55% | -19% | -19% | -34% | -24% | -19% |

## 2011-01-03 to 2026-10-06

| Plan | Per year | Worst drop | Worst year | Dot-com | 2008 | Flash 2011 | Q4 2018 | COVID | 2022 | 2025 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Boost 1x (today) | +43% | -36% | -12% | — | — | -18% | -19% | -29% | -4% | -30% |
| Boost 1.5x constant | +61% | -50% | -22% | — | — | -28% | -28% | -41% | -11% | -42% |
| Boost 2x constant | +77% | -62% | -32% | — | — | -37% | -36% | -52% | -20% | -53% |
| 1.5x in uptrend, 1x otherwise | +56% | -42% | -23% | — | — | -25% | -26% | -33% | -4% | -39% |
| 2x in uptrend, 1x otherwise | +67% | -51% | -33% | — | — | -31% | -32% | -37% | -4% | -47% |
| 1.5x in uptrend, 0.6x otherwise | +51% | -40% | -25% | — | — | -22% | -24% | -26% | -0% | -36% |
| 1.25x in uptrend, 0.6x otherwise | +45% | -35% | -19% | — | — | -19% | -21% | -24% | -0% | -31% |
| 2x in uptrend, 0.6x otherwise | +62% | -52% | -35% | — | — | -29% | -30% | -30% | -0% | -44% |
| 2x in uptrend, cash otherwise | +54% | -55% | -38% | — | — | -27% | -28% | -20% | +3% | -40% |
| 1x + SPY put hedge | +39% | -28% | -15% | — | — | -12% | -11% | -11% | +0% | -22% |
| 2x constant + SPY put hedge | +70% | -52% | -35% | — | — | -26% | -23% | -20% | -12% | -42% |
| 1.5x in uptrend / 0.6x + put hedge | +47% | -42% | -27% | — | — | -17% | -12% | -13% | +9% | -31% |
| 2x in uptrend / 0.6x + put hedge | +57% | -54% | -37% | — | — | -23% | -16% | -17% | +12% | -40% |
| SPY buy & hold | +14% | -34% | -18% | — | — | -19% | -19% | -34% | -24% | -19% |

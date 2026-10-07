# Boost: Favoring the More Volatile Picks — 2026-10-07

NIBII's Auto + News boost with its stock picks tilted toward higher 63-day volatility, 2000-2026 (`backtest_long_history.build(boost=True)`, same costs and Monday trading). Survivorship bias flatters every line — volatile stocks most, since the ones that collapsed are missing.

## Full period

| Variant | Per year | Worst drop | Worst year | Top 5 alone per year | Top 5 alone worst drop |
|---|---:|---:|---:|---:|---:|
| Boost (today) | +31.9% | -62% | -43% | +32.3% | -70% |
| Pool 10: most volatile of the best 10 | +30.0% | -64% | -47% | +29.9% | -74% |
| Pool 20: most volatile of the best 20 | +25.5% | -66% | -44% | +25.7% | -76% |
| Tilt 0.5: strength x vol^0.5 | +31.1% | -69% | -53% | +31.0% | -77% |
| Tilt 1: strength x vol | +28.4% | -68% | -52% | +28.2% | -76% |
| Same picks, weighted by volatility | +34.6% | -72% | -44% | +33.4% | -77% |
| Only buy 40%+ volatility | +33.8% | -63% | -47% | +32.5% | -71% |
| Only buy 30%+ volatility | +31.3% | -60% | -42% | +31.9% | -69% |
| SPY | +8.4% | -55% | -37% | | |

## By decade (per year) — does any edge hold in each?

| Variant | 2000-09 | 2010-19 | 2020-26 |
|---|---:|---:|---:|
| Boost (today) | +17.2% | +23.2% | +73.0% |
| Pool 10: most volatile of the best 10 | +12.7% | +22.6% | +73.9% |
| Pool 20: most volatile of the best 20 | +12.8% | +19.6% | +57.2% |
| Tilt 0.5: strength x vol^0.5 | +14.4% | +22.4% | +76.7% |
| Tilt 1: strength x vol | +13.6% | +20.6% | +68.2% |
| Same picks, weighted by volatility | +17.5% | +25.4% | +81.7% |
| Only buy 40%+ volatility | +11.4% | +32.3% | +77.4% |
| Only buy 30%+ volatility | +18.5% | +21.0% | +71.5% |

## Crashes

| Variant | Dot-com | 2008 | COVID | 2022 | 2025 |
|---|---:|---:|---:|---:|---:|
| Boost (today) | -45% | -58% | -29% | -4% | -30% |
| Pool 10: most volatile of the best 10 | -46% | -62% | -29% | -22% | -32% |
| Pool 20: most volatile of the best 20 | -53% | -63% | -35% | -20% | -31% |
| Tilt 0.5: strength x vol^0.5 | -47% | -68% | -33% | -13% | -32% |
| Tilt 1: strength x vol | -46% | -66% | -37% | -19% | -32% |
| Same picks, weighted by volatility | -54% | -61% | -29% | -7% | -31% |
| Only buy 40%+ volatility | -45% | -61% | -35% | -6% | -29% |
| Only buy 30%+ volatility | -36% | -57% | -30% | -2% | -30% |

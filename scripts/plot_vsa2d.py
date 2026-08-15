#!/usr/bin/env python3
"""VSA "Volume @ Price" 2D chart builder — ports the Colab
`plot_vol_at_price_2d` function to a static, self-contained HTML report,
driven off already-downloaded OHLCV data (no live network calls here;
`scan_volume.py` supplies the data).

Each ticker gets one chart: the close-price line, with a green bar above
the close on each day sized to that day's estimated buyer volume, and a
red bar below sized to estimated seller volume (buyer/seller split
estimated from where the close landed within the day's H/L range -- the
same crude VSA heuristic as the Colab cell). A dashed reference box in
the corner shows what "one average day's volume" looks like at this
chart's scale.
"""
from __future__ import annotations

import json

import plotly.graph_objects as go
import plotly.io as pio


def build_chart_html(ticker: str, category: str, note: str, ohlcv_rows: list[dict],
                     include_plotlyjs: bool = False) -> tuple[str | None, str]:
    rows = sorted(ohlcv_rows, key=lambda r: r["t"])
    rows = [r for r in rows if r.get("c") is not None]
    if len(rows) < 2:
        return None, f"too few bars for {ticker} ({len(rows)})"

    dates = [r["t"] for r in rows]
    c_arr = [float(r["c"]) for r in rows]
    o_arr = [float(r["o"]) if r.get("o") is not None else float(r["c"]) for r in rows]
    h_arr = [float(r["h"]) if r.get("h") is not None else max(o_arr[i], c_arr[i]) for i, r in enumerate(rows)]
    l_arr = [float(r["l"]) if r.get("l") is not None else min(o_arr[i], c_arr[i]) for i, r in enumerate(rows)]
    v_arr = [float(r["v"]) if r.get("v") is not None else 0.0 for r in rows]

    n = len(rows)
    day_range = [(h_arr[i] - l_arr[i]) or 0.001 for i in range(n)]
    buyer_pct = [min(max(((c_arr[i] - o_arr[i]) / day_range[i]) * 0.5 + 0.5, 0.0), 1.0) for i in range(n)]
    buyer_vol = [v_arr[i] * buyer_pct[i] for i in range(n)]
    seller_vol = [v_arr[i] * (1.0 - buyer_pct[i]) for i in range(n)]

    avg_vol = sum(v_arr) / n if n else 0.0
    price_range = (max(c_arr) - min(c_arr)) if c_arr else 0.0
    if price_range < 1e-8:
        price_range = c_arr[0] * 0.1 if c_arr and c_arr[0] else 1.0
    vol_scale = price_range * 0.08

    buy_h = [(buyer_vol[i] / avg_vol) * vol_scale if avg_vol else 0.0 for i in range(n)]
    sell_h = [(seller_vol[i] / avg_vol) * vol_scale if avg_vol else 0.0 for i in range(n)]

    meta = [
        (c_arr[i], int(v_arr[i]), int(buyer_vol[i]), int(seller_vol[i]),
         round(buyer_pct[i] * 100, 1), round((1.0 - buyer_pct[i]) * 100, 1))
        for i in range(n)
    ]

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=dates, y=buy_h, base=c_arr, name="Buyer volume",
        marker=dict(color="rgba(0,200,150,0.70)", line=dict(color="rgba(0,220,170,0.90)", width=0.4)),
        customdata=meta,
        hovertemplate=(
            "<b>Buyer pressure</b><br>Date: %{x}<br>Close: $%{customdata[0]:.2f}<br>"
            "Buyer vol: %{customdata[2]:,}<br>Buyer pct: %{customdata[4]:.1f}%<br>"
            "Total vol: %{customdata[1]:,}<extra></extra>"
        ),
    ))

    red_base = [c_arr[i] - sell_h[i] for i in range(n)]
    fig.add_trace(go.Bar(
        x=dates, y=sell_h, base=red_base, name="Seller volume",
        marker=dict(color="rgba(255,82,82,0.70)", line=dict(color="rgba(255,100,100,0.90)", width=0.4)),
        customdata=meta,
        hovertemplate=(
            "<b>Seller pressure</b><br>Date: %{x}<br>Close: $%{customdata[0]:.2f}<br>"
            "Seller vol: %{customdata[3]:,}<br>Seller pct: %{customdata[5]:.1f}%<br>"
            "Total vol: %{customdata[1]:,}<extra></extra>"
        ),
    ))

    fig.add_trace(go.Scatter(
        x=dates, y=c_arr, mode="lines", name="Close price",
        line=dict(color="rgba(240,246,252,0.85)", width=1.6),
        hovertemplate="Date: %{x}<br>Close: $%{y:.2f}<extra></extra>",
    ))

    ref_top = min(c_arr) - vol_scale * 0.5
    ref_base = ref_top - vol_scale
    fig.add_shape(
        type="rect", x0=dates[0], x1=dates[min(3, n - 1)], y0=ref_base, y1=ref_top,
        fillcolor="rgba(139,148,158,0.18)", line=dict(color="#8b949e", width=1, dash="dot"),
    )
    fig.add_annotation(
        x=dates[min(4, n - 1)], y=(ref_base + ref_top) / 2,
        text=f"= avg vol ({int(avg_vol):,})", showarrow=False, xanchor="left",
        font=dict(color="#8b949e", size=10),
    )

    last_price = c_arr[-1]
    last_bpct = round(buyer_pct[-1] * 100, 1)

    fig.update_layout(
        title=dict(
            text=(
                f"{ticker}  ·  VSA Volume @ Price  ·  {category} · {note}<br>"
                f"<span style='font-size:12px;color:#8b949e;'>"
                f"{dates[0]} → {dates[-1]}  |  Last close: ${last_price:.2f}  |  Avg vol: {int(avg_vol):,}  |  "
                f"Last day buyer %: {last_bpct:.1f}%  |  "
                f"Green ▲ above close = buyer vol  ·  Red ▼ below close = seller vol"
                f"</span>"
            ),
            font=dict(size=16, color="#f0f6fc"), x=0.02,
        ),
        barmode="overlay", bargap=0.12,
        xaxis=dict(title="Date", gridcolor="#21262d", color="#c9d1d9", showgrid=True, zeroline=False),
        yaxis=dict(title="Price ($)", gridcolor="#21262d", color="#c9d1d9", showgrid=True, zeroline=False),
        template="plotly_dark", paper_bgcolor="#0d1117", plot_bgcolor="#0d1117",
        autosize=False, width=1180, height=680,
        margin=dict(l=70, r=20, b=50, t=110),
        legend=dict(font=dict(color="#c9d1d9", size=12), bgcolor="rgba(13,17,23,0.85)",
                    bordercolor="#30363d", borderwidth=1, orientation="h", y=1.03, x=0),
    )

    html_div = pio.to_html(
        fig, full_html=False,
        # Embed Plotly directly (True) instead of "cdn" -- a CDN <script>
        # tag leaves every chart blank when the file is opened somewhere
        # without internet access to cdn.plot.ly.
        include_plotlyjs=True if include_plotlyjs else False,
        config={"scrollZoom": True, "displayModeBar": True},
    )
    return html_div, f"ok ({n} bars, {dates[0]}→{dates[-1]})"


def build_report_html(report_date: str, flagged: dict[str, dict], ohlcv: dict[str, list[dict]]) -> str:
    """flagged: {ticker: {"category": str, "note": str}}  (order preserved)
    ohlcv:    {ticker: [{"t","o","h","l","c","v"}, ...]}
    """
    sections, skipped = [], []
    first = True
    ok = fail = 0

    for ticker, meta in flagged.items():
        rows = ohlcv.get(ticker, [])
        html_div, msg = build_chart_html(ticker, meta["category"], meta["note"], rows,
                                         include_plotlyjs=first)
        if html_div:
            first = False
            ok += 1
            sections.append(
                f"<div style='margin:0 0 22px;padding:6px;background:#0d1117;"
                f"border:1px solid #21262d;border-radius:8px;'>{html_div}</div>"
            )
        else:
            fail += 1
            skipped.append(ticker)
            sections.append(
                f"<div style='margin:0 0 14px;padding:14px;background:#161b22;"
                f"border:1px solid #30363d;border-radius:8px;font-family:monospace;"
                f"color:#8b949e;'>⚠ {ticker} — {msg}</div>"
            )

    skipped_note = (
        f"<p style='font-size:11px;color:#6e7681;'>Skipped (insufficient history): "
        f"{', '.join(skipped)}</p>" if skipped else ""
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>VSA Volume @ Price — Volume Scan {report_date}</title>
<style>
  body {{ background:#0d1117; color:#c9d1d9; font-family:'Courier New',monospace; margin:0; padding:24px; }}
  .hdr {{ background:linear-gradient(135deg,#0d1117 0%,#161b22 100%); padding:16px 20px;
          border-radius:10px; border:1px solid #30363d; margin-bottom:18px; }}
  .hdr h1 {{ font-size:18px; color:#f0f6fc; letter-spacing:2px; margin:0 0 6px; }}
  .hdr p {{ font-size:12px; color:#8b949e; margin:2px 0; }}
  .legend-note {{ font-size:11px; color:#6e7681; margin-top:8px; line-height:1.6; }}
</style>
</head>
<body>
  <div class="hdr">
    <h1>📊 VSA VOLUME @ PRICE — VOLUME SCAN {report_date}</h1>
    <p>Ported from the Colab "VSA 3D Performance Analyzer" (Vol @ Price 2D mode / plot_vol_at_price_2d) — buyer/seller volume bars anchored to the close price.</p>
    <p>{ok} chart(s) rendered, {fail} skipped &nbsp;·&nbsp; Green above close = buyer volume, Red below close = seller volume</p>
    <div class="legend-note">
      Tickers: every "fresh volume high" plus the top-ranked volume-spike names from today's scan across
      S&amp;P 500, Nasdaq Composite, and ETFs. Buyer/seller split is estimated from where each day's close
      landed within its High/Low range. Hover any bar for the exact split; scroll to zoom.
    </div>
    {skipped_note}
  </div>
  {''.join(sections)}
</body>
</html>"""


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("usage: plot_vsa2d.py <ohlcv_bundle.json> <out.html>", file=sys.stderr)
        raise SystemExit(1)
    with open(sys.argv[1]) as f:
        bundle = json.load(f)
    html = build_report_html(bundle["report_date"], bundle["flagged"], bundle["ohlcv"])
    with open(sys.argv[2], "w") as f:
        f.write(html)
    print(f"Wrote {sys.argv[2]}")

#!/usr/bin/env python3
"""3D Price + Volume chart builder — ports the Colab "VSA 3D Performance
Analyzer" (`plot_price_volume`) Scatter3d ribbon logic to a static,
self-contained HTML report, driven off already-downloaded OHLCV data
(no live network calls here; `scan_volume.py` supplies the data).

Each ticker gets one 3D chart: Date x Price x Volume, green ribbon
segments for up days, red for down days, with a volume drop-line down to
zero on every bar (same visual language as the Colab cell).
"""
from __future__ import annotations

import json
from typing import Iterable

import plotly.graph_objects as go
import plotly.io as pio


def _bars_from_ohlcv(rows: list[dict]) -> list[dict]:
    """Normalize a list of {"t","o","h","l","c","v"} rows (already sorted or
    not) into the {"date","price","vol","up"} shape the ribbon builder wants."""
    rows = sorted(rows, key=lambda r: r["t"])
    bars = []
    for r in rows:
        o = float(r["o"]) if r.get("o") is not None else float(r["c"])
        c = float(r["c"])
        v = float(r.get("v") or 0)
        bars.append({"date": r["t"], "price": c, "vol": v, "up": c >= o})
    return bars


def build_chart_html(ticker: str, category: str, note: str, ohlcv_rows: list[dict],
                     include_plotlyjs: bool = False) -> tuple[str | None, str]:
    bars = _bars_from_ohlcv(ohlcv_rows)
    if len(bars) < 2:
        return None, f"too few bars for {ticker} ({len(bars)})"

    fig = go.Figure()

    for i in range(len(bars) - 1):
        d0, d1 = bars[i], bars[i + 1]
        col = "#00c896" if d0["up"] else "#ff5252"
        fig.add_trace(go.Scatter3d(
            x=[d0["date"], d1["date"]], y=[d0["price"], d1["price"]], z=[d0["vol"], d1["vol"]],
            mode="lines",
            name="Up day" if (i == 0 and d0["up"]) else ("Down day" if i == 0 else None),
            showlegend=(i == 0), legendgroup="up" if d0["up"] else "down",
            line=dict(width=6, color=col),
            hovertemplate=(f"<b>{'▲ Up' if d0['up'] else '▼ Down'} day</b><br>"
                           f"Date: {d0['date']}<br>Price: ${d0['price']:.4f}<br>"
                           f"Volume: {int(d0['vol']):,}<extra></extra>"),
        ))

    last = bars[-1]
    fig.add_trace(go.Scatter3d(
        x=[last["date"]], y=[last["price"]], z=[last["vol"]],
        mode="markers", showlegend=False,
        marker=dict(size=5, color="#00c896" if last["up"] else "#ff5252"),
    ))

    gx, gy, gz, rx, ry, rz = [], [], [], [], [], []
    for d in bars:
        tx, ty, tz = (gx, gy, gz) if d["up"] else (rx, ry, rz)
        tx += [d["date"], d["date"], None]
        ty += [d["price"], d["price"], None]
        tz += [0, d["vol"], None]
    if gx:
        fig.add_trace(go.Scatter3d(x=gx, y=gy, z=gz, mode="lines", name="Volume (up)",
                                   line=dict(width=4, color="rgba(0,200,150,0.45)")))
    if rx:
        fig.add_trace(go.Scatter3d(x=rx, y=ry, z=rz, mode="lines", name="Volume (down)",
                                   line=dict(width=4, color="rgba(255,82,82,0.45)")))

    last_price = bars[-1]["price"]
    max_vol = max(d["vol"] for d in bars)
    pct_chg = ((bars[-1]["price"] / bars[0]["price"]) - 1) * 100 if bars[0]["price"] else 0.0
    first_date, last_date = bars[0]["date"], bars[-1]["date"]

    fig.update_layout(
        title=dict(
            text=(f"{ticker}  ·  {category}  ·  {note}<br>"
                  f"<span style='font-size:12px;color:#8b949e;'>"
                  f"Date × Price × Volume  ·  {first_date} → {last_date}  |  "
                  f"Last: ${last_price:.2f} ({pct_chg:+.1f}%)  |  Max vol: {int(max_vol):,}  |  "
                  f"Green = up day  ·  Red = down day</span>"),
            font=dict(size=16, color="#f0f6fc"), x=0.02),
        scene=dict(
            xaxis=dict(title="Date",           backgroundcolor="#0d1117", gridcolor="#30363d", color="#c9d1d9", showspikes=True),
            yaxis=dict(title="Price ($)",       backgroundcolor="#0d1117", gridcolor="#30363d", color="#c9d1d9", showspikes=True),
            zaxis=dict(title="Volume (shares)", backgroundcolor="#0d1117", gridcolor="#30363d", color="#c9d1d9", showspikes=True),
            camera=dict(eye=dict(x=1.8, y=-1.6, z=1.1)),
            aspectmode="manual", aspectratio=dict(x=2.2, y=1.2, z=1.0),
        ),
        template="plotly_dark", paper_bgcolor="#0d1117",
        autosize=False, width=1180, height=800,
        margin=dict(l=0, r=0, b=0, t=95),
        legend=dict(font=dict(color="#c9d1d9", size=11), bgcolor="rgba(13,17,23,0.85)",
                    bordercolor="#30363d", borderwidth=1, x=1.01, y=0.95),
    )

    html_div = pio.to_html(
        fig, full_html=False,
        include_plotlyjs="cdn" if include_plotlyjs else False,
        config={"scrollZoom": True, "displayModeBar": True},
    )
    return html_div, f"ok ({len(bars)} bars, {first_date}→{last_date}, {pct_chg:+.1f}%)"


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
<title>3D Price/Volume — Volume Scan {report_date}</title>
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
    <h1>⚡ 3D PRICE + VOLUME — VOLUME SCAN {report_date}</h1>
    <p>Ported from the Colab "VSA 3D Performance Analyzer" (plot_price_volume) — Date × Price × Volume ribbon, one chart per ticker.</p>
    <p>{ok} chart(s) rendered, {fail} skipped &nbsp;·&nbsp; Green = up day, Red = down day</p>
    <div class="legend-note">
      Tickers: every "fresh volume high" plus the top-ranked volume-spike names from today's scan across
      S&amp;P 500, Nasdaq Composite, and ETFs. Drag to rotate each chart · scroll to zoom · hover for date/price/volume.
    </div>
    {skipped_note}
  </div>
  {''.join(sections)}
</body>
</html>"""


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("usage: plot_3d.py <ohlcv_bundle.json> <out.html>", file=sys.stderr)
        raise SystemExit(1)
    with open(sys.argv[1]) as f:
        bundle = json.load(f)
    html = build_report_html(bundle["report_date"], bundle["flagged"], bundle["ohlcv"])
    with open(sys.argv[2], "w") as f:
        f.write(html)
    print(f"Wrote {sys.argv[2]}")

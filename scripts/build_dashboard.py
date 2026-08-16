#!/usr/bin/env python3
"""Builds reports/index.html -- a single-page toggle/tab dashboard linking
together the three reports this repo produces:

  1. Volume Scan (Top Movers)  -- reports/latest.md      (scan_volume.py)
  2. Volume @ Price (2D)       -- reports/volume_2d_latest.html (scan_volume.py / plot_vsa2d.py)
  3. Dual-Timeframe Watchlist  -- reports/dual_timeframe_latest.html (dual_timeframe_scan.py)

Run this LAST in the workflow, after the scripts that produce those three
files, so it always reflects whatever exists in reports/ at that point.
It never fails the whole build over a single missing report -- a tab whose
source file isn't present yet (e.g. the very first run before a given
script has ever succeeded) just renders a short "not available yet" note
instead of a broken iframe.

GitHub does not render .html files inline when browsing the repo, so this
still needs to be downloaded (or served via GitHub Pages) to view --
but it replaces having to separately open 2-3 files with one page and a
tab bar.
"""
from __future__ import annotations

import os
import re
import sys
from datetime import datetime, timezone

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(REPO_ROOT, "reports")

# Deep-links straight to this workflow's "Run workflow" button on GitHub.
# Deliberately NOT a one-click API trigger -- that would require embedding a
# GitHub access token in this page's HTML, and since GitHub Pages serves this
# publicly, anyone viewing the page could lift that token and use it to push
# to or modify the repo. This link just gets you to the button in one click;
# you still confirm the run yourself, signed in as you, on github.com.
WORKFLOW_RUN_URL = "https://github.com/danreed001-droid/volume/actions/workflows/volume-scan.yml"


def _escape(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def markdown_to_html(md_text: str) -> str:
    """Minimal Markdown -> HTML for the specific subset scan_volume.py writes:
    #/##/### headers, plain paragraphs, single-line italics (_like this_),
    and GFM pipe tables. Not a general-purpose Markdown parser -- just enough
    to render reports/latest.md's exact shape without adding a dependency.
    """
    lines = md_text.splitlines()
    out: list[str] = []
    i, n = 0, len(lines)

    while i < n:
        stripped = lines[i].strip()

        if not stripped:
            i += 1
            continue

        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            level = len(m.group(1))
            out.append(f"<h{level}>{_escape(m.group(2))}</h{level}>")
            i += 1
            continue

        is_table_sep = i + 1 < n and re.match(r"^\|?[\s:|-]+\|?$", lines[i + 1].strip())
        if stripped.startswith("|") and is_table_sep:
            header_cells = [c.strip() for c in stripped.strip("|").split("|")]
            aligns = []
            for c in lines[i + 1].strip().strip("|").split("|"):
                c = c.strip()
                if c.startswith(":") and c.endswith(":"):
                    aligns.append("center")
                elif c.endswith(":"):
                    aligns.append("right")
                else:
                    aligns.append("left")
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1

            def _row(cells, tag):
                tds = "".join(
                    f"<{tag} style='text-align:{aligns[j] if j < len(aligns) else 'left'}'>"
                    f"{_escape(c)}</{tag}>"
                    for j, c in enumerate(cells)
                )
                return f"<tr>{tds}</tr>"

            out.append("<table>")
            out.append(f"<thead>{_row(header_cells, 'th')}</thead>")
            out.append("<tbody>" + "".join(_row(r, "td") for r in rows) + "</tbody>")
            out.append("</table>")
            continue

        m = re.match(r"^_(.*)_$", stripped)
        if m:
            out.append(f"<p><em>{_escape(m.group(1))}</em></p>")
            i += 1
            continue

        out.append(f"<p>{_escape(stripped)}</p>")
        i += 1

    return "\n".join(out)


# Order matters -- this is the left-to-right tab order in the UI.
TABS = [
    {"id": "scan", "label": "Volume Scan (Top Movers)", "kind": "markdown", "path": "latest.md"},
    {"id": "2d", "label": "Volume @ Price (2D)", "kind": "iframe", "path": "volume_2d_latest.html"},
    {"id": "dual", "label": "Dual-Timeframe Watchlist", "kind": "iframe", "path": "dual_timeframe_latest.html"},
    # A separate repo/site (not one of this workflow's own reports), so it's
    # "external" rather than "iframe": always available (no local file to
    # check for), and rendered with a visible "open directly" link alongside
    # the embed in case GitHub Pages or that repo ever adds framing
    # restrictions this workflow has no control over.
    {
        "id": "moneyflow",
        "label": "Money Flow",
        "kind": "external",
        "url": "https://danreed001-droid.github.io/moneyflow/",
    },
]

PAGE_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Volume Reports Dashboard</title>
<style>
  :root {
    --plane: #0d1117; --surface: #161b22; --ink: #f0f6fc; --muted: #8b949e;
    --border: #30363d; --series: #58a6ff; --good: #3fb950; --critical: #f85149;
  }
  * { box-sizing: border-box; }
  body {
    background: var(--plane); color: var(--ink); margin: 0; padding: 20px;
    font-family: 'Courier New', monospace;
  }
  .hdr {
    background: linear-gradient(135deg, #0d1117 0%, #161b22 100%);
    padding: 14px 18px; border-radius: 10px; border: 1px solid var(--border);
    margin-bottom: 16px;
    display: flex; align-items: center; justify-content: space-between; gap: 16px;
    flex-wrap: wrap;
  }
  .hdr h1 { font-size: 18px; letter-spacing: 1px; margin: 0 0 4px; }
  .hdr p { font-size: 12px; color: var(--muted); margin: 2px 0; }
  .run-btn {
    background: var(--good); color: #0d1117; border: none; border-radius: 999px;
    padding: 10px 18px; font: inherit; font-size: 12px; font-weight: bold;
    letter-spacing: 0.5px; text-decoration: none; white-space: nowrap;
    display: inline-flex; align-items: center; gap: 6px;
  }
  .run-btn:hover { filter: brightness(1.1); }
  .tabbar { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 14px; }
  .tab-btn {
    background: var(--surface); color: var(--ink); border: 1px solid var(--border);
    border-radius: 999px; padding: 8px 16px; font: inherit; font-size: 12px;
    cursor: pointer; letter-spacing: 0.5px;
  }
  .tab-btn:hover:not(:disabled) { border-color: var(--series); }
  .tab-btn.active { background: var(--series); color: #0d1117; border-color: var(--series); font-weight: bold; }
  .tab-btn:disabled { opacity: 0.45; cursor: not-allowed; }
  .tab-panel { display: none; }
  .tab-panel.active { display: block; }
  .report-frame {
    width: 100%; height: 82vh; border: 1px solid var(--border); border-radius: 8px;
    background: var(--plane);
  }
  .external-note {
    font-size: 11px; color: var(--muted); margin: 0 0 8px;
  }
  .external-note a { color: var(--series); }
  .md-report {
    background: var(--surface); border: 1px solid var(--border); border-radius: 8px;
    padding: 16px 20px; max-height: 82vh; overflow: auto;
  }
  .md-report h1 { font-size: 17px; }
  .md-report h2 { font-size: 15px; color: var(--series); margin-top: 22px; }
  .md-report h3 { font-size: 13px; color: var(--muted); margin-top: 16px; }
  .md-report p { font-size: 12px; color: var(--muted); }
  table { border-collapse: collapse; width: 100%; margin: 10px 0 18px; font-size: 12px; }
  th, td { border-bottom: 1px solid var(--border); padding: 5px 10px; }
  th { color: var(--muted); font-weight: normal; text-transform: uppercase; font-size: 11px; }
  .empty-note {
    background: var(--surface); border: 1px dashed var(--border); border-radius: 8px;
    padding: 24px; color: var(--muted); font-size: 12px; line-height: 1.6;
  }
  .empty-note code { color: var(--ink); }
</style>
</head>
<body>
  <div class="hdr">
    <div>
      <h1>Volume Reports Dashboard</h1>
      <p>Generated __GENERATED__ &middot; toggle between the three reports below &mdash; each tab is the same file you'd otherwise open separately from reports/</p>
    </div>
    <div>
      <a class="run-btn" href="__WORKFLOW_RUN_URL__" target="_blank" rel="noopener">&#9654; Run scan now</a>
    </div>
  </div>
  <div class="tabbar">
__TAB_BUTTONS__
  </div>
__TAB_PANELS__
  <script>
    const buttons = document.querySelectorAll('.tab-btn');
    const panels = document.querySelectorAll('.tab-panel');

    function activate(tabId) {
      buttons.forEach(b => b.classList.toggle('active', b.dataset.tab === tabId));
      panels.forEach(p => p.classList.toggle('active', p.id === 'panel-' + tabId));
      const panel = document.getElementById('panel-' + tabId);
      if (panel) {
        const frame = panel.querySelector('iframe[data-src]');
        if (frame) {
          frame.src = frame.getAttribute('data-src');
          frame.removeAttribute('data-src');
        }
      }
    }

    buttons.forEach(b => {
      if (!b.disabled) b.addEventListener('click', () => activate(b.dataset.tab));
    });

    const defaultTab = '__DEFAULT_TAB__';
    if (defaultTab) activate(defaultTab);
  </script>
</body>
</html>
"""


def build_dashboard() -> str:
    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    tab_buttons: list[str] = []
    tab_panels: list[str] = []
    first_available: str | None = None

    for tab in TABS:
        if tab["kind"] == "external":
            # A link to a different site entirely -- always "available" since
            # there's no local file to check for; embedded via iframe with a
            # plain link right above it in case that site (out of this repo's
            # control) ever blocks being framed.
            available = True
        else:
            full_path = os.path.join(REPORTS_DIR, tab["path"])
            available = os.path.isfile(full_path)

        if available and first_available is None:
            first_available = tab["id"]

        disabled_attr = "" if available else " disabled"
        suffix = "" if available else " (unavailable)"
        tab_buttons.append(
            f'    <button class="tab-btn" data-tab="{tab["id"]}"{disabled_attr}>'
            f'{_escape(tab["label"])}{suffix}</button>'
        )

        if not available:
            body = (
                '<div class="empty-note">This report has not been generated yet '
                f'(<code>reports/{_escape(tab["path"])}</code> not found). '
                "It will appear here automatically once that step of the workflow "
                "runs successfully.</div>"
            )
        elif tab["kind"] == "iframe":
            body = f'<iframe data-src="{tab["path"]}" class="report-frame"></iframe>'
        elif tab["kind"] == "external":
            body = (
                f'<p class="external-note">From a separate site/repo &mdash; '
                f'<a href="{tab["url"]}" target="_blank" rel="noopener">open directly '
                f'in a new tab &#8599;</a> if it doesn\'t load below.</p>'
                f'<iframe data-src="{tab["url"]}" class="report-frame"></iframe>'
            )
        else:
            with open(full_path, encoding="utf-8") as f:
                body = f'<div class="md-report">{markdown_to_html(f.read())}</div>'

        tab_panels.append(f'  <section class="tab-panel" id="panel-{tab["id"]}">{body}</section>')

    html = PAGE_HEAD
    html = html.replace("__GENERATED__", generated)
    html = html.replace("__WORKFLOW_RUN_URL__", WORKFLOW_RUN_URL)
    html = html.replace("__TAB_BUTTONS__", "\n".join(tab_buttons))
    html = html.replace("__TAB_PANELS__", "\n".join(tab_panels))
    html = html.replace("__DEFAULT_TAB__", first_available or "")
    return html


def main() -> None:
    os.makedirs(REPORTS_DIR, exist_ok=True)
    html = build_dashboard()
    out_path = os.path.join(REPORTS_DIR, "index.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Wrote {out_path}", file=sys.stderr)


if __name__ == "__main__":
    main()

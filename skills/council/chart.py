#!/usr/bin/env python3
"""Draw the council's score climb as a full-width vector chart (inline SVG in HTML): horizontal bars, one per
delegate, while there is one round; from round 2 on, one combined line chart with a line per delegate.

Usage: python3 chart.py scores.json out.html

scores.json:
{
  "title": "PR #1 council",
  "bar": 9,
  "started": "2026-11-17T00:56:22Z",              # when the council began
  "rounds": [{"finished": "2026-11-17T01:20:00Z"}, {"finished": null}],   # null = still running
  "delegates": [{"name": "Claude Opus 5.5", "scores": [8, null]}, ...]    # null = no score yet
}

Each round's step time is from the previous round's finish (or `started`) to this round's finish, in minutes:
the fixing and the reviewing together. Delegates keep their color for the whole loop, in list order.
"""
from datetime import datetime
from html import escape
import json
import sys

LIGHT = ['#2a78d6', '#eb6834', '#1baf7a']  # validated categorical slots 1-3 (dataviz reference palette)
DARK = ['#3987e5', '#d95926', '#199e70']
W, H = 720, 400


def when(text: str | None) -> datetime | None:
    return datetime.fromisoformat(text.replace('Z', '+00:00')) if text else None


def step_times(data: dict) -> list[str]:
    """Each round's step time: from the previous round's finish (or the council's start) to this round's finish."""
    out, previous = [], when(data.get('started'))
    for rnd in data['rounds']:
        finished = when(rnd.get('finished'))
        out.append(f'{(finished - previous).total_seconds() / 60:.0f} min' if finished and previous else 'running')
        previous = finished or previous
    return out


def bars(data: dict) -> tuple[list[str], int]:
    """One round: a horizontal bar per delegate, score 0-10, with the bar line dashed across."""
    delegates, bar = data['delegates'], data.get('bar', 9)
    left, right, top, row = 140, 40, 8, 52
    height = top + row * len(delegates) + 56
    plot_w = W - left - right

    def x(score: float) -> float:
        return left + plot_w * score / 10

    parts = []
    for s in range(0, 11):
        parts.append(f'<line class="grid" x1="{x(s):.1f}" x2="{x(s):.1f}" y1="{top}" y2="{top + row * len(delegates)}"/>')
        parts.append(f'<text class="axis" x="{x(s):.1f}" y="{top + row * len(delegates) + 18}" text-anchor="middle">{s}</text>')
    for d, delegate in enumerate(delegates):
        cy = top + row * d + row / 2
        name = escape(delegate['name'])
        parts.append(f'<text class="axis" x="{left - 12}" y="{cy + 4:.1f}" text-anchor="end">{name}</text>')
        score = delegate['scores'][0] if delegate['scores'] else None
        if score is None:
            parts.append(f'<text class="axis" x="{left + 8}" y="{cy + 4:.1f}">pending</text>')
            continue
        parts.append(f'<g><title>{name}, round 1: {score}/10</title>'
                     f'<rect class="s{d}" x="{left}" y="{cy - 14:.1f}" width="{x(score) - left:.1f}" height="28" rx="4"/>'
                     f'<text class="val" x="{x(score) + 8:.1f}" y="{cy + 5:.1f}">{score:g}</text></g>')
    parts.append(f'<line class="bar" x1="{x(bar):.1f}" x2="{x(bar):.1f}" y1="{top - 4}" y2="{top + row * len(delegates) + 4}"/>')
    parts.append(f'<text class="axis" x="{left + plot_w / 2:.1f}" y="{height - 8}" text-anchor="middle">'
                 f'Round 1 · {step_times(data)[0]}</text>')
    return parts, height


def lines(data: dict) -> tuple[list[str], int]:
    """Two or more rounds: one line per delegate, a point per round with its score, the bar dashed across."""
    rounds, delegates, bar = data['rounds'], data['delegates'], data.get('bar', 9)
    left, right, top, bottom = 48, 24, 24, 64
    n = len(rounds)
    plot_w, plot_h = W - left - right, H - top - bottom

    def x(i: int) -> float:
        return left + plot_w * (0.06 + 0.88 * i / (n - 1))

    def y(score: float) -> float:
        return top + plot_h * (1 - score / 10)

    def px(d: int, i: int) -> float:
        """x of delegate d's point in round i; tied scores sit side by side so no point hides another."""
        s = delegates[d]['scores'][i]
        same = [e for e in range(len(delegates)) if i < len(delegates[e]['scores']) and delegates[e]['scores'][i] == s]
        return x(i) + (same.index(d) - (len(same) - 1) / 2) * 16

    parts = []
    for s in range(0, 11):
        parts.append(f'<line class="grid" x1="{left}" x2="{W - right}" y1="{y(s):.1f}" y2="{y(s):.1f}"/>')
        parts.append(f'<text class="axis" x="{left - 10}" y="{y(s) + 4:.1f}" text-anchor="end">{s}</text>')
    parts.append(f'<line class="bar" x1="{left}" x2="{W - right}" y1="{y(bar):.1f}" y2="{y(bar):.1f}"/>')
    for i, step in enumerate(step_times(data)):
        parts.append(f'<text class="axis" x="{x(i):.1f}" y="{H - bottom + 22}" text-anchor="middle">Round {i + 1}</text>')
        parts.append(f'<text class="step" x="{x(i):.1f}" y="{H - bottom + 40}" text-anchor="middle">{step}</text>')
    for d, delegate in enumerate(delegates):
        points = [(i, s) for i, s in enumerate(delegate['scores']) if s is not None]
        if len(points) > 1:
            path = ' '.join(f'{"M" if k == 0 else "L"}{px(d, i):.1f},{y(s):.1f}' for k, (i, s) in enumerate(points))
            parts.append(f'<path class="s{d}" d="{path}" fill="none" stroke-width="2"/>')
        for i, s in points:
            cx = px(d, i)
            parts.append(f'<g><title>{escape(delegate["name"])}, round {i + 1}: {s}/10</title>'
                         f'<circle class="s{d}" cx="{cx:.1f}" cy="{y(s):.1f}" r="6"/>'
                         f'<circle cx="{cx:.1f}" cy="{y(s):.1f}" r="14" fill="transparent"/>'
                         f'<text class="val" x="{cx:.1f}" y="{y(s) - 12:.1f}" text-anchor="middle">{s:g}</text></g>')
    return parts, H


def main(source: str, target: str) -> None:
    data = json.load(open(source))
    delegates, bar = data['delegates'], data.get('bar', 9)
    parts, height = bars(data) if len(data['rounds']) <= 1 else lines(data)

    legend = ''.join(
        f'<span><i class="k{d}"></i>{escape(dl["name"])}: '
        f'{" → ".join("pending" if s is None else f"{s:g}" for s in dl["scores"])}</span>'
        for d, dl in enumerate(delegates))
    color_css = '\n'.join(f'.s{d}{{stroke:{c};fill:{c}}} path.s{d}{{fill:none}} .k{d}{{background:{c}}}'
                          for d, c in enumerate(LIGHT))
    dark_css = '\n'.join(f'.s{d}{{stroke:{c};fill:{c}}} path.s{d}{{fill:none}} .k{d}{{background:{c}}}'
                         for d, c in enumerate(DARK))
    html = f'''<!doctype html><meta charset="utf-8">
<style>
.chart{{width:100%;font-family:var(--font-sans,system-ui)}}
.chart h3{{margin:0 0 4px;font-size:15px;font-weight:600}}
.chart p{{margin:0 0 8px;font-size:13px;color:var(--muted-foreground,#666)}}
svg{{width:100%;height:auto;display:block;overflow:visible}}
.grid{{stroke:var(--border,#ddd);stroke-width:1}}
.axis,.step{{font-size:12px;fill:var(--muted-foreground,#666)}}
.step{{font-size:11px}}
.bar{{stroke:var(--foreground,#222);stroke-width:1.5;stroke-dasharray:6 5;opacity:.6}}
.barlabel{{font-size:11px;fill:var(--muted-foreground,#666)}}
.val{{font-size:13px;font-weight:600;fill:var(--foreground,#222)}}
.legend{{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:13px;margin-top:6px}}
.legend i{{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:6px;vertical-align:-1px}}
{color_css}
@media (prefers-color-scheme: dark) {{
{dark_css}
}}
</style>
<div class="chart">
<h3>{escape(data.get("title", "Council scores by round"))}</h3>
<p>Score out of 10 per round. Dashed line: the {bar}/10 bar every delegate must reach. Minutes per round: how long that step took (fixes plus review).</p>
<svg viewBox="0 0 {W} {height}" role="img" aria-label="Council scores by round">{"".join(parts)}</svg>
<div class="legend">{legend}</div>
</div>'''
    open(target, 'w').write(html)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])

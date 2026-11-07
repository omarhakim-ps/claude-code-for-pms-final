"""Build the weekly 4.2 outcome review page.

Usage: python3 -I build_report.py <data.json> <config.json> <out.html> <as_of YYYY-MM-DD>

<data.json> holds the rows from queries/weekly.sql: either a JSON list of
row objects, or the rook-database reply pasted as-is (one JSON object per line).
Prints KEY=value lines for the skill to read.
"""
import datetime as dt
import html
import json
import sys


def load_rows(path):
    text = open(path, encoding="utf-8").read()
    try:
        rows = json.loads(text)
    except ValueError:
        rows = [json.loads(l) for l in text.splitlines() if l.strip().startswith("{")]
    out = []
    for r in rows:
        row = {k: (int(v) if k != "week_start" and v is not None else v) for k, v in r.items()}
        row["week_start"] = str(r["week_start"])[:10]
        out.append(row)
    return sorted(out, key=lambda r: r["week_start"])


def d(s):
    return dt.date.fromisoformat(s) if s else None


def week_of(day):
    return day - dt.timedelta(days=day.weekday()) if day else None


def pct(n, m):
    return round(100.0 * n / m, 1) if m else None


def main(data_path, cfg_path, out_path, as_of):
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    rows = load_rows(data_path)
    if not rows:
        print("RESULT=no-data")
        return

    w42 = d(cfg["release_42_week"])
    ship = {k: d(cfg[k]["ship_date"]) for k in ("release_a", "release_b")}
    ship_wk = {k: week_of(v) for k, v in ship.items()}
    baseline = set(cfg["baseline_weeks"])
    n_window = cfg["verdict_window_weeks"]

    def phase(wk):
        if wk < w42:
            return "Before 4.2"
        if wk == w42:
            return "4.2 week"
        b, a = ship_wk["release_b"], ship_wk["release_a"]
        if b and wk == b:
            return "Release B week"
        if b and wk > b:
            return "After B"
        if a and wk == a:
            return "Release A week"
        if a and wk > a:
            return "After A"
        return "After 4.2"

    for r in rows:
        wk = d(r["week_start"])
        r["phase"] = phase(wk)
        r["full_week"] = r.get("days_with_data", 7) >= 7

    def evaluable(r, release):
        """A full week after the ship week of the release this measure waits on."""
        sw = ship_wk[release]
        return bool(sw) and r["full_week"] and d(r["week_start"]) > sw

    measures = {}
    for key, m in cfg["measures"].items():
        base_n = sum(r[m["numerator"]] for r in rows if r["week_start"] in baseline)
        base_d = sum(r[m["denominator"]] for r in rows if r["week_start"] in baseline)
        series, statuses = [], []
        for r in rows:
            v = pct(r[m["numerator"]], r[m["denominator"]])
            series.append(v)
            if v is None or not evaluable(r, m["expected_from"]):
                statuses.append("")
            elif v >= m["on_track_at"]:
                statuses.append("on")
            elif v >= m["range_low"]:
                statuses.append("watch")
            else:
                statuses.append("off")
        elig = [r for r in rows if evaluable(r, m["expected_from"])]
        window = elig[-n_window:]
        if not ship[m["expected_from"]]:
            verdict, vtext, pooled = "pending", "Not shipped yet: no ship date set for " + (
                "Release A" if m["expected_from"] == "release_a" else "Release B"), None
        elif len(window) < n_window:
            verdict, pooled = "pending", None
            vtext = "Too early: %d of %d full weeks after %s" % (
                len(window), n_window, "Release A" if m["expected_from"] == "release_a" else "Release B")
        else:
            pooled = pct(sum(r[m["numerator"]] for r in window), sum(r[m["denominator"]] for r in window))
            if pooled >= m["on_track_at"]:
                verdict, vtext = "on", "Reached"
            elif pooled >= m["range_low"]:
                verdict, vtext = "watch", "Within range, below target"
            else:
                verdict, vtext = "off", "Not reached"
        latest_full = [r for r in rows if r["full_week"]][-1]
        measures[key] = {
            "label": m["label"], "source": m["source"],
            "target": m["on_track_at"], "low": m["range_low"],
            "baseline": pct(base_n, base_d),
            "series": series, "statuses": statuses,
            "verdict": verdict, "verdict_text": vtext, "pooled": pooled,
            "window": [r["week_start"] for r in window],
            "latest": pct(latest_full[m["numerator"]], latest_full[m["denominator"]]),
            "latest_week": latest_full["week_start"],
            "expected_from": "Release A" if m["expected_from"] == "release_a" else "Release B",
        }

    payload = {
        "as_of": as_of,
        "weeks": [r["week_start"] for r in rows],
        "phases": [r["phase"] for r in rows],
        "full": [r["full_week"] for r in rows],
        "rows": rows,
        "measures": measures,
        "markers": {k: v for k, v in {
            "4.2": str(w42),
            "Release A": str(ship_wk["release_a"]) if ship_wk["release_a"] else None,
            "Release B": str(ship_wk["release_b"]) if ship_wk["release_b"] else None,
        }.items() if v},
        "releases": {k: {"name": cfg[k]["name"], "ship_date": cfg[k]["ship_date"]} for k in ("release_a", "release_b")},
        "window_n": n_window,
    }
    page = TEMPLATE.replace("__DATA__", json.dumps(payload).replace("</", "<\\/")).replace(
        "__ASOF__", html.escape(as_of))
    open(out_path, "w", encoding="utf-8").write(page)

    last = rows[-1]["week_start"]
    print("RESULT=built")
    print("OUT=" + out_path)
    print("LAST_WEEK=" + last)
    print("WEEKS_AFTER_A=%d" % sum(1 for r in rows if r["phase"] in ("After A", "Release B week", "After B")))
    print("WEEKS_AFTER_B=%d" % sum(1 for r in rows if r["phase"] == "After B"))
    for k, m in measures.items():
        print("%s=%s|%s|latest %s%% (week of %s)|pooled %s|baseline %s%%|target %s%%" % (
            k.upper(), m["verdict"], m["verdict_text"], m["latest"], m["latest_week"],
            m["pooled"], m["baseline"], m["target"]))


TEMPLATE = r"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Weekly Outcome Review</title>
<style>
:root{--bg:#fafaf8;--card:#fff;--ink:#1d1d1b;--muted:#6b6b66;--line:#e4e3de;
--on:#1f7a4d;--on-bg:#e3f3ea;--watch:#9a6200;--watch-bg:#fbf0d9;--off:#b3261e;--off-bg:#fbe4e2;
--pend:#5b5b57;--pend-bg:#efefec;--series:#2f5fb3;--target:#1f7a4d;--base:#8a8a85;--band:rgba(31,122,77,.10);
color-scheme:light}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);
font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
main{max-width:1100px;margin:0 auto;padding:24px 16px 48px}
h1{font-size:24px;margin:0 0 4px}h2{font-size:17px;margin:32px 0 10px}
.sub{color:var(--muted);margin:0 0 20px}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px}
.card .lbl{font-size:13px;color:var(--muted)}.card .big{font-size:28px;font-weight:650;margin:4px 0}
.pill{display:inline-block;font-size:12px;font-weight:600;padding:2px 8px;border-radius:99px}
.on{color:var(--on);background:var(--on-bg)}.watch{color:var(--watch);background:var(--watch-bg)}
.off{color:var(--off);background:var(--off-bg)}.pending{color:var(--pend);background:var(--pend-bg)}
.card .meta{font-size:13px;color:var(--muted);margin-top:6px}
.charts{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,480px),1fr));gap:12px}
.chart{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}
.chart h3{font-size:14px;margin:0 0 8px}.cv{position:relative;height:230px}
.tablewrap{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:10px}
table{border-collapse:collapse;width:100%;font-size:13px}th,td{padding:6px 10px;text-align:right;
border-bottom:1px solid var(--line);white-space:nowrap}th:first-child,td:first-child,th:nth-child(2),td:nth-child(2){text-align:left}
th{color:var(--muted);font-weight:600}tr.partial td{color:var(--muted);font-style:italic}
td .pill{margin-left:4px}
.notes{font-size:13px;color:var(--muted)}.notes li{margin:4px 0}
</style></head><body><main>
<h1>Weekly outcome review</h1>
<p class="sub" id="sub"></p>
<div class="cards" id="cards"></div>
<h2>Trends</h2>
<p class="notes">Blue: weekly rate. Grey dashed: before-4.2 average. Green: target, with the brief's range shaded. Vertical lines mark 4.2 and each release.</p>
<div class="charts" id="charts"></div>
<h2>Ping-related support tickets</h2>
<div class="chart"><div class="cv"><canvas id="tickets"></canvas></div></div>
<h2>Week by week</h2>
<div class="tablewrap"><table id="tbl"></table></div>
<h2>How this review decides</h2>
<ul class="notes" id="rules"></ul>
</main>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.js"></script>
<script>
const D = __DATA__;
const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const fmtWk = s => new Date(s+"T00:00:00").toLocaleDateString("en-GB",{day:"numeric",month:"short"});
const pillCls = v => ({on:"on",watch:"watch",off:"off"}[v]||"pending");
const pillTxt = v => ({on:"On track",watch:"Watch",off:"Off track"}[v]||"");
const rel = D.releases;
document.getElementById("sub").textContent =
  "As of " + "__ASOF__" + " · data through the week of " + fmtWk(D.weeks[D.weeks.length-1]) +
  " · Release A " + (rel.release_a.ship_date || "not set") + " · Release B " + (rel.release_b.ship_date || "not set");

const cards = document.getElementById("cards");
for (const [k,m] of Object.entries(D.measures)) {
  const el = document.createElement("div"); el.className = "card";
  const shown = m.pooled != null ? m.pooled : m.latest;
  const what = m.pooled != null ? "last " + D.window_n + " full weeks, pooled" : "latest full week (" + fmtWk(m.latest_week) + ")";
  el.innerHTML = `<div class="lbl"></div><div class="big">${shown}%</div>
   <span class="pill ${pillCls(m.verdict)}"></span>
   <div class="meta">${what}<br>Target ${m.target}% · range from ${m.low}% · before 4.2 ${m.baseline}%<br>Judged after ${m.expected_from}</div>`;
  el.querySelector(".lbl").textContent = m.label;
  el.querySelector(".pill").textContent = m.verdict_text;
  cards.appendChild(el);
}

const markerPlugin = {id:"markers", afterDatasetsDraw(c){
  const {ctx, chartArea:a, scales:{x}} = c;
  ctx.save(); ctx.font = "11px sans-serif"; ctx.fillStyle = css("--muted");
  Object.entries(D.markers).forEach(([name, wk], j) => {
    const i = D.weeks.indexOf(wk); if (i < 0) return;
    const px = x.getPixelForValue(i);
    ctx.strokeStyle = css("--muted"); ctx.setLineDash([2,3]); ctx.beginPath();
    ctx.moveTo(px, a.top); ctx.lineTo(px, a.bottom); ctx.stroke();
    ctx.setLineDash([]); ctx.fillText(name, px + 3, a.top + 10 + 12 * j);
  });
  ctx.restore();
}};
const labels = D.weeks.map(fmtWk);
const charts = document.getElementById("charts");
const haveCharts = typeof Chart !== "undefined";
if (!haveCharts) {
  charts.innerHTML = '<p class="notes">Charts need an internet connection to load. Open this file in your web browser (Chrome, Safari) while online. The verdicts and the week-by-week table below are complete without them.</p>';
  document.getElementById("tickets").parentNode.parentNode.style.display = "none";
}
if (haveCharts) {
const base = {responsive:true, maintainAspectRatio:false, animation:false,
  plugins:{legend:{display:false}, tooltip:{mode:"index", intersect:false}},
  scales:{x:{grid:{display:false}, ticks:{color:css("--muted"), maxRotation:0, autoSkip:true}},
          y:{grid:{color:css("--line")}, ticks:{color:css("--muted"), callback:v=>v+"%"}}}};
for (const [k,m] of Object.entries(D.measures)) {
  const box = document.createElement("div"); box.className = "chart";
  box.innerHTML = `<h3></h3><div class="cv"><canvas></canvas></div>`;
  box.querySelector("h3").textContent = m.label;
  charts.appendChild(box);
  const n = D.weeks.length;
  const vals = m.series.concat([m.target, m.low, m.baseline]).filter(v => v != null);
  const lo = Math.max(0, Math.floor((Math.min(...vals) - 5) / 5) * 5);
  const hi = Math.min(100, Math.ceil((Math.max(...vals) + 3) / 5) * 5);
  new Chart(box.querySelector("canvas"), {type:"line", plugins:[markerPlugin],
    data:{labels, datasets:[
      {label:"Range low", data:Array(n).fill(m.low), borderWidth:0, pointRadius:0, fill:false},
      {label:"Target", data:Array(n).fill(m.target), borderColor:css("--target"), borderWidth:1.5,
       pointRadius:0, fill:"-1", backgroundColor:css("--band")},
      {label:"Before 4.2", data:Array(n).fill(m.baseline), borderColor:css("--base"), borderDash:[5,4],
       borderWidth:1.5, pointRadius:0, fill:false},
      {label:"Weekly", data:m.series, borderColor:css("--series"), backgroundColor:css("--series"),
       borderWidth:2.5, pointRadius:D.full.map(f => f ? 3 : 2), pointStyle:D.full.map(f => f ? "circle" : "crossRot"),
       fill:false, tension:0}
    ]},
    options:{...base, scales:{...base.scales, y:{...base.scales.y, min:lo, max:hi}}}});
}
new Chart(document.getElementById("tickets"), {type:"bar", plugins:[markerPlugin],
  data:{labels, datasets:[
    {label:"\"No pings\"", data:D.rows.map(r=>r.no_pings_tickets), backgroundColor:css("--series")},
    {label:"\"Gone before I could answer\"", data:D.rows.map(r=>r.gone_tickets), backgroundColor:css("--watch")}
  ]},
  options:{...base, plugins:{...base.plugins, legend:{display:true, labels:{color:css("--ink")}}},
    scales:{x:{...base.scales.x, stacked:true}, y:{stacked:true, grid:{color:css("--line")}, ticks:{color:css("--muted"), precision:0}}}}});
}

const keys = Object.keys(D.measures);
let h = "<tr><th>Week of</th><th>Phase</th><th>Callouts</th><th>Pings</th>" +
  keys.map(k => `<th>${D.measures[k].label.split(" (")[0]}</th>`).join("") +
  "<th>Missed</th><th>No-pings tickets</th><th>Gone tickets</th><th>All tickets</th></tr>";
D.rows.forEach((r,i) => {
  h += `<tr class="${r.full_week ? "" : "partial"}"><td>${fmtWk(r.week_start)}${r.full_week ? "" : " (partial)"}</td><td>${r.phase}</td>` +
    `<td>${r.callouts}</td><td>${r.pings}</td>` +
    keys.map(k => { const m = D.measures[k], s = m.statuses[i];
      return `<td>${m.series[i] ?? "–"}%${s ? `<span class="pill ${s}">${pillTxt(s)}</span>` : ""}</td>`; }).join("") +
    `<td>${r.missed}</td><td>${r.no_pings_tickets}</td><td>${r.gone_tickets}</td><td>${r.all_tickets}</td></tr>`;
});
document.getElementById("tbl").innerHTML = h;

const rules = [
  "Before-4.2 average: the six full weeks from 29 Jun to 3 Aug. The 4.2 week (10 Aug) and each release's ship week are shown but never judged.",
  "Pings answered and pings taken are judged from the first full week after Release A (alerts and nudges). Callouts filled and the quiet four's share are judged from the first full week after Release B (penalty, restore, recovery, retry).",
  "Each judged week: On track at or above the brief's central projection; Watch inside the brief's range; Off track below it.",
  "Headline verdict: the last " + D.window_n + " judged weeks pooled together (about 500 pings), because one week of ~165 pings moves a rate by several points on noise alone.",
  "Quiet four: Vesper, The Undertow, Farlight and Meteor Mite. Its 20% watch floor is a review assumption; the brief gives only 27%.",
  "Ticket groups match subject lines (\"hardly anything for\", \"has not gone off\", \"moved on\", \"gone before\" and similar). Once Release A adds per-ping tickets with categories, switch to those categories.",
  "Partial weeks (fewer than 7 days of callouts) are shown in italics and not judged."
];
document.getElementById("rules").innerHTML = rules.map(t => `<li>${t}</li>`).join("");
</script></body></html>
"""

if __name__ == "__main__":
    main(*sys.argv[1:5])

"""Release QA helper for Rook Dispatch routing.

  python3 -I qa.py scan   --repo <repo> --levers <levers.json> --out <facts.json>
  python3 -I qa.py page   --findings <findings.json> --out <page.html>
  python3 -I qa.py record --repo <repo> --levers <levers.json> --facts <facts.json>
  python3 -I qa.py ship   --repo <repo> --levers <levers.json> --label <e.g. 4.3>

State lives in <repo>/qa/state.json. "The upcoming release" is everything in
the routing code folder that differs from the code as it was when the last
release shipped (committed or not), plus the CHANGELOG sections above the
last shipped version. Prints KEY=value lines.
"""
import argparse
import ast
import datetime as dt
import hashlib
import html
import json
import os
import re
import subprocess
import sys


def git(repo, *args, check=True):
    r = subprocess.run(["git", "-C", repo] + list(args), capture_output=True, text=True)
    if check and r.returncode != 0:
        sys.exit("git %s failed: %s" % (" ".join(args), r.stderr.strip()))
    return r.stdout


def load_state(repo, levers):
    path = os.path.join(repo, "qa", "state.json")
    if os.path.exists(path):
        return path, json.load(open(path, encoding="utf-8"))
    head = git(repo, "rev-parse", "HEAD").strip()
    state = {"shipped_baseline": head, "last_shipped": levers["last_shipped"],
             "baseline_set_on": dt.date.today().isoformat(), "last_run": None,
             "file_hashes": {}, "constant_status": {}}
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(state, open(path, "w", encoding="utf-8"), indent=2)
    return path, state


def constants(src):
    out = {}
    if src is None:
        return out
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return {"__syntax_error__": True}
    for node in tree.body:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id.isupper():
                    out[t.id] = node.value.value
    return out


def upcoming_changelog(text, last_shipped):
    if not text:
        return []
    parts = re.split(r"(?m)^## ", text)
    out = []
    for p in parts[1:]:
        heading, _, body = p.partition("\n")
        if heading.strip().startswith(last_shipped):
            break
        out.append({"heading": heading.strip(), "body": body.strip()})
    return out


def file_diffs(repo, base, code_dir):
    diff = git(repo, "diff", "--no-color", "--no-ext-diff", base, "--", code_dir)
    files = {}
    cur = None
    for line in diff.splitlines():
        m = re.match(r"^diff --git a/(.+?) b/(.+)$", line)
        if m:
            cur = m.group(2)
            files[cur] = []
            continue
        if cur is not None:
            files[cur].append(line)
    untracked = git(repo, "ls-files", "--others", "--exclude-standard", "--", code_dir).split()
    for f in untracked:
        if os.path.basename(f) == ".DS_Store":
            continue
        try:
            body = open(os.path.join(repo, f), encoding="utf-8").read().splitlines()
        except (UnicodeDecodeError, OSError):
            body = ["(binary or unreadable)"]
        files[f] = ["new file (not yet committed)", "+++ b/" + f] + ["+" + l for l in body]
    return files


def cmd_scan(a):
    levers = json.load(open(a.levers, encoding="utf-8"))
    repo = git(a.repo, "rev-parse", "--show-toplevel").strip()
    state_path, state = load_state(repo, levers)
    code_dir = levers["code_dir"]
    base = state["shipped_baseline"]
    head = git(repo, "rev-parse", "HEAD").strip()

    files = file_diffs(repo, base, code_dir)
    hashes = {f: hashlib.sha1("\n".join(l).encode()).hexdigest() for f, l in files.items()}
    new_since_last = sorted(f for f, h in hashes.items() if state["file_hashes"].get(f) != h)
    reverted_since_last = sorted(f for f in state["file_hashes"] if f not in hashes)

    cfg_path = code_dir + "/config.py"
    base_src = git(repo, "show", "%s:%s" % (base, cfg_path), check=False) or None
    cur_file = os.path.join(repo, cfg_path)
    cur_src = open(cur_file, encoding="utf-8").read() if os.path.exists(cur_file) else None
    c_base, c_now = constants(base_src), constants(cur_src)
    const_changes = [{"name": k, "was": c_base.get(k), "now": c_now.get(k)}
                     for k in sorted(set(c_base) | set(c_now)) if c_base.get(k) != c_now.get(k)]

    def rx(p):
        pre = r"(?<![A-Za-z0-9_])" if re.match(r"[A-Za-z0-9_]", p) else ""
        post = r"(?![A-Za-z0-9_])" if re.search(r"[A-Za-z0-9_]$", p) else ""
        return re.compile(pre + re.escape(p) + post)
    compiled = [(lv, [rx(p) for p in lv["patterns"]]) for lv in levers["levers"]]

    hits = {}
    for f, lines in files.items():
        func = ""  # the def/class a changed line sits in, from hunk headers and context
        for line in lines:
            if line.startswith("@@"):
                m = re.match(r"(def|class) (\w+)", line.split("@@")[-1].strip())
                func = "%s %s" % (m.group(1), m.group(2)) if m else ""
                continue
            m = re.match(r"^[ +-](def|class) (\w+)", line)
            if m:
                func = "%s %s" % (m.group(1), m.group(2))
            if not line or line[0] not in "+-" or line.startswith(("+++", "---")):
                continue
            text = line + "  [in " + func + "]" if func else line
            for lv, pats in compiled:
                if any(p.search(text) for p in pats):
                    hits.setdefault(lv["id"], []).append({"file": f, "line": text[:220]})
    lever_hits = [{"id": lv["id"], "name": lv["name"], "outcomes": lv["outcomes"], "why": lv["why"],
                   "lines": hits[lv["id"]][:15], "count": len(hits[lv["id"]])}
                  for lv in levers["levers"] if lv["id"] in hits]

    agreed = []
    for spec in levers["agreed_constants"]:
        n = spec["name"]
        v = c_now.get(n)
        if v is None:
            status = spec.get("if_missing", "warn")
            detail = "not in config.py"
        elif "range" in spec:
            lo, hi = spec["range"]
            ok = isinstance(v, (int, float)) and lo <= v <= hi
            status = "pass" if ok else spec["if_different"]
            detail = "%s (agreed %s to %s)" % (v, lo, hi)
        else:
            ok = v == spec["expect"]
            status = "pass" if ok else spec["if_different"]
            detail = "%s (agreed %s)" % (v, spec["expect"])
        prev = state["constant_status"].get(n)
        agreed.append({"name": n, "status": status, "detail": detail, "why": spec["why"],
                       "regressed": prev == "pass" and status != "pass"})

    cl_path = os.path.join(repo, code_dir, "CHANGELOG.md")
    cl = open(cl_path, encoding="utf-8").read() if os.path.exists(cl_path) else ""

    facts = {
        "run_date": dt.date.today().isoformat(),
        "repo_head": head, "shipped_baseline": base, "last_shipped": state["last_shipped"],
        "baseline_set_on": state["baseline_set_on"], "last_run": state["last_run"],
        "changed_files": sorted(files), "new_since_last_run": new_since_last,
        "reverted_since_last_run": reverted_since_last,
        "uncommitted": bool(git(repo, "status", "--porcelain", "--", code_dir).strip()),
        "constant_changes": const_changes, "lever_hits": lever_hits,
        "agreed_constants": agreed,
        "changelog_upcoming": upcoming_changelog(cl, state["last_shipped"]),
        "diff": {f: "\n".join(l[:400]) for f, l in files.items()},
        "file_hashes": hashes,
    }
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(facts, open(a.out, "w", encoding="utf-8"), indent=2, default=str)
    print("RESULT=scanned")
    print("FACTS=" + a.out)
    print("BASELINE=%s (%s shipped, set %s)" % (base[:8], state["last_shipped"], state["baseline_set_on"]))
    print("CHANGED_FILES=%d" % len(files))
    print("NEW_SINCE_LAST_RUN=%s" % (",".join(new_since_last) or "none"))
    print("CONSTANT_CHANGES=%s" % (",".join("%s:%s->%s" % (c["name"], c["was"], c["now"]) for c in const_changes) or "none"))
    print("LEVERS_TOUCHED=%s" % (",".join(h["id"] for h in lever_hits) or "none"))
    print("AGREED=%s" % ",".join("%s:%s%s" % (x["name"], x["status"], "(REGRESSED)" if x["regressed"] else "") for x in agreed))
    print("CHANGELOG_UPCOMING=%s" % (" | ".join(s["heading"] for s in facts["changelog_upcoming"]) or "none"))


def cmd_record(a):
    levers = json.load(open(a.levers, encoding="utf-8"))
    repo = git(a.repo, "rev-parse", "--show-toplevel").strip()
    path, state = load_state(repo, levers)
    facts = json.load(open(a.facts, encoding="utf-8"))
    state["last_run"] = facts["run_date"]
    state["file_hashes"] = facts["file_hashes"]
    state["constant_status"] = {x["name"]: x["status"] for x in facts["agreed_constants"]}
    json.dump(state, open(path, "w", encoding="utf-8"), indent=2)
    print("RESULT=recorded")


def cmd_ship(a):
    levers = json.load(open(a.levers, encoding="utf-8"))
    repo = git(a.repo, "rev-parse", "--show-toplevel").strip()
    path, state = load_state(repo, levers)
    if git(repo, "status", "--porcelain", "--", levers["code_dir"]).strip():
        print("RESULT=refused")
        print("REASON=routing code has uncommitted changes; commit what shipped first")
        return
    state["shipped_baseline"] = git(repo, "rev-parse", "HEAD").strip()
    state["last_shipped"] = a.label
    state["baseline_set_on"] = dt.date.today().isoformat()
    state["file_hashes"] = {}
    json.dump(state, open(path, "w", encoding="utf-8"), indent=2)
    print("RESULT=shipped")
    print("BASELINE=%s (%s)" % (state["shipped_baseline"][:8], a.label))


def esc(s):
    return html.escape(str(s if s is not None else ""))


LABEL = {"block": "Block", "warn": "Warn", "pass": "Pass", "info": "Info", "not_yet": "Not in code yet"}
OUT_NAMES = {"answered": "Pings answered", "taken": "Pings taken", "filled": "Callouts filled",
             "share": "Quiet four's share"}


def cmd_page(a):
    F = json.load(open(a.findings, encoding="utf-8"))
    v = F.get("verdict", "info")
    parts = []
    parts.append('<header><h1>Release QA</h1><p class="sub">%s · %s · as of %s</p></header>' % (
        esc(F.get("release_name", "Upcoming release")), esc(F.get("scope_line", "")), esc(F.get("as_of", ""))))
    parts.append('<section class="hero %s"><span class="pill %s">%s</span><p>%s</p></section>' % (
        v, v, esc(LABEL.get(v, v)), esc(F.get("summary", ""))))

    imp = F.get("impact", [])
    if imp:
        cards = "".join(
            '<div class="card"><div class="lbl">%s</div><div class="dir %s">%s</div>'
            '<div class="size">%s</div><p>%s</p></div>' % (
                esc(OUT_NAMES.get(i.get("outcome"), i.get("outcome"))), esc(i.get("direction", "none")),
                {"up": "&#9650; Up", "down": "&#9660; Down", "none": "&#8212; No effect", "unclear": "? Unclear"}.get(i.get("direction"), "?"),
                esc(i.get("size", "")), esc(i.get("basis", "")))
            for i in imp)
        parts.append('<h2>Projected impact on the four outcomes</h2><p class="note">Estimates from the brief\'s model and the 4.2 analysis, not measurements.</p><div class="cards">%s</div>' % cards)

    for sec in F.get("sections", []):
        rows = "".join(
            '<tr><td><span class="pill %s">%s</span></td><td><b>%s</b>%s</td><td>%s</td><td class="oc">%s</td></tr>' % (
                esc(c.get("status")), esc(LABEL.get(c.get("status"), c.get("status"))), esc(c.get("name")),
                ' <span class="new">new this week</span>' if c.get("new") else "",
                esc(c.get("detail")), esc(", ".join(OUT_NAMES.get(o, o) for o in c.get("outcomes", []))))
            for c in sec.get("checks", []))
        parts.append('<h2>%s</h2><div class="tw"><table><tr><th>Result</th><th>Check</th><th>What we found</th><th>Outcomes</th></tr>%s</table></div>' % (
            esc(sec.get("title")), rows or '<tr><td colspan="4" class="note">Nothing to check.</td></tr>'))

    acts = F.get("actions", [])
    if acts:
        parts.append("<h2>Before this ships</h2><ul class=\"acts\">%s</ul>" % "".join(
            "<li><b>%s</b>: %s</li>" % (esc(x.get("who")), esc(x.get("what"))) for x in acts))
    files = F.get("changed_files", [])
    parts.append('<h2>What was compared</h2><p class="note">%s</p>' % esc(F.get("compared", "")))
    if files:
        parts.append('<p class="note">Changed files: %s</p>' % esc(", ".join(files)))

    page = TEMPLATE.replace("__BODY__", "\n".join(parts))
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    open(a.out, "w", encoding="utf-8").write(page)
    print("RESULT=built")
    print("OUT=" + a.out)


TEMPLATE = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Release QA</title>
<style>
:root{color-scheme:light;--bg:#fafaf8;--card:#fff;--ink:#1d1d1b;--muted:#6b6b66;--line:#e4e3de;
--pass:#1f7a4d;--pass-bg:#e3f3ea;--warn:#9a6200;--warn-bg:#fbf0d9;--block:#b3261e;--block-bg:#fbe4e2;
--info:#2f5fb3;--info-bg:#e6edf9;--na:#5b5b57;--na-bg:#efefec}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);
font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
main{max-width:1000px;margin:0 auto;padding:24px 16px 48px}
h1{font-size:24px;margin:0}h2{font-size:17px;margin:28px 0 10px}.sub,.note{color:var(--muted)}
.note{font-size:13px}.sub{margin:2px 0 16px}
.hero{background:var(--card);border:1px solid var(--line);border-left-width:6px;border-radius:10px;padding:14px 16px}
.hero p{margin:8px 0 0}.hero.block{border-left-color:var(--block)}.hero.warn{border-left-color:var(--warn)}
.hero.pass{border-left-color:var(--pass)}.hero.info{border-left-color:var(--info)}
.pill{display:inline-block;font-size:12px;font-weight:600;padding:2px 8px;border-radius:99px;white-space:nowrap}
.pass{color:var(--pass);background:var(--pass-bg)}.warn{color:var(--warn);background:var(--warn-bg)}
.block{color:var(--block);background:var(--block-bg)}.info{color:var(--info);background:var(--info-bg)}
.not_yet{color:var(--na);background:var(--na-bg)}
.hero.pass,.hero.warn,.hero.block,.hero.info{background:var(--card);color:var(--ink)}
.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}
.card .lbl{font-size:13px;color:var(--muted)}.card .dir{font-size:20px;font-weight:650;margin:2px 0}
.dir.up{color:var(--pass)}.dir.down{color:var(--block)}.dir.none,.dir.unclear{color:var(--na)}
.card .size{font-weight:600;font-size:13px}.card p{font-size:13px;margin:6px 0 0;color:var(--muted)}
.tw{overflow-x:auto;background:var(--card);border:1px solid var(--line);border-radius:10px}
table{border-collapse:collapse;width:100%;font-size:14px}th,td{padding:8px 10px;text-align:left;vertical-align:top;
border-bottom:1px solid var(--line)}th{color:var(--muted);font-weight:600;font-size:13px}td.oc{font-size:13px;color:var(--muted)}
tr:last-child td{border-bottom:none}.new{font-size:11px;color:var(--info);font-weight:600;margin-left:4px}
.acts li{margin:6px 0}
</style></head><body><main>
__BODY__
</main></body></html>
"""


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan"); s.add_argument("--repo", default="."); s.add_argument("--levers", required=True); s.add_argument("--out", required=True)
    s = sub.add_parser("record"); s.add_argument("--repo", default="."); s.add_argument("--levers", required=True); s.add_argument("--facts", required=True)
    s = sub.add_parser("ship"); s.add_argument("--repo", default="."); s.add_argument("--levers", required=True); s.add_argument("--label", required=True)
    s = sub.add_parser("page"); s.add_argument("--findings", required=True); s.add_argument("--out", required=True)
    a = p.parse_args()
    {"scan": cmd_scan, "record": cmd_record, "ship": cmd_ship, "page": cmd_page}[a.cmd](a)


if __name__ == "__main__":
    main()

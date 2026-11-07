---
name: release-qa
description: Weekly pre-release QA for Rook Dispatch routing. Checks whether the upcoming release (routing code changed since the last shipped release, plus the CHANGELOG's upcoming section) could move the four outcomes the approved brief targets — pings answered, pings taken, callouts filled and the quiet four's share of pings — whether it keeps the agreed fixes intact, and whether it follows the release plan. Use it when the PM says "release QA", "run the release check", "QA the upcoming release", "will the next release affect our outcomes", or when the Monday scheduled run starts. Also use "mark <version> as shipped" to move the baseline after a release goes out.
---

# Release QA

A Monday check, before anything ships, that the next Dispatch release won't
undo or upset the outcomes in `05-super-speed/brief.md`. Helen has approved
the brief; none of it has shipped yet. The PM's request (or the scheduled
run) is the go-ahead: start with one plain line such as "Running this
week's release QA."

Files in this skill's folder:

- `levers.json`: the routing settings and code that move each outcome, and
  the agreed values from the brief.
- `references/impact-guide.md`: targets, the seven changes, which release
  each belongs to, and the numbers to size an effect with. Read it every run.
- `scripts/qa.py`: `scan` gathers the facts, `page` builds the report,
  `record` remembers this run, `ship` moves the baseline.

State lives in `qa/state.json`. "The upcoming release" is everything in
`00-rook/code/dispatch-routing/` that differs from the code as it was when
the last release shipped (committed or not), plus CHANGELOG sections above
the last shipped version. On the very first run the baseline is today's
code, which is 4.2 as shipped.

## 1. Gather the facts

```bash
python3 -I .claude/skills/release-qa/scripts/qa.py scan --repo . \
  --levers .claude/skills/release-qa/levers.json --out qa/runs/<today>-facts.json
```

Read the printed lines, then the facts file: the diff of every changed file,
constants before and now, which levers the diff touches, the agreed-value
checks, and the upcoming CHANGELOG text. Read the changed files in full too.
The pattern match only points; you decide.

If `CHANGED_FILES=0` and there's no upcoming CHANGELOG section, the result
is **Info: nothing queued for release**. Still show the agreed-value table,
build the page, and keep the message to two lines.

## 2. Judge it

Use four sections, in this order. Each check has a status: `block`, `warn`,
`pass`, `info` or `not_yet`. Mark checks for files in `NEW_SINCE_LAST_RUN`
with `"new": true`.

**A. Outcome levers touched.** One check per lever in `LEVERS_TOUCHED`. Say
in plain words what changed and which outcomes it can move. Use `warn` when
a lever moves and no agreed change explains it, and `pass` when it's an
agreed change done as specified. Use `block` for a change to the ping wait,
or anything that makes a miss cost more, recovery slower, or the list
shorter.

**B. Agreed fixes intact.** Start from `agreed_constants` as given. A
`(REGRESSED)` flag means a value that passed last week no longer does: make
it `block`. Then read the code for the changes no constant can show, using
`not_yet` until it appears:

- 3b: turning down an out-of-area ping costs nothing (and a miss still
  costs the miss penalty).
- 4: a one-time restore to 11 Aug scores. It must run once, not on every
  start, and needs a source for the 11 Aug values (open question for Wen).
- 5: recovery drifts up to 0.5 over about 4 weeks, only while available,
  never lifts anyone above 0.5, and doesn't lower anyone above 0.5.
- 6: one retry only, for a missed first ping on a local callout, after the
  next responder (unless Wen has decided otherwise, which the CHANGELOG
  should say).
- 2 and 1: alert and visibility work mostly lives outside this folder. Say
  "not visible in routing code" rather than pass it.
- Misses and turn-downs are still recorded separately (`offer.py`).

**C. Projected impact.** One card per outcome: direction (`up`, `down`,
`none`, `unclear`), a rough size against the brief's targets, and the basis
in one line, from `references/impact-guide.md`. Count only changes actually
in the code or CHANGELOG. When nothing touches an outcome, say "No effect".

**D. Release-plan rules.**
- Changes 1, 2, 7 (Release A) and 3–6 (Release B) aren't in the same
  release. Both in one release is `block`.
- A change to `current_record` or what the availability record returns:
  `warn`, with the action "tell Supply before it ships".
- Any change to `config.py`: `info`, with the action "Marcus to be told"
  (the file's own rule).
- Every code change has a CHANGELOG line, and every upcoming CHANGELOG line
  has code (or is marked as outside this service). A mismatch is `warn`.
- If Release A is in this release: answer-time logging should be in
  `offer_to` (brief: start logging now). Missing is `warn`. Also add the
  Security Policy 4.1 review of the new cards and tickets as an action.

Overall verdict: `block` if any check blocks, else `warn` if any warns,
else `pass`, or `info` if nothing is queued.

## 3. Build the page

Write `qa/runs/<today>-findings.json`:

```json
{"release_name": "<from CHANGELOG heading, or 'Upcoming release'>",
 "scope_line": "<n> files changed since <last_shipped>",
 "as_of": "<today>", "verdict": "block|warn|pass|info",
 "summary": "<two plain sentences: the verdict and the one thing that matters most>",
 "impact": [{"outcome": "answered|taken|filled|share", "direction": "up|down|none|unclear",
             "size": "e.g. towards 91.5%", "basis": "one line"}],
 "sections": [{"title": "Outcome levers touched", "checks": [
   {"status": "warn", "name": "...", "detail": "...", "outcomes": ["share"], "new": true}]}],
 "actions": [{"who": "Wen", "what": "..."}],
 "compared": "Routing code at <baseline short hash> (<last_shipped> as shipped) against the working copy today.",
 "changed_files": ["..."]}
```

Then:

```bash
python3 -I .claude/skills/release-qa/scripts/qa.py page \
  --findings qa/runs/<today>-findings.json --out qa/<today>-release-qa.html
python3 -I .claude/skills/release-qa/scripts/qa.py record --repo . \
  --levers .claude/skills/release-qa/levers.json --facts qa/runs/<today>-facts.json
```

The page is light mode only (the PM's preference) and needs no internet.
Open it in the PM's own browser with `open qa/<today>-release-qa.html`, not
the app's file preview. In a scheduled run, skip `open` and give the path.

## 4. Tell the PM

Short and plain:

1. The verdict and the summary.
2. Every `block`, one line each, with who needs to act (Wen for routing and
   scores, Marcus for config and engineering, Sofia for the alert and apps,
   Nadia for tickets, Supply for the availability record).
3. The four impact cards in one line each.
4. What's new since last week's run.
5. The page's path.

Say what the code shows. Don't guess at intent, and don't suggest fixes
beyond naming the agreed value or the owner.

## After a release ships

When the PM says a release has shipped ("mark 4.3 as shipped"), commit
first if the routing code has uncommitted changes (ask before committing),
then:

```bash
python3 -I .claude/skills/release-qa/scripts/qa.py ship --repo . \
  --levers .claude/skills/release-qa/levers.json --label <version>
```

The next run compares against that release.

## Rules

- Read and write only inside the course folder. Never change routing code;
  this skill only reads it.
- Never overwrite an earlier week's page or findings.
- Never show or infer responder cover identities (Security Policy 4.1).
- Handler- and responder-facing wording says "a routing change in August";
  this report is internal, so "4.2" is fine.

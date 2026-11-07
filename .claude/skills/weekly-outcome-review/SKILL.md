---
name: weekly-outcome-review
description: Weekly check on whether the Rook Dispatch fixes that followed 4.2 reached their targets — pings answered, pings taken, callouts filled and the quiet four's share of pings — against the brief's projections and the before-4.2 baseline. Use it when the PM says "weekly review", "run the weekly outcome review", "how are the 4.2 fixes doing", "are we on track", or "check the outcomes this week". Builds a dated HTML report with charts in weekly-reviews/.
---

# Weekly outcome review

Checks, once a week, whether the fixes in `05-super-speed/brief.md` brought
Dispatch back to where it was before 4.2. The PM's request is their yes:
start with one plain sentence such as "Running this week's outcome review."

Everything this skill needs is in its folder:

- `config.json` — ship dates, targets and ranges. The targets come from the
  brief; don't change them unless the PM asks.
- `queries/weekly.sql` — the one query that pulls every number.
- `scripts/build_report.py` — turns the query rows into the HTML report.

## 1. Check the ship dates

Read `config.json`. The fixes ship in two releases:

- **Release A** (changes 1, 2, 7): visibility, the harder-to-miss alert,
  tickets per ping. Pings answered and pings taken are judged from here.
- **Release B** (changes 3–6): miss penalty, score restore, slow recovery,
  one retry. Callouts filled and the quiet four's share are judged from here.

If either `ship_date` is `null`, ask the PM once for both dates
(YYYY-MM-DD), write them into
`config.json`, and carry on. If they say a release hasn't shipped, leave it
`null`; the report then marks those measures "Not shipped yet".

## 2. Pull the numbers

Read `queries/weekly.sql` and send it unchanged, as one call, to the
rook-database tool `run_query`. If it says it's busy or "Something went
wrong" about connections, wait 30 seconds and retry, up to 3 times. If the
rook-database tools aren't in the session at all, stop and tell the PM to
start a new session in this folder.

Save the reply's rows (one JSON object per line is fine, as returned) to
`weekly-reviews/data/<today>.json`. Don't edit the numbers.

## 3. Build the report

```bash
python3 -I .claude/skills/weekly-outcome-review/scripts/build_report.py \
  weekly-reviews/data/<today>.json \
  .claude/skills/weekly-outcome-review/config.json \
  weekly-reviews/<today>.html <today>
```

It prints `RESULT=built`, the last week in the data, how many weeks fall
after each release, and one line per measure:
`VERDICT|text|latest|pooled|baseline|target`. Open the page in the PM's own
web browser with `open weekly-reviews/<today>.html`. Don't send it as a file
card or open it in the app's file preview: that preview doesn't run the
page's scripts and shows a blank page. The charts need internet to load
Chart.js; without it the page says so and still shows the verdicts and table.

## 4. Sanity checks before reporting

Run these and say so in one line each if any fails; don't hide it:

- **Baseline still matches the brief.** The before-4.2 numbers should read
  answered 97.7%, taken ≈77%, filled 94.9%, quiet four 28%. If they don't,
  the data has been restated; flag it.
- **Fresh data.** If `LAST_WEEK` is the same as last week's report (look at
  the newest earlier file in `weekly-reviews/data/`), say the database has no
  new week yet.
- **Partial week.** The newest week may be partial; the report shows it but
  doesn't judge it.

## 5. Tell the PM

Short and plain, in this order:

1. One line per measure: the verdict, the pooled rate for the last 3 judged
   weeks (or the latest full week if it's too early), the target and the
   before-4.2 level. Use the report's words: *Reached*, *Within range, below
   target*, *Not reached*, *Too early*, *Not shipped yet*.
2. One line on ping tickets ("no pings" and "gone before I could answer")
   this week against last week. Tickets lag pings by 2–3 days.
3. What changed since last week's report, if there is one.
4. The link to the report.

Report what the numbers show. Don't offer a theory of why a measure moved
unless the PM asks. If a measure is *Not reached* or two weeks in a row are
Off track, say which owner from the brief's open questions it points to
(Wen for routing and scores, Sofia for the alert, Nadia for tickets) and
stop there.

## Rules

- Read and write only inside this course folder. Reports go in
  `weekly-reviews/`; never overwrite an earlier week's file.
- Reports are light mode only, even when the computer is set to dark mode.
  The PM prefers light visuals; don't add a dark theme back.
- Responder and handler names are fine in the report; never anything about
  cover identities (Security Policy 4.1).
- Handler- and responder-facing wording says "a routing change in August",
  not "4.2". This report is internal, so "4.2" is fine here.
- When Release A's per-ping ticket categories exist, the ticket grouping in
  `weekly.sql` should switch to them. Tell the PM when that happens; don't
  change the query on your own.

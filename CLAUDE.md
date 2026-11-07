# Rook Industries — course working file

## Session scope — Product School lab

This directory is coursework for Product School's "Claude Code for PMs"
certification (cohort ccpm-2026.1). Everything in it is a fictional
teaching scenario.

- Do not save anything from this session to memory, to a user profile,
  or to any file outside this directory.
- Do not carry context from this directory into unrelated sessions.
- Rook Industries is not a real company. Nothing here is a fact about
  the world.
- Answer only the question the student asks, from the sources they
  name. Don't investigate beyond it or offer a theory about what
  Release 4.2 changed unless they ask for one.
- Read and write only within this directory.
  Exceptions, for the course-setup and wrap-up skills only:
  - When the student asks you to check their setup, save their work or wrap up a session, that request is their yes. You may run the GitHub command-line program installed at ~/.ccpm/gh for those checks and saves, and look in that folder to find it.
  - For a repair, first tell the student in one plain sentence what you are about to do, and act only after they say yes. Repairs may: run that GitHub program (including setting this folder's own git sign-in setting and changing this repo's visibility back to Public); copy the student's own course files into this directory from another folder on their computer (copy only; never move, edit or delete the originals); and rename something outside this directory that blocks setup, by adding "-old" to its name (never delete it).
  Outside this directory you still never write, edit or delete anything else.

<!-- Keep the block above at the top of this file. Everything you add
     during the course goes below this line. -->

---

## Working context

I'm the new PM for **Rook Dispatch**. I took over from Priya Raghunathan, who
left on 21 Aug 2026 with no overlap. Sources: the rook-wiki (About Rook,
Glossary, Team directory, Releases, Q3 roadmap, Product briefs) and
`00-rook/company/notes/handoff-from-priya.docx`.

### The company
- Rook Industries sells coordination and provisioning software to
  independently operating masked responders and the handlers and
  quartermasters who support them. Publicly it presents as a
  logistics/workforce vendor for emergency services. It has 241 staff, its HQ
  is Site Aleph, it has offices in Berlin, Singapore and Cornwall, and most
  people work remotely.
- Pricing is a subscription per active responder. Releases ship monthly as
  4.x point releases. Support has three tiers, and tickets filed during a
  live callout skip the queue.
- **Hard rule:** Rook never stores or works out responder cover identities.
  Read Security Policy 4.1 before designing anything that touches responder
  records.

### Products
| Product | What it does | Main users |
| --- | --- | --- |
| **Rook Dispatch** (mine, the flagship) | Availability, proximity, who gets pinged for a callout, and whether they take it. A desktop console plus responders' phones. | Handlers, responders |
| **Rook Supply** | Requisitions, maintenance, field failure reports | Handlers, quartermasters |

The two products share the **Responder Availability Record**. Dispatch writes
it and Supply reads it for maintenance scheduling.

### Vocabulary (Rook-specific meanings)
- **Responder**: not an employee. In our systems a responder is only capability tags plus availability. **Handler**: looks after one or a few responders and is usually the person using the product. **Quartermaster**: owns gear stock and approvals (Supply).
- **Callout**: a request to attend an incident, and the unit of work. **Ping**: one callout offered to one responder's phone. The outcome is **Taken**, **Turned down**, or **Missed** (the ping wait ran out). Turned down and Missed are recorded separately, but both send the ping on to the next responder.
- **Ping wait**: one global value, set per release. It was 90s and is 60s since 4.2.
- **Routing priority**: the score that ranks responders. Its inputs are proximity (a travel-time estimate), availability, capability match and recent acceptance history. Turning a ping down or missing it lowers a responder's future rank. There is **no written description** of how this works. Wen Li built it, and Priya asked me to write the description.
- **Acceptance rate**: the share of pings that are taken. It is the headline metric. **Time-to-accept**: the median number of seconds to take a ping. **Coverage gap**: no available responder had the required tags (nobody *could* go). It is tracked separately from acceptance.
- **Capability tags**: flight, structural-entry, hazmat-tolerant, cold-weather, aquatic, crowd-management, de-escalation.
- **Mutual aid**: responders covering for each other across areas. Not supported yet and on the Q4 exploration list.
- **Supply terms:** requisition, field failure report, service interval.

### People (Dispatch team, wiki role → person)
4.2 comments are signed by role. Here is who each role is:
| Role in comments | Person | Location | Notes |
| --- | --- | --- | --- |
| Director of Product | **Helen Achebe** | Site Aleph | My director. Owns the roadmap and commitments. |
| Engineering manager | **Marcus Oyelaran** | Site Aleph | Runs Dispatch engineering. Priya's advice: start with him when unsure. Has Priya's number. |
| Staff engineer | **Wen Li** | Berlin | Built the routing/ping logic. Away 14–24 Aug. Wants direct messages. |
| Product designer | **Sofia Marino** | Site Aleph | Owns the console and phone app UX. Ran the September interviews. |
| Support lead | **Nadia Hoffmann** | Berlin | Owns tickets and hears handler complaints first. Priya suggested a standing 15 minutes. |
| Data analyst | **Ravi Menon** | Singapore | Owns the official weekly acceptance numbers. Did not appear in the 4.2 thread. |
| Former PM | Priya Raghunathan | — | Left 21 Aug. Every roadmap item still lists her as owner. |

Customer names that appear in the briefs and research: handlers Halloran (Sgt. Bulwark, a frequent Supply requester), Aunt Dot (Vesper), Mr. Ambrose (Captain Vantage) and Kip (Meteor Mite, The Gale).

### Releases
- **4.0** (7 Apr): new console navigation, responder profile redesign, routing override audit log.
- **4.1** (16 Jun): proximity switched to a travel-time estimate, bulk callout, more reliable push delivery.
- **4.2** (12 Aug): proximity weighted up relative to recent acceptance history, ping wait cut from 90s to 60s, console filters now persist, three defect fixes.

### Where things stand on 4.2 (facts from the thread and the handoff)
- It shipped clean. Since 18 Aug, callout tickets have run at about 3× normal and have levelled off but not dropped. Nadia's split is about ⅔ "my phone never goes off" and ⅓ "it was gone before I could answer". She can explain the second (the shorter ping wait) but not the first. A handler emailed her directly, which never happens.
- Marcus's question from 14 Aug is **still unanswered**: was the routing change meant to apply to responders who've been turning jobs down, or did it "just fall out that way"? He says the config doesn't distinguish them.
- Priya thinks it is mostly the usual August softness. She advised against reverting because the change was a long-standing ask from wide-area responders. Nadia asked for real acceptance trend data, and so far only Marcus has offered "rough" numbers.
- Marcus planned to regroup on 4.2 with the new PM after their first week. Nadia has a ticket breakdown ready.
- Priya also flagged that the filter-persistence tickets are cosmetic noise.

### Roadmap (Q3, last reviewed 30 Jun, so stale)
| Item | Target | Status | Note |
| --- | --- | --- | --- |
| Change to who gets pinged | 4.2 | Committed | Shipped in 4.2 |
| Ping timeout tuning | 4.2 | Committed | Shipped in 4.2 (90s→60s) |
| Availability Confidence (a confidence score on stated availability) | 4.2 | Committed | **Not in the 4.2 release notes** |
| Requisition approval chains (Supply) | 4.3 | Committed | The brief's scope has grown well beyond "a second approval over $2,000" |
| Handler phone app | Q4 | Exploring | Sofia exploring, not staffed. Brief dated 8 Sep. |
| Shared cover between responders | Q4 | Exploring | Probably the same thing as "mutual aid" |

Items listed against a numbered release are locked, and changes go through Product. Priya asked me to confirm with Helen which items were squeezed out of 4.2 and are still Q3 commitments. That conversation hasn't happened yet.

### My open to-dos from the handoff
1. Talk to Helen about which of the deferred 4.2 items are still commitments.
2. Write down how routing priority / "who gets pinged" works (with Wen).
3. Get properly up to speed on 4.2 with Marcus, Nadia, Wen and Ravi.
4. Update the roadmap owners and statuses, since Priya is gone.

- Sources that mattered: `00-rook/code/dispatch-routing/` (config.py, history.py, offer.py, routing.py) and the rook-database tables pings, callouts, responders and support_tickets. The data covers only 29 Jun to 6–7 Sep 2026, so Priya's "August is seasonal" claim can't be checked.
- Acceptance was about 75–78% a week before 4.2, fell to 54% in the release week, then 66–73%. Missed pings went from 2–6 a week to 21–38. Tickets went from about 6–7 a week to 20–32.
- Four responders (Vesper, The Undertow, Farlight, Meteor Mite) went from about 12 pings a week to 2–3. The local responder got the first ping in about 80% of their area's callouts before 4.2 and 13–25% after.
- My working diagnosis, from the code: a missed ping is penalised like a refusal (−0.12 vs +0.08 for taking one), scores never recover, and the 60s wait multiplied misses. The proximity weighting up isn't the cause, but it didn't protect local responders.
- I drafted a top-3 fix list with a rollout plan: (1) miss penalty and score recovery, (2) ping wait, (3) handler visibility and score records. Fix 3 ships first; 1 and 2 are piloted in Old Town, Harborside, Uptown and Eastgate, with Hillcrest and Midtown as comparisons.
- Still open: a per-area routing switch doesn't exist yet (routing settings ship globally with each release), there's no data after 6 Sep, Security Policy 4.1 isn't in the wiki, and Supply should be told before any routing change.
- Interviews (Customer interviews database, run by Sofia, 2–5 Sep) were framed as console redesign research and never asked about pings. Even so, 3 of 4 handlers described a lost callout and 3 of 4 want to be told when a ping is live or moves on. Only Ambrose raised it unprompted.
- All 147 support tickets are grouped: 30 "no pings" and 15 "gone before I could answer" since 4.2 (exactly Nadia's ⅔ / ⅓ split), 16 about filters, 24 for Supply. Many tickets repeat earlier wording, so the counts overstate unique issues.
- The two sources barely overlap. Of the four interviewees, only Ambrose filed a ticket. The "no pings" tickets are about Farlight, The Undertow, Corporal Ashgrove and Halfmoon, while Vesper and Meteor Mite (the quietest in the data) have none. They contradict each other on maintenance scheduling.
- The priority heatmap is at `01-origin-story/priority-heatmap.html`. Work items live in the ITEMS list in the file. Weights: outcomes 40, interview 20, support 25, redesign 15. Areas rank by best item. It tops out with the miss penalty and ping wait at 90 and the handler alert at 78.
- Still open: confirm the redesign scope with Sofia, interview the handlers who filed tickets (e.g. Linda Pruitt, Desmond Okafor), and merge repeated tickets into unique issues.
- Pings grouped by change in volume (6 full weeks before 4.2 vs 3 full weeks after, release week excluded; ±3 pings a week): pinged more (6: The Gale, Nightwell, Stormwrack, Captain Vantage, Sgt. Falkirk, Ironvale) went from 41% to 61% of pings; about the same (6: Cindermark, Sgt. Bulwark, The Longcast, The Drift, Halfmoon, Corporal Ashgrove) from 30% to 34%; pinged less (the 4 quiet responders) from 28% to 5%. All three took about 76–77% before. After, the pinged-less group took 12% and missed 64%, on only 25 pings.
- On the same windows: pings answered fell from 97.7% to 84.9%, turned-down share fell from 20.9% to 16.5%, callouts nobody took rose from 5.1% to 10.8% (5.5% in the last week), and callouts with at least one ping fell from 139.5 to 124 a week. The gap after a missed ping went from about 92s to 62s, starting 12 Aug.
- "Premature callout termination" is not in the code. `dispatch` (offer.py) only stops at a yes or the end of the list, with no cap or timeout. The list is available responders in the callout's region, and running out returns None with no retry, wider region or alert in this code. Likely cause of unfilled callouts is short lists, unconfirmed because `available_for` is a stub.
- The 4.2 weight change alone doesn't explain the shift: it halved a failed ping's effect (worth about 2.25 minutes of travel time, was 4.8). A responder's score falls if they take under 60% of pings. So misses are the likely driver, unproven because no score history is recorded. `_scores` is held in memory, so ask Wen how it's stored in production and whether a restart resets everyone to 0.5.
- Still open: the support_tickets vs pings comparison hasn't been run, because rook-database dropped out of the session and didn't come back. Prior notes suggest pings moved on 12 Aug and tickets around 18 Aug, but that lag is unmeasured. Also check the callouts table for final status and list lengths.
- The support_tickets vs pings comparison has now been run and replaces the note above. The two agree on what happened, not on when it was worst: acceptance was lowest in the release week and reached 72.7% by the week of 31 Aug, while tickets peaked at 32 in the week of 24 Aug and were still 25 the week after.
- Three dated moves: missed pings jumped on 12 Aug (4 across 1–11 Aug, 37 across 12–16 Aug); tickets rose on 13–14 Aug from about 1 a day to 3–5, five days before the "since 18 Aug" in the thread; the four quiet responders held normal volume through 14 Aug, then fell from 15 Aug (about 49 pings a week to 20, then 3), and "no pings" tickets started 17 Aug.
- Agreed customer-outcome summary: (1) ping volume shifted between responders; support confirms the timing with a 2–3 day lag but under-reports who is affected, because Vesper and Meteor Mite have no tickets while Ashgrove and Halfmoon lost only about 20% and have five each. (2) Missed pings went up; all 15 "gone" tickets match a missed ping within 48 hours and they rise and fall together, with about a day's lag. "No pings" tickets belong with (1), not (2).
- Unfulfilled callouts are set aside as an internal concern, not a key customer outcome. No ticket subject line mentions one.
- The ticket groups above come from matching subject lines. Halfmoon's ping-count claims weren't checked ping by ping. Tickets outside these groups also about doubled (about 6 a week to 9–15), and filter tickets add to the 13–14 Aug rise.
- Vesper week by week (Old Town, handler Aunt Dot): 13–15 pings a week through the week of 3 Aug, then 12, 5, 2, 1. They took 68 of 83 (82%) and missed 3 in the six weeks before the release week, then took 7 of 20 and missed 9 from the release week on. They took nothing in the last two weeks.
- Vesper was picked only from the four known quiet responders; all responders were not searched. Farlight is the starker case: no pings at all in the week of 31 Aug, and nothing taken after the week of 10 Aug. The Undertow also ended on one missed ping a week.
- Still open: the chart of one responder per customer outcome, each showing weekly pings and outcomes, isn't built because rook-database dropped out again and there's no local copy of the data. Farlight is a provisional pick for "pinged less" (they have "no pings" tickets), but that needs checking against weekly ticket dates. Still needed: a responder who gained pings, and a named responder for missed pings.
- The one-responder-per-outcome chart is now built and replaces the "still open" note above: Farlight (Linda Pruitt, Uptown) for pinged less, 12 pings a week down to 10, 3, 1, 0; Ironvale (Teresa Alvarez, Riverside) for missed pings, 1 missed of 48 in the six weeks before the 4.2 week, then 7 of 42. It only exists in the session, not as a file.
- Tickets match pings exactly for these picks: all 11 of Farlight's "quiet" tickets (and all 11 of The Undertow's, a near-tie) and both of Ironvale's "lost it" tickets. Ironvale also shows the receiving side, rising from about 8 to 12 pings a week.
- Both charts now use one y-axis: pings as a percentage of the responder's own average week over the six full weeks before the 4.2 week (Farlight 12, Ironvale 8; Ironvale reaches 150%).
- Responder scores are reconstructed from the history.py rules, not stored, so most weeks are ranges. Farlight's score reaches exactly 0 by the week of 24 Aug whatever it started at, using their exact ping order from 10 Aug; Ironvale ends between 0.64 and 1.0. Routing priority itself can't be charted because it's per callout and needs travel time.
- Still open: add in-area vs out-of-area pings to the chart, proposed as in-area above the baseline and out-of-area mirrored below. It needs rook-database and confirmation that `callouts` has an area column.
- The in-area vs out-of-area split is now done and replaces the "still open" note above. `callouts` has an area column, and a ping is in-area when it matches the responder's area in `responders`. It sits in its own weekly chart for each responder, between the outcome and score charts, on the same percentage scale.
- Before vs from the 4.2 week: Farlight took 53 of 57 in-area and 0 of 15 out-of-area, then 4 of 8 and 0 of 6. Ironvale took 37 of 39 in-area and 0 of 9 out-of-area, then 19 of 25 and 9 of 17. All of Ironvale's growth was out-of-area, and they took none until the week of 17 Aug. 5 of their 7 misses were in-area.
- These are two responders only; the area split hasn't been run across everyone.
- The charts now live in `01-origin-story/priority-heatmap.html` under a "Responder charts" tab, which replaces the note that they only exist in the session. Each responder has outcome (% of normal week), paired in-area and out-of-area columns by outcome (count), and score charts. Chart data is hard-coded in the RESPONDERS list in the file, and the tab needs internet to load Chart.js.
- The paired columns show neither responder took an out-of-area ping before 4.2: Farlight never did in ten weeks, and Ironvale first did in the week of 17 Aug.
- Working summary of 4.2: the shorter ping wait is the likely root cause (not proven, because the ranking change shipped the same day). Treating misses like refusals and having no score recovery are pre-existing. The shift in ping volumes and the move to out-of-area pings are follow-on effects.
- The score has no recovery at all: only a taken ping raises it. At the 4.2 weights, a score of 0 vs 1 is worth about 19 minutes of travel time (40 before 4.2), and a responder at 0 needs seven taken pings to reach 0.5.
- Other pre-existing issue: out-of-area pings that aren't taken lower a responder's score. Farlight and Ironvale took 0 of 24 before 4.2 (20 turned down, 4 missed).
- Proposed fixes, numbers to agree with Wen: cut the miss penalty to about 0.04, no penalty for out-of-area pings not taken, scores move halfway back to 0.5 every two weeks, a one-time reset for anyone below 0.5, then test 90s separately. Keep the 4.2 weights for now. Without a per-area switch, ship the penalty and recovery changes and the wait change in separate releases.
- Still open: the re-validation against rook-database didn't run because it wasn't connected. Next: count pre-4.2 takes that came after 60 seconds, see whether misses spread across most responders, check that misses came before volume fell for all 16 responders, run the area split for everyone, and look for data after 6 Sep.
- The re-validation against rook-database has now run and replaces the "still open" note above. Scores were all 0.80 or higher on 12 Aug, so the penalty and lack of time-based recovery did little visible harm until misses jumped. The 4.2 change applied to everyone with no split by turn-down history, which answers Marcus's question, but whether that was intended is still unknown.
- Ping wait is the strongest cause but unproven: first pings to in-area responders were missed 0.7% before and 11.4% after, and misses jumped on 12 Aug. Answer times for taken pings aren't stored, turn-downs never took over 40s, and on 12–14 Aug the quiet four missed 14 of 21 against 13 of 59 for everyone else.
- New unexplained issue: out-of-area first pings jumped from 20% to 51% on 12–14 Aug, before scores fell and despite proximity being weighted up. Out-of-area pings went from 0 of 178 taken to 84 of 186, and 128 of those 186 were for callouts in the quiet four's areas. The about-the-same group's out-of-area pings doubled too, so it isn't only the gainers. Ask Wen first.
- All 1,319 callouts have at least one ping, so true coverage gaps aren't in the data. Unfilled callouts rose from 5.1% to 10.8%, entirely from callouts ending on a miss; those ending on a turn-down stayed about 7 a week. 35 of 40 unfilled after 4.2 stopped after one ping.
- Agreed direction, replacing the earlier recovery proposal: slow time-based recovery up to 0.5 over about 4 weeks, only while marked available. Unfilled callouts alert first, then retry missed pings once, then widen the search as a last resort needing a product decision. The nine-step rollout is in the "Fix plan" tab of `01-origin-story/priority-heatmap.html`, held in the FIXES list.
- The "Parameter model" tab projects rates and seconds lost from sliders. It is calibrated to before and after data, but the 60–90s curve is assumed, the quiet four's 64% miss rate rests on 25 pings, and local calls aren't projected. It suggests the ping wait does most of the work, recovery alone stalls at a score of 0.13, and quiet responders could recover without new logic if they answer as before 4.2. Check that on real answer times once they're logged.
- Module 5: Helen's request (`05-super-speed/director-request.txt`) asked for a one-pager on what we'd build, seen by a handler like Kip and by a quiet responder, plus something clickable, before any code changes. Built `brief.md` and `one-pager.html` (same content; the HTML adds projection charts) and `prototype.html` (console in a browser window, Kip's phone, Meteor Mite's phone, with numbered annotation pins and a key that can be switched off).
- The proposal keeps the 60s ping wait and makes seven changes: (1) visibility: live pings with Nudge, weekly balance, a page per responder with ranking over time, alerts, a handler availability switch, and a handler phone app brought forward from Q4; (2) a harder-to-miss alert; (3) a miss penalty of −0.04 and no penalty for out-of-area turn-downs; (4) a one-time restore of scores to 11 Aug; (5) slow recovery; (6) one retry, after the next responder; (7) support tickets per ping plus a general form.
- Central projection (alerts win back three quarters of the 60s miss increase): answered 84.9% → 91.5%, taken → 72%, filled 89.2% → 94.0%, quiet four's share 5% → 27%. Filled and share recover in every scenario, while answered and taken depend on the alerts working. Without the restore, recovery alone tops out at about 64% of a responder's usual pings.
- Kip handles Meteor Mite (Eastgate, 11 → 1 pings a week) and The Gale (13 → 21, absorbed about 8 of Meteor Mite's 10 lost pings). Handler- and responder-facing text shouldn't mention "4.2"; say "a routing change in August".
- Still open: Wen on whether the second chance comes straight back or only after the next responder; Nadia on ticket categories and routing; a Security Policy 4.1 review of the new cards and tickets; Sofia to scope the console, phone and handler-app work.
- Module 6: built two skills. `weekly-outcome-review` (after shipping) runs one query (`queries/weekly.sql`) and builds `weekly-reviews/<date>.html`. On track means at or above the brief's central projection, Watch means inside its range, and the verdict pools the last 3 full weeks after the relevant release. Answered and taken are judged after Release A (changes 1, 2, 7); filled and share after Release B (3–6). Ship dates in its `config.json` are still blank. The quiet four's 20% Watch floor is my assumption, not from the brief.
- The weekly query reproduces the brief exactly (before 4.2: 97.7% answered, 76.8% taken, 94.9% filled, 28.4% share; after: 84.9%, 89.2% filled, 5.2% share). Ticket subject-line rules give exactly 30 "no pings" and 15 "gone" tickets.
- `release-qa` (before shipping) compares `00-rook/code/dispatch-routing/` against 4.2 as shipped (baseline in `qa/state.json`), with outcome levers and agreed values in `levers.json`. It gives Block, Warn, Pass, Not in code yet or Info on levers, agreed fixes, projected impact and release-plan rules, and writes `qa/<date>-release-qa.html`. "Mark <version> as shipped" moves the baseline. The first real run found nothing queued.
- `release-qa` checks routing code only, not the console or phone UI (changes 1, 2, 7). A UI check needs the app code or a staging build from Sofia or Marcus. The Monday 8:00 schedule isn't created yet: it writes outside the course folder, so it needs the student's yes.
- Report pages are light mode only (student preference) and must open in a real browser, because the app's file preview shows them blank.
- Final report: `final-report.html` (repo root) is an 11-slide, self-contained presentation: cover, what I'd do (two releases, KPI before/now/projected), live prototype demo, what happened (12–18 Aug timeline), one slide per module with its strongest prompt (1·#1, 2·#8, 3·#1, 4·#19, 5·#4, 6·#5), then the open asks.
- The prototype is embedded base64-encoded and driven through a postMessage bridge; the 6-step demo autoplays at 4× speed. Source template is in the session scratchpad, so later edits go straight into `final-report.html` (or rebuild by re-embedding `05-super-speed/prototype.html`).
- The "if release-qa had seen 4.2" table (Block on ping wait, Warn on ranking weights, Info on config.py) applies the skill's rules by hand; it's not a recorded run.
- Confirmed from the wiki: the four interviewees were Aunt Dot (Vesper), Mr. Ambrose (Captain Vantage), Halloran (Sgt. Bulwark) and Kip (Meteor Mite, The Gale), all interviewed by the product designer 2–5 Sep.
- Checked at desktop size only, not on a phone.

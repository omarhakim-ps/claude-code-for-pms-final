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

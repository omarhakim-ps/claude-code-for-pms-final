# Bringing the quiet responders back, without a longer ping wait

One-pager for Helen Achebe · Rook Dispatch · 7 Nov 2026 · Draft for discussion, no code changed · Clickable prototype: [prototype.html](prototype.html)

Since 4.2, four responders have nearly stopped getting pings. They missed a few in the first days of the 60-second wait. The system counted each miss like a refusal, their scores dropped and never came back, and their callouts went to responders further away. Nobody was told this was happening. The plan below keeps the 60s wait. It makes a ping easier to catch inside those 60 seconds, stops one bad week from becoming permanent, and shows handlers and responders where they stand.

## What it looks like to the people it happens to

### Handler · Kip: Kip sees the imbalance before they have to file a ticket

*Today: The Gale went from 13 pings a week to 21. Meteor Mite went from 11 to 1. Kip had no way to see either change.*

- **Live pings with Nudge.** "Meteor Mite has a live ping, 42s left." Three of the four handlers we interviewed asked for this.
- **Each responder's week at a glance.** Pings against their usual week, outcomes, ranking, and an availability switch.
- **A page per responder.** Their last 10 pings (the same list the responder sees), their ranking now, and their ranking over time with an 8-week projection.
- **Alerts.** 3 missed pings in a row, under half the usual pings for 2 weeks, unfilled callouts, and availability changes made by either Kip or the responder.
- **On Kip's phone too.** All of the above away from the desk. This brings forward the Q4 handler phone app, which is exploring and not staffed.
- **Report a problem.** Any ping can become a support ticket, and there's a general form at the bottom of each app.

> **Console · Monday digest**
> Meteor Mite: 1 ping last week (usual 11). Ranking: lower than usual, recovering. The Gale: 21 pings (usual 13), covering Meteor Mite's callouts.

### Responder · Farlight: Farlight can tell a quiet week from being sidelined

*Today: 12 pings a week down to 0 by 31 Aug. Their score hit the floor and the app showed nothing.*

- **Hard to miss.** A full-screen countdown that gets more urgent in the last 20 seconds, and one-tap *Take*. The wait stays 60s.
- **Second chance.** A missed ping on a local callout goes to the next responder, and comes back once if they don't take it.
- **"Your pings".** Their last 10 pings, and their standing in plain words (*normal*, *slightly lower*, *lower, recovering*) with an estimate such as *back to normal in about 5 weeks*.
- **Fair rules, spelled out.** A miss costs a third of a turn-down. Turning down a ping outside their area costs nothing. A low ranking drifts back over about 4 weeks while they're available, and doesn't drop while they're unavailable.
- **Report a problem.** The same as for Kip.

> **Phone · after a miss**
> You missed a ping at 14:02 (Uptown, structural-entry). It's been offered to the next responder. Missed pings lower your ranking a little. You're still ranked normally.

## The changes behind it

| # | Change | Who feels it | Fixes |
|---|---|---|---|
| 1 | **Visibility:** live pings and Nudge, weekly balance, responder pages with ranking over time, alerts, a handler availability switch, and the "Your pings" card, on the console and both apps | Kip, Linda, Farlight | Nobody can see a responder going quiet |
| 2 | **Easier to catch in 60s:** a full-screen countdown that gets urgent near the end, and lock-screen *Take* | Responders | Pings answered, pings taken |
| 3 | **Miss penalty cut** from −0.12 to about −0.04. No penalty for turning down a ping outside your area | Responders | One slow week sinks a responder |
| 4 | **Make the four whole:** a one-time restore of every responder's score to its 11 Aug value | The quiet four | Share of pings |
| 5 | **Slow recovery:** a score drifts back up to 0.5 over about 4 weeks, only while the responder is available. This settles Wen's 2019 note in the code | Everyone, long term | No way back today |
| 6 | **One retry:** a missed first ping on a local callout comes back once if the next responder doesn't take it | Handlers, callers | Callouts filled |
| 7 | **Report a problem where it happened:** one ticket per ping with its record attached, plus a general form | Handlers, responders, support | Tickets that lack ping details and repeat each other |

Considered and rejected: a "Seen, deciding" tap that holds the ping longer. It would be a longer wait in disguise, and since turn-downs never took more than 40s, the time goes into reaching the phone, not deciding. Routing settings ship globally, so 3–6 can't be piloted by area. They ship in a separate release from 1, 2 and 7, so each effect can be measured on its own.

## Where it gets us

| Measure (all responders, weekly) | Before 4.2 | Now | Projected | Range |
|---|--:|--:|--:|--:|
| Pings answered (taken or turned down) | 97.7% | 84.9% | 91.5% | 85–98% |
| Pings taken (acceptance rate) | ≈77% | 66–73% | 72% | 67–77% |
| Callouts filled | 94.9% | 89.2% | 94.0% | 93–95% |
| Quiet four's share of pings | 28% | 5% | 27% | 27%* |

The projection depends on how much of the 60s miss increase the alert and nudge changes win back: all of it (optimistic), three quarters (central) or half (pessimistic). **Callouts filled and the quiet four's share come back in every case.** Answered and taken only return to their pre-4.2 levels if the alerts work. That is why the alerts ship first and get measured.

\*The ping share holds in all three cases, because a miss now costs less than a taken ping earns. It assumes Wen can explain and correct the jump in out-of-area first pings on 12–14 Aug (20% → 51%). Without the restore in change 4, recovery alone tops out at about 64% of a responder's usual pings.

## Projected pings for Kip's two responders and Farlight

*The HTML version ([one-pager.html](one-pager.html)) shows these as charts. Markdown can't draw charts, so the same data is below as a table. Projected weeks show the central case, with the pessimistic-to-optimistic range for pings taken in brackets.*

- Meteor Mite: Kip · Eastgate · usual week 11
- The Gale: Kip · Eastgate · usual week 13
- Farlight: Linda Pruitt · Uptown · usual week 12

| Week | Meteor Mite pings | Meteor Mite taken | The Gale pings | The Gale taken | Farlight pings | Farlight taken |
|---|--:|--:|--:|--:|--:|--:|
| 29 Jun | 11 | 7 | 13 | 10 | 12 | 9 |
| 6 Jul | 12 | 9 | 12 | 9 | 12 | 9 |
| 13 Jul | 10 | 6 | 13 | 10 | 11 | 8 |
| 20 Jul | 11 | 7 | 14 | 11 | 12 | 9 |
| 27 Jul | 12 | 9 | 13 | 11 | 13 | 10 |
| 3 Aug | 11 | 8 | 13 | 10 | 12 | 8 |
| 10 Aug | 10 | 4 | 15 | 9 | 10 | 4 |
| 17 Aug | 4 | 1 | 17 | 12 | 3 | 0 |
| 24 Aug | 2 | 0 | 20 | 14 | 1 | 0 |
| 31 Aug | 1 | 0 | 21 | 16 | 0 | 0 |
| *Changes ship* | | | | | | |
| Ship +1 | 10.7 | 6.2 (5.0–7.3) | 13.4 | 10.4 (10.1–10.7) | 11.5 | 7.2 (5.9–8.5) |
| Ship +2 | 11.2 | 6.5 (5.1–7.7) | 13.0 | 10.1 (10.0–10.3) | 12.0 | 7.5 (6.1–9.0) |
| Ship +3 | 11.2 | 6.5 (5.1–7.7) | 13.0 | 10.1 (10.0–10.3) | 12.0 | 7.5 (6.1–9.0) |
| Ship +4 | 11.2 | 6.5 (5.2–7.7) | 13.0 | 10.1 (9.9–10.3) | 12.0 | 7.5 (6.1–9.0) |
| Ship +5 | 11.2 | 6.5 (5.2–7.7) | 13.0 | 10.1 (9.8–10.3) | 12.0 | 7.5 (6.1–9.0) |
| Ship +6 | 11.2 | 6.5 (5.3–7.7) | 13.0 | 10.1 (9.8–10.3) | 12.0 | 7.5 (6.1–9.0) |
| Ship +7 | 11.2 | 6.5 (5.3–7.7) | 13.0 | 10.1 (9.8–10.3) | 12.0 | 7.5 (6.1–9.0) |
| Ship +8 | 11.2 | 6.5 (5.3–7.7) | 13.0 | 10.1 (9.8–10.3) | 12.0 | 7.5 (6.1–9.0) |

Actual weeks run from 29 Jun to 31 Aug (rook-database). There is no data after 6 Sep, so the projection starts in the week the changes ship, not on a calendar date. For Kip, the projection moves about 8 pings a week back from The Gale to Meteor Mite. That reverses what happened after 4.2, when roughly 8 of the 10 pings Meteor Mite lost went to The Gale.

## Before we build: open questions

- **Wen:** why did out-of-area first pings jump on 12–14 Aug, before any scores fell? Does a restart reset scores to 0.5? Do we have the 11 Aug scores needed for the restore?
- **Wen:** should the second chance (change 6) come straight back to the responder, or only after the next responder has had it, as the prototype shows? Straight back is faster for the callout but holds everyone else up for another 60 seconds.
- **Security Policy 4.1** isn't in the wiki. The new cards and support tickets show callsigns, tags and ping history only, never cover identity, but they still need a review against the policy.
- **Nadia:** agree the ticket categories and how tickets raised from a ping are routed. One ticket per ping, with its record attached, should cut the repeated tickets support sees today.
- **Answer times aren't logged.** Start logging them now, so we can tell whether misses come from reaching the phone or from deciding.
- **Supply** reads the Availability Record and needs to hear about this before any routing change ships.
- **Sofia** needs to scope the console and phone work alongside the redesign. That includes the handler phone app, which is on the Q4 roadmap as exploring and not staffed.

# Impact guide: how routing changes move the four outcomes

Use this to write the "Projected impact" cards. Every projection is an
estimate. Say what it rests on, and say "unclear" rather than guess.

## The targets (from `05-super-speed/brief.md`)

| Outcome | Before 4.2 | Now (after 4.2) | Brief's central projection | Range |
|---|--:|--:|--:|--:|
| Pings answered (taken or turned down) | 97.7% | 84.9% | 91.5% | 85–98% |
| Pings taken (acceptance rate) | ≈77% | 66–73% | 72% | 67–77% |
| Callouts filled | 94.9% | 89.2% | 94.0% | 93–95% |
| Quiet four's share of pings | 28% | 5% | 27% | 27% |

Quiet four: Vesper, The Undertow, Farlight, Meteor Mite.

## The seven agreed changes and which release they belong to

| # | Change | Release | Mainly moves |
|---|---|---|---|
| 1 | Visibility: live pings and Nudge, weekly balance, responder pages, alerts, handler availability switch, "Your pings" card | A | (handler awareness; indirectly answered) |
| 2 | Harder to miss in 60s: full-screen countdown, lock-screen Take | A | answered, taken |
| 7 | Report a problem per ping, plus a general form | A | (tickets, not the four outcomes) |
| 3 | Miss penalty about −0.04; no penalty for turning down an out-of-area ping | B | share, taken |
| 4 | One-time restore of every score to its 11 Aug value | B | share |
| 5 | Slow recovery up to 0.5 over about 4 weeks, only while available | B | share |
| 6 | One retry: a missed first ping on a local callout comes back once, after the next responder | B | filled, answered |

Release A (1, 2, 7) and Release B (3–6) ship separately so each can be
measured on its own. Routing settings ship globally, so 3–6 can't be piloted
by area.

## Anchors for sizing an effect

- **Ping wait.** 90s → 60s took first pings missed by in-area responders
  from 0.7% to 11.4%, and pings answered from 97.7% to 84.9%. Missed pings
  went from 2–6 a week to 21–38. Turn-downs never took over 40s, so the lost
  time goes on reaching the phone. Any change to the wait moves all four
  outcomes and muddies measuring Release A. Lengthening it trades callout
  speed for answers; shortening it repeats 4.2.
- **Alerts (change 2).** The brief's central case assumes alerts win back
  three quarters of the 60s miss increase (answered 91.5%). Optimistic: all
  of it (~98%). Pessimistic: half (~85%).
- **Miss penalty.** Today a miss costs −0.12 against +0.08 for a take, so
  anyone taking under 60% of pings drifts down. At −0.04, a miss costs a
  third of a turn-down and the ping share holds in every scenario.
- **Scores and recovery.** With no recovery, a responder at 0 needs seven
  taken pings to reach 0.5. At the 4.2 weights, a score of 0 vs 1 is worth
  about 19 minutes of travel time. Recovery alone (no restore) tops out at
  about 64% of a responder's usual pings; with the restore, the quiet four's
  share returns to about 27%.
- **Ranking weights.** The 4.2 change halved a failed ping's effect (worth
  about 2.25 minutes of travel, was 4.8). Out-of-area first pings jumped from
  20% to 51% on 12–14 Aug, unexplained (open question for Wen). Out-of-area
  pings were 0 of 178 taken before 4.2. Anything that sends more first pings
  out of area lowers taken and answered.
- **Retry and the list.** Unfilled callouts rose from 5.1% to 10.8%, all from
  callouts ending on a miss; those ending on a turn-down stayed about 7 a
  week. 35 of 40 unfilled after 4.2 stopped after one ping. A retry that
  comes straight back holds everyone else up another 60s; the brief's design
  retries after the next responder.
- **Not modelled:** answer times (not logged), local-callout speed, and the
  60–90s curve (assumed). Say so when an estimate leans on them.

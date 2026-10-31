# 04 · X-Ray Vision — prompts

**Context:** You joined Rook two weeks ago as PM on Dispatch.
Release 4.2 shipped on 12 August, just before you arrived, and
landed badly. Last session the numbers showed you what happened: a
ping used to wait ninety seconds and now it waits sixty, people
missed pings they used to catch, and missing one counts the same as
turning one down — so four responders stopped hearing from us
altogether.

At the end of the session, type wrap up, and Claude Code saves the
prompts you wrote yourself below — not the starter prompt — updates
CLAUDE.md, and saves your work to GitHub. By Module 6 this file is a
prompt library built from your own questions.

---

### 1.

Pick one responder from the pings table who went quiet. Show me every week since June: how many pings, and what they did with each. Use their name.

### 2.

Why did you pick vesper

### 3.

For each of these customer outcomes, pick one user (for each) where ping an support data correlate well. As a chart, show me every week since June: how many pings, and what they did with each. Use their name. Keep it concise.

* Ping volumes have shifted towards a subset of users and away from others
* Missed pings have gone up

### 4.

find a way standardize both charts against the same y-axis metric

### 5.

Add to both charts their responder scores

### 6.

Is it possible to visually factor in the in-area/out-of-area callout types in the chart

### 7.

Let's revert that and instead separate out the in/out of area bit onto it's own weekly chart alongside the others

### 8.

for the in/out of area, just do it by volume

### 9.

for the in/out of area, add another dimension (or do a separate chart if cleaner) to show the missed/turned down/taken metrics for in vs out of area callouts

### 10.

add the legend above the ironvale chart as well for easier readability. Then add the charts to the priority-heatmap.html as a separate tab.

### 11.

Review the ping and support data (where there's strong correlation) to investigate where release 4.2 went wrong. Focus on the following outcomes we've identified in previous sessions, and point out where 4.2 made undesirable changes and how to fix them, and how to best test/rollout/measure. Keep everything concise. Call out any issues that may have been preexisting.

* Missed pings has increased
* Ping volumes have shifted to subset of users
* In/out-of-area pings have shifted as well
* Ping scores not recovering quickly enough

### 12.

So to summarize:

* Pre-existing issue: poor/no score recovery 
* Root cause from 4.2: decreased ping wait times
* Follow-on issues due to 4.2: shift in ping volumes to a subset of users

### 13.

Re-validate the root cause and follow-on issue against the database

### 14.

Review the code and database (pre- and post-4.2) to validate the summary of issues below:

* Pre-existing issue: poor/no score recovery, and missing are treated the same as turn downs
* Root cause from 4.2: decreased ping wait times
* Follow-on issues due to 4.2: shift in ping volumes to a subset of users, with those users getting an increase in out-of-area calls
* Not sure where this issue sits: No fallback options when the list of available responders runs out

### 15.

Give me a more concise summary

### 16.

Here's a question from Marcus out Eng lead:

Quick one, did the change to who gets asked first apply to responders who'd already been turning jobs down, or just new ones? Can't tell from the code and don't want to guess on this. Anyone know?

### 17.

So just confirm, the question that Marcus asked doesn't add to the issues we've already identified?

### 18.

Review the code base and identify where these issues exist, and suggest the fix needed. List everything in the appropriate rollout order to accurately test/measure that we're solving the problems correctly. Suggest success metrics for each as well. For the unexplained issue, suggest where in the code base we need to investigate. Keep everything very concise. 

* Pre-existing: a miss costs the same as a turn-down, and scores recover only by taking pings, so low-ranked responders get stuck. There is also no fallback in this code when the list runs out.
* 4.2 trigger: the shorter ping wait is the strongest explanation for the jump in misses, though answer times aren’t recorded.
* Likely follow-on: repeated misses pushed four responders’ scores to 0, and their pings moved to others. Unfilled callouts doubled for the same reason.
* Unexplained: out-of-area first pings jumped on release day, before scores fell and against the intent of the proximity change. Out-of-area pings also went from never taken to often taken.

### 19.

Find me the part of this code that takes points off somebody when they miss a ping or turn one down. Show it to me and explain it in plain English. Then find me every single thing in this code that puts points back on.

### 20.

Somebody has been quiet for a month. Walk me through, step by step, exactly what would have to happen for them to start getting work again.

### 21.

Thank you, re-summarize the suggested fixes (where/how/what to measure) and prioritize accordingly so that:

* Fewer responders are missing their pings
* Responders aren't punished as heavily for missing vs turning down
* In-area calls go to local responders at a similar rate to what it was prior to 4.2

### 22.

Feels like there are two additional issues we haven't decided if/how to resolve

* Scores aren't auto-recovering over time without the responder accepting callouts
* Callouts are ending unanswered if we run out of responders to ping


Suggest what a good outcome/solution would be for this. Provide a concise explanation.

### 23.

Thank you, re-summarize the suggested fixes (where/how/what to measure) and prioritize accordingly so that:

* Fewer responders are missing their pings
* Responders aren't punished as heavily for missing vs turning down
* In-area calls go to local responders at a similar rate to what it was prior to 4.2
* Scores recover naturally over time without having to accept callouts (use the approach you suggested)
* Callouts don't end silently when we run out of responders to ping (use the approach you suggested)

### 24.

Add the fix summary to the priority-heatmap.html as a separate tab

To help the convo with Wen, add a modelling chart that allows to visualize how tweaking the relevant parameters impacts the (projected) response rates and times.

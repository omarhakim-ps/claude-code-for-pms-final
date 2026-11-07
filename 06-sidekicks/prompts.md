# 06 · Sidekicks — prompts

**Context:** You joined Rook two weeks ago as PM on Dispatch.
Release 4.2 shipped on 12 August, just before you arrived, and
landed badly. You've spent five sessions on it: finding out what
went wrong, then building the fix nobody had — a working prototype,
by hand, in one sitting, for one room.

At the end of the session, type wrap up, and Claude Code saves the
prompts you wrote yourself below — not the starter prompt — updates
CLAUDE.md, and saves your work to GitHub. By Module 6 this file is a
prompt library built from your own questions.

---

### 1.

Assume helen has approved the changes/fixes proposed in the brief and prototype, and we've successfully shipped it. 

Make a skill that I can run on a weekly basis to compile and review the relevant metrics so that we can confirm whether the targeted outcomes were reached - pings answered, pings taken, callouts fulfilled, and share of calls restored that what it was before 4.2 (within reason). 

Ask me clarifying questions as needed.

### 2.

The page is blank?

### 3.

I prefer light mode visuals. Update the skill accordingly.

### 4.

The mock report is still dark mode

### 5.

Let's take a step back and pretend Helen has approved the brief/prototype, but we've not deployed them yet.

Create a scheduled QA skill that runs at the start of each week to validate whether upcoming releases will impact the same outcomes

Ask clarifying questions as needed

### 6.

Will the QA skill validate both the code and the UI?

### 7.

No changes required yet, but how would you improve these for the following scenarios/audiences?

* Exec review - they want to know what went wrong and how we fix and prevent
* Product team review - to share how we went from issue to fix
* Squad retro - to improve ways of working between Eng and Product

### 8.

How do the proposed fixes impact the wider responder base beyond the quiet four?

### 9.

Model projections for all 16 responders

### 10.

Based on the 16 projections, do you think we should proceed with the proposed changes?

### 11.

Ensure the presentation reflects that we've modelled/projected for the entire responder base (and we didn't just tunnel vision on 4 responders) and why we think the proposed changes are on the right track. Be sure to include callouts/contingencies for:

* Release A makes no difference to misses. Then the problem is the 60-second window itself, not visibility, and the brief’s premise of keeping 60s needs revisiting.
* The out-of-area jump turns out to be a separate bug. Then fixing it may matter more than the score changes, and Release B should be rescoped.

### 12.

sanity check the deck to ensure the framing, storytelling, narrative, proof and projections are all in alignment with one another

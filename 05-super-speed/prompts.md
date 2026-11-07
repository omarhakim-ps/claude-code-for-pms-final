# 05 · Super Speed — prompts

**Context:** You joined Rook two weeks ago as PM on Dispatch.
Release 4.2 shipped on 12 August, just before you arrived, and
landed badly. You've spent three sessions finding out what went
wrong: the two piles of feedback that didn't agree, the numbers that
hid four people inside an average, and the code that settled it —
the shorter timeout is what did it.

At the end of the session, type wrap up, and Claude Code saves the
prompts you wrote yourself below — not the starter prompt — updates
CLAUDE.md, and saves your work to GitHub. By Module 6 this file is a
prompt library built from your own questions.

---

### 1.

Bring up my html artifact

### 2.

Tell me what's my director's request is in 05-super-speed/director-request.txt

### 3.

Which responders did we review last time to the see impact of 4.2?

### 4.

Review the director's request and create:

* one-pager brief - no prototype or code changes yet
* propose a change (or set of changes) where:
   * We retain the 60 second ping wait
   * We can return the pings answered, pings taken, callouts filled, and share of the quiet four's share of pings to what it was before 4.2 (within reason)
   * We can provide better notice/visibility to handlers and responders of where they are in terms of their ping/callout histories, their eligibility (and how it will/could improve over time)
* include a chart to project the impact on Kip and Farlight for the proposed changes

### 5.

Switch brief to light mode

### 6.

No changes required yet. Was not pushing the first miss part of the brief? I don't see it in the prototype.

### 7.

We'll need a handler phone app as well

### 8.

Something looks off about the slider in the handler's phone app relative to the responder's phone app - see screenshot.

Separately, add a visual to the handler's console when they drill through on a responder so they can see the responder's ranking and projected recovery.

### 9.

the ranking visual/chart in the handler console shouldn't be about before/after 4.2 - they have no idea what that means. It's meant to reflect the responder's historical, current, and projected rankings over time.

### 10.

Add the ability for a handler to mark a responder as unavailable

### 11.

If the handler marks a responder as unavailable, and the responder restores their availability, then that should clear the "handler marked you unavailable" notification and send a "responder is available again" notificaition. Also consider a notification to the handler for when a responder marks themselves as unavailable.

### 12.

On the handler console, the availability button toggle/button should be visible without requiring drill through on a responder

To the handler app, allow the handler to drill through to a similar last 10 pings view as the responder.

To the console and both apps, allow the user to tap/click on a particular ping to raise a support ticket specific to that event.

### 13.

To the console and both apps, add a way to easily raise a support ticket for issues in general.

Ensure the brief and prototype are in alignment with one another.

Save changes to both the brief and prototype files.

### 14.

I need to present the prototype to helen and convince her what we're changes/fixes we're proposing will satisfy her request. Add concise annotations to the prototype to call out the proposed changes from the brief. Where relevant, highlight the impact and before/after metrics.

Save the changes to the prototype file.

### 15.

In the apps, move the "report problem" button to the bottom of the page. In the console, I'm not sure why the "report problem" button has/needs a number next to it?

Move out the annotation currently placed inside the responder app. Put it somewhere more appropriate without disrupting the design. Use arrows (or something similar) if you really need to pinpoint something.

Is there any merit in staging the console inside a desktop/browser window the same way we've stage the apps in phone window? Not a must have, just a consideration.

### 16.

Yes, stage the console.

Ensure the app titles are appropriately matched - see screenshot.

There are way too many annotations now - or at least they seem to visually dominate the prototype. It looks chaotic. Suggest a better and more concise way to annotate before making a change.

### 17.

In the console responder drill through, display the last 10 pings vertically (same order as apps) to improve readability and navigation.

Spacing looks strange in the top pin descriptions panel - see screenshot.

Remove click to persist on pins - annotations should show on hover only.

Review the positioning of the pins and make sure they're appropriate.

### 18.

Why is pin 7 on the generic report problem button and not on a ping? Seems to conflict with it's description?

### 19.

Ensure the brief and prototype are aligned. Keep the brief and annotations concise.

Save changes to brief and prototype files.

Wrap up.

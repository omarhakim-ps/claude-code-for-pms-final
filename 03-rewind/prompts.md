# 03 · Rewind — prompts

**Context:** You joined Rook two weeks ago as PM on Dispatch.
Release 4.2 shipped on 12 August, just before you arrived, and
landed badly.

Last session you read four conversations and every support ticket
since 4.2 — and found the two piles did not agree.

At the end of the session, type wrap up, and Claude Code saves the
prompts you wrote yourself below — not the starter prompt — updates
CLAUDE.md, and saves your work to GitHub. By Module 6 this file is a
prompt library built from your own questions.

---

### 1.

Recategorize the data into

* Who got pinged more (+3)
* Who got pinged roughly the same 
* Who got pinged less (-3)


Same metrics, just recategorized for a different view

### 2.

Summarize what you're seeing in terms of changes to customer outcomes/behaviours. Keep it concise. Focus on topline metrics.

### 3.

Summarize what you're seeing in terms of changes to customer outcomes/behaviours based on the 3 groups. Keep it concise. Focus on topline metrics.

### 4.

Would it be accurate to say the main issues with release 4.2:

* Ping volumes have shifted towards a smaller group of responders
* More pings are missed due to the shorter response period

### 5.

Why are callouts are going unfilled?

### 6.

Double-check the metrics behind the following:

* Ping volumes shifting towards a subset of users
* Ping responses has dropped (due to shorter ping waits)
* Ping fulfilment has dropped (due to premature callout termination)


Review the code base and identify where and why these issues are arising.

### 7.

Compare the support_tickets table on rook-database against the pings table. Do they agree with each other? When do the numbers actually move?

### 8.

How do I reconnect

### 9.

Give me a concise summary and focus on topline metrics

### 10.

So if I was to summarize:

* Ping volumes have shifted to a subset of users
   * Ping and support data agree - though support is trailing as you would expect
* Ping misses have gone up (due to shorter ping wait and slow/non-recovering score decreases)
   * Ping data shows this, but support data is seeing more of "I'm getting no pings at all"?
* Unfulfilled callouts have gone up (due to lack of fallback options when responder lists run out)
   * Ping data shows this, but support data doesn't show this at all?

### 11.

Let's ignore the unfulfilled callout since that's more an internal concern.

Focusing on the key customer outcomes then:

* Ping volume shifted away/towards from/to a subset of responders
   * Ping and support data correlate well, albeit with support trailing as we would expect
* Missed pings have gone up
   * Ping and support data correlate well, albeit with support trailing as we would expect


Is that a fair summary?

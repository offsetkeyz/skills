---
id: batching
name: Batch Size
category: simplify
triggers:
  - work is collected and processed weekly or monthly
  - items wait for a batch to fill before moving
  - same small task repeated with constant interruptions
blocking_inputs: [volume, time_wait]
version: 1.0
---
# Batch Size

## What it is
Batch size is how many items are gathered before they are processed or passed on together.
Smaller batches cut wait time, smooth out swings in workload, and surface mistakes sooner.
Each run also carries a fixed overhead (setup, logging in, context switching), so the best size balances that overhead against the cost of items sitting and aging.
When switching cost is high, grouping scattered small tasks into one sitting can be the better move.

## When to apply
**Apply when:** work is held and processed on a cycle (weekly, monthly, "when the pile is big enough"), items wait for a batch to fill, or one role is pulled away by the same small task many times a day.
**Do not apply when:** items are processed one at a time as they arrive with no waiting; volume is too low for a cycle to matter (a few items a month); or the cycle is fixed by an outside party (a bank cutoff, a court calendar, a vendor's billing date).

## Diagnostic questions
- [blocking] How often is this work processed (daily, weekly, monthly, when the pile gets big)? → unlocks: batch-delay estimate
- [blocking] About how many items arrive in each cycle? → unlocks: total waiting time across items
- [nice-to-have] What does each run cost to set up (opening systems, gathering files, getting into the task)? → default: low; recommendation leans toward smaller batches
- [nice-to-have] Does delay cost anything (late fees, missed discounts, unhappy customers, slower cash)? → default: moderate
- [nice-to-have] Do items arrive fairly evenly through the cycle? → default: yes; half-interval estimate used and marked (verify)

## How to apply
1. From the step table, find steps where `time_wait` comes from waiting for a scheduled run or a full pile rather than waiting on a person.
2. Estimate the average delay the batch adds: about half the batch interval when items arrive evenly. Show the units and mark estimates with "(verify)".
3. Estimate setup overhead per run and multiply by runs per period to get overhead for each option.
4. Compare: hours of overhead added (or saved) against days of delay removed (or added), and against what delay costs.
5. Recommend a direction, smaller batches or grouped work, with the math inline.

Worked example: an office enters 40 vendor bills per week in one Friday session. Bills arrive evenly over 5 business days, so the average bill waits about 2.5 business days (half of 5) before entry. Switching to a daily session cuts the average wait to about 0.5 business days, a saving of about 2 business days per bill. If each session takes 15 minutes to set up, overhead goes from 15 min/week (1 run) to 75 min/week (5 runs), an extra 1 hr/week. The report states the trade plainly: about 1 extra hr/week of setup buys about 2 fewer business days of delay per bill (40 bills/week). Recommend daily if late fees, missed early-pay discounts or vendor calls cost more than that hour; otherwise suggest twice weekly (average wait about 1.25 business days, extra 15 min/week) as a middle step.

## Typical recommendations
- Move from weekly or monthly processing to daily or twice weekly for work where delay costs money or goodwill (ladder tier 1)
- Group scattered interruptions (quick requests, status questions, small entries) into fixed time blocks, with an exception path for urgent items (ladder tier 1)
- Process items as they arrive instead of waiting for a pile, when setup is near zero (ladder tier 1)
- Cut setup time so small batches are cheap: saved views, templates, bookmarked reports, pre-filled forms (ladder tier 2)
- Automate the collection or setup step (scheduled imports, auto-filing to a shared queue) so each run starts ready (ladder tier 3)

## Failure modes
- Applying a one-size rule ("always smaller") without weighing setup cost
- Ignoring setup or switching cost, so the daily run costs more hours than the delay was worth
- Batching customer-facing work that needs a fast response (replies, booking confirmations)
- Treating the half-interval estimate as exact when items arrive in bursts (for example, all at month end)
- Shrinking batches on a step the owner keeps manual by choice without asking (check `manual_by_choice`)

## Citations
- Reinertsen, D.G., *The Principles of Product Development Flow: Second Generation Lean Product Development* (2009). Celeritas Publishing, Redondo Beach, CA. [book] https://search.worldcat.org/title/The-principles-of-product-development-flow-:-second-generation-lean-product-development/oclc/435994279

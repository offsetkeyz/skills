---
id: littles-law
name: Little's Law
category: bottleneck
triggers:
  - a queue or backlog is described with counts or times
  - user asks how long items take end to end
  - large batches build up before a handoff
blocking_inputs: [volume, time_wait]
version: 1.0
---
# Little's Law

## What it is
In a stable system, the average number of items in progress (L) equals the average arrival rate (λ) times the average time each item spends in the system (W): L = λ × W.
"Stable" means items leave about as fast as they arrive, so the backlog is not growing over time.
If you know any two of work in progress, throughput, and lead time, you can work out the third.
It needs no assumptions about how work arrives or the order it is handled; it is about averages over a long enough period.

## When to apply
**Apply when:** average weekly (or daily) volume is known, plus either the size of the backlog or the typical time items take end to end.
**Do not apply when:** the backlog is growing week over week (the system is not stable), or the work is a one-off project rather than a repeating flow.

## Diagnostic questions
- [blocking] How many items arrive per week? → unlocks: throughput (λ)
- [blocking] About how many are in progress or waiting right now? → unlocks: lead-time estimate (W = L ÷ λ)
- [nice-to-have] Is the backlog roughly steady, or growing? → default: steady; if growing, the report says arrivals exceed capacity and Little's Law results are not used
- [nice-to-have] Do you count time in calendar days or business days? → default: business days (5 per week), stated in the math

## How to apply
1. Pull `volume` and any backlog count or `time_wait` from the step table. Convert to one set of units (for example, items per business day and business days) and show the conversion.
2. Compute the missing quantity: W = L ÷ λ, L = λ × W, or λ = L ÷ W.
3. Compare W with the total `time_touch` for one item to show what share of the lead time is waiting rather than work.
4. Show the math inline. Mark any result built on `~estimated` inputs with "(verify)".
5. Worked example: a 6-person accounting firm receives about 40 client document requests per week (8 per business day). The office manager says about 60 are open at any time. W = 60 ÷ 8 = 7.5 business days end to end. Hands-on time is about 20 minutes per request, so roughly 99% of the lead time is waiting (verify).
6. If the backlog is growing, stop here and report that arrivals exceed capacity; route to the bottleneck analysis instead.

## Typical recommendations
- Cap work in progress: set a limit on how many items can be open at one step, and finish before starting new ones (ladder tier 1)
- Cut batch size: hand off work daily instead of weekly so items stop waiting for the batch to fill (ladder tier 1)
- Reduce arrivals of avoidable work, such as duplicate requests or follow-ups caused by missing information, using a checklist or required form fields (ladder tier 1–2)

## Failure modes
- Applying it to a growing backlog, where the averages are not stable and the result is misleading.
- Mixing units, such as volume per calendar week with time in business days.
- Treating the result as exact for every item rather than an average across many items.
- Using a single busy-week snapshot of the backlog as if it were the long-run average.

## Citations
- Little, J.D.C., "A Proof for the Queuing Formula: L = λW" (1961). *Operations Research* 9(3):383–387, INFORMS (then Operations Research Society of America). [peer-reviewed] https://doi.org/10.1287/opre.9.3.383

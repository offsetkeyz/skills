---
id: vsm
name: Value Stream Mapping
category: waste
triggers:
  - 3 or more handoffs between roles
  - total wait time is much larger than total touch time
  - user wants an end-to-end view
blocking_inputs: [time_touch, time_wait]
version: 1.0
---
# Value Stream Mapping

## What it is
Draw the work as it really flows today, from the first trigger to the finished output, including how information passes between people.
Record hands-on (touch) time and waiting time for every step, then add them up to get lead time.
Flow efficiency is total touch time divided by lead time. In office work it is often a small percentage, because most time is spent waiting.
Then design a future state that removes the biggest waits and handoffs, and plan the steps to get there.

## When to apply
**Apply when:** the process has several steps and passes between two or more roles (for example, a client intake that moves from front desk to paralegal to attorney to billing), and you need to see where the time goes end to end.
**Do not apply when:** one person does a single step start to finish. There are no handoffs or waits to map, so use a simpler lens such as ECRS or a checklist.

## Diagnostic questions
- [blocking] How long does work sit between each handoff before the next person picks it up? → unlocks: lead time and flow efficiency
- [blocking] Does this list match what actually happens day to day, including workarounds, re-sends and side spreadsheets? → unlocks: current-state accuracy
- [nice-to-have] How does the next person learn that work is ready for them? → default: email or verbal; signaling fixes flagged Medium confidence
- [nice-to-have] Do some items skip steps or loop back for corrections? → default: no; rework not included in lead time

## How to apply
1. Build the current-state timeline from the step table in order: actor, tool, `time_touch`, then the `time_wait` before each step.
2. Convert to one unit (show the conversion), then sum touch time and wait time. Lead time = total touch + total wait.
3. Compute flow efficiency = total touch ÷ lead time. Show the math inline and add "(verify)" when any input is `~estimated`.
4. Mark every handoff (where `handoff_to` changes) and the largest waits. Name the top two or three waits as findings.
5. Sketch a future state: fewer handoffs, a clear ready signal so work is pulled instead of waiting in inboxes, and adjacent steps combined. Recompute lead time and flow efficiency for the future state.
6. List the changes needed to get from current to future state, each mapped to a fix-ladder tier.

## Typical recommendations
- Give one role end-to-end ownership of a stretch of steps to remove handoffs, e.g. the same person who takes the intake call also opens the file (ladder tier 1)
- Add a ready signal so the next person sees waiting work without being chased: a shared queue, a status field, or an assigned-to view in the tool already in use (ladder tier 2)
- Combine adjacent steps done by the same role or in the same tool into one pass (ladder tier 1)
- Set a fixed daily pickup time for a recurring handoff instead of "when someone notices" (ladder tier 1)

## Failure modes
- Mapping the official or written process instead of the real one, which hides the workarounds where the waits live.
- Mapping without times, which produces a flowchart, not a value stream map, and gives no lead time or flow efficiency.
- Drawing a future state with no plan, owners or order of changes to reach it.
- Treating estimated wait times as exact; flag them and confirm on the walkthrough.

## Citations
- Rother, M. & Shook, J., *Learning to See: Value-Stream Mapping to Create Value and Eliminate Muda* (1999). Lean Enterprise Institute. [book] https://www.lean.org/store/book/learning-to-see/

---
id: toc
name: Theory of Constraints
category: bottleneck
triggers:
  - time_wait at one step is 3x or more its time_touch
  - work queues in front of one actor or step
  - one role appears in many steps and others wait on it
blocking_inputs: [time_touch, time_wait, volume]
version: 1.0
---
# Theory of Constraints

## What it is
Every process has one step or role that limits how much work gets through: the constraint.
Speeding up any other step does not raise output. It only grows the pile in front of the constraint.
The method uses five focusing steps: identify the constraint, exploit it (get the most from what it already has),
subordinate everything else to its pace, elevate it (add capacity), then repeat.
When repeating, do not let old habits or policies become the new constraint.

## When to apply
**Apply when:** work clearly piles up or waits at one point, such as files sitting in a partner's review queue or invoices waiting on one approver.
**Do not apply when:** there is no timing or volume data to show where work waits; or the process is mostly idle waiting on demand (the constraint is the market, not the process).

## Diagnostic questions
- [blocking] Where does work wait longest, and for how long? → unlocks: constraint identification
- [blocking] How many items per week enter the process, and how many leave it finished? → unlocks: throughput check (is a queue growing, and where)
- [nice-to-have] Does the constrained person or step also do work that is not on the constraint? → default: yes; offload recommendation flagged Medium confidence
- [nice-to-have] Is the constraint ever idle because it is waiting on inputs? → default: no

## How to apply
1. Scan the step table for the largest `time_wait` or queue. Compare it to `time_touch` at that step and to `volume` in and out.
2. Name the constraint: the step and its `actor`. Confirm with wait data, not with who seems busiest.
3. Exploit it: strip non-essential work off the constrained role, batch its interruptions into set times, and make sure inputs arrive complete so it never reworks or chases missing items.
4. Subordinate: pace upstream steps to what the constraint can handle. Releasing more work faster only lengthens the queue.
5. Elevate only after exploiting: add capacity, delegate part of the work, or add a tool.
6. Re-check the step table after each fix. Find where work now waits longest; that is the new constraint.

## Typical recommendations
- Move tasks that are not constraint work off the constrained role, for example scheduling or filing handled by a front-desk role instead of the owner (ladder tier 1)
- Fix incomplete inputs upstream with required fields on the intake form or a short checklist before handoff (ladder tier 1–2)
- Set a fixed daily review window for the constrained role instead of reviewing ad hoc (ladder tier 1)
- Delegate approvals under a set dollar threshold to a second role, keeping a human approval for anything that moves money (ladder tier 1)

## Failure modes
- Optimizing a step that is not the constraint, which adds cost and no output.
- Elevating (hiring, buying software) before exploiting the capacity the constraint already has.
- Treating the busiest-looking person as the constraint without wait or queue data.
- Not re-checking after a fix, so the team keeps working on a constraint that has already moved.

## Citations
- Eliyahu M. Goldratt and Jeff Cox, *The Goal: Excellence in Manufacturing* (1984). North River Press. [book] https://search.worldcat.org/title/12721255
- Eliyahu M. Goldratt, *What Is This Thing Called Theory of Constraints and How Should It Be Implemented?* (1990). North River Press. [book] https://search.worldcat.org/title/26552157

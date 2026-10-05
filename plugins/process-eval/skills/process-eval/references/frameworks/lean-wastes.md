---
id: lean-wastes
name: Lean Wastes
category: waste
triggers:
  - duplicate data entry or re-keying
  - steps that only move, copy, or check work
  - rework greater than zero
  - work produced before anyone needs it
blocking_inputs: [step, actor, tool]
version: 1.0
---
# Lean Wastes

## What it is
Toyota's production chief named seven kinds of waste: transport, inventory, motion, waiting, overproduction, overprocessing, and defects.
Waste is any activity that uses time or effort but adds nothing the customer would pay for.
Later Toyota literature added an eighth: unused employee talent and ideas.
DOWNTIME (Defects, Overproduction, Waiting, Non-utilized talent, Transport, Inventory, Motion, Extra processing) is a practitioner mnemonic, not part of the original list.
The goal is to see each step as value-adding, necessary but non-value-adding, or pure waste, then cut or shrink the waste.

## When to apply
**Apply when:** the step table shows re-keying, copying, forwarding, checking, or rework, or steps whose output nobody seems to use.
**Do not apply when:** the process is a single short step with no handoffs, or the only problem is a queue at one point (use toc or littles-law instead).

## Diagnostic questions
- [blocking] Which steps add something the customer would pay for, and which only move, copy, or check work? → unlocks: value vs. waste classification
- [nice-to-have] Which reports, copies, or files does nobody read or use? → default: all used; no overproduction findings raised
- [nice-to-have] Where is the same information typed in more than once? → default: none; re-keying findings only where the step table shows it

## How to apply
1. Read each row of the step table and label it value-adding, necessary non-value-adding (legal, compliance, safety), or waste.
2. For each waste row, name the waste type using the office translation table below.

   | Waste | What it looks like in an office |
   |---|---|
   | Transport | Forwarding or re-sending files and emails between people |
   | Inventory | Backlogs, unread inboxes and queues, half-finished files |
   | Motion | Switching between tools, hunting for files or passwords |
   | Waiting | Waiting on approvals, signatures, or replies |
   | Overproduction | Reports or copies nobody reads; work done before it is needed |
   | Overprocessing | Extra sign-offs, re-formatting, more detail than the user needs |
   | Defects | Errors, missing info, and the rework they cause (`rework` > 0) |
   | Unused talent | Skilled staff doing clerical work; ideas from staff never asked for |

3. Use `actor` and `tool` to spot re-keying (same data, two tools) and talent waste (a senior role on a clerical step).
4. Rank waste rows by `time_touch` × `volume` plus rework cost; mark rankings without timing data as `~estimated`.
5. Skip any row with `manual_by_choice = Y` for tiers 2–4, and keep necessary non-value-adding steps unless a cheaper way to meet the same requirement exists.

## Typical recommendations
- Delete steps that add no value and are not required (ladder tier 1)
- Stop producing reports or copies nobody uses (ladder tier 1)
- Move clerical steps off skilled roles (ladder tier 1)
- Make one system the single source of truth so data is typed once (ladder tier 2–3)

## Failure modes
- Labeling necessary compliance, legal, or safety steps as waste.
- Cutting steps the owner values; always check `manual_by_choice` first.
- Waste-hunting without timing or volume, so trivial waste is ranked above costly waste.
- Treating every check as overprocessing when it prevents expensive defects.

## Citations
- Taiichi Ohno, *Toyota Production System: Beyond Large-Scale Production* (English ed. 1988; Japanese original 1978). Productivity Press. [book] https://www.routledge.com/Toyota-Production-System-Beyond-Large-Scale-Production/Ohno/p/book/9780915299140
- Jeffrey K. Liker, *The Toyota Way: 14 Management Principles from the World's Greatest Manufacturer* (2004). McGraw-Hill. [book] Source for the eighth waste (unused employee creativity). https://search.worldcat.org/title/toyota-way-14-management-principles-from-the-worlds-greatest-manufacturer/oclc/54005437

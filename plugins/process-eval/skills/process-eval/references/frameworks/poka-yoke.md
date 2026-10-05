---
id: poka-yoke
name: Poka-yoke (Error-proofing)
category: error-proof
triggers:
  - rework greater than zero
  - repeated checking or proofreading steps
  - errors reach customers or money
blocking_inputs: [rework]
version: 1.0
---
# Poka-yoke (Error-proofing)

## What it is
Design each step so a mistake either cannot happen or is caught the moment it happens, at the source, instead of being found by inspection later.
Two modes: a control method stops the work until the error is fixed (it prevents the error), and a warning method signals the error but lets the work continue.
In an office this means the form, template or system catches the mistake while the person is still on the step, so nobody has to proofread it later.

## When to apply
**Apply when:** a step has rework above zero, the process includes checking or proofreading steps that exist only to catch earlier mistakes, or errors reach customers or money (⚑ steps).
**Do not apply when:** there is no error or rework data and the user cannot name an error that happens; the error is very rare and cheap compared with time savings elsewhere; or the "error" is really a judgment call where people disagree on the right answer (clarify the rule first).

## Diagnostic questions
- [blocking] Which errors happen most often? → unlocks: error-proofing target
- [blocking] At which step is each error created (not where it is noticed)? → unlocks: source step for the fix
- [nice-to-have] How late in the process are errors found today? → default: found downstream, by a later reviewer or the customer
- [nice-to-have] What does an error cost when it happens (rework time, refunds, late fees, unhappy customers)? → default: low; error-proofing fixes ranked below time savings

## How to apply
1. From the step table, list every step with `rework` above zero and every step whose only job is to check, review or proofread earlier work.
2. For each error, trace it back to the step where it is created (often an earlier step than the one where it is noticed). That source step is the target.
3. Rank errors by frequency × cost. Work on the common, costly errors first.
4. At the source step, prefer a control (the error cannot be entered or the work cannot move on) over a warning (a message the person can dismiss).
5. Prefer prevention at the source over adding a later inspection step. If a later check stays, note why (for example, a ⚑ step that keeps human approval).
6. Once the source fix is in place, re-estimate the rework rate and the time the old checking step took. Recommend removing or shrinking that check only if errors have actually dropped.

## Typical recommendations
- Make key form or CRM fields required so incomplete records cannot be saved (ladder tier 2)
- Replace free-text fields with dropdowns or picklists for values that come from a fixed list (ladder tier 2)
- Add input validation for formats such as dates, phone numbers, amounts and account codes (ladder tier 2)
- Use templates with locked fields so standard wording and figures cannot be changed by accident (ladder tier 2)
- Turn on duplicate detection for contacts, invoices or bills (ladder tier 2)
- Add a short pre-send check before any ⚑ step that moves money or contacts customers, keeping a human approval point (ladder tier 1)

## Failure modes
- Adding another inspection or review step instead of preventing the error at its source.
- Relying on warnings that pop up so often people learn to click past them.
- Error-proofing a rare error while a common one keeps causing rework.
- Making so many fields required that staff enter junk values just to get past the form.
- Removing a human approval on a ⚑ step because a validation rule now exists.

## Citations
- Shigeo Shingo, *Zero Quality Control: Source Inspection and the Poka-yoke System* (1986). Productivity Press (English translation by A. P. Dillon; now a Routledge imprint). [book] https://www.routledge.com/Zero-Quality-Control-Source-Inspection-and-the-Poka-Yoke-System/Shingo/p/book/9780915299072

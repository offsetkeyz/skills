---
id: ecrs
name: ECRS
category: simplify
triggers:
  - same actor does adjacent steps in the same tool
  - a step exists only to prepare for another step
  - steps could happen in parallel or a different order
blocking_inputs: [step, actor, tool]
version: 1.0
---
# ECRS

## What it is
A method-study habit for improving work one step at a time: Eliminate, Combine, Rearrange, Simplify, tried in that order.
Each step is first challenged on its purpose, place, sequence, person and means (why, where, when, who, how).
Only steps that survive the purpose question move on to combining, reordering or simplifying.
The four-word label is a practitioner shorthand; the questioning comes from classic work study.

## When to apply
**Apply when:** the step table has several small steps, steps that only prepare or pass on work, or the same person touching the same item in the same tool more than once.
**Do not apply when:** the process is one or two steps; or the main problem is waiting between roles (use a bottleneck or value stream view first); or the steps are legal, audit or safety controls that cannot change.

## Diagnostic questions
- [blocking] What would break if this step were removed, and who would notice? → unlocks: eliminate candidates
- [blocking] Who does each step and in which tool? → unlocks: combine candidates (same actor, same tool, back to back)
- [nice-to-have] Could the same person do these steps in one sitting? → default: yes if same actor and tool
- [nice-to-have] Must these steps happen in this order? → default: yes; rearrange recs flagged Medium

## How to apply
1. Take each step in the step table and ask its purpose. If nothing breaks without it, mark it Eliminate.
2. For steps that stay, look for neighbors with the same actor and tool. Mark them Combine (one form, one sitting, one pass).
3. Ask whether order, place or person could change. Mark Rearrange when moving a check earlier, running steps in parallel, or moving work to the person who already has the information.
4. Only then ask how to make what is left easier. Mark Simplify (template, default values, fewer fields).
5. Record the question that justified each change next to the step, so the owner can see why.
6. Skip tiers 2–4 for any step with `manual_by_choice = Y`, and keep any control step unless the owner agrees to drop it.

Example: in a 6-person accounting firm, the office manager prints an engagement letter, scans the signed copy, renames the file and then logs it in a tracker. Printing and scanning go (Eliminate, with e-signature already paid for). Renaming and logging become one step (Combine).

## Typical recommendations
- Eliminate a step that nothing downstream uses (ladder tier 1)
- Combine repeated data entry into one form or one sitting (ladder tier 1–2)
- Rearrange to front-load checks, so errors are caught before work moves on (ladder tier 1)
- Simplify a remaining step with a template or saved defaults (ladder tier 2)

## Failure modes
- Simplifying or automating a step before asking whether it should exist at all.
- Combining steps owned by different roles without both roles agreeing.
- Removing a control step (approval, reconciliation, a ⚑ money or customer check) because it looks like overhead.
- Reordering steps without checking for hidden dependencies, such as a document that is not ready yet.

## Citations
- Kanawaty, G. (ed.), *Introduction to Work Study*, 4th (revised) ed. (1992). International Labour Office, Geneva. ISBN 92-2-107108-1. Source for the method-study questioning technique (primary and secondary questions on purpose, place, sequence, person, means). [standards body] https://www.ilo.org/publications/introduction-work-study-4th-revised-edition
- Bârsan, R.M. & Codrea, F.-M., "Lean university: applying the ECRS method to improve an administrative process," *MATEC Web of Conferences* 290, 07003 (2019). EDP Sciences. Names the four steps explicitly and applies them to an office process. [peer-reviewed] https://doi.org/10.1051/matecconf/201929007003

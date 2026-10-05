---
id: checklists
name: Checklists
category: checklist
triggers:
  - fixed sequence of steps done by people
  - a missed step is costly or has happened
  - step is rare enough that people forget it
  - manual_by_choice step that still needs consistency
blocking_inputs: [step, actor]
version: 1.0
---
# Checklists

## What it is
A short checklist used at a set pause point catches critical steps that skilled people still miss.
There are two types. DO-CONFIRM: people work from memory, then stop and confirm each item was done.
READ-DO: people read each item and do it, one at a time.
Good checklists hold only the "killer items" (the steps that cause real harm if skipped), roughly 5 to 9.
They are tested in real use and revised, not written once and filed.

## When to apply
**Apply when:** people do a fixed sequence by hand; a skipped step is costly or has already happened; a procedure is rare enough that people forget parts of it; or a `manual_by_choice = Y` step still needs to be done the same way every time.
**Do not apply when:** the steps change every time and need judgment rather than recall; the step can be error-proofed in the tool instead (see poka-yoke); or the list would only repeat steps nobody ever misses.

## Diagnostic questions
- [blocking] Which steps, if skipped, cause real harm (money, a missed deadline, an upset customer)? → unlocks: killer items
- [nice-to-have] Are these steps done by experienced staff from memory? → default: yes; DO-CONFIRM recommended
- [nice-to-have] Where is the natural pause point in the work? → default: before the output leaves the actor

## How to apply
1. List candidate items from the step table: each `step` for the `actor` in scope, plus any step with `rework` above zero or a ⚑ flag.
2. Keep only killer items: steps that are easy to skip and costly when skipped. Drop anything people never miss. Aim for about 5 to 9 items.
3. Choose the type by experience level. Experienced staff doing routine work get DO-CONFIRM. New staff or rare procedures get READ-DO.
4. Place the checklist at a pause point, such as just before a handoff or before the output leaves the actor. Name who runs it.
5. Plan a short trial (for example two weeks of real use), then ask users what was missing, confusing or ignored, and revise.
6. Evidence note: in a study of the WHO Surgical Safety Checklist at 8 hospitals around the world, the death rate fell from 1.5% to 0.8% and inpatient complications fell from 11.0% to 7.0% after the checklist was introduced (Haynes et al., 2009). This was a before-and-after study in surgery, not an office setting; treat it as evidence that short checklists at pause points can work, not as a predicted effect size.

## Typical recommendations
- A DO-CONFIRM checklist at the handoff between roles, run by the person handing off (ladder tier 1)
- A READ-DO checklist for rare procedures such as year-end close or onboarding a new client (ladder tier 1)
- Embed the checklist in the tool's task or project template so it appears automatically (ladder tier 2)

## Failure modes
- Long checklists that turn into box-ticking; people stop reading them.
- Listing obvious steps nobody skips, which hides the ones that matter.
- Never testing or updating the list, so it drifts from how the work is really done.
- Adding a checklist where the tool could prevent the error outright.

## Citations
- Gawande, A., *The Checklist Manifesto: How to Get Things Right* (2009). Metropolitan Books (Henry Holt), New York. [book] https://search.worldcat.org/title/checklist-manifesto-how-to-get-things-right/oclc/465378674
- Haynes, A.B., Weiser, T.G., Berry, W.R., et al., "A Surgical Safety Checklist to Reduce Morbidity and Mortality in a Global Population," *New England Journal of Medicine* 360(5):491–499 (2009). Massachusetts Medical Society. [peer-reviewed] https://doi.org/10.1056/NEJMsa0810119

---
id: sipoc-raci
name: SIPOC and RACI
category: scope
triggers:
  - unclear start or end of the process
  - steps with no clear owner
  - the same step has more than one approver
  - user cannot name who receives the output
blocking_inputs: [actor, trigger, output]
version: 1.0
---
# SIPOC and RACI

## What it is
SIPOC (Suppliers, Inputs, Process, Outputs, Customers) frames a process on one page.
It shows the process at a high level, in about 5 to 7 core steps, with who feeds it and who receives what it makes.
RACI (Responsible, Accountable, Consulted, Informed) assigns a role to each person or team for each step.
Responsible does the work. Accountable owns the result. Consulted gives input before. Informed is told after.
Each step has exactly one Accountable.

## When to apply
**Apply when:** nobody can say where the process starts or ends, a step has no clear owner, a step needs sign-off from more than one person, or work stalls while people wait to be asked their opinion.
**Do not apply when:** the scope and owners are already clear and agreed, and the problem is speed or errors inside a known step (use a bottleneck or error-proofing framework instead).

## Diagnostic questions
- [blocking] Who is accountable for the final output, the one role that answers for it if it goes wrong? → unlocks: ownership findings
- [blocking] Who supplies the inputs to the process, and in what form do they arrive (email, form, paper, phone)? → unlocks: input-quality findings
- [nice-to-have] Who needs to be told when the work is done? → default: requester only

## How to apply
1. Build one SIPOC row from the step table. Suppliers and inputs come from the first steps' `trigger`. Outputs and customers come from the last steps' `output` and `handoff_to`.
2. Collapse the process into 5 to 7 core steps. If you cannot name the first trigger or the final customer, raise a gap question.
3. Build a RACI grid: steps down the side, roles across the top, one letter per cell.
4. Flag any step with no Accountable or with two or more Accountable.
5. Flag Consulted entries where the step waits on that role's answer (check `time_wait`). Ask whether the input is really needed before the step, or only a notice after it.
6. Flag inputs that arrive incomplete or in mixed formats; they point to a supplier standard to agree.

## Typical recommendations
- Name one owner for each step, for example the office manager owns final sign-off on new-client setup (ladder tier 1)
- Move a role from Consulted to Informed where their input is not needed before the step (ladder tier 1)
- Agree an input standard with suppliers, such as a short list of what a request must include (ladder tier 1)
- Enforce that input standard with required fields in an intake form the business already pays for (ladder tier 2)

## Failure modes
- A SIPOC with 15 or 20 steps; it turns into a detailed map and loses the one-page view
- A RACI where almost everyone is Consulted on everything, which builds in waits
- Documenting roles in a chart without changing who actually does or approves the work
- Naming real people instead of roles, so the chart breaks when someone leaves

## Citations
- American Society for Quality (ASQ), "SIPOC+CM Diagram" (n.d.). ASQ. [standards body] https://asq.org/quality-resources/sipoc
- Project Management Institute, *A Guide to the Project Management Body of Knowledge (PMBOK Guide)*, Sixth Edition (2017), section 9.1.2.2 (responsibility assignment matrix and RACI chart). Project Management Institute. [standards body] https://www.pmi.org/-/media/pmi/documents/public/pdf/pmbok-standards/errata-sheet-qas-6th.pdf?rev=84dd4da9023844deb30bb18fd3e3ebcd
- Project Management Institute, "How to assign RACI roles when AI agents join the team" (n.d.). PMI blog. [practitioner] https://www.pmi.org/blog/stakeholder-management-raci

# Step table schema

Every input (narrative, transcript, SOP, step list, timing data) is normalized into this table before any analysis. One row per step.

| Field | Meaning | Example |
|---|---|---|
| `step_id` | Sequential id. Branches use letters (S3a, S3b) | S4 |
| `step` | Verb-first description | Enter invoice into accounting system |
| `actor` | Role, never a person's name | AP clerk |
| `tool` | System or medium | QuickBooks, email, paper |
| `trigger` | What starts the step | Invoice arrives by email |
| `output` | What the step produces | Draft bill |
| `handoff_to` | Next actor, if it changes | Office manager |
| `time_touch` | Hands-on time per occurrence | 6 min |
| `time_wait` | Time waiting before this step starts | ~2 days |
| `volume` | Occurrences per period | 40/week |
| `rework` | How often the step is redone or corrected | 1 in 10 |
| `decision` | Y if the step branches | N |
| `manual_by_choice` | Y if the owner wants to keep doing it by hand | N |
| `src` | Source tag per field (see below) | |

## Source tags

Tag every value:

- `stated`: the user said it or it is in their document, including their own approximations ("about 3 hours"). Shown plain.
- `~estimated`: derived by you from context or calculation, not given by the user. Shown with `~` prefix (`~2 days`).
- `?missing`: not known. Shown as `?`. Becomes a gap question.

## Rules

1. Never invent a value. Unknown is `?`, not a guess.
2. Replace names of real people, clients and employers with roles or generic labels.
3. Keep the user's units; convert only for math, and show the conversion.
4. `manual_by_choice = Y` only when the user says they enjoy, value, or want to keep the step. Ask if unclear; default is N. Split a step so Y covers only the part the owner keeps (e.g. bake = N, decorate = Y).
5. Split a step when it has two actors or two tools. Merge only when the user describes it as one action.
6. Any step that moves money, contacts customers, or adds a customer to a list that will be contacted is flagged `⚑` in the `step` column.

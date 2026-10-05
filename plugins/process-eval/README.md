# process-eval

A universal skill that evaluates any process (business, ops, IT, personal) against established, citable frameworks. It finds bottlenecks, waste, steps to combine or group, and candidates for checklists or error-proofing. Every recommendation traces back to (a) evidence in the process itself and (b) a named framework with a primary source. The core is brand-neutral; branded methods can plug in later as optional profiles.

## Install

Claude Code:

```
/plugin marketplace add offsetkeyz/skills
/plugin install process-eval@offsetkeyz-skills
```

claude.ai (upload as a skill): build a `.skill` bundle from the repo root, then upload `dist/process-eval.skill`.

```
mkdir -p dist && cd plugins/process-eval/skills && zip -r ../../../dist/process-eval.skill process-eval
```

## How it works

```
Input (any form: narrative, transcript, SOP, step list, timing data)
  1. Normalize   → step table (schema.md); every field tagged stated / estimated / missing
  2. Route       → match step-table patterns to framework triggers; load only matched files
  3. Gap check   → questions from matched frameworks + schema gaps, tiered BLOCKING / NICE-TO-HAVE
  ⏸ GATE         → return step table + tiered questions. No findings in this pass.
  4. Answers     → update table. If any BLOCKING gap remains, re-ask only those.
  5. Analyze     → apply each matched framework → findings with evidence + citation
  6. Rank        → fix list ordered by impact ÷ effort, ties broken by fix-ladder tier
  → Report: Findings (A) + Ranked fix list (B)
  → On request only: checklists, ECRS grouping proposals, SOP draft, current/future-state Mermaid map
```

The gate:

- **Blocking** questions must be answered (or the framework removed from scope) before any findings are produced.
- **Nice-to-have** questions each carry a default. If unanswered, the default is listed under Assumptions and dependent findings are marked Low confidence.
- At most 8 questions per round, blocking first. Pass 1 always runs, even when the input already answers everything.

## Frameworks

Citations as they appear in each file's Citations section. Every one has a verification URL in the file.

| File | Category | Sources (evidence type) |
|---|---|---|
| `toc.md` | bottleneck | Goldratt & Cox, *The Goal* (1984) [book]; Goldratt, *What Is This Thing Called Theory of Constraints and How Should It Be Implemented?* (1990) [book] |
| `littles-law.md` | bottleneck | Little, "A Proof for the Queuing Formula: L = λW," *Operations Research* 9(3):383–387 (1961) [peer-reviewed] |
| `vsm.md` | waste | Rother & Shook, *Learning to See* (Lean Enterprise Institute, 1999) [book] |
| `lean-wastes.md` | waste | Ohno, *Toyota Production System* (English ed. 1988) [book]; Liker, *The Toyota Way* (2004), for the eighth waste [book] |
| `ecrs.md` | simplify | Kanawaty (ed.), *Introduction to Work Study*, 4th rev. ed. (ILO, 1992) [standards body]; Bârsan & Codrea, "Lean university: applying the ECRS method to improve an administrative process," *MATEC Web of Conferences* 290 (2019) [peer-reviewed] |
| `batching.md` | simplify | Reinertsen, *The Principles of Product Development Flow* (2009) [book] |
| `poka-yoke.md` | error-proof | Shingo, *Zero Quality Control: Source Inspection and the Poka-yoke System* (1986) [book] |
| `checklists.md` | checklist | Gawande, *The Checklist Manifesto* (2009) [book]; Haynes et al., *NEJM* 360(5):491–499 (2009) [peer-reviewed] |
| `sipoc-raci.md` | scope | ASQ, "SIPOC+CM Diagram" (n.d.) [standards body]; PMI, *PMBOK Guide*, 6th ed. (2017), §9.1.2.2 [standards body]; PMI blog, "How to assign RACI roles when AI agents join the team" (n.d.) [practitioner] |

## Example

Input (`evals/inputs/bakery-orders.md`):

> Transcript excerpt, owner of a 4-person bakery:
>
> "Custom cake orders come in by phone, Instagram DMs, and walk-in. I write them on a paper pad. Maybe 25 a week. Sometimes we forget to ask about allergies or the pickup time and have to call back, probably 3 or 4 times a week. Last month we wrote the wrong date on one and the customer showed up and there was no cake. Decorating is my favorite part, I don't want any of that automated. I just want orders to stop slipping."

Pass 1 output (abbreviated):

```markdown
### Step table (draft)
? = missing · ~ = estimated · ⚑ = moves money or contacts customers

| # | Step | Actor | Tool | Touch | Wait | Volume | Rework | Manual by choice |
|---|---|---|---|---|---|---|---|---|
| S1 | ⚑ Take custom cake order | ~Owner | Phone, Instagram DM, walk-in | ? | — | ~25/wk | ? | N |
| S2 | Write order on paper pad | Owner | Paper pad | ? | — | ~25/wk | ~3–4/wk missing allergy or pickup time; 1 wrong date last month | N |
| S3 | ⚑ Call customer back for missing details | ? | Phone | ? | ? | ~3–4/wk | — | N |
| S4 | Decorate cake | Owner | ? | ? | ? | ~25/wk | ? | Y |
| S5 | ⚑ Hand cake to customer at pickup | ? | In store | ? | ? | ~25/wk | 1 no-cake pickup last month | N |

Note: S2 records customer allergy details (health information). Keep order records where only staff can see them.

### Frameworks in scope
Poka-yoke, Checklists (rework at S2 drives call-backs at S3; a missed date caused a failed pickup at S5)

### Questions
#### Blocking (needed before the report)
1. [Poka-yoke] Are allergies, pickup time and date missed while taking the order (S1–S2), or written down but misread later? → unlocks: error-proofing target
2. [Checklists] Besides allergies, pickup time and date, which order details cause real trouble if missed (size, flavor, wording, deposit)? → unlocks: killer items
3. [Timing] Roughly how long does taking an order (S1–S2) and a call-back (S3) take? → unlocks: hours/week impact

#### Nice-to-have (assumed if unanswered)
4. [Checklists] Who takes orders, and do they work from memory? → assumed if unanswered: experienced staff from memory; DO-CONFIRM checklist

Kept manual: S4 decorating (manual_by_choice = Y). No automation will be proposed for it.
```

Pass 2 runs only after the blocking questions are answered.

## Adding a framework

1. Copy an existing file in `skills/process-eval/references/frameworks/` as the skeleton. Keep the frontmatter (`id`, `name`, `category`, `triggers`, `blocking_inputs`, `version`) and the seven sections in order: What it is, When to apply, Diagnostic questions, How to apply, Typical recommendations, Failure modes, Citations.
2. Add the file id to `FRAMEWORKS` in `tests/test_structure.py`.
3. Add a routing row to the table in `skills/process-eval/SKILL.md`.
4. Add an eval case (input file plus entry in `evals/evals.json`).
5. Run `pytest plugins/process-eval/tests`.

See `CONTRIBUTING.md` for the source and paraphrase rules.

## Fix ladder

Fixes are ranked by impact ÷ effort, with ties going to the simplest tier: remove or change the process, then configure tools already paid for, then standard automation, then AI only where the simpler tiers cannot cope. This ladder is a house heuristic, not a cited framework. Teams can swap or reorder it, and the report should state the replacement when they do.

## License

MIT. See `LICENSE`.

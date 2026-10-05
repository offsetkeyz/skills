# process-eval: Design Spec

- **Date:** 2026-10-05
- **Status:** Draft, pending author review
- **Location:** `plugins/process-eval/skills/process-eval/` (this marketplace)

## 1. Purpose

A universal skill that evaluates any process (business, ops, IT, personal) against established, citable frameworks. It finds bottlenecks, waste, steps to combine or group, and candidates for checklists or error-proofing. Every recommendation traces back to (a) evidence in the process itself and (b) a named framework with a primary source.

**Audience:** work use, consulting use, and public community release. The core stays brand-neutral. Branded methods (e.g. SeRKeT) plug in later as optional profiles.

**Non-goals (v1):**
- No deterministic calc script. The model does the math, and number-based findings carry a "verify" note.
- No DMAIC/SPC, FMEA, or BPMN notation. Add these when a real case needs them.
- No tool or vendor recommendations beyond naming a tool category and a cost estimate when the user asks.

## 2. Workflow

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

### Gate rule (tiered)
- **Blocking:** a matched framework cannot produce *any* finding without this answer (e.g. no wait-time data means no bottleneck claim). The report is not produced until every blocking question is answered or the user removes that framework from scope.
- **Nice-to-have:** each one ships with a stated default assumption. If it goes unanswered, the assumption appears in the report's Assumptions section and the findings that depend on it are marked Low confidence.
- At most 8 questions per round, ordered by what each one unlocks.
- If the input already answers every blocking question, pass 1 still runs. It shows the step table and any nice-to-haves, and the user confirms before pass 2.

## 3. Step-table schema (`references/schema.md`)

| Field | Meaning |
|---|---|
| `step_id` | Sequential id (S1, S2…); decision branches use S3a/S3b |
| `step` | Verb-first description |
| `actor` | Role, not person name |
| `tool` | System or medium used (email, spreadsheet, paper…) |
| `trigger` | What starts the step |
| `output` | What the step produces |
| `handoff_to` | Next actor, if one changes |
| `time_touch` | Hands-on time per occurrence |
| `time_wait` | Time waiting before this step starts |
| `volume` | Occurrences per period |
| `rework` | How often the step is redone or corrected |
| `decision` | Y if the step branches |
| `manual_by_choice` | Y if the owner wants to keep it manual. **Excluded from automation recommendations.** |
| `src` | Per-field tag: `stated` · `~estimated` · `?missing` |

Rules: never invent values. A missing field becomes a gap question. Names of real people, clients, or employers are replaced with roles.

## 4. Routing triggers

Triggers live in each framework file's frontmatter. The v1 defaults:

| Pattern in step table | Frameworks |
|---|---|
| `time_wait` ≥ 3× `time_touch`, or a queue before one actor | ToC, Little's Law, VSM |
| Same actor + adjacent steps + same tool | ECRS (combine), batching |
| ≥ 3 handoffs between roles | VSM, Lean wastes (transport/motion), SIPOC/RACI |
| `rework` > 0, or repeated verification steps | Poka-yoke, checklists, Lean wastes (defects) |
| Fixed sequence, human-run, costly if a step is missed | Checklists (READ-DO / DO-CONFIRM) |
| Unclear start/end, owner, or customer | SIPOC/RACI |
| Large batches before a hand-off | Batching, Little's Law |
| `manual_by_choice = Y` | **Exclusion:** no automation; a checklist or SOP may still be suggested |

If nothing matches, the skill says so and does not stretch a framework to fit.

## 5. Framework files (`references/frameworks/*.md`)

### Contract
```markdown
---
id: toc
name: Theory of Constraints
category: bottleneck   # bottleneck | waste | simplify | error-proof | scope | checklist
triggers: [...]        # plain-language patterns, matched against step table
blocking_inputs: [time_touch, time_wait, volume]
version: 1.0
---
## What it is            ≤5 lines, paraphrased
## When to apply / not
## Diagnostic questions  each tagged blocking | nice-to-have, with a default assumption for nice-to-haves
## How to apply          steps against the step table
## Typical recommendations
## Failure modes
## Citations             primary first; evidence type labeled
```

### v1 set

| File | Category | Primary source (verify before shipping) |
|---|---|---|
| `toc.md` | bottleneck | Goldratt & Cox, *The Goal* (1984): Five Focusing Steps |
| `littles-law.md` | bottleneck | Little, "A Proof for the Queuing Formula: L = λW," *Operations Research* 9(3), 1961 |
| `vsm.md` | waste/flow | Rother & Shook, *Learning to See* (Lean Enterprise Institute, 1999) |
| `lean-wastes.md` | waste | Ohno, *Toyota Production System* (English ed. 1988); 8th waste via Liker, *The Toyota Way* (2004) |
| `ecrs.md` | simplify/group | ILO, *Introduction to Work Study* (Kanawaty, ed.) |
| `batching.md` | simplify/group | Reinertsen, *The Principles of Product Development Flow* (2009) |
| `poka-yoke.md` | error-proof | Shingo, *Zero Quality Control: Source Inspection and the Poka-yoke System* (1986) |
| `checklists.md` | checklist | Gawande, *The Checklist Manifesto* (2009); Haynes et al., *NEJM* 360:491–499 (2009) |
| `sipoc-raci.md` | scope/ownership | ASQ (SIPOC); PMI, *PMBOK Guide* (responsibility assignment matrix) |

### Citation policy
- Paraphrase only. Quotes, if any, stay under 15 words. Required for public release.
- Label each source's evidence type: `book` · `peer-reviewed` · `standards body` · `practitioner`.
- Each citation is verified against a publisher, DOI, or standards-body page before the file merges.
- The **fix ladder** (remove/change process > configure existing tools > standard automation > AI) is labeled a **house heuristic**, not a cited framework. It is configurable.

## 6. Output formats (`references/report-template.md`)

### Pass 1
```markdown
## Step table (draft)        ? = missing, ~ = estimated
## Questions
### Blocking
1. [Framework] Question → unlocks: <finding type>
### Nice-to-have
4. [Framework] Question → assumed if unanswered: <default>
```

### Pass 2
```markdown
## Summary        top constraint, top 3 fixes, est. hours/week back (3–5 lines)
## Findings
### F1 · <title>                                   [High | Medium | Low]
- Evidence: step rows + values
- Framework: <name(s)>
- Why it matters: <mechanism; any math shown>
- Recommendation
- Source: <short cite>
## Fix list (ranked)
| # | Fix | Finding | Ladder tier | Impact (hrs/wk) | Effort (hrs) | Tool + $/mo | Maint. risk |
## Assumptions    unanswered nice-to-haves and their effect
## Kept manual    manual_by_choice steps, untouched
## Sources        full citations
```

- **Confidence:** High = all evidence `stated`. Medium = any `~estimated`. Low = rests on an assumption.
- **Ranking:** impact ÷ effort, ties broken by ladder tier (lower tier wins).
- **Safety:** any step that moves money or contacts customers keeps human approval in every recommendation.

## 7. Repo layout

```
plugins/process-eval/
  .claude-plugin/plugin.json
  skills/process-eval/
    SKILL.md
    references/
      schema.md
      question-bank.md        cross-framework gap questions (schema gaps)
      report-template.md
      fix-ladder.md           house heuristic, configurable
      frameworks/  toc.md littles-law.md vsm.md lean-wastes.md ecrs.md
                   batching.md poka-yoke.md checklists.md sipoc-raci.md
  evals/                      sample inputs + expected outcomes
  README.md                   usage, example run, how to add a framework
  CONTRIBUTING.md             new framework = 1 file + 1 eval + primary source
```
The marketplace entry is added to `.claude-plugin/marketplace.json`, and the root README plugin table is updated.

**License (proposed):** MIT for structure/instructions, CC-BY-4.0 for framework summaries. To be confirmed by the author before public release.

## 8. Testing

Evals are run with skill-creator. Each case lists expected framework triggers plus findings that must and must not appear.

| Case | Input | Should trigger | Trap |
|---|---|---|---|
| AP invoice approval | narrative | ToC, Little's Law | approval queue is the constraint |
| Client onboarding (accounting firm) | SOP doc | ECRS, SIPOC/RACI | duplicate data entry → combine |
| Bakery custom orders | transcript | checklists, poka-yoke | owner keeps cake decorating manual |
| Patch management | step table with timings | VSM, batching | batch size drives wait |
| Appointment reminders | thin input | none yet | must stop at gate with blocking questions |
| Already-lean process | full data | possibly none | must report "nothing significant" |

**Pass/fail checks:**
1. Gate respected (no findings in pass 1; no report with an open blocking gap)
2. Every finding cites ≥1 step row and ≥1 framework source
3. No automation recommended for a `manual_by_choice` step
4. No citation outside the framework files' verified source lists
5. Fix ladder applied in ranking ties
6. ≤8 questions per round
7. Example content uses roles and generic orgs only (no real names)

## 9. Open items
- Confirm license choice before flipping marketplace visibility / announcing.
- v1.1 candidates: `scripts/flow_metrics.py` (optional deterministic math), `profiles/serket.md` lens, FMEA-lite.

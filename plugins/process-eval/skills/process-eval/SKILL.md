---
name: process-eval
description: Evaluate any business or operational process against established, cited frameworks (Theory of Constraints, Little's Law, Value Stream Mapping, Lean wastes, ECRS, batch size, poka-yoke, checklists, SIPOC/RACI) to find bottlenecks, waste, steps to combine, and checklist or error-proofing candidates. Use when someone describes how work gets done (notes, transcript, SOP, step list, or timing data) and wants it improved, sped up, simplified, or checked. Always asks clarifying questions before reporting.
---

# Process Evaluation

Turn any description of a process into a step table, ask the questions that matter, then report findings that are backed by evidence from the process and by a cited framework. No finding without both.

## Workflow

### Pass 1: Map and ask (always runs, never contains findings)

1. **Normalize.** Read `references/schema.md`. Build the step table from whatever the user gave. Tag every value stated, ~estimated or ?missing. Never invent values. Replace real names with roles.
2. **Route.** Compare the table to the triggers below. Read only the matched framework files.
3. **Gap check.** Collect questions from the matched frameworks' "Diagnostic questions" and from `references/question-bank.md` for `?` fields. Tag each one blocking or nice-to-have.
4. **Stop.** Output using the Pass 1 format in `references/report-template.md`: step table, frameworks in scope, questions. Max 8 questions per round, blocking first.

### Gate

- Do not produce findings while any blocking question is open. If the user answers some, update the table and re-ask only the remaining blocking ones.
- The user can remove a framework from scope instead of answering its blocking question.
- Nice-to-have questions carry a stated default. If unanswered, use the default and list it under Assumptions.
- If the input already answers every blocking question, still show Pass 1 and get a go-ahead.

### Pass 2: Analyze and rank

5. **Analyze.** Apply each matched framework's "How to apply" to the table. Each finding names its evidence rows, framework, mechanism (show any math with units), recommendation and source.
6. **Rank.** Read `references/fix-ladder.md`. Order fixes by impact ÷ effort; ties go to the lower ladder tier.
7. **Report.** Use the Pass 2 format in `references/report-template.md`.

### On request only

Checklists (use checklists.md), ECRS grouping proposals, SOP drafts, current/future-state Mermaid maps.

## Routing

| Pattern in the step table | Read |
|---|---|
| time_wait ≥ 3× time_touch at a step, or a queue before one actor | `references/frameworks/toc.md`, `references/frameworks/littles-law.md`, `references/frameworks/vsm.md` |
| Backlog counts or end-to-end time questions | `references/frameworks/littles-law.md` |
| 3+ handoffs between roles | `references/frameworks/vsm.md`, `references/frameworks/lean-wastes.md`, `references/frameworks/sipoc-raci.md` |
| Re-keying, copy/move-only steps, unused outputs | `references/frameworks/lean-wastes.md` |
| Same actor + adjacent steps + same tool | `references/frameworks/ecrs.md` |
| Work processed weekly/monthly, or waits for a batch | `references/frameworks/batching.md` |
| rework > 0, repeated checking | `references/frameworks/poka-yoke.md`, `references/frameworks/checklists.md` |
| Fixed human sequence where a miss is costly | `references/frameworks/checklists.md` |
| Unclear start/end, owner, or customer | `references/frameworks/sipoc-raci.md` |

Each framework's frontmatter `triggers` list adds detail. If nothing matches, say so plainly. Do not stretch a framework to fit.

## Hard rules

- **Evidence + citation.** Every finding cites at least one step row and one framework source from that framework's Citations section. Never cite anything else.
- **manual_by_choice.** Never recommend automating (ladder tiers 2–4) a step marked manual_by_choice = Y. A checklist or SOP is allowed. List these under "Kept manual".
- **Human approval.** Any step that moves money or contacts customers (⚑) keeps human approval in every recommendation.
- **Confidence.** High = all evidence stated; Medium = any ~estimated; Low = rests on an assumption.
- **No inflation.** If the process is already lean, say so. A short report is a valid report.
- **Paraphrase sources.** No quotes of 15+ words.
- **Privacy.** Roles, not names. Flag confidential data (financial, legal, health) if it appears in the input.

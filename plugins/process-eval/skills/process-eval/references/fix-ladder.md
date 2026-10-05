# Fix ladder (house heuristic)

This is a house heuristic, not a cited framework. It reflects a common practitioner view that the cheapest durable fix is usually the simplest one. Teams may swap or reorder it; if they do, state the replacement in the report.

Prefer the lowest tier that solves the finding:

1. **Remove or change the process.** Delete the step, change who does it, change the order, add a checklist.
2. **Configure existing tools.** Use features already paid for (templates, rules, required fields, built-in reminders).
3. **Standard automation.** Forms, scheduling, integrations (Zapier, Make, n8n), CRM/POS/ticketing rules.
4. **AI.** Only when tiers 1–3 cannot handle the variability (unstructured text, judgment-heavy triage). Always with human review.

## Use in ranking

Fixes rank by impact ÷ effort. On a tie, the lower tier wins.

## Hard rules

- Never recommend tiers 2–4 for a `manual_by_choice = Y` step. Tier 1 (checklist, SOP) is allowed.
- Any fix touching a ⚑ step (moves money or contacts customers) keeps a human approval point.

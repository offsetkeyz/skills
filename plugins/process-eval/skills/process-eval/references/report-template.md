# Report templates

## Pass 1: Step table + questions

No findings in this pass.

```markdown
### Step table (draft)
? = missing · ~ = estimated · ⚑ = moves money or contacts customers

| # | Step | Actor | Tool | Touch | Wait | Volume | Rework | Manual by choice |
|---|---|---|---|---|---|---|---|---|
| S1 | Receive invoice by email | AP clerk | Email | 1 min | — | 40/wk | ? | N |

### Frameworks in scope
Theory of Constraints, Little's Law (wait before S4 is large vs. touch time)

### Questions
#### Blocking (needed before the report)
1. [Theory of Constraints] How long does an invoice wait before S4? → unlocks: bottleneck finding

#### Nice-to-have (assumed if unanswered)
2. [Checklists] Has a missed S6 ever caused a late payment? → assumed if unanswered: no
```

Max 8 questions, one question mark per item. Order by what each unlocks (blocking first).

## Pass 2: Findings + fix list

```markdown
### Summary
3–5 lines: the main constraint, top 3 fixes, estimated hours/week back.

### Findings
#### F1 · Approval queue is the constraint            [High]
- **Evidence:** S3→S4 wait ~2 days vs. 10 min touch; 40/week
- **Framework:** Theory of Constraints; Little's Law
- **Why it matters:** ~40/wk × 0.4 wk ≈ 16 invoices waiting at any time
- **Recommendation:** …
- **Source:** Goldratt & Cox (1984); Little (1961)

### Fix list
| # | Fix | Finding | Ladder tier | Impact (hrs/wk) | Effort (hrs) | Tool + $/mo | Maint. risk |
|---|---|---|---|---|---|---|---|

Prefix Impact, Effort and $/mo with ~ unless the user stated them. Say under the table which measure drives the ranking (hours, lead time, or risk avoided).

### Assumptions
Unanswered nice-to-have questions, the assumption used, and which findings depend on it.

### Kept manual
Steps with manual_by_choice = Y. Not automated. Any checklist or SOP suggestion listed here.

### Sources
Full citations for every framework used, copied from the framework files.
```

## Confidence

- **High:** every value in the evidence is `stated`.
- **Medium:** at least one `~estimated` value.
- **Low:** depends on an unanswered nice-to-have assumption.

## Math

Show every calculation inline with units. Add "(verify)" after any number derived from 2+ estimated values.

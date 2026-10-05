# Question bank: schema gaps

Framework-specific questions live in each framework file. These cover gaps in the step table itself. Pick only the ones whose field is `?` and that a matched framework needs. Rephrase to name the actual step ("How long does an invoice wait before the office manager approves it?").

Format: `[tier] question → unlocks: <finding>` or `→ default: <assumption if unanswered>`.

## Scope
- [blocking] Where does this process start and end (first trigger, final output)? → unlocks: any finding; defines the map boundary
- [blocking] Who receives the final output, and what do they need from it? → unlocks: value vs. waste judgments

## Timing
- [blocking] Roughly how long does each step take hands-on? → unlocks: effort and flow-efficiency findings
- [blocking] Where does work sit waiting, and for how long? → unlocks: bottleneck findings
- [blocking] How often does this happen (per day, week, month)? → unlocks: hours/week impact and queue math

## People and tools
- [nice-to-have] Which tools or systems are used at each step? → default: tool unknown; no configuration fixes proposed for that step
- [nice-to-have] Do any steps hand work to another person? → default: same actor as previous step

## Quality
- [nice-to-have] Which steps get redone, corrected, or chased up? → default: no rework; error-proofing frameworks not applied
- [nice-to-have] Has a missed step ever caused a real problem (money, customer, compliance)? → default: no; checklist findings rated Medium

## Preferences
- [nice-to-have] Are there steps you enjoy or want to keep doing by hand? → default: none flagged; ask again before recommending automation

# Output Skill Template

Use this to package the person's profile as their own "write like me" skill. The folder name defaults to `my-writing-style`; use another if they prefer.

Contents: folder layout, SKILL.md template, file notes, sharing warning.

## Folder layout

```
my-writing-style/
├── SKILL.md
├── references/
│   ├── voice-profile.md     (the filled profile template)
│   ├── anti-patterns.md     (generic AI tells + person-specific trims)
│   └── feedback-log.md      (empty log, format below)
└── samples/
    ├── raw-01-<slug>.md     (verbatim sample + short evaluation notes)
    └── approved-01-<slug>.md (added later, drafts they approved)
```

## SKILL.md template

Fill the bracketed parts. Keep the description pushy so the skill triggers on any publishable writing request.

```markdown
---
name: my-writing-style
description: Write blogs, posts, articles, newsletters, and other first-person drafts in <name>'s voice (<two or three voice words>). Use this skill whenever <name> asks for a draft they'll publish or send under their own name, even if they don't mention style or voice. Also use it when they paste their own edits to a draft, want something rewritten to sound more like them, or ask to update their voice profile.
---

# My Writing Style (<name>)

<One paragraph on the goal: drafts should read like <name> talking to <audience>, so edits stay light.>

## Workflow
1. Read references/voice-profile.md and references/anti-patterns.md. Skim references/feedback-log.md, since recent corrections override everything else.
2. Open the one or two samples closest to the requested format. Match rhythm, not content.
3. Find the single idea. State it as a contrast or a clear claim before drafting. If there is none, ask for one real moment or opinion. Do not invent anecdotes.
4. Draft following the structure rules below.
5. Self-audit against the checklist, then fix.
6. Deliver the draft with a short calibration note: what you leaned on, facts needing confirmation, one tone question. Invite edits.
7. When they edit a draft, diff it against yours, extract the pattern behind each change, and append it to references/feedback-log.md. Offer to promote patterns seen twice into the profile.

## Structure rules
<Per-format rules from the profile: opening, length, list vs. prose, closing, humor level.>

## Content guardrails
<From the profile: what stays out, what gets flagged, no invented facts.>

## Pre-delivery checklist
<Checklist drawn from the profile: opening, concrete detail, signature move, filler removed, key nouns not repeated, AI tells scrubbed, register matches format.>
```

## feedback-log.md format

```markdown
# Feedback Log
Newest first. After each edited draft record the change, the pattern behind it, and whether to promote it. Patterns confirmed twice get promoted to voice-profile.md.

### YYYY-MM-DD: <draft title>
- Change: <before -> after, short>
- Pattern: <underlying preference>
- Promote? yes / not yet
```

## Packaging

1. Validate with the skill-creator `quick_validate` script when available.
2. Package with its `package_skill` script and deliver the `.skill` file, or propose it with a skill-proposal tool if one exists.
3. Tell the person it hasn't been test-run against a real draft yet, and run step 7 of the main workflow next.

## Sharing warning

The personal skill contains the person's raw writing. Before they publish or share it, scan the samples for employer-internal details, names of colleagues or customers, and private anecdotes. Offer to produce a shareable version that includes only the profile and anti-patterns, with samples removed or redacted.

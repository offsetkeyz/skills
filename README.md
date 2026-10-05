# offsetkeyz-skills

Claude Code plugin marketplace of personal skills.

## Install

```
/plugin marketplace add offsetkeyz/skills
/plugin install find-your-voice@offsetkeyz-skills
/plugin install process-eval@offsetkeyz-skills
```

Local testing: `/plugin marketplace add ./` from this folder.

## Plugins

| Plugin | Description |
|---|---|
| find-your-voice | Discover your writing voice, package it as a "write like me" skill |
| process-eval | Evaluate any process against cited frameworks (ToC, Lean, ECRS, checklists). Questions first, then a ranked fix list |

## Adding a skill

1. `mkdir -p plugins/<name>/.claude-plugin plugins/<name>/skills/<name>`
2. Add `plugins/<name>/skills/<name>/SKILL.md`
3. Add `plugins/<name>/.claude-plugin/plugin.json`
4. Add an entry to `.claude-plugin/marketplace.json`
5. `claude plugin validate .`

## Build a `.skill` bundle (for claude.ai upload)

```
cd plugins/<name>/skills && zip -r ../../../dist/<name>.skill <name>
```

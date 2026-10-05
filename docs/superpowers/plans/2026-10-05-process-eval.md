# process-eval Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the `process-eval` plugin: a universal, two-pass process-evaluation skill that cites established frameworks, added to the `offsetkeyz-skills` marketplace.

**Architecture:** A content-first Agent Skill. `SKILL.md` holds the workflow (normalize → route → gap-check → gate → analyze → rank). `references/` holds the schema, templates, house fix ladder, and one file per framework. A pytest structure suite enforces the framework file contract and repo wiring (TDD for content). skill-creator evals check behavior.

**Tech Stack:** Markdown + YAML frontmatter; Python 3 + pytest + PyYAML (dev-only tests, not shipped in the skill); Claude Code plugin marketplace JSON; skill-creator for evals.

**Spec:** `docs/specs/2026-10-05-process-eval-design.md` (approved 2026-10-05). Read it before starting.

**Branch:** `spec/process-eval` (already exists on origin; continue on it).

**Content rules for every task (apply to all prose you write):**
- Paraphrase. No quote over 15 words from any source, max one quote per source per file.
- Examples use roles ("office manager", "AP clerk") and generic orgs ("a 6-person accounting firm"). No real people, clients or employers.
- Plain English, short sentences, no hype.

---

## File Structure

```
.claude-plugin/marketplace.json                          MODIFY: add plugin entry
README.md                                                MODIFY: plugin table row
plugins/process-eval/
  .claude-plugin/plugin.json                             CREATE: plugin manifest
  LICENSE                                                CREATE: MIT
  README.md                                              CREATE: usage, example run, add-a-framework
  CONTRIBUTING.md                                        CREATE: contribution rules
  requirements-dev.txt                                   CREATE: pytest, pyyaml
  tests/test_structure.py                                CREATE: contract + wiring tests (dev only)
  evals/evals.json                                       CREATE: skill-creator eval cases
  evals/inputs/*.md                                      CREATE: 6 sample process inputs
  skills/process-eval/
    SKILL.md                                             CREATE: workflow + rules
    references/schema.md                                 CREATE: step-table schema
    references/fix-ladder.md                             CREATE: house heuristic
    references/question-bank.md                          CREATE: schema-gap questions
    references/report-template.md                        CREATE: pass 1 + pass 2 formats
    references/frameworks/{toc,littles-law,vsm,lean-wastes,ecrs,batching,poka-yoke,checklists,sipoc-raci}.md
```

Tests live outside `skills/process-eval/` so the `.skill` bundle stays content-only.

---

### Task 1: Dev tooling + structure test suite (all red)

**Files:**
- Create: `plugins/process-eval/requirements-dev.txt`
- Create: `plugins/process-eval/tests/test_structure.py`

- [ ] **Step 1: Create requirements file**

`plugins/process-eval/requirements-dev.txt`:
```
pytest>=8
pyyaml>=6
```

- [ ] **Step 2: Install**

Run: `pip install --break-system-packages -r plugins/process-eval/requirements-dev.txt`
Expected: installs or "Requirement already satisfied".

- [ ] **Step 3: Write the full test suite**

`plugins/process-eval/tests/test_structure.py`:
```python
"""Structure tests for the process-eval plugin.

These enforce the framework file contract and repo wiring from
docs/specs/2026-10-05-process-eval-design.md. They do not judge prose quality;
skill-creator evals do that.
"""
import json
import re
from pathlib import Path

import pytest
import yaml

PLUGIN = Path(__file__).resolve().parents[1]
REPO = PLUGIN.parents[1]
SKILL_DIR = PLUGIN / "skills" / "process-eval"
REFS = SKILL_DIR / "references"
FW_DIR = REFS / "frameworks"

FRAMEWORKS = [
    "toc", "littles-law", "vsm", "lean-wastes", "ecrs",
    "batching", "poka-yoke", "checklists", "sipoc-raci",
]
CATEGORIES = {"bottleneck", "waste", "simplify", "error-proof", "scope", "checklist"}
FW_SECTIONS = [
    "## What it is",
    "## When to apply",
    "## Diagnostic questions",
    "## How to apply",
    "## Typical recommendations",
    "## Failure modes",
    "## Citations",
]
EVIDENCE_TAGS = ("[book]", "[peer-reviewed]", "[standards body]", "[practitioner]")
SCHEMA_FIELDS = [
    "step_id", "step", "actor", "tool", "trigger", "output", "handoff_to",
    "time_touch", "time_wait", "volume", "rework", "decision",
    "manual_by_choice", "src",
]
REFERENCE_FILES = ["schema.md", "fix-ladder.md", "question-bank.md", "report-template.md"]


def split_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    assert m, f"{path.name}: missing YAML frontmatter"
    return yaml.safe_load(m.group(1)), m.group(2)


def section_body(body: str, heading: str) -> str:
    """Text between `heading` and the next '## ' heading."""
    start = body.index(heading) + len(heading)
    nxt = body.find("\n## ", start)
    return body[start:] if nxt == -1 else body[start:nxt]


def bullets(text: str):
    return [ln.strip() for ln in text.splitlines() if ln.strip().startswith("- ")]


def long_quotes(text: str, limit: int = 15):
    quotes = re.findall(r"[\"“]([^\"”]+)[\"”]", text)
    return [q for q in quotes if len(q.split()) >= limit]


# ---------- repo wiring ----------

def test_plugin_manifest():
    data = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text())
    assert data["name"] == "process-eval"
    assert re.match(r"^\d+\.\d+\.\d+$", data["version"])
    assert data["license"] == "MIT"
    assert len(data["description"]) > 40


def test_marketplace_lists_plugin():
    data = json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text())
    entry = next(p for p in data["plugins"] if p["name"] == "process-eval")
    assert entry["source"] == "./plugins/process-eval"
    plugin = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text())
    assert entry["version"] == plugin["version"]


def test_license_is_mit():
    assert "MIT License" in (PLUGIN / "LICENSE").read_text()


def test_root_readme_lists_plugin():
    assert "| process-eval |" in (REPO / "README.md").read_text()


def test_plugin_docs_exist():
    readme = (PLUGIN / "README.md").read_text()
    for needle in ("Install", "How it works", "Adding a framework"):
        assert needle in readme, f"plugin README missing '{needle}'"
    assert (PLUGIN / "CONTRIBUTING.md").exists()


# ---------- SKILL.md ----------

def test_skill_frontmatter():
    fm, body = split_frontmatter(SKILL_DIR / "SKILL.md")
    assert fm["name"] == "process-eval"
    assert 50 <= len(fm["description"]) <= 1024
    assert "process" in fm["description"].lower()
    assert "<" not in fm["description"] and ">" not in fm["description"]


def test_skill_points_to_every_reference():
    _, body = split_frontmatter(SKILL_DIR / "SKILL.md")
    for f in REFERENCE_FILES:
        assert f"references/{f}" in body, f"SKILL.md never references {f}"
    for fid in FRAMEWORKS:
        assert f"frameworks/{fid}.md" in body, f"SKILL.md routing table missing {fid}"


def test_skill_states_gate_and_exclusion_rules():
    text = (SKILL_DIR / "SKILL.md").read_text().lower()
    for needle in ("blocking", "nice-to-have", "manual_by_choice", "human approval", "8 questions"):
        assert needle in text, f"SKILL.md missing rule keyword '{needle}'"


def test_skill_md_under_500_lines():
    assert len((SKILL_DIR / "SKILL.md").read_text().splitlines()) < 500


# ---------- shared references ----------

def test_schema_lists_all_fields():
    text = (REFS / "schema.md").read_text()
    for f in SCHEMA_FIELDS:
        assert f"`{f}`" in text, f"schema.md missing `{f}`"
    for tag in ("stated", "~estimated", "?missing"):
        assert tag in text


def test_fix_ladder_order_and_label():
    text = (REFS / "fix-ladder.md").read_text()
    assert "house heuristic" in text.lower()
    tiers = ["Remove or change the process", "Configure existing tools",
             "Standard automation", "AI"]
    positions = [text.index(t) for t in tiers]
    assert positions == sorted(positions), "fix ladder tiers out of order"


def test_report_template_sections():
    text = (REFS / "report-template.md").read_text()
    for h in ("## Pass 1", "## Pass 2", "### Step table", "### Questions",
              "### Summary", "### Findings", "### Fix list", "### Assumptions",
              "### Kept manual", "### Sources"):
        assert h in text, f"report-template.md missing '{h}'"
    for col in ("Ladder tier", "Impact (hrs/wk)", "Effort (hrs)", "Tool + $/mo", "Maint. risk"):
        assert col in text


def test_question_bank_tags():
    lines = bullets((REFS / "question-bank.md").read_text())
    assert len(lines) >= 8
    for ln in lines:
        assert ln.startswith("- [blocking]") or ln.startswith("- [nice-to-have]"), ln
        if ln.startswith("- [nice-to-have]"):
            assert "→ default:" in ln, f"nice-to-have without default: {ln}"
        else:
            assert "→ unlocks:" in ln, f"blocking without unlocks: {ln}"


# ---------- framework contract ----------

@pytest.mark.parametrize("fid", FRAMEWORKS)
def test_framework_frontmatter(fid):
    fm, _ = split_frontmatter(FW_DIR / f"{fid}.md")
    assert fm["id"] == fid
    assert fm["name"]
    assert fm["category"] in CATEGORIES
    assert isinstance(fm["triggers"], list) and fm["triggers"]
    assert set(fm["blocking_inputs"]) <= set(SCHEMA_FIELDS), fm["blocking_inputs"]
    assert str(fm["version"]) == "1.0"


@pytest.mark.parametrize("fid", FRAMEWORKS)
def test_framework_sections_in_order(fid):
    _, body = split_frontmatter(FW_DIR / f"{fid}.md")
    pos = [body.find(h) for h in FW_SECTIONS]
    assert all(p >= 0 for p in pos), f"{fid}: missing {[h for h, p in zip(FW_SECTIONS, pos) if p < 0]}"
    assert pos == sorted(pos), f"{fid}: sections out of order"


@pytest.mark.parametrize("fid", FRAMEWORKS)
def test_framework_what_it_is_short(fid):
    _, body = split_frontmatter(FW_DIR / f"{fid}.md")
    lines = [l for l in section_body(body, "## What it is").splitlines() if l.strip()]
    assert len(lines) <= 5, f"{fid}: 'What it is' is {len(lines)} lines (max 5)"


@pytest.mark.parametrize("fid", FRAMEWORKS)
def test_framework_questions_tagged(fid):
    _, body = split_frontmatter(FW_DIR / f"{fid}.md")
    qs = bullets(section_body(body, "## Diagnostic questions"))
    assert len(qs) >= 3, f"{fid}: need >=3 diagnostic questions"
    assert any(q.startswith("- [blocking]") for q in qs), f"{fid}: no blocking question"
    for q in qs:
        assert q.startswith("- [blocking]") or q.startswith("- [nice-to-have]"), q
        if q.startswith("- [nice-to-have]"):
            assert "→ default:" in q, f"{fid}: nice-to-have without default: {q}"
        else:
            assert "→ unlocks:" in q, f"{fid}: blocking without unlocks: {q}"


@pytest.mark.parametrize("fid", FRAMEWORKS)
def test_framework_citations_labeled(fid):
    _, body = split_frontmatter(FW_DIR / f"{fid}.md")
    cites = bullets(section_body(body, "## Citations"))
    assert cites, f"{fid}: no citations"
    for c in cites:
        assert any(t in c for t in EVIDENCE_TAGS), f"{fid}: unlabeled citation: {c}"
        assert "http" in c, f"{fid}: citation without verification URL: {c}"


@pytest.mark.parametrize("fid", FRAMEWORKS)
def test_framework_no_long_quotes(fid):
    text = (FW_DIR / f"{fid}.md").read_text()
    assert not long_quotes(text), f"{fid}: quote of 15+ words: {long_quotes(text)}"


# ---------- evals ----------

def test_evals_file():
    data = json.loads((PLUGIN / "evals" / "evals.json").read_text())
    assert data["skill_name"] == "process-eval"
    assert len(data["evals"]) == 6
    for ev in data["evals"]:
        assert ev["prompt"] and ev["expected_output"]
        assert ev["assertions"], f"eval {ev['id']} has no assertions"
        for f in ev["files"]:
            assert (PLUGIN / f).exists(), f"missing eval input {f}"
```

- [ ] **Step 4: Run, confirm everything fails for missing files (not syntax)**

Run: `cd /home/claude/skills && python -m pytest plugins/process-eval/tests -q 2>&1 | tail -5`
Expected: all tests FAIL/ERROR with `FileNotFoundError` or `StopIteration`. Zero `SyntaxError`/`NameError`.

- [ ] **Step 5: Commit**

```bash
git add plugins/process-eval/requirements-dev.txt plugins/process-eval/tests/test_structure.py
git commit -m "test(process-eval): structure + contract test suite"
```

---

### Task 2: Plugin scaffold, manifest, marketplace, license

**Files:**
- Create: `plugins/process-eval/.claude-plugin/plugin.json`
- Create: `plugins/process-eval/LICENSE`
- Modify: `.claude-plugin/marketplace.json`
- Modify: `README.md` (root)

- [ ] **Step 1: Manifest**

`plugins/process-eval/.claude-plugin/plugin.json`:
```json
{
  "name": "process-eval",
  "description": "Evaluate any process against established, cited frameworks (Theory of Constraints, Lean, VSM, ECRS, checklists, poka-yoke) to find bottlenecks, steps to combine, and checklist candidates. Asks questions first, then reports.",
  "version": "0.1.0",
  "author": { "name": "Colin M." },
  "license": "MIT",
  "keywords": ["process improvement", "lean", "theory of constraints", "bottleneck", "checklist", "operations"]
}
```

- [ ] **Step 2: License**

`plugins/process-eval/LICENSE`: standard MIT text, `Copyright (c) 2026 Colin M.` Get exact text from https://opensource.org/license/mit (first line must be `MIT License`).

- [ ] **Step 3: Marketplace entry**

Append to the `plugins` array in `.claude-plugin/marketplace.json`:
```json
{
  "name": "process-eval",
  "source": "./plugins/process-eval",
  "description": "Evaluate any process against established, cited frameworks to find bottlenecks, steps to combine, and checklist candidates. Asks questions first, then reports.",
  "version": "0.1.0",
  "category": "productivity"
}
```

- [ ] **Step 4: Root README**

Add a row under `## Plugins` table:
```
| process-eval | Evaluate any process against cited frameworks (ToC, Lean, ECRS, checklists). Questions first, then a ranked fix list |
```
And add an install line under `## Install`:
```
/plugin install process-eval@offsetkeyz-skills
```

- [ ] **Step 5: Run wiring tests**

Run: `python -m pytest plugins/process-eval/tests -q -k "manifest or marketplace or license or root_readme"`
Expected: 4 passed.

- [ ] **Step 6: Validate marketplace (if CLI available)**

Run: `claude plugin validate . 2>&1 || python -c "import json;json.load(open('.claude-plugin/marketplace.json'));print('json ok')"`
Expected: validation passes, or `json ok` if the CLI is absent.

- [ ] **Step 7: Commit**

```bash
git add .claude-plugin/marketplace.json README.md plugins/process-eval/.claude-plugin plugins/process-eval/LICENSE
git commit -m "feat(process-eval): plugin scaffold, MIT license, marketplace entry"
```

---

### Task 3: `references/schema.md`

**Files:** Create `plugins/process-eval/skills/process-eval/references/schema.md`

- [ ] **Step 1: Write the file**

```markdown
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

- `stated`: the user said it or it is in their document. Shown plain.
- `~estimated`: inferred from context or a stated range. Shown with `~` prefix (`~2 days`).
- `?missing`: not known. Shown as `?`. Becomes a gap question.

## Rules

1. Never invent a value. Unknown is `?`, not a guess.
2. Replace names of real people, clients and employers with roles or generic labels.
3. Keep the user's units; convert only for math, and show the conversion.
4. `manual_by_choice = Y` only when the user says they enjoy, value, or want to keep the step. Ask if unclear; default is N.
5. Split a step when it has two actors or two tools. Merge only when the user describes it as one action.
6. Any step that moves money or contacts customers is flagged `⚑` in the `step` column.
```

- [ ] **Step 2: Run test**

Run: `python -m pytest plugins/process-eval/tests -q -k schema`
Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add plugins/process-eval/skills/process-eval/references/schema.md
git commit -m "feat(process-eval): step-table schema"
```

---

### Task 4: `references/fix-ladder.md`

**Files:** Create `plugins/process-eval/skills/process-eval/references/fix-ladder.md`

- [ ] **Step 1: Write the file**

```markdown
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
```

- [ ] **Step 2: Run test**

Run: `python -m pytest plugins/process-eval/tests -q -k fix_ladder`
Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add plugins/process-eval/skills/process-eval/references/fix-ladder.md
git commit -m "feat(process-eval): fix ladder house heuristic"
```

---

### Task 5: `references/question-bank.md`

**Files:** Create `plugins/process-eval/skills/process-eval/references/question-bank.md`

- [ ] **Step 1: Write the file**

```markdown
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
```

- [ ] **Step 2: Run test**

Run: `python -m pytest plugins/process-eval/tests -q -k question_bank`
Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add plugins/process-eval/skills/process-eval/references/question-bank.md
git commit -m "feat(process-eval): schema-gap question bank"
```

---

### Task 6: `references/report-template.md`

**Files:** Create `plugins/process-eval/skills/process-eval/references/report-template.md`

- [ ] **Step 1: Write the file**

````markdown
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

Max 8 questions. Order by what each unlocks (blocking first).

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
````

- [ ] **Step 2: Run test**

Run: `python -m pytest plugins/process-eval/tests -q -k report_template`
Expected: PASS.

- [ ] **Step 3: Commit**

```bash
git add plugins/process-eval/skills/process-eval/references/report-template.md
git commit -m "feat(process-eval): pass 1 and pass 2 report templates"
```

---

### Tasks 7–15: Framework files

**Shared instructions for each framework task (repeat for every file):**

File path: `plugins/process-eval/skills/process-eval/references/frameworks/<id>.md`.

Exact skeleton (fill every section from the task's content spec; no extra `##` headings):

```markdown
---
id: <id>
name: <Name>
category: <category>
triggers:
  - <trigger 1>
blocking_inputs: [<schema fields>]
version: 1.0
---
# <Name>

## What it is
<≤5 non-blank lines, paraphrased>

## When to apply
**Apply when:** …
**Do not apply when:** …

## Diagnostic questions
- [blocking] <question> → unlocks: <finding>
- [nice-to-have] <question> → default: <assumption>

## How to apply
1. <step against the step table>

## Typical recommendations
- <recommendation> (ladder tier N)

## Failure modes
- <misuse>

## Citations
- <Author>, *<Title>* (<Year>). <Publisher>. [<evidence type>] <verification URL>
```

Citation verification (required per file): before committing, open the URL with WebFetch or WebSearch and confirm author, title, year and publisher. If a detail differs, correct it to the source. If no authoritative URL exists, use the publisher's catalog page or WorldCat record. Record any correction in the commit message.

Per-file verification steps:
- Run: `python -m pytest plugins/process-eval/tests -q -k <id>` → Expected: 6 passed (frontmatter, sections, what_it_is, questions, citations, long_quotes).
- Commit: `git add <file> && git commit -m "feat(process-eval): <id> framework"`

---

### Task 7: `toc.md`

- [ ] **Step 1: Write file** using the skeleton with:
  - `name: Theory of Constraints`, `category: bottleneck`, `blocking_inputs: [time_touch, time_wait, volume]`
  - triggers: `time_wait at one step is 3x or more its time_touch`; `work queues in front of one actor or step`; `one role appears in many steps and others wait on it`
  - What it is: a system's output is limited by one constraint; improving anything else doesn't raise output. Five Focusing Steps: identify, exploit, subordinate, elevate, repeat (don't let inertia become the constraint).
  - Apply when: clear queue/wait at one point. Not when: no timing or volume data; work is mostly idle demand (constraint is the market, not the process).
  - Questions: [blocking] where does work wait longest and how long → unlocks: constraint identification · [blocking] how many items per week enter vs. leave the process → unlocks: throughput check · [nice-to-have] does the constrained person/step also do non-constraint work → default: yes; offload recommendation flagged Medium · [nice-to-have] is the constraint's time ever idle (waiting on inputs) → default: no
  - How to apply: find max time_wait/queue → name constraint → exploit (remove non-essential work from it, batch interruptions, ensure inputs are complete before they reach it) → subordinate (pace upstream to it) → elevate only after exploit (add capacity, delegate, tool) → re-check where the new constraint is.
  - Typical recs: move non-constraint tasks off the constrained role (tier 1); fix incomplete inputs upstream with required fields/checklist (tier 1–2); set a fixed review window instead of ad hoc (tier 1); delegate approvals under a threshold, keeping human approval for money (tier 1).
  - Failure modes: optimizing a non-constraint; elevating (hiring/buying) before exploiting; treating the busiest person as the constraint without wait data; not re-checking after a fix.
  - Citations: Goldratt & Cox, *The Goal* (1984), North River Press [book]; Goldratt, *Theory of Constraints* (1990), North River Press [book]. Find verification URLs (publisher or WorldCat).
- [ ] **Step 2: Verify citations** (see shared instructions)
- [ ] **Step 3: Run tests** `-k toc` → 6 passed
- [ ] **Step 4: Commit**

### Task 8: `littles-law.md`

- [ ] **Step 1: Write file** with:
  - `name: Little's Law`, `category: bottleneck`, `blocking_inputs: [volume, time_wait]`
  - triggers: `a queue or backlog is described with counts or times`; `user asks how long items take end to end`; `large batches build up before a handoff`
  - What it is: in a stable system, average items in progress (L) = arrival rate (λ) × average time in system (W). Lets you get any one of WIP, throughput or lead time from the other two.
  - Apply when: average volumes and either backlog count or time are known. Not when: system is unstable (backlog growing week over week) or a one-off project.
  - Questions: [blocking] how many items arrive per week → unlocks: throughput · [blocking] about how many are in progress or waiting right now → unlocks: lead-time estimate · [nice-to-have] is the backlog roughly steady or growing → default: steady; if growing, report says arrivals exceed capacity
  - How to apply: convert to consistent units → compute the missing quantity → compare to touch time to show share of time waiting → show the math inline with "(verify)" when inputs are estimated.
  - Typical recs: cap work in progress (tier 1); cut batch size (tier 1); reduce arrivals of avoidable work, e.g. duplicate requests (tier 1–2).
  - Failure modes: applying to a growing backlog; mixing units (days vs. business days); treating the result as exact rather than an average.
  - Citations: Little, J.D.C., "A Proof for the Queuing Formula: L = λW," *Operations Research* 9(3):383–387 (1961) [peer-reviewed] https://doi.org/10.1287/opre.9.3.383
- [ ] **Step 2–4:** verify, `-k littles` → 6 passed, commit.

### Task 9: `vsm.md`

- [ ] **Step 1: Write file** with:
  - `name: Value Stream Mapping`, `category: waste`, `blocking_inputs: [time_touch, time_wait]`
  - triggers: `3 or more handoffs between roles`; `total wait time is much larger than total touch time`; `user wants an end-to-end view`
  - What it is: map the actual current flow of work and information, with touch time and wait time per step; compute lead time and flow efficiency (touch ÷ lead time); design a future state that removes waits.
  - Apply when: multi-step, multi-role process. Not when: single-person, single-step task.
  - Questions: [blocking] wait time between each handoff → unlocks: lead time and flow efficiency · [blocking] does the map reflect what actually happens, including workarounds → unlocks: current-state accuracy · [nice-to-have] how is the next person told work is ready → default: email/verbal; signaling fixes flagged Medium
  - How to apply: build the current-state timeline from the step table → sum touch and wait → compute flow efficiency → mark waits and handoffs → propose a future state (fewer handoffs, pull signals, combined steps).
  - Typical recs: remove handoffs by giving one role end-to-end ownership (tier 1); add a ready-signal (shared queue, status field) (tier 2); combine adjacent steps (tier 1).
  - Failure modes: mapping the official process instead of the real one; mapping without times; drawing a future state with no plan to reach it.
  - Citations: Rother & Shook, *Learning to See* (1999), Lean Enterprise Institute [book] (find LEI page).
- [ ] **Step 2–4:** verify, `-k vsm` → 6 passed, commit.

### Task 10: `lean-wastes.md`

- [ ] **Step 1: Write file** with:
  - `name: Lean Wastes`, `category: waste`, `blocking_inputs: [step, actor, tool]`
  - triggers: `duplicate data entry or re-keying`; `steps that only move, copy, or check work`; `rework greater than zero`; `work produced before anyone needs it`
  - What it is: Ohno's seven wastes (transport, inventory, motion, waiting, overproduction, overprocessing, defects) plus unused talent, added in later Toyota literature. DOWNTIME is a practitioner mnemonic.
  - Include an office translation table inside **How to apply** (not a new `##`): transport → forwarding/re-sending; inventory → backlogs, unread queues; motion → switching tools, hunting for files; waiting → approvals, replies; overproduction → reports nobody reads; overprocessing → extra sign-offs, re-formatting; defects → errors and rework; unused talent → skilled staff doing clerical work.
  - Questions: [blocking] which steps add something the customer would pay for → unlocks: value vs. waste classification · [nice-to-have] which reports or copies does nobody use → default: all used · [nice-to-have] where is the same information typed twice → default: none
  - Typical recs: delete non-value steps (tier 1); single source of truth to stop re-keying (tier 2–3); stop unread reports (tier 1).
  - Failure modes: labeling necessary compliance steps as waste; cutting steps the owner values (check manual_by_choice); waste-hunting without timing to rank.
  - Citations: Ohno, *Toyota Production System: Beyond Large-Scale Production* (English ed. 1988), Productivity Press [book]; Liker, *The Toyota Way* (2004), McGraw-Hill [book].
- [ ] **Step 2–4:** verify, `-k lean` → 6 passed, commit.

### Task 11: `ecrs.md`

- [ ] **Step 1: Write file** with:
  - `name: ECRS`, `category: simplify`, `blocking_inputs: [step, actor, tool]`
  - triggers: `same actor does adjacent steps in the same tool`; `a step exists only to prepare for another step`; `steps could happen in parallel or a different order`
  - What it is: method-study sequence for improving work: Eliminate, Combine, Rearrange, Simplify, applied in that order after questioning each step (what, why, where, when, who, how).
  - Questions: [blocking] what would break if this step were removed → unlocks: eliminate candidates · [nice-to-have] could the same person do these steps in one sitting → default: yes if same actor and tool · [nice-to-have] must these steps happen in this order → default: yes; rearrange recs flagged Medium
  - How to apply: run each step through E, then C, then R, then S; record the question that justified each change.
  - Typical recs: eliminate a step (tier 1); combine data entry into one form (tier 1–2); rearrange to front-load checks (tier 1); simplify with a template (tier 2).
  - Failure modes: simplifying before eliminating; combining steps owned by different roles without agreement; removing control steps.
  - Citations: Kanawaty (ed.), *Introduction to Work Study*, 4th ed. (1992), International Labour Office [standards body] (find ILO/WorldCat page).
- [ ] **Step 2–4:** verify, `-k ecrs` → 6 passed, commit.

### Task 12: `batching.md`

- [ ] **Step 1: Write file** with:
  - `name: Batch Size`, `category: simplify`, `blocking_inputs: [volume, time_wait]`
  - triggers: `work is collected and processed weekly or monthly`; `items wait for a batch to fill before moving`; `same small task repeated with constant interruptions`
  - What it is: smaller batches cut wait time, variability and feedback delay; the best size balances per-batch overhead (setup, context switching) against holding cost (delay, aging). Batching can also help when switching cost is high.
  - Questions: [blocking] how often is this work processed (daily, weekly) → unlocks: batch-delay estimate · [nice-to-have] what is the setup cost of each run → default: low; recommendation leans smaller batches · [nice-to-have] does delay cost anything (late fees, unhappy customers) → default: moderate
  - How to apply: estimate average delay added by the batch (≈ half the batch interval) → compare with setup overhead → recommend direction (smaller or grouped) with the math.
  - Typical recs: move from weekly to daily processing (tier 1); group scattered interruptions into fixed blocks (tier 1); automate setup to make small batches cheap (tier 2–3).
  - Failure modes: one-size rule ("always small"); ignoring setup cost; batching customer-facing work that needs fast response.
  - Citations: Reinertsen, *The Principles of Product Development Flow* (2009), Celeritas Publishing [book].
- [ ] **Step 2–4:** verify, `-k batching` → 6 passed, commit.

### Task 13: `poka-yoke.md`

- [ ] **Step 1: Write file** with:
  - `name: Poka-yoke (Error-proofing)`, `category: error-proof`, `blocking_inputs: [rework]`
  - triggers: `rework greater than zero`; `repeated checking or proofreading steps`; `errors reach customers or money`
  - What it is: design the step so mistakes are impossible or caught immediately at the source, instead of inspected later. Two modes: control (prevents the error) and warning (signals it).
  - Questions: [blocking] which errors happen and at which step → unlocks: error-proofing target · [nice-to-have] how are errors found today, and how late → default: found downstream · [nice-to-have] what does an error cost when it happens → default: low; ranked below time savings
  - How to apply: trace each error to the step that creates it → prefer control over warning → prefer prevention at source over later inspection.
  - Typical recs (office): required fields, dropdowns, input validation, templates with locked fields, duplicate detection (tier 2); a pre-send check step for ⚑ steps (tier 1).
  - Failure modes: adding inspection instead of prevention; warnings people learn to ignore; error-proofing a rare error over a common one.
  - Citations: Shingo, *Zero Quality Control: Source Inspection and the Poka-yoke System* (1986), Productivity Press [book].
- [ ] **Step 2–4:** verify, `-k poka` → 6 passed, commit.

### Task 14: `checklists.md`

- [ ] **Step 1: Write file** with:
  - `name: Checklists`, `category: checklist`, `blocking_inputs: [step, actor]`
  - triggers: `fixed sequence of steps done by people`; `a missed step is costly or has happened`; `step is rare enough that people forget it`; `manual_by_choice step that still needs consistency`
  - What it is: short checklists at defined pause points catch missed critical steps; two types: DO-CONFIRM (do from memory, then confirm) and READ-DO (read and do each item). Keep to killer items, roughly 5–9, tested in real use.
  - Questions: [blocking] which steps, if skipped, cause real harm → unlocks: killer items · [nice-to-have] are these done by experienced staff from memory → default: yes; DO-CONFIRM recommended · [nice-to-have] where is the natural pause point → default: before the output leaves the actor
  - How to apply: list candidate items from the step table → keep only killer items → choose type by experience level → place at a pause point → plan a trial and revise.
  - Typical recs: a DO-CONFIRM checklist at handoff (tier 1); READ-DO for rare procedures (tier 1); embed checklist in the tool's task template (tier 2).
  - Failure modes: long checklists that become box-ticking; listing obvious steps; never testing or updating.
  - Evidence note in How to apply: the WHO Surgical Safety Checklist study (8 hospitals) reported lower death and complication rates after introduction. Paraphrase; cite the NEJM paper.
  - Citations: Gawande, *The Checklist Manifesto* (2009), Metropolitan Books [book]; Haynes et al., "A Surgical Safety Checklist to Reduce Morbidity and Mortality in a Global Population," *NEJM* 360:491–499 (2009) [peer-reviewed] https://doi.org/10.1056/NEJMsa0810119
- [ ] **Step 2–4:** verify, `-k checklists` → 6 passed, commit.

### Task 15: `sipoc-raci.md`

- [ ] **Step 1: Write file** with:
  - `name: SIPOC and RACI`, `category: scope`, `blocking_inputs: [actor, trigger, output]`
  - triggers: `unclear start or end of the process`; `steps with no clear owner`; `the same step has more than one approver`; `user cannot name who receives the output`
  - What it is: SIPOC (Suppliers, Inputs, Process, Outputs, Customers) frames a process at a high level in about 5–7 steps. RACI (Responsible, Accountable, Consulted, Informed) assigns roles per step; each step has exactly one Accountable.
  - Questions: [blocking] who is accountable for the final output → unlocks: ownership findings · [blocking] who supplies the inputs and in what form → unlocks: input-quality findings · [nice-to-have] who needs to be told when it's done → default: requester only
  - How to apply: build a SIPOC row from the step table → build a RACI grid across steps × roles → flag steps with 0 or 2+ Accountable, and Consulted lists that cause waits.
  - Typical recs: name one owner per step (tier 1); move "Consulted" to "Informed" where input isn't needed (tier 1); agree input standards with suppliers (tier 1–2).
  - Failure modes: SIPOC with too many steps; RACI with everyone Consulted; documenting roles without changing behavior.
  - Citations: American Society for Quality (ASQ), "SIPOC Diagram" resource page [standards body] (find asq.org URL); Project Management Institute, *A Guide to the Project Management Body of Knowledge (PMBOK Guide)* (responsibility assignment matrix) [standards body] (find pmi.org URL; cite edition used).
- [ ] **Step 2–4:** verify, `-k sipoc` → 6 passed, commit.

---

### Task 16: `SKILL.md`

**Files:** Create `plugins/process-eval/skills/process-eval/SKILL.md`

- [ ] **Step 1: Write the file**

```markdown
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
```

- [ ] **Step 2: Run SKILL tests**

Run: `python -m pytest plugins/process-eval/tests -q -k skill`
Expected: 4 passed. If `8 questions` fails, check the exact phrase "Max 8 questions" lower-cases to contain `8 questions`.

- [ ] **Step 3: Commit**

```bash
git add plugins/process-eval/skills/process-eval/SKILL.md
git commit -m "feat(process-eval): SKILL.md workflow, routing, hard rules"
```

---

### Task 17: Eval inputs and evals.json

**Files:**
- Create: `plugins/process-eval/evals/inputs/{ap-invoice,client-onboarding,bakery-orders,patch-management,appointment-reminders,lean-already}.md`
- Create: `plugins/process-eval/evals/evals.json`

- [ ] **Step 1: Write the 6 inputs**

`evals/inputs/ap-invoice.md`:
```markdown
Notes from a call with the office manager at a 9-person property management company.

Invoices come in by email, about 40 a week. Our AP clerk saves the PDF to a shared folder (1 min) and types it into QuickBooks (about 6 min each). Then she emails the office manager to approve. The office manager approves in batches when she gets to it, usually every two or three days, and it takes her about 10 minutes per invoice because she has to look up the contract. After approval the clerk schedules payment (2 min). Maybe 1 in 10 invoices gets entered wrong and has to be fixed.
```

`evals/inputs/client-onboarding.md`:
```markdown
SOP: New client onboarding (6-person accounting firm)

1. Admin receives signed engagement letter by email.
2. Admin creates client folder in the shared drive.
3. Admin types client name, address, EIN, contact info into the practice management system.
4. Admin types the same client info into the tax software.
5. Admin types the same contact info into the email newsletter tool.
6. Admin emails the client a document request list.
7. Partner reviews the file before first meeting.
Each entry step takes about 5–8 minutes. We onboard 15 clients a month, more in Jan–Mar.
```

`evals/inputs/bakery-orders.md`:
```markdown
Transcript excerpt, owner of a 4-person bakery:

"Custom cake orders come in by phone, Instagram DMs, and walk-in. I write them on a paper pad. Maybe 25 a week. Sometimes we forget to ask about allergies or the pickup time and have to call back, probably 3 or 4 times a week. Last month we wrote the wrong date on one and the customer showed up and there was no cake. Decorating is my favorite part, I don't want any of that automated. I just want orders to stop slipping."
```

`evals/inputs/patch-management.md`:
```markdown
| Step | Actor | Tool | Touch | Wait before | Volume |
|---|---|---|---|---|---|
| Vendor releases patches | — | — | — | — | ~30/month |
| Collect patches for monthly window | IT admin | ticketing | 2 h/month | up to 30 days | 1 batch/month |
| Test patches on staging | IT admin | VMs | 6 h/batch | 3 days | 1/month |
| Change approval meeting | IT manager | meeting | 1 h | 7 days (meets weekly) | 1/month |
| Deploy to production | IT admin | RMM tool | 3 h/batch | 2 days | 1/month |
| Verify and close tickets | IT admin | ticketing | 2 h/batch | 1 day | 1/month |
Rework: about 1 deploy in 6 needs a rollback.
```

`evals/inputs/appointment-reminders.md`:
```markdown
We call patients to remind them about appointments. It takes forever. Can you fix it?
```

`evals/inputs/lean-already.md`:
```markdown
Process: daily cash deposit at a 3-person coffee shop.
1. Closing barista counts the drawer using the POS end-of-day report (10 min, daily).
2. Barista bags cash with the printed report (2 min).
3. Owner drops the bag at the bank night deposit on her way home (5 min, on her route).
4. Owner matches the bank deposit to the POS report in the accounting app the next morning (3 min; bank feed imports automatically).
No waiting between steps beyond overnight. Mismatches maybe twice a year. The owner likes doing the morning match herself.
```

- [ ] **Step 2: Write evals.json**

`plugins/process-eval/evals/evals.json`:
```json
{
  "skill_name": "process-eval",
  "evals": [
    {
      "id": 1,
      "prompt": "Evaluate this process and tell me what to fix.",
      "files": ["evals/inputs/ap-invoice.md"],
      "expected_output": "Pass 1 step table and questions (no findings). After answers, pass 2 identifies the approval wait at the office manager as the constraint using Theory of Constraints and Little's Law, keeps human approval on payment.",
      "assertions": [
        "First response contains a step table and questions but no findings section",
        "Office manager approval step is tagged as the likely constraint in frameworks in scope",
        "Pass 2 cites Goldratt and/or Little (1961)",
        "No recommendation removes human approval before payment"
      ]
    },
    {
      "id": 2,
      "prompt": "Here's our onboarding SOP. Where can we tighten it up?",
      "files": ["evals/inputs/client-onboarding.md"],
      "expected_output": "Routes to ECRS and Lean wastes for triple data entry; SIPOC/RACI may flag partner review. Recommends single entry or sync (combine) with ECRS citation.",
      "assertions": [
        "Steps 3-5 are identified as duplicate data entry",
        "ECRS is in scope and cited in pass 2",
        "Fix list ranks a process or configuration change at or above any AI option"
      ]
    },
    {
      "id": 3,
      "prompt": "Can you look at how we take cake orders?",
      "files": ["evals/inputs/bakery-orders.md"],
      "expected_output": "Checklists and poka-yoke in scope for missed allergy/pickup details. Decorating marked manual_by_choice and listed under Kept manual, never automated.",
      "assertions": [
        "Decorating is marked manual_by_choice = Y",
        "No recommendation automates decorating",
        "Recommends an order checklist or required-field order form, citing checklist or poka-yoke sources"
      ]
    },
    {
      "id": 4,
      "prompt": "Analyze our patching process.",
      "files": ["evals/inputs/patch-management.md"],
      "expected_output": "VSM shows low flow efficiency; batching flags the monthly window as the main source of wait; ToC may flag the weekly change meeting. Shows math.",
      "assertions": [
        "Flow efficiency or touch vs. wait comparison is calculated with units",
        "Batch size framework is in scope and the monthly batch is named as a driver of wait",
        "Rollback rework is noted"
      ]
    },
    {
      "id": 5,
      "prompt": "Fix this.",
      "files": ["evals/inputs/appointment-reminders.md"],
      "expected_output": "Stops at the gate with blocking questions about volume, time per call, who calls, and tools. No findings, no tool recommendations.",
      "assertions": [
        "Response contains blocking questions about volume and time",
        "Response contains no findings and no fix list",
        "Response asks 8 or fewer questions"
      ]
    },
    {
      "id": 6,
      "prompt": "Anything to improve here?",
      "files": ["evals/inputs/lean-already.md"],
      "expected_output": "After pass 1 confirmation, reports that no significant improvements were found; does not invent problems; keeps the owner's morning match manual.",
      "assertions": [
        "Pass 2 states the process is already efficient or that no significant findings were made",
        "Morning match step is listed under Kept manual",
        "No more than 2 fixes are proposed, all low effort"
      ]
    }
  ]
}
```

- [ ] **Step 3: Run test**

Run: `python -m pytest plugins/process-eval/tests -q -k evals`
Expected: PASS.

- [ ] **Step 4: Commit**

```bash
git add plugins/process-eval/evals
git commit -m "test(process-eval): 6 eval cases with sample inputs"
```

---

### Task 18: Plugin README + CONTRIBUTING

**Files:** Create `plugins/process-eval/README.md`, `plugins/process-eval/CONTRIBUTING.md`

- [ ] **Step 1: README** with these sections, in order:
  - `# process-eval`: one-paragraph purpose (from spec §1).
  - `## Install`: the two `/plugin` commands from the root README, plus the `.skill` zip command for claude.ai.
  - `## How it works`: the two-pass flow (spec §2 diagram), the gate rule in 3 bullets.
  - `## Frameworks`: table of the 9 files with category and primary source (spec §5 table).
  - `## Example`: the bakery input (Task 17) and an abbreviated pass 1 output (5-row step table + 4 questions) written by actually running the skill on that input.
  - `## Adding a framework`: copy the skeleton from Tasks 7–15, add a routing row to SKILL.md, add an eval case, run `pytest plugins/process-eval/tests`.
  - `## Fix ladder`: one paragraph, noting it is a house heuristic.
  - `## License`: MIT.

- [ ] **Step 2: CONTRIBUTING** with these rules:
  - One framework per PR: 1 file + 1 eval case + routing row.
  - Primary source required, with a URL that confirms author, title and year. Evidence type label required.
  - Paraphrase only; no quotes of 15+ words.
  - Examples use roles and generic organizations, never real people or companies.
  - `pytest plugins/process-eval/tests` must pass.

- [ ] **Step 3: Run full suite**

Run: `python -m pytest plugins/process-eval/tests -q`
Expected: all passed (wiring 5 + skill 4 + refs 4 + frameworks 54 + evals 1 = 68).

- [ ] **Step 4: Commit**

```bash
git add plugins/process-eval/README.md plugins/process-eval/CONTRIBUTING.md
git commit -m "docs(process-eval): README and contributing guide"
```

---

### Task 19: Behavioral evals (skill-creator)

- [ ] **Step 1:** Load the `skill-creator` skill and follow its eval-run procedure using `plugins/process-eval/evals/evals.json` and the skill at `plugins/process-eval/skills/process-eval/`. For cases 1–4 and 6, run a second turn that answers the blocking questions with plausible values, so pass 2 is exercised.
- [ ] **Step 2:** Grade each assertion pass/fail. Target: all assertions pass on all 6 cases.
- [ ] **Step 3:** For each failure, fix the smallest thing (routing row, rule wording, framework "How to apply"), re-run `pytest`, re-run that eval case.
- [ ] **Step 4: Commit** fixes with messages naming the eval id, e.g. `fix(process-eval): eval 5 — gate held, removed tool hints from pass 1`.

---

### Task 20: Ship

- [ ] **Step 1:** `python -m pytest plugins/process-eval/tests -q` → all pass.
- [ ] **Step 2:** `claude plugin validate .` (or the JSON fallback from Task 2).
- [ ] **Step 3:** Build bundle: `mkdir -p dist && cd plugins/process-eval/skills && zip -r ../../../dist/process-eval.skill process-eval && cd -` (dist/ is gitignored).
- [ ] **Step 4:** `git fetch origin main && git rebase origin/main && git push --force-with-lease`
- [ ] **Step 5:** Open a PR `spec/process-eval` → `main` titled `process-eval v0.1.0`. Body: summary, framework list, eval results table (case, pass/fail), citation verification notes, and the attribution footer.

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

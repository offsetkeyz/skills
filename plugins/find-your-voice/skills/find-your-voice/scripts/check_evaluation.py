#!/usr/bin/env python3
"""Sanity-check an evaluation reply against the writing samples it describes.

Usage:
    python scripts/check_evaluation.py --samples sample1.txt [sample2.txt ...] --reply reply.md

Reports three things so the reply can be fixed before it's sent:
  1. Word count of each sample (use these numbers, never estimate).
  2. Quoted phrases in the reply that are NOT found verbatim in the samples.
     Ellipses are allowed: "a ... b" is checked as the fragments "a" and "b".
     Phrases that are intentionally not from the samples (intake wording,
     generic AI-tell examples, labels) will show up too; ignore those.
     Reworded or reordered quotes are the ones to fix.
  3. Possible third-party names: capitalized multi-word names that appear in
     the samples and also in the reply. Refer to people by role instead
     ("a customer", "a coworker"). This is a heuristic and can miss names.
"""
import argparse
import re
import sys


def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace('"', "").replace("'", "")  # ignore quote-style differences, e.g. nested quotes
    return re.sub(r"\s+", " ", s).strip().lower()


def fragments(q: str):
    parts = re.split(r"\.\.\.|…", q)
    out = []
    for p in parts:
        p = norm(p).strip(" .,;:!?-—'\"")
        if p:
            out.append(p)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--samples", nargs="+", required=True)
    ap.add_argument("--reply", required=True)
    a = ap.parse_args()

    raw = {p: open(p, encoding="utf-8").read() for p in a.samples}
    corpus = norm(" ".join(raw.values()))
    reply = open(a.reply, encoding="utf-8").read()

    print("== Sample word counts ==")
    for p, t in raw.items():
        print(f"  {len(t.split()):5d}  {p}")

    print("\n== Quoted phrases not found verbatim in the samples ==")
    text = reply.replace("“", '"').replace("”", '"')
    quotes = re.findall(r'"([^"\n]{4,}?)"', text)
    missing = []
    for q in quotes:
        frs = fragments(q)
        if frs and not all(f in corpus for f in frs):
            missing.append(q)
    if missing:
        for q in missing:
            print(f"  ? {q}")
        print("  (Fix reworded or reordered quotes. Ignore intake wording, labels, and generic examples.)")
    else:
        print("  none")

    print("\n== Possible third-party names carried into the reply ==")
    name_re = re.compile(r"\b[A-Z][a-z]+(?: [A-Z][a-z]+)+\b")
    names = {n for t in raw.values() for n in name_re.findall(t)}
    hits = sorted(n for n in names if n in reply)
    if hits:
        for n in hits:
            print(f"  ! {n}")
        print("  (If any is a person, replace it with a role.)")
    else:
        print("  none")
    return 0


if __name__ == "__main__":
    sys.exit(main())

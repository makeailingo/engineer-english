#!/usr/bin/env python3
"""Skill 判断基準に沿った 100 語 expected を生成する。"""

from __future__ import annotations

import json
from pathlib import Path

# (generalFamiliarity, engineerFamiliarity, contextualLearningNeeded, nearestExamples, difficulty)
JUDGMENTS: dict[str, tuple] = {
    # --- Beginner (21) ---
    "approach": ("high", "high", "low", ["approach", "feedback"], "Beginner"),
    "approval": ("high", "medium", "low", ["feedback", "deadline"], "Beginner"),
    "communication": ("high", "high", "low", ["feedback", "approach"], "Beginner"),
    "deadline": ("high", "high", "low", ["deadline", "feedback"], "Beginner"),
    "failure": ("high", "high", "low", ["failure", "approach"], "Beginner"),
    "fetch": ("medium", "high", "low", ["fetch", "query"], "Beginner"),
    "insert": ("high", "high", "low", ["query", "fetch"], "Beginner"),
    "install": ("high", "high", "low", ["install", "fetch"], "Beginner"),
    "interaction": ("high", "medium", "low", ["approach", "feedback"], "Beginner"),
    "interface": ("medium", "high", "low", ["query", "fetch"], "Beginner"),
    "mentoring": ("medium", "medium", "low", ["feedback", "approach"], "Beginner"),
    "operation": ("high", "high", "low", ["query", "fetch"], "Beginner"),
    "prevent": ("high", "medium", "low", ["approach", "failure"], "Beginner"),
    "profile": ("high", "medium", "low", ["query", "fetch"], "Beginner"),
    "query": ("medium", "high", "low", ["query", "fetch"], "Beginner"),
    "recover": ("high", "medium", "low", ["failure", "approach"], "Beginner"),
    "replace": ("high", "high", "low", ["replace", "fetch"], "Beginner"),
    "tension": ("high", "medium", "low", ["feedback", "approach"], "Beginner"),
    "trace": ("medium", "high", "low", ["query", "fetch"], "Beginner"),
    "transaction": ("medium", "high", "low", ["query", "fetch"], "Beginner"),
    "feedback": ("high", "high", "low", ["feedback", "deadline"], "Beginner"),
    # --- Intermediate (64) ---
    "abort": ("medium", "high", "medium", ["dispatch", "defer"], "Intermediate"),
    "assertion": ("low", "medium", "medium", ["regression", "constraint"], "Intermediate"),
    "availability": ("medium", "high", "medium", ["scope", "defer"], "Intermediate"),
    "bypass": ("medium", "medium", "medium", ["defer", "dispatch"], "Intermediate"),
    "capacity": ("medium", "medium", "medium", ["scope", "defer"], "Intermediate"),
    "clarify": ("medium", "medium", "medium", ["clarify", "defer"], "Intermediate"),
    "clone": ("medium", "high", "medium", ["dispatch", "defer"], "Intermediate"),
    "collaborate": ("medium", "medium", "medium", ["clarify", "defer"], "Intermediate"),
    "compress": ("medium", "medium", "medium", ["defer", "scope"], "Intermediate"),
    "constraint": ("medium", "medium", "medium", ["constraint", "scope"], "Intermediate"),
    "constructive": ("medium", "medium", "medium", ["clarify", "defer"], "Intermediate"),
    "coverage": ("medium", "high", "medium", ["regression", "scope"], "Intermediate"),
    "criterion": ("medium", "medium", "medium", ["constraint", "scope"], "Intermediate"),
    "critique": ("medium", "medium", "medium", ["clarify", "escalate"], "Intermediate"),
    "deadlock": ("low", "high", "medium", ["regression", "constraint"], "Intermediate"),
    "decompose": ("medium", "medium", "medium", ["defer", "scope"], "Intermediate"),
    "decrypt": ("medium", "high", "medium", ["dispatch", "defer"], "Intermediate"),
    "defer": ("medium", "medium", "medium", ["defer", "clarify"], "Intermediate"),
    "dependency": ("medium", "high", "medium", ["scope", "constraint"], "Intermediate"),
    "deploy": ("medium", "high", "medium", ["dispatch", "defer"], "Intermediate"),
    "dispatch": ("medium", "medium", "medium", ["dispatch", "defer"], "Intermediate"),
    "encrypt": ("medium", "high", "medium", ["dispatch", "defer"], "Intermediate"),
    "enforce": ("medium", "medium", "medium", ["constraint", "defer"], "Intermediate"),
    "escalate": ("medium", "medium", "medium", ["escalate", "defer"], "Intermediate"),
    "expectations": ("medium", "medium", "medium", ["scope", "clarify"], "Intermediate"),
    "implementation": ("medium", "high", "medium", ["scope", "defer"], "Intermediate"),
    "index": ("medium", "high", "medium", ["query", "dispatch"], "Intermediate"),
    "infrastructure": ("medium", "high", "medium", ["scope", "constraint"], "Intermediate"),
    "inspect": ("medium", "medium", "medium", ["clarify", "defer"], "Intermediate"),
    "invoke": ("medium", "high", "medium", ["dispatch", "defer"], "Intermediate"),
    "isolate": ("medium", "medium", "medium", ["clarify", "regression"], "Intermediate"),
    "latency": ("medium", "high", "medium", ["scope", "regression"], "Intermediate"),
    "mandatory": ("medium", "medium", "medium", ["constraint", "defer"], "Intermediate"),
    "monitor": ("medium", "high", "medium", ["dispatch", "scope"], "Intermediate"),
    "objective": ("medium", "medium", "medium", ["scope", "clarify"], "Intermediate"),
    "optimize": ("medium", "high", "medium", ["scope", "regression"], "Intermediate"),
    "overload": ("medium", "medium", "medium", ["constraint", "scope"], "Intermediate"),
    "ownership": ("medium", "high", "medium", ["scope", "escalate"], "Intermediate"),
    "pass": ("medium", "medium", "medium", ["regression", "defer"], "Intermediate"),
    "pinpoint": ("medium", "medium", "medium", ["clarify", "defer"], "Intermediate"),
    "preload": ("medium", "medium", "medium", ["fetch", "dispatch"], "Intermediate"),
    "priority": ("medium", "medium", "medium", ["scope", "defer"], "Intermediate"),
    "progress": ("medium", "medium", "medium", ["defer", "scope"], "Intermediate"),
    "readability": ("medium", "medium", "medium", ["clarify", "constraint"], "Intermediate"),
    "record": ("medium", "medium", "medium", ["dispatch", "defer"], "Intermediate"),
    "recovery": ("medium", "high", "medium", ["regression", "scope"], "Intermediate"),
    "regression": ("medium", "high", "medium", ["regression", "constraint"], "Intermediate"),
    "reinforcement": ("medium", "medium", "medium", ["defer", "scope"], "Intermediate"),
    "reject": ("medium", "medium", "medium", ["defer", "clarify"], "Intermediate"),
    "reliability": ("medium", "high", "medium", ["scope", "constraint"], "Intermediate"),
    "replication": ("medium", "high", "medium", ["regression", "scope"], "Intermediate"),
    "reproduce": ("medium", "high", "medium", ["regression", "isolate"], "Intermediate"),
    "requirements": ("medium", "high", "medium", ["scope", "clarify"], "Intermediate"),
    "respectful": ("medium", "medium", "medium", ["clarify", "defer"], "Intermediate"),
    "scalability": ("medium", "high", "medium", ["scope", "regression"], "Intermediate"),
    "schema": ("medium", "high", "medium", ["constraint", "scope"], "Intermediate"),
    "scope": ("medium", "medium", "medium", ["scope", "defer"], "Intermediate"),
    "self-contained": ("medium", "medium", "medium", ["constraint", "scope"], "Intermediate"),
    "specification": ("medium", "high", "medium", ["constraint", "scope"], "Intermediate"),
    "target": ("medium", "medium", "medium", ["scope", "defer"], "Intermediate"),
    "trade-off": ("medium", "medium", "medium", ["trade-off", "scope"], "Intermediate"),
    "unavailable": ("medium", "medium", "medium", ["defer", "scope"], "Intermediate"),
    "validate": ("medium", "medium", "medium", ["regression", "clarify"], "Intermediate"),
    "velocity": ("medium", "high", "medium", ["scope", "defer"], "Intermediate"),
    # --- Advanced (15) ---
    "abstraction": ("medium", "high", "high", ["abstraction", "demonstrate"], "Advanced"),
    "authenticate": ("medium", "high", "high", ["demonstrate", "abstraction"], "Advanced"),
    "complexity": ("medium", "high", "high", ["abstraction", "demonstrate"], "Advanced"),
    "consensus": ("low", "medium", "high", ["consensus", "discretion"], "Advanced"),
    "correctness": ("low", "medium", "high", ["abstraction", "demonstrate"], "Advanced"),
    "courteous": ("low", "low", "high", ["courteous", "scrutiny"], "Advanced"),
    "demonstrate": ("medium", "medium", "high", ["demonstrate", "abstraction"], "Advanced"),
    "diagnose": ("medium", "medium", "high", ["demonstrate", "scrutiny"], "Advanced"),
    "discretion": ("low", "low", "high", ["discretion", "scrutiny"], "Advanced"),
    "functionality": ("low", "medium", "high", ["abstraction", "demonstrate"], "Advanced"),
    "iterate": ("medium", "medium", "high", ["abstraction", "demonstrate"], "Advanced"),
    "sanitize": ("low", "medium", "high", ["scrutiny", "discretion"], "Advanced"),
    "scrutiny": ("low", "low", "high", ["scrutiny", "discretion"], "Advanced"),
    "severity": ("medium", "medium", "high", ["scrutiny", "demonstrate"], "Advanced"),
    "validation": ("medium", "medium", "high", ["abstraction", "demonstrate"], "Advanced"),
}


def build_expected() -> dict:
    out = {}
    for term in sorted(JUDGMENTS.keys()):
        gf, ef, cl, ne, diff = JUDGMENTS[term]
        out[term] = {
            "difficulty": diff,
            "reasoning": {
                "generalFamiliarity": gf,
                "engineerFamiliarity": ef,
                "contextualLearningNeeded": cl,
                "nearestExamples": ne,
            },
        }
    return out


def build_report(expected: dict) -> str:
    import re

    vocab: dict[str, str] = {}
    for path in sorted(Path("docs/vocabulary").glob("*.md")):
        text = path.read_text(encoding="utf-8")
        term = re.search(r'^term:\s*"?([^"\n]+)"?\s*$', text, re.M)
        diff = re.search(r'^difficulty:\s*"?([^"\n]+)"?\s*$', text, re.M)
        if term and diff:
            vocab[term.group(1).strip()] = diff.group(1).strip()

    lines = [
        "# Difficulty 判断結果（100語）",
        "",
        "evaluating-difficulty Skill（判断基準 + 代表例）に基づく expected。",
        "",
        "| 集計 | 語数 |",
        "| --- | ---: |",
    ]
    for level in ("Beginner", "Intermediate", "Advanced"):
        n = sum(1 for e in expected.values() if e["difficulty"] == level)
        lines.append(f"| {level} | {n} |")

    mismatches = [
        t for t, e in expected.items() if vocab.get(t) != e["difficulty"]
    ]
    lines += [
        "",
        f"現行 Vocabulary との不一致: **{len(mismatches)}/100**",
        "",
        "---",
        "",
        "| term | difficulty | general | engineer | context | nearestExamples | 現行 |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for i, term in enumerate(sorted(expected.keys()), 1):
        e = expected[term]
        r = e["reasoning"]
        cur = vocab.get(term, "?")
        mark = cur if cur == e["difficulty"] else f"{cur} **≠**"
        ne = ", ".join(r["nearestExamples"])
        lines.append(
            f"| {term} | {e['difficulty']} | {r['generalFamiliarity']} "
            f"| {r['engineerFamiliarity']} | {r['contextualLearningNeeded']} "
            f"| {ne} | {mark} |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    expected = build_expected()
    assert len(expected) == 100, len(expected)

    out_dir = Path(__file__).parent
    (out_dir / "regression_expected.json").write_text(
        json.dumps(expected, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (out_dir / "judgments_100.md").write_text(
        build_report(expected), encoding="utf-8"
    )
    print(f"Wrote {len(expected)} judgments")


if __name__ == "__main__":
    main()

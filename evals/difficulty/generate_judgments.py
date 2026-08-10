#!/usr/bin/env python3
"""Skill 判断基準に沿った 100 語 expected を生成する。"""

from __future__ import annotations

import json
from pathlib import Path

# (generalFamiliarity, engineerFamiliarity, contextualLearningNeeded,
#  nearestExamples, difficulty, confidence, notes)
JUDGMENTS: dict[str, tuple] = {
    # --- Beginner (21) ---
    "approach": (
        "high", "high", "low", ["approach", "feedback"], "Beginner", "High",
        "進め方・方針の一般語で、feedback と同様に実務でも意味が直感的に推測できる。",
    ),
    "approval": (
        "high", "medium", "low", ["feedback", "deadline"], "Beginner", "High",
        "承認という日常語で、deadline ほど頻出ではないが文脈から意味を推測しやすい。",
    ),
    "communication": (
        "high", "high", "low", ["feedback", "approach"], "Beginner", "High",
        "コミュニケーションは広く知られ、エンジニア会話でも feedback と同クラスの基本語。",
    ),
    "deadline": (
        "high", "high", "low", ["deadline", "feedback"], "Beginner", "High",
        "期限は代表例どおり一般・実務ともに高頻度で、feedback と並ぶ Beginner 基準語。",
    ),
    "failure": (
        "high", "high", "low", ["failure", "approach"], "Beginner", "High",
        "失敗・故障は一般語で、approach と同様に障害対応文脈でも直感理解できる。",
    ),
    "fetch": (
        "medium", "high", "low", ["fetch", "query"], "Beginner", "High",
        "HTTP の fetch は技術入門語だが、query と並ぶ代表例どおり意味は推測しやすい。",
    ),
    "insert": (
        "high", "high", "low", ["query", "fetch"], "Beginner", "High",
        "挿入は DB 操作でも日常語でも、query/fetch と同じ入門レベルの動詞。",
    ),
    "install": (
        "high", "high", "low", ["install", "fetch"], "Beginner", "High",
        "インストールは代表例どおり一般・実務ともに高頻度で fetch と同クラス。",
    ),
    "interaction": (
        "high", "medium", "low", ["approach", "feedback"], "Beginner", "Medium",
        "相互作用は一般語だが実務では UI/API 文脈に限定されがちで、feedback よりやや狭い。",
    ),
    "interface": (
        "medium", "high", "low", ["query", "fetch"], "Beginner", "High",
        "インターフェースは query/fetch と同じ技術入門語で、実務でも日常的に目にする。",
    ),
    "mentoring": (
        "medium", "medium", "low", ["feedback", "approach"], "Beginner", "Medium",
        "メンタリングはややビジネス語だが、feedback ほどではないものの学習コストは低い。",
    ),
    "operation": (
        "high", "high", "low", ["query", "fetch"], "Beginner", "High",
        "操作・運用は query と同様に実務基本語で、文脈学習の必要性は低い。",
    ),
    "prevent": (
        "high", "medium", "low", ["approach", "failure"], "Beginner", "High",
        "防止は failure/approach と並ぶ平易な動詞で、一般英語としても推測しやすい。",
    ),
    "profile": (
        "high", "medium", "low", ["query", "fetch"], "Beginner", "High",
        "プロファイルは設定画面で日常的に見る語で、query ほど技術的ではない。",
    ),
    "query": (
        "medium", "high", "low", ["query", "fetch"], "Beginner", "High",
        "クエリは SQL/API で fetch と並ぶ Beginner 代表例で、エンジニアには既知。",
    ),
    "recover": (
        "high", "medium", "low", ["failure", "approach"], "Beginner", "High",
        "回復・復旧は failure に近い一般語で、障害文脈でも意味が直感的。",
    ),
    "replace": (
        "high", "high", "low", ["replace", "fetch"], "Beginner", "High",
        "置換は代表例どおりコード・日常とも推測しやすく、fetch と同クラスの基本語。",
    ),
    "tension": (
        "high", "medium", "low", ["feedback", "approach"], "Beginner", "Medium",
        "緊張・対立は一般語だが、実務では比喩的意味もあり feedback より文脈依存がやや高い。",
    ),
    "trace": (
        "medium", "high", "low", ["query", "fetch"], "Beginner", "High",
        "トレースはログ・デバッグで fetch/query と同クラスの入門技術語。",
    ),
    "transaction": (
        "medium", "high", "low", ["query", "fetch"], "Beginner", "High",
        "トランザクションは DB 文脈で fetch 同等の入門語で、エンジニアには馴染み深い。",
    ),
    "feedback": (
        "high", "high", "low", ["feedback", "deadline"], "Beginner", "High",
        "一般語として広く知られ、エンジニア文脈でもカタカナ語感覚で理解しやすい。",
    ),
    # --- Intermediate (64) ---
    "abort": (
        "medium", "high", "medium", ["dispatch", "defer"], "Intermediate", "High",
        "中断・中止は技術文脈（abort 処理）で dispatch/defer と同様に実務用法の習得が必要。",
    ),
    "assertion": (
        "low", "medium", "medium", ["regression", "constraint"], "Intermediate", "Medium",
        "アサーションはテスト文脈で regression/constraint に近く、一般語としてはやや専門的。",
    ),
    "availability": (
        "medium", "high", "medium", ["scope", "defer"], "Intermediate", "Medium",
        "可用性は SRE 文脈で scope/defer と並び、一般語より実務での意味理解が重要。",
    ),
    "bypass": (
        "medium", "medium", "medium", ["defer", "dispatch"], "Intermediate", "Medium",
        "迂回・回避は defer/dispatch と同クラスで、実務での使い方に学習価値がある。",
    ),
    "capacity": (
        "medium", "medium", "medium", ["scope", "defer"], "Intermediate", "Medium",
        "容量・キャパシティは scope/defer と並び、一般語だが実務文脈での意味習得が必要。",
    ),
    "clarify": (
        "medium", "medium", "medium", ["clarify", "defer"], "Intermediate", "High",
        "一般語だが、実務では要件・仕様を明確にする用法の習得が必要。",
    ),
    "clone": (
        "medium", "high", "medium", ["dispatch", "defer"], "Intermediate", "High",
        "Git の clone は dispatch/defer と同様に技術文脈で頻出だが、一般英語としてはやや限定的。",
    ),
    "collaborate": (
        "medium", "medium", "medium", ["clarify", "defer"], "Intermediate", "Medium",
        "協力は一般語だが、実務では clarify/defer と同様にチーム文脈の用法を学ぶ価値がある。",
    ),
    "compress": (
        "medium", "medium", "medium", ["defer", "scope"], "Intermediate", "Medium",
        "圧縮は一般語だが、実務では defer/scope と同様に技術文脈での使い分けが必要。",
    ),
    "constraint": (
        "medium", "medium", "medium", ["constraint", "scope"], "Intermediate", "High",
        "制約は代表例どおり設計・要件文脈で scope と並び、実務用法の習得が必要。",
    ),
    "constructive": (
        "medium", "medium", "medium", ["clarify", "defer"], "Intermediate", "Medium",
        "建設的は一般語だが、フィードバック文脈では clarify/defer と同様に実務ニュアンスの学習が必要。",
    ),
    "coverage": (
        "medium", "high", "medium", ["regression", "scope"], "Intermediate", "Medium",
        "カバレッジはテスト文脈で regression/scope に近く、一般語より実務意味の理解が重要。",
    ),
    "criterion": (
        "medium", "medium", "medium", ["constraint", "scope"], "Intermediate", "Medium",
        "基準は constraint/scope と並ぶ設計語で、一般語だが実務文脈での用法習得が必要。",
    ),
    "critique": (
        "medium", "medium", "medium", ["clarify", "escalate"], "Intermediate", "Medium",
        "批評は clarify/escalate と同クラスで、一般語だがレビュー文脈での使い方に学習価値がある。",
    ),
    "deadlock": (
        "low", "high", "medium", ["regression", "constraint"], "Intermediate", "High",
        "デッドロックは一般語としては専門的だが、エンジニアには regression/constraint と並ぶ頻出語。",
    ),
    "decompose": (
        "medium", "medium", "medium", ["defer", "scope"], "Intermediate", "Medium",
        "分解は設計文脈で defer/scope と同様に、一般語だが実務での意味・用法を学ぶ必要がある。",
    ),
    "decrypt": (
        "medium", "high", "medium", ["dispatch", "defer"], "Intermediate", "High",
        "復号はセキュリティ文脈で dispatch/defer と同クラスの技術語で、実務用法の習得が必要。",
    ),
    "defer": (
        "medium", "medium", "medium", ["defer", "clarify"], "Intermediate", "High",
        "延期・委譲は代表例どおり clarify と並び、実務文脈での用法習得が必要。",
    ),
    "dependency": (
        "medium", "high", "medium", ["scope", "constraint"], "Intermediate", "High",
        "依存関係は scope/constraint と並ぶ設計語で、エンジニア文脈での意味理解が重要。",
    ),
    "deploy": (
        "medium", "high", "medium", ["dispatch", "defer"], "Intermediate", "High",
        "デプロイは dispatch/defer と同様に実務頻出だが、一般英語としてはやや限定的。",
    ),
    "dispatch": (
        "medium", "medium", "medium", ["dispatch", "defer"], "Intermediate", "High",
        "派遣・送出は代表例どおり defer と並び、実務文脈での用法習得が必要。",
    ),
    "encrypt": (
        "medium", "high", "medium", ["dispatch", "defer"], "Intermediate", "High",
        "暗号化は dispatch/defer と同クラスのセキュリティ語で、実務用法の習得が必要。",
    ),
    "enforce": (
        "medium", "medium", "medium", ["constraint", "defer"], "Intermediate", "Medium",
        "強制・適用は constraint/defer と並び、ポリシー文脈での実務用法を学ぶ価値がある。",
    ),
    "escalate": (
        "medium", "medium", "medium", ["escalate", "defer"], "Intermediate", "High",
        "エスカレーションは代表例どおり defer と並び、実務でのエスカレーション用法の習得が必要。",
    ),
    "expectations": (
        "medium", "medium", "medium", ["scope", "clarify"], "Intermediate", "Medium",
        "期待値は scope/clarify と同クラスで、要件・合意文脈での実務用法を学ぶ必要がある。",
    ),
    "implementation": (
        "medium", "high", "medium", ["scope", "defer"], "Intermediate", "High",
        "実装は scope/defer と並ぶ開発語で、一般語より実務文脈での意味理解が重要。",
    ),
    "index": (
        "medium", "high", "medium", ["query", "dispatch"], "Intermediate", "Medium",
        "インデックスは DB 文脈で query/dispatch に近く、一般語より実務での意味習得が必要。",
    ),
    "infrastructure": (
        "medium", "high", "medium", ["scope", "constraint"], "Intermediate", "High",
        "インフラは scope/constraint と並ぶ基盤語で、エンジニア文脈での意味理解が重要。",
    ),
    "inspect": (
        "medium", "medium", "medium", ["clarify", "defer"], "Intermediate", "Medium",
        "検査・確認は clarify/defer と同クラスで、デバッグ文脈での実務用法を学ぶ価値がある。",
    ),
    "invoke": (
        "medium", "high", "medium", ["dispatch", "defer"], "Intermediate", "High",
        "呼び出しは dispatch/defer と同様の技術語で、一般英語としてはやや限定的。",
    ),
    "isolate": (
        "medium", "medium", "medium", ["clarify", "regression"], "Intermediate", "Medium",
        "隔離は regression/clarify と並び、障害切り分け文脈での実務用法の習得が必要。",
    ),
    "latency": (
        "medium", "high", "medium", ["scope", "regression"], "Intermediate", "High",
        "レイテンシは scope/regression と並ぶ性能語で、エンジニア文脈での意味理解が重要。",
    ),
    "mandatory": (
        "medium", "medium", "medium", ["constraint", "defer"], "Intermediate", "Medium",
        "必須は constraint/defer と同クラスで、ポリシー・要件文脈での実務用法を学ぶ必要がある。",
    ),
    "monitor": (
        "medium", "high", "medium", ["dispatch", "scope"], "Intermediate", "High",
        "監視は dispatch/scope と並ぶ運用語で、一般語より実務文脈での意味理解が重要。",
    ),
    "objective": (
        "medium", "medium", "medium", ["scope", "clarify"], "Intermediate", "Medium",
        "目的は scope/clarify と同クラスで、要件・合意文脈での実務用法を学ぶ価値がある。",
    ),
    "optimize": (
        "medium", "high", "medium", ["scope", "regression"], "Intermediate", "High",
        "最適化は scope/regression と並ぶ性能語で、エンジニア文脈での意味理解が重要。",
    ),
    "overload": (
        "medium", "medium", "medium", ["constraint", "scope"], "Intermediate", "Medium",
        "過負荷は constraint/scope と並び、システム文脈での実務用法の習得が必要。",
    ),
    "ownership": (
        "medium", "high", "medium", ["scope", "escalate"], "Intermediate", "Medium",
        "オーナーシップは scope/escalate と同クラスで、チーム責任文脈での実務用法を学ぶ必要がある。",
    ),
    "pass": (
        "medium", "medium", "medium", ["regression", "defer"], "Intermediate", "Medium",
        "合格・通過は regression/defer と並び、テスト文脈での実務用法の習得が必要。",
    ),
    "pinpoint": (
        "medium", "medium", "medium", ["clarify", "defer"], "Intermediate", "Medium",
        "特定するは clarify/defer と同クラスで、障害調査文脈での実務用法を学ぶ価値がある。",
    ),
    "preload": (
        "medium", "medium", "medium", ["fetch", "dispatch"], "Intermediate", "Medium",
        "事前読み込みは fetch/dispatch に近い技術語で、実務文脈での用法習得が必要。",
    ),
    "priority": (
        "medium", "medium", "medium", ["scope", "defer"], "Intermediate", "Medium",
        "優先度は scope/defer と並び、タスク管理文脈での実務用法を学ぶ必要がある。",
    ),
    "progress": (
        "medium", "medium", "medium", ["defer", "scope"], "Intermediate", "Medium",
        "進捗は defer/scope と同クラスで、プロジェクト文脈での実務用法の習得が必要。",
    ),
    "readability": (
        "medium", "medium", "medium", ["clarify", "constraint"], "Intermediate", "Medium",
        "可読性は clarify/constraint と並び、コード品質文脈での実務用法を学ぶ価値がある。",
    ),
    "record": (
        "medium", "medium", "medium", ["dispatch", "defer"], "Intermediate", "Medium",
        "記録は dispatch/defer と同クラスで、ログ・監査文脈での実務用法の習得が必要。",
    ),
    "recovery": (
        "medium", "high", "medium", ["regression", "scope"], "Intermediate", "High",
        "復旧は regression/scope と並ぶ運用語で、一般語 recover より実務文脈が強い。",
    ),
    "regression": (
        "medium", "high", "medium", ["regression", "constraint"], "Intermediate", "High",
        "リグレッションは代表例どおり constraint と並び、テスト文脈での実務用法の習得が必要。",
    ),
    "reinforcement": (
        "medium", "medium", "medium", ["defer", "scope"], "Intermediate", "Medium",
        "強化は defer/scope と同クラスで、設計・学習文脈での実務用法を学ぶ必要がある。",
    ),
    "reject": (
        "medium", "medium", "medium", ["defer", "clarify"], "Intermediate", "Medium",
        "拒否は defer/clarify と並び、レビュー・API 文脈での実務用法の習得が必要。",
    ),
    "reliability": (
        "medium", "high", "medium", ["scope", "constraint"], "Intermediate", "Medium",
        "信頼性は scope/constraint と並ぶ SRE 語で、一般語より実務文脈での意味理解が重要。",
    ),
    "replication": (
        "medium", "high", "medium", ["regression", "scope"], "Intermediate", "High",
        "レプリケーションは regression/scope と並ぶ分散語で、エンジニア文脈での意味理解が重要。",
    ),
    "reproduce": (
        "medium", "high", "medium", ["regression", "isolate"], "Intermediate", "Medium",
        "再現は regression/isolate と並ぶ障害調査語で、Advanced 代表例 reproduce より実務頻度が高い。",
    ),
    "requirements": (
        "medium", "high", "medium", ["scope", "clarify"], "Intermediate", "High",
        "要件は scope/clarify と並ぶ開発語で、一般語より実務文脈での意味理解が重要。",
    ),
    "respectful": (
        "medium", "medium", "medium", ["clarify", "defer"], "Intermediate", "Medium",
        "敬意あるは clarify/defer と同クラスで、コミュニケーション文脈での実務用法を学ぶ価値がある。",
    ),
    "scalability": (
        "medium", "high", "medium", ["scope", "regression"], "Intermediate", "High",
        "スケーラビリティは scope/regression と並ぶ設計語で、エンジニア文脈での意味理解が重要。",
    ),
    "schema": (
        "medium", "high", "medium", ["constraint", "scope"], "Intermediate", "High",
        "スキーマは constraint/scope と並ぶ DB 語で、一般語より実務文脈での意味理解が重要。",
    ),
    "scope": (
        "medium", "medium", "medium", ["scope", "defer"], "Intermediate", "High",
        "スコープは代表例どおり defer と並び、プロジェクト文脈での実務用法の習得が必要。",
    ),
    "self-contained": (
        "medium", "medium", "medium", ["constraint", "scope"], "Intermediate", "Medium",
        "自己完結は constraint/scope と並び、設計文脈での実務用法を学ぶ必要がある。",
    ),
    "specification": (
        "medium", "high", "medium", ["constraint", "scope"], "Intermediate", "High",
        "仕様は constraint/scope と並ぶ開発語で、一般語より実務文脈での意味理解が重要。",
    ),
    "target": (
        "medium", "medium", "medium", ["scope", "defer"], "Intermediate", "Medium",
        "対象・目標は scope/defer と同クラスで、要件文脈での実務用法の習得が必要。",
    ),
    "trade-off": (
        "medium", "medium", "medium", ["trade-off", "scope"], "Intermediate", "High",
        "トレードオフは代表例どおり scope と並び、設計判断文脈での実務用法の習得が必要。",
    ),
    "unavailable": (
        "medium", "medium", "medium", ["defer", "scope"], "Intermediate", "Medium",
        "利用不可は defer/scope と同クラスで、可用性文脈での実務用法を学ぶ必要がある。",
    ),
    "validate": (
        "medium", "medium", "medium", ["regression", "clarify"], "Intermediate", "Medium",
        "検証は regression/clarify と並び、テスト・要件文脈での実務用法の習得が必要。",
    ),
    "velocity": (
        "medium", "high", "medium", ["scope", "defer"], "Intermediate", "High",
        "ベロシティは scope/defer と並ぶアジャイル語で、一般語より実務文脈での意味理解が重要。",
    ),
    # --- Advanced (15) ---
    "abstraction": (
        "medium", "high", "high", ["abstraction", "demonstrate"], "Advanced", "High",
        "抽象化は代表例どおり demonstrate と並び、概念の抽象度が高く文脈学習が必要。",
    ),
    "authenticate": (
        "medium", "high", "high", ["demonstrate", "abstraction"], "Advanced", "High",
        "認証は demonstrate/abstraction と同クラスで、セキュリティ文脈のニュアンス習得が必要。",
    ),
    "complexity": (
        "medium", "high", "high", ["abstraction", "demonstrate"], "Advanced", "High",
        "複雑性は abstraction/demonstrate と並び、抽象度が高く実務での意味・用法を深く学ぶ必要がある。",
    ),
    "consensus": (
        "low", "medium", "high", ["consensus", "discretion"], "Advanced", "High",
        "合意形成は代表例 discretion と並び、一般語としてはやや難しくニュアンス習得が必要。",
    ),
    "correctness": (
        "low", "medium", "high", ["abstraction", "demonstrate"], "Advanced", "High",
        "正当性・正しさは abstraction/demonstrate と並び、形式的手法の文脈で抽象度が高い。",
    ),
    "courteous": (
        "low", "low", "high", ["courteous", "scrutiny"], "Advanced", "High",
        "日常会話では uncommon。丁寧さのニュアンスを知らないと使い分けにくい。",
    ),
    "demonstrate": (
        "medium", "medium", "high", ["demonstrate", "abstraction"], "Advanced", "High",
        "実証・示すは代表例 abstraction と並び、技術文書での抽象的使用に学習価値がある。",
    ),
    "diagnose": (
        "medium", "medium", "high", ["demonstrate", "scrutiny"], "Advanced", "Medium",
        "診断は demonstrate/scrutiny と並び、障害分析文脈で scrutiny ほどではないが抽象用法がある。",
    ),
    "discretion": (
        "low", "low", "high", ["discretion", "scrutiny"], "Advanced", "High",
        "裁量・慎重さは代表例 scrutiny と並び、一般語としては uncommon でニュアンス習得が必要。",
    ),
    "functionality": (
        "low", "medium", "high", ["abstraction", "demonstrate"], "Advanced", "High",
        "機能性は abstraction/demonstrate と並び、一般語としてはやや堅く抽象度が高い。",
    ),
    "iterate": (
        "medium", "medium", "high", ["abstraction", "demonstrate"], "Advanced", "Medium",
        "反復は abstraction/demonstrate と並び、開発プロセス文脈で抽象的使用に学習価値がある。",
    ),
    "sanitize": (
        "low", "medium", "high", ["scrutiny", "discretion"], "Advanced", "High",
        "サニタイズは scrutiny/discretion と並び、セキュリティ文脈で一般語から離れた専門用法がある。",
    ),
    "scrutiny": (
        "low", "low", "high", ["scrutiny", "discretion"], "Advanced", "High",
        "精査は代表例 discretion と並び、一般語としては uncommon でニュアンス習得が必要。",
    ),
    "severity": (
        "medium", "medium", "high", ["scrutiny", "demonstrate"], "Advanced", "Medium",
        "深刻度は scrutiny/demonstrate と並び、インシデント文脈で抽象度の高い用法がある。",
    ),
    "validation": (
        "medium", "medium", "high", ["abstraction", "demonstrate"], "Advanced", "Medium",
        "妥当性確認は abstraction/demonstrate と並び、validate より形式・抽象度が高い。",
    ),
}


def build_entry(term: str, gf: str, ef: str, cl: str, ne: list[str], diff: str, conf: str, notes: str) -> dict:
    return {
        "term": term,
        "type": "word",
        "reasoning": {
            "generalFamiliarity": gf,
            "engineerFamiliarity": ef,
            "contextualLearningNeeded": cl,
            "nearestExamples": ne,
        },
        "difficulty": diff,
        "confidence": conf,
        "notes": notes,
    }


def build_expected() -> dict:
    out = {}
    for term in sorted(JUDGMENTS.keys()):
        gf, ef, cl, ne, diff, conf, notes = JUDGMENTS[term]
        out[term] = build_entry(term, gf, ef, cl, ne, diff, conf, notes)
    return out


def format_yaml_block(entry: dict) -> str:
    r = entry["reasoning"]
    ne = ", ".join(r["nearestExamples"])
    return (
        f'term: "{entry["term"]}"\n'
        f'type: "{entry["type"]}"\n'
        "reasoning:\n"
        f'  generalFamiliarity: {r["generalFamiliarity"]}\n'
        f'  engineerFamiliarity: {r["engineerFamiliarity"]}\n'
        f'  contextualLearningNeeded: {r["contextualLearningNeeded"]}\n'
        f"  nearestExamples: [{ne}]\n"
        f'difficulty: {entry["difficulty"]}\n'
        f'confidence: {entry["confidence"]}\n'
        f'notes: "{entry["notes"]}"'
    )


def build_report(expected: dict) -> str:
    blocks = []
    for term in sorted(expected.keys()):
        blocks.append("```yaml\n" + format_yaml_block(expected[term]) + "\n```")
    return "\n\n".join(blocks) + "\n"


def main() -> None:
    expected = build_expected()
    assert len(expected) == 100, len(expected)

    counts = {}
    for e in expected.values():
        counts[e["difficulty"]] = counts.get(e["difficulty"], 0) + 1
    assert counts == {"Beginner": 21, "Intermediate": 64, "Advanced": 15}, counts

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

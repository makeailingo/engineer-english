#!/usr/bin/env python3
"""2観点 + 固定決定表で 100 語 expected を生成する。"""

from __future__ import annotations

import json
from pathlib import Path

# generalFamiliarity キャリブレーション代表例（Skill と同一）
CALIBRATION: dict[str, list[str]] = {
    "high": ["feedback", "deadline", "replace"],
    "medium": ["clarify", "mandatory", "defer"],
    "low": ["courteous", "scrutiny", "discretion"],
}


def decide_difficulty(general: str, engineer: str) -> str:
    if general == "high" and engineer != "low":
        return "Beginner"
    if general == "low" and engineer == "low":
        return "Advanced"
    return "Intermediate"


# (generalFamiliarity, engineerFamiliarity, contextualLearningNeeded, confidence, notes)
JUDGMENTS: dict[str, tuple[str, str, str, str, str]] = {
    "abort": ("medium", "high", "medium", "High", "処理中断は技術語だが一般語の abort も知られており、engineer には既知。"),
    "abstraction": ("medium", "high", "high", "Medium", "抽象化は一般語としてはやや専門的だが、エンジニアには馴染み深い。"),
    "approach": ("high", "high", "low", "High", "進め方・方針は feedback と同様の一般語。"),
    "approval": ("high", "medium", "low", "High", "承認は日常語で general high。実務頻度は deadline ほどではない。"),
    "assertion": ("low", "medium", "medium", "Medium", "一般英語では uncommon。テスト文脈では engineer medium。"),
    "authenticate": ("medium", "high", "high", "Medium", "認証はセキュリティ文脈で engineer high だが general は medium。"),
    "availability": ("medium", "high", "medium", "High", "可用性は SRE 語彙で engineer high。一般語としては medium。"),
    "bypass": ("medium", "medium", "medium", "Medium", "迂回は一般語として知られるが実務用法に学習価値あり。"),
    "capacity": ("medium", "medium", "medium", "Medium", "容量は一般語だが実務文脈での意味習得が必要。"),
    "clarify": ("medium", "medium", "medium", "High", "明確にするは代表例 clarify/mandatory/defer に近い。"),
    "clone": ("medium", "high", "medium", "High", "複製は Git 文脈で engineer high。"),
    "collaborate": ("medium", "medium", "medium", "Medium", "協力は一般語だがビジネス用法に学習価値あり。"),
    "communication": ("high", "high", "low", "High", "コミュニケーションは広く知られる一般語。"),
    "complexity": ("medium", "high", "high", "Medium", "複雑性は CS 文脈で engineer high。"),
    "compress": ("medium", "medium", "medium", "Medium", "圧縮は一般語だが技術用法に学習価値あり。"),
    "consensus": ("low", "medium", "high", "Medium", "合意形成は一般語としてやや堅い。engineer は medium。"),
    "constraint": ("medium", "medium", "medium", "Medium", "制約は設計文脈で clarify/defer に近い。"),
    "constructive": ("medium", "medium", "medium", "Medium", "建設的は一般語だがレビュー文脈の用法に学習価値あり。"),
    "correctness": ("low", "medium", "high", "Medium", "正当性は形式的手法の語で general low。"),
    "courteous": ("low", "low", "high", "High", "丁寧さを表す語で代表例 courteous/scrutiny/discretion に近い。"),
    "coverage": ("medium", "high", "medium", "High", "カバレッジはテスト文脈で engineer high。"),
    "criterion": ("medium", "medium", "medium", "Medium", "基準は一般語だが単数形 criterion はやや堅い。"),
    "critique": ("medium", "medium", "medium", "Medium", "批評はレビュー文脈で clarify に近い。"),
    "deadline": ("high", "high", "low", "High", "期限は代表例 feedback/deadline/replace に近い。"),
    "deadlock": ("low", "high", "medium", "Medium", "デッドロックは一般語として low だが engineer には既知。"),
    "decompose": ("medium", "medium", "medium", "Medium", "分解は一般語だが設計文脈の用法に学習価値あり。"),
    "decrypt": ("medium", "high", "medium", "High", "復号はセキュリティ文脈で engineer high。"),
    "defer": ("medium", "medium", "medium", "High", "延期・委譲は代表例 defer/mandatory/clarify に近い。"),
    "demonstrate": ("medium", "medium", "high", "Medium", "実証するは一般語 medium。技術文書での用法に学習価値あり。"),
    "dependency": ("medium", "high", "medium", "High", "依存関係は開発文脈で engineer high。"),
    "deploy": ("medium", "high", "medium", "High", "デプロイは engineer high。一般語としては medium。"),
    "diagnose": ("medium", "medium", "high", "Medium", "診断するは一般語 medium。障害分析文脈に学習価値あり。"),
    "discretion": ("low", "low", "high", "High", "裁量・慎重さは代表例 discretion/scrutiny に近い。"),
    "dispatch": ("medium", "medium", "medium", "Medium", "派遣・送出は一般語だが実務用法に学習価値あり。"),
    "encrypt": ("medium", "high", "medium", "High", "暗号化はセキュリティ文脈で engineer high。"),
    "enforce": ("medium", "medium", "medium", "Medium", "強制するは一般語 medium。ポリシー文脈に学習価値あり。"),
    "escalate": ("medium", "medium", "medium", "High", "エスカレーションは clarify/defer と同クラス。"),
    "expectations": ("medium", "medium", "medium", "Medium", "期待は一般語だが要件文脈の用法に学習価値あり。"),
    "failure": ("high", "high", "low", "High", "失敗・故障は一般語として広く知られる。"),
    "feedback": ("high", "high", "low", "High", "一般語として広く知られ、エンジニア文脈でも理解しやすい。"),
    "fetch": ("medium", "high", "low", "High", "HTTP fetch は engineer high だが一般英語としては medium。"),
    "functionality": ("low", "medium", "high", "Medium", "機能性は一般語としてやや堅い formal 語。"),
    "implementation": ("medium", "high", "medium", "High", "実装は開発文脈で engineer high。"),
    "index": ("medium", "high", "medium", "High", "索引・インデックスは DB 文脈で engineer high。"),
    "infrastructure": ("medium", "high", "medium", "High", "インフラは SRE 文脈で engineer high。"),
    "insert": ("high", "high", "low", "High", "挿入は日常語・SQL 語ともに基本。"),
    "inspect": ("medium", "medium", "medium", "Medium", "検査するは一般語 medium。"),
    "install": ("high", "high", "low", "High", "インストールは一般・実務とも高頻度。"),
    "interaction": ("high", "medium", "low", "Medium", "相互作用は一般語 high。実務では UI 文脈に限定されがち。"),
    "interface": ("medium", "high", "medium", "High", "インターフェースは engineer high。"),
    "invoke": ("medium", "high", "medium", "High", "呼び出すはプログラミング文脈で engineer high。"),
    "isolate": ("medium", "medium", "medium", "Medium", "隔離は一般語 medium。障害調査文脈に学習価値あり。"),
    "iterate": ("medium", "medium", "high", "Medium", "反復は開発プロセス文脈に学習価値あり。"),
    "latency": ("medium", "high", "medium", "High", "レイテンシは SRE 文脈で engineer high。"),
    "mandatory": ("medium", "medium", "medium", "High", "必須は代表例 mandatory/clarify/defer に近い。"),
    "mentoring": ("medium", "medium", "low", "Medium", "メンタリングはややビジネス語。"),
    "monitor": ("medium", "high", "medium", "High", "監視は Ops 文脈で engineer high。"),
    "objective": ("medium", "medium", "medium", "Medium", "目的は一般語 medium。"),
    "operation": ("high", "high", "low", "High", "操作・運用は一般語 high。"),
    "optimize": ("medium", "high", "medium", "High", "最適化は engineer high。"),
    "overload": ("medium", "medium", "medium", "Medium", "過負荷は一般語 medium。"),
    "ownership": ("medium", "high", "medium", "High", "オーナーシップは SRE/チーム文脈で engineer high。"),
    "pass": ("medium", "medium", "medium", "Medium", "合格・通過は文脈依存で clarify に近い。"),
    "pinpoint": ("medium", "medium", "medium", "Medium", "特定するは一般語 medium。"),
    "preload": ("medium", "medium", "medium", "Medium", "事前読込は Web 文脈に学習価値あり。"),
    "prevent": ("high", "medium", "low", "High", "防止は一般語 high。"),
    "priority": ("medium", "medium", "medium", "Medium", "優先度は一般語 medium。"),
    "profile": ("high", "medium", "low", "Medium", "プロファイルは設定画面で見る一般語 high。"),
    "progress": ("medium", "medium", "medium", "Medium", "進捗は一般語 medium。"),
    "query": ("medium", "high", "low", "High", "クエリは SQL/API で engineer high。"),
    "readability": ("medium", "medium", "medium", "Medium", "可読性はコード品質文脈に学習価値あり。"),
    "record": ("medium", "medium", "medium", "Medium", "記録は一般語 medium。"),
    "recover": ("high", "medium", "low", "High", "回復は一般語 high。"),
    "recovery": ("medium", "high", "medium", "High", "復旧は SRE 文脈で engineer high。"),
    "regression": ("medium", "high", "medium", "High", "リグレッションはテスト文脈で engineer high。"),
    "reinforcement": ("medium", "medium", "medium", "Medium", "強化は一般語 medium。"),
    "reject": ("medium", "medium", "medium", "Medium", "拒否は PR 文脈に学習価値あり。"),
    "reliability": ("medium", "high", "medium", "High", "信頼性は SRE 文脈で engineer high。"),
    "replace": ("high", "high", "low", "High", "置換は代表例 replace/feedback/deadline に近い。"),
    "replication": ("medium", "high", "medium", "High", "レプリケーションは DB 文脈で engineer high。"),
    "reproduce": ("medium", "high", "medium", "High", "再現は障害調査文脈で engineer high。"),
    "requirements": ("medium", "high", "medium", "High", "要件は開発文脈で engineer high。"),
    "respectful": ("medium", "medium", "medium", "Medium", "敬意は一般語 medium。"),
    "sanitize": ("low", "medium", "high", "Medium", "サニタイズは一般語として uncommon。"),
    "scalability": ("medium", "high", "medium", "High", "スケーラビリティは engineer high。"),
    "schema": ("medium", "high", "medium", "High", "スキーマは DB 文脈で engineer high。"),
    "scope": ("medium", "medium", "medium", "Medium", "スコープは clarify/defer に近い。"),
    "scrutiny": ("low", "low", "high", "High", "精査は代表例 scrutiny/discretion に近い。"),
    "self-contained": ("medium", "medium", "medium", "Medium", "自己完結は設計文脈に学習価値あり。"),
    "severity": ("medium", "medium", "high", "Medium", "深刻度はインシデント文脈に学習価値あり。"),
    "specification": ("medium", "high", "medium", "High", "仕様は開発文脈で engineer high。"),
    "target": ("medium", "medium", "medium", "Medium", "目標は一般語 medium。"),
    "tension": ("high", "medium", "low", "Medium", "緊張・対立は一般語 high。"),
    "trace": ("medium", "high", "medium", "High", "トレースはログ文脈で engineer high。"),
    "trade-off": ("medium", "medium", "medium", "Medium", "トレードオフは境界語。代表例には入れない。"),
    "transaction": ("medium", "high", "medium", "High", "トランザクションは DB 文脈で engineer high。"),
    "unavailable": ("medium", "medium", "medium", "Medium", "利用不可は一般語 medium。"),
    "validate": ("medium", "medium", "medium", "Medium", "検証するは clarify/defer に近い。"),
    "validation": ("medium", "medium", "high", "Medium", "妥当性確認は形式的名詞で medium。"),
    "velocity": ("medium", "high", "medium", "High", "ベロシティはアジャイル文脈で engineer high。"),
}


def build_entry(term: str, gf: str, ef: str, cl: str, conf: str, notes: str) -> dict:
    diff = decide_difficulty(gf, ef)
    return {
        "term": term,
        "type": "word",
        "reasoning": {
            "generalFamiliarity": gf,
            "engineerFamiliarity": ef,
            "contextualLearningNeeded": cl,
        },
        "difficulty": diff,
        "confidence": conf,
        "notes": notes,
    }


def build_expected() -> dict:
    out = {}
    for term in sorted(JUDGMENTS.keys()):
        gf, ef, cl, conf, notes = JUDGMENTS[term]
        out[term] = build_entry(term, gf, ef, cl, conf, notes)
    return out


def format_yaml_block(entry: dict) -> str:
    r = entry["reasoning"]
    return (
        f'term: "{entry["term"]}"\n'
        f'type: "{entry["type"]}"\n'
        "reasoning:\n"
        f'  generalFamiliarity: {r["generalFamiliarity"]}\n'
        f'  engineerFamiliarity: {r["engineerFamiliarity"]}\n'
        f'  contextualLearningNeeded: {r["contextualLearningNeeded"]}\n'
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

    counts: dict[str, int] = {}
    for e in expected.values():
        counts[e["difficulty"]] = counts.get(e["difficulty"], 0) + 1
    print(f"Wrote {len(expected)} judgments: {counts}")

    out_dir = Path(__file__).parent
    (out_dir / "regression_expected.json").write_text(
        json.dumps(expected, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (out_dir / "judgments_100.md").write_text(
        build_report(expected), encoding="utf-8"
    )


if __name__ == "__main__":
    main()

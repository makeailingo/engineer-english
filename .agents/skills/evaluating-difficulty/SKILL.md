---
name: evaluating-difficulty
description: 固定の判断基準と代表例に基づき Vocabulary の difficulty を判定する。Vocabulary の作成・更新前に使用する。
---

# Evaluating Difficulty

外部データ（CEFR、TOEIC リスト等）を正解ラベルとしては使わない。  
**固定の判断基準と代表例** に基づき、理由を構造化してから Difficulty を決める。

## Difficulty 定義

| Difficulty | 目安 |
| --- | --- |
| Beginner | 一般的な英語、または日本人エンジニアが日常的に目にする語で、意味を推測しやすい |
| Intermediate | 一般語だが実務での意味・使い方に学習価値がある。または技術文脈で頻出だが、自然な英語としては少し難しい |
| Advanced | 一般的に難しい語、抽象度が高い語、または意味・ニュアンスを知らないと推測しにくい |

## 判断観点（3つ）

各観点を **low / medium / high** で短く評価する。数値化しない。

| 観点 | 問い |
| --- | --- |
| `generalFamiliarity` | 一般英語として、意味を推測しやすいか |
| `engineerFamiliarity` | 日本人ソフトウェアエンジニアが既知である可能性が高いか |
| `contextualLearningNeeded` | 実務文脈で意味・用法を学ぶ必要があるか |

## 判定手順

1. 上記 3 観点を評価する（`reasoning` に記録）。
2. 代表例と比較し、**最も近い Difficulty の語群**を選ぶ。
3. その Difficulty を採用する。
4. 迷う場合は **高い方** を選ぶ（理解に必要な知識が多い側）。

いきなりラベルを出さない。必ず `reasoning` → `difficulty` の順。

## 代表例

新しい語は、どの代表例に最も近いかで比較する。

### Beginner

`feedback`, `deadline`, `query`, `fetch`, `replace`, `install`, `approach`, `failure`

### Intermediate

`clarify`, `trade-off`, `defer`, `escalate`, `constraint`, `regression`, `dispatch`, `scope`

### Advanced

`courteous`, `scrutiny`, `discretion`, `abstraction`, `demonstrate`, `consensus`, `reproduce`

## Input

```yaml
term: "feedback"
type: "word" # word | phrase
```

## Output

```yaml
term: "feedback"
type: "word"
reasoning:
  generalFamiliarity: high
  engineerFamiliarity: high
  contextualLearningNeeded: low
  nearestExamples: [feedback, deadline]
difficulty: Beginner
confidence: High
notes: "一般語として広く知られ、エンジニア文脈でもカタカナ語感覚で理解しやすい。"
```

```yaml
term: "courteous"
type: "word"
reasoning:
  generalFamiliarity: low
  engineerFamiliarity: low
  contextualLearningNeeded: high
  nearestExamples: [courteous, scrutiny]
difficulty: Advanced
confidence: High
notes: "日常会話では uncommon。丁寧さのニュアンスを知らないと使い分けにくい。"
```

```yaml
term: "clarify"
type: "word"
reasoning:
  generalFamiliarity: medium
  engineerFamiliarity: medium
  contextualLearningNeeded: medium
  nearestExamples: [clarify, defer]
difficulty: Intermediate
confidence: High
notes: "一般語だが、実務では要件・仕様を明確にする用法の習得が必要。"
```

## Confidence

- `High`: 3 観点が一貫し、代表例との近さが明確。
- `Medium`: 2 観点で迷いがあるが、代表例の比較で決められる。
- `Low`: 観点が割れ、代表例間でも判断が分かれる。`notes` に理由を記録する。

## 回帰確認

判断基準や代表例を変更したときは、代表例と既知の不整合候補を含む約 100 語で回帰確認する。

回帰スクリプト: `evals/difficulty/run_regression.py`

## Vocabulary への反映

Eval 結果の `difficulty` を Vocabulary の Front Matter に転記する。  
`reasoning` は Eval の中間出力として残してよいが、Vocabulary 本体には載せない。  
`source` には引き続き Engineering 一次資料のみを記録する（[researching-vocabulary](.agents/skills/researching-vocabulary/SKILL.md) に従う）。

## やらないこと

- CEFR / TOEIC / 外部語彙リストを正解ラベルとして使う
- 観点を数値化して機械的に足し合わせる
- 外部データ未取得を理由に判定をスキップする（代表例との比較で決める）

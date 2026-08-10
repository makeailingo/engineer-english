---
name: evaluating-difficulty
description: 2観点の評価と固定決定表で Vocabulary の difficulty を判定する。Vocabulary の作成・更新前に使用する。
---

# Evaluating Difficulty

外部データ（CEFR、TOEIC リスト等）を正解ラベルとしては使わない。  
AI は **2つの観点だけ** を評価し、**Difficulty は固定決定表** で決める。

## 判断観点（2つ）

各観点を **low / medium / high** で評価する。

| 観点 | 問い |
| --- | --- |
| `generalFamiliarity` | 一般的な英語として、意味を推測しやすいか |
| `engineerFamiliarity` | 日本人ソフトウェアエンジニアが、英単語として意味を理解している可能性が高いか |

## 決定表（Difficulty）

観点評価のあと、次の表だけで Difficulty を決める。例外解釈はしない。

| 条件 | Difficulty |
| --- | --- |
| `generalFamiliarity` = high **かつ** `engineerFamiliarity` ≠ low | Beginner |
| `generalFamiliarity` = low **かつ** `engineerFamiliarity` = low | Advanced |
| 上記以外 | Intermediate |

## 代表例（キャリブレーション）

代表例は **観点評価の基準** として使う。Difficulty を直接決めない。

`generalFamiliarity` の代表例:

| 値 | 代表例 |
| --- | --- |
| high | `feedback`, `deadline`, `replace` |
| medium | `clarify`, `mandatory`, `defer` |
| low | `courteous`, `scrutiny`, `discretion` |

境界語（例: `trade-off`）は代表例に入れない。

## 判定手順

1. 代表例を参考に `generalFamiliarity` を評価する。
2. 代表例を参考に `engineerFamiliarity` を評価する。
3. **決定表** で Difficulty を決める。
4. `confidence` を付与する。
5. 必要なら `contextualLearningNeeded` を記録する（Difficulty 判定には使わない）。

いきなり Difficulty を出さない。必ず `reasoning` → `difficulty` の順。

## contextualLearningNeeded

Difficulty を決める入力には **使わない**。  
記録のみ。将来の学習価値・収録優先度などに使う。

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
difficulty: Beginner
confidence: High
notes: "一般語として広く知られ、エンジニア文脈でも理解しやすい。"
```

```yaml
term: "clarify"
type: "word"
reasoning:
  generalFamiliarity: medium
  engineerFamiliarity: medium
  contextualLearningNeeded: medium
difficulty: Intermediate
confidence: High
notes: "一般語だが実務での用法に学習価値がある。代表例 mandatory/defer に近い。"
```

```yaml
term: "courteous"
type: "word"
reasoning:
  generalFamiliarity: low
  engineerFamiliarity: low
  contextualLearningNeeded: high
difficulty: Advanced
confidence: High
notes: "日常会話では uncommon。代表例 scrutiny/discretion と同クラス。"
```

## Confidence

- `High`: 2観点と代表例から明確に評価できる。
- `Medium`: どちらかの観点が境界的だが、決定表で判定できる。
- `Low`: `generalFamiliarity` / `engineerFamiliarity` 自体の評価に迷う。

`confidence` が Low でも、Difficulty は決定表に従って出す。`notes` に迷いを記録する。

## 回帰確認

判断基準や決定表を変更したときは、約 100 語で回帰確認する。

- **Golden Cases**（明らかな期待値）が決定表どおりか
- **前回 baseline との差分**（何語が Beginner → Intermediate など）

回帰スクリプト: `evals/difficulty/run_regression.py`

## Vocabulary への反映

Eval 結果の `difficulty` を Vocabulary の Front Matter に転記する。  
`reasoning` は Eval の中間出力として残してよいが、Vocabulary 本体には載せない。

## やらないこと

- CEFR / TOEIC / 外部語彙リストを正解ラベルとして使う
- 代表例との類似度で Difficulty を直接決める
- `contextualLearningNeeded` を Difficulty 判定に使う
- 迷ったら高い方を選ぶ

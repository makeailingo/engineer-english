---
name: evaluating-difficulty
description: 2観点の評価と判定ルールで Vocabulary の difficulty を決める。Vocabulary の作成・更新前に使用する。
---

# Evaluating Difficulty

Vocabulary の `difficulty` は、CEFR・TOEIC 等の外部語彙リストでは決めない。  
2つの観点を評価し、下記の判定ルールで Beginner / Intermediate / Advanced を決める。

## Difficulty 定義

| Difficulty | 目安 |
| --- | --- |
| Beginner | 一般語として広く知られ、エンジニアも意味を推測しやすい |
| Intermediate | 一般語だが実務での用法に学習価値がある、または技術文脈で頻出する |
| Advanced | 一般英語として日常的に使われず、エンジニアも英単語としては馴染みが薄い |

## 判断観点

各観点を **low / medium / high** で評価する。

| 観点 | 問い |
| --- | --- |
| `generalFamiliarity` | 一般的な英語として、意味を推測しやすいか |
| `engineerFamiliarity` | 日本人ソフトウェアエンジニアが、英単語として意味を理解している可能性が高いか |

## 判定ルール

観点評価のあと、次のルールだけで Difficulty を決める。**例外解釈はしない。**

| 条件 | Difficulty |
| --- | --- |
| `generalFamiliarity` = high **かつ** `engineerFamiliarity` ≠ low | Beginner |
| `generalFamiliarity` = low **かつ** `engineerFamiliarity` = low | Advanced |
| 上記以外 | Intermediate |

## 代表例

代表例は観点評価の **参考** に使う。Difficulty は代表例から直接決めない。

### generalFamiliarity

| 値 | 代表例 |
| --- | --- |
| high | `feedback`, `deadline`, `replace` |
| medium | `clarify`, `mandatory`, `defer` |
| low | `courteous`, `scrutiny`, `discretion` |

判定が分かれやすい語（例: `trade-off`）は代表例に入れない。

## 手順

1. 代表例を参考に `generalFamiliarity` を評価する
2. 代表例を参考に `engineerFamiliarity` を評価する
3. 判定ルールで Difficulty を決める
4. `confidence` を付与する
5. 任意で `contextualLearningNeeded` を記録する（Difficulty 判定には使わない）

`reasoning` を先に書き、その後 `difficulty` を書く。

## contextualLearningNeeded

Difficulty 判定には使わない。記録のみ（将来の学習価値・収録優先度などに利用）。

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
notes: "一般語だが、実務での用法に学習価値がある。"
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
notes: "日常会話ではあまり使われない。丁寧さのニュアンスを知らないと使い分けにくい。"
```

## Confidence

- `High`: 2観点と代表例から明確に評価できる
- `Medium`: どちらかの観点が境界的だが、判定ルールで決められる
- `Low`: 2観点自体の評価に迷う

`confidence` が Low でも、Difficulty は判定ルールに従って出す。`notes` に迷いを記録する。

## Vocabulary への反映

評価結果の `difficulty` を Vocabulary の YAML Front Matter に転記する。  
`reasoning` は中間出力として残してよいが、Vocabulary 本体には載せない。

## 禁止事項

- 外部語彙リストを正解ラベルとして使う
- 代表例との類似度で Difficulty を直接決める
- `contextualLearningNeeded` を Difficulty 判定に使う
- 迷ったら高い方を選ぶ

## 文言

Skill 本文では、一般的でない専門用語を使わない（例: 固定決定表、uncommon）。

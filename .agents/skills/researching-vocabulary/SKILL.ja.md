---
name: researching-vocabulary
description: ソフトウェアエンジニア自身が英語で働く中で見聞きした語彙について、意味・品詞・英語の発音記号を辞書で確認する。Vocabularyの作成・更新前に使用する。
---
# Researching Vocabulary

> English: [SKILL.md](SKILL.md)

## 辞書

- 確認に使う辞書: [Cambridge Dictionary](https://dictionary.cambridge.org/dictionary/english/)
- 照合に使う辞書: [Oxford Advanced Learner's Dictionary](https://www.oxfordlearnersdictionaries.com/definition/english/)

Cambridgeでは品詞、意味ごとの定義、発音記号を同じ項目で確認できる。Oxfordでは発音と意味を別の辞書で照合できる。

## Input

```yaml
term: "address"
observedUsage: "<英語で働く中で実際に見聞きした使われ方>"
```

## Workflow

1. `observedUsage`を読み、対象語がどの意味で使われていたかを特定する。
2. Cambridgeで対象語の品詞と意味を確認する。
3. Cambridgeで英語の発音記号を確認する。
4. `observedUsage`に一致する意味を選ぶ。
5. 選んだ意味に限定して、自然で簡潔な日本語訳を作成する。
6. Oxfordで品詞、意味、英語の発音記号を照合し、不一致がないか確認する。
7. 各Vocabularyを確定する前に、`evaluating-meaningJa`のルールを適用する。

   特に次の点を確認する。

   - `meaningJa`は、日本人学習者が英語の意味を理解できる内容にする。
   - カタカナ表記だけを意味として記載しない。
   - カタカナを残す場合は、役に立つ日本語の説明を添える。
   - 説明は簡潔にし、`usageExample`で使われている意味に合わせる。

   例:

   NG:
   blocker → ブロッカー
   backlog → バックログ
   on-call → オンコール

   OK:
   blocker → 作業の進行を妨げる問題、ブロッカー
   backlog → 未着手の作業や要望の一覧、バックログ
   on-call → 障害対応のため待機する当番、オンコール

不一致を解消できない場合は推測せず、`confidence: Low`として理由を示す。

## Output

```yaml
partOfSpeech: "<選んだ意味に対応する品詞>"
meaning: "<observedUsageに合う簡潔な英語の意味>"
meaningJa: "<選んだ意味の自然な日本語訳>"
description: "<使われ方をまとめた簡潔な英語の説明>"
pronunciation: "<英語の発音記号>"
confidence: "<High | Medium | Low>"
notes: "<必要な場合のみ、不確かな点と理由>"
```

## Confidence

- `High`: 2つの辞書で、選んだ意味、品詞、発音記号に不一致がない。
- `Medium`: 選んだ意味は一致しているが、表記や発音に差がある。
- `Low`: 必須情報が不足している、または不一致を解消できない。Vocabularyには採用しない。

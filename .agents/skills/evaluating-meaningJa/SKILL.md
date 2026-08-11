---
name: evaluating-meaningJa
description: meaningJa が日本語の学習者向け意味説明として成立しているか評価する。Vocabulary の作成・更新前、または meaningJa の検証時に使用する。
---

# Evaluating MeaningJa

Evaluate whether `meaningJa` works as a useful Japanese explanation
for a Japanese software engineer learning English.

## Goal

`meaningJa` must explain the English meaning.

It must not merely transliterate the English term into katakana.

The learner should be able to understand the word's practical meaning
from `meaningJa` even if they do not already know the English term.

## Input

```yaml
term: "blocker"
meaningJa: "ブロッカー"
usageExample: "This dependency is a release blocker."
usageExampleJa: "この依存はリリースブロッカーです。"
```

## Evaluation

Return FAIL when any of the following applies.

### 1. Katakana-only translation

FAIL:

* blocker → ブロッカー
* backlog → バックログ
* on-call → オンコール
* cold-start → コールドスタート

These do not explain the meaning.

### 2. Katakana is included, but no useful Japanese meaning is provided

FAIL:

* epic → エピック
* triage → トリアージ
* feature-flag → フィーチャーフラグ

PASS:

* blocker → 作業の進行を妨げる問題、ブロッカー
* backlog → 未着手の作業や要望の一覧、バックログ
* on-call → 障害対応のため待機する当番、オンコール
* cold-start → 停止状態からの初回起動、コールドスタート
* triage → 問題の緊急度を判断して優先順位を付けること、トリアージ
* feature-flag → 機能の有効・無効を切り替える設定、フィーチャーフラグ

### 3. Japanese explanation is unnatural or misleading

FAIL when:

* the Japanese is unnatural
* the translation uses the wrong sense
* the explanation is too vague to understand the intended meaning
* the explanation is inconsistent with `usageExample`

Examples:

* lifecycle → 寿命周期
* systemic → 体系的な

### 4. Part of speech and Japanese meaning do not match

Example:

```yaml
partOfSpeech: noun
meaningJa: "集約する"
```

FAIL because the Japanese translation is verbal while the entry is a noun.

## Rules

* Katakana itself is allowed.
* Do not FAIL merely because `meaningJa` contains katakana.
* Prefer:
  `plain Japanese meaning, established katakana term`
* If plain Japanese alone is natural and sufficient, katakana is unnecessary.
* Do not turn `meaningJa` into a long technical definition.
* Keep the explanation concise.
* Evaluate the intended sense shown by `usageExample`.
* Do not evaluate another possible sense of the term.
* Do not change `term`, `difficulty`, or `scene`.

## Decision criterion

Ask:

> If a Japanese software engineer does not already know this English term,
> can they understand its intended meaning from `meaningJa`?

If no, FAIL.

## Output

```yaml
result: FAIL
term: "blocker"
currentMeaningJa: "ブロッカー"
expectedMeaningJa: "作業の進行を妨げる問題、ブロッカー"
reason: "The current Japanese only transliterates the English term and does not explain its meaning."
```

For PASS:

```yaml
result: PASS
term: "baseline"
currentMeaningJa: "基準値、ベースライン"
reason: "The Japanese explains the meaning while preserving the established katakana term."
```

## 文言

Skill 本文では、一般的でない専門用語を使わない。

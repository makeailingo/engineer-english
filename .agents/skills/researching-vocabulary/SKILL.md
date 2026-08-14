---
name: researching-vocabulary
description: Check meaning, part of speech, and English IPA for a term personally heard or seen by a software engineer working in English. Use before creating or updating Vocabulary.
---

# Researching Vocabulary

> Japanese: [SKILL.ja.md](SKILL.ja.md)

## Dictionaries

- Check in: [Cambridge Dictionary](https://dictionary.cambridge.org/dictionary/english/)
- Cross-check in: [Oxford Advanced Learner's Dictionary](https://www.oxfordlearnersdictionaries.com/definition/english/)

Cambridge provides parts of speech, definitions for each meaning, and IPA in one entry. Oxford provides an independent cross-check of pronunciation and meaning.

## Input

```yaml
term: "address"
observedUsage: "<how the term was heard or seen while working in English>"
```

## Workflow

1. Read `observedUsage` and identify the intended meaning.
2. Confirm the part of speech and meanings in Cambridge.
3. Confirm the English IPA in Cambridge.
4. Select the dictionary meaning that matches `observedUsage`.
5. Write a natural, concise Japanese translation for that meaning.
6. Cross-check the part of speech, meaning, and English IPA in Oxford.
7. Before finalizing each vocabulary item, apply the evaluating-meaningJa rules.

   In particular:

   - `meaningJa` must explain the English meaning to a Japanese learner.
   - `meaning` must state the adopted English sense concisely for learners.
   - `description` must summarize professional usage in English within 120 characters.
   - Do not use katakana transliteration alone as the meaning.
   - Katakana may be retained only when accompanied by a useful Japanese explanation.
   - Keep explanations concise and aligned with the intended sense in `usageExample`.

   Examples:

   NG:
   blocker → ブロッカー
   backlog → バックログ
   on-call → オンコール

   OK:
   blocker → 作業の進行を妨げる問題、ブロッカー
   backlog → 未着手の作業や要望の一覧、バックログ
   on-call → 障害対応のため待機する当番、オンコール

If inconsistencies cannot be resolved, do not guess. Set `confidence: Low` and explain why.

## Output

```yaml
partOfSpeech: "<part of speech for the adopted sense>"
meaning: "<concise English meaning matching observedUsage>"
meaningJa: "<natural Japanese translation of the adopted meaning>"
description: "<concise English note on how the term is used>"
pronunciation: "<English IPA>"
confidence: "<High | Medium | Low>"
notes: "<reason for uncertainty, when needed>"
```

## Confidence

- `High`: both dictionaries support the selected meaning, part of speech, and IPA
- `Medium`: the selected meaning agrees, but notation or pronunciation differs
- `Low`: required information is missing, or inconsistencies cannot be resolved. Do not adopt the entry.

Copy `meaning` and `description` into Vocabulary front matter.

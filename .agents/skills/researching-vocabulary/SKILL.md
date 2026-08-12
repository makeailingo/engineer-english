---
name: researching-vocabulary
description: Research part of speech, sense, US English IPA, and software-development usage from multiple sources. Use before creating or updating Vocabulary.
---

# Researching Vocabulary

> Japanese: [SKILL.ja.md](SKILL.ja.md)

## Dictionaries

- Primary dictionary: [Cambridge Dictionary](https://dictionary.cambridge.org/dictionary/english/)
- Cross-check dictionary: [Oxford Advanced Learner's Dictionary](https://www.oxfordlearnersdictionaries.com/definition/english/)

Cambridge provides part of speech, sense-specific definitions, and US English IPA in one entry. It is learner-oriented and corpus-based, so use it as the primary dictionary source. Oxford provides General American IPA, senses, and examples independently, so use it for cross-checking.

## Input

```yaml
term: "address"
```

## Workflow

1. Confirm the part of speech in Cambridge.
2. Confirm general senses and sense divisions in Cambridge.
3. Confirm US English IPA in Cambridge.
4. Confirm professional usage in an approved primary source: Google Engineering Practices, explicitly licensed Google SRE CC BY 4.0 materials, MDN Web Docs, or Amazon Jobs Interview Prep.
5. Identify which dictionary senses are actually used in the software development context from those primary sources.
6. For the adopted sense only, write a natural, concise Japanese translation.
7. Cross-check part of speech, sense, and US English IPA in Oxford.
8. Before finalizing each vocabulary item, apply the evaluating-meaningJa rules.

   In particular:

   - `meaningJa` must explain the English meaning to a Japanese learner.
   - `meaning` must state the adopted English sense concisely for learners.
   - `description` must summarize professional usage in English within 80 characters.
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

Do not decide from search-result snippets alone. Open each page and verify. If inconsistencies cannot be resolved, do not guess; set `confidence: Low` and explain why.

## Source Handling

Follow the primary-source categories in the vocabulary-markdown rule. Amazon Jobs Interview Prep is a usage-verification-only source because no open license has been identified. Use it only to confirm that a term appears in an engineering context.

For an Amazon Jobs source:

- Do not copy, translate, summarize, or adapt its body text, examples, or questions.
- Write all learner-facing fields and `source.context` independently.
- Set `source.license` to `No open license identified`.

## Output

```yaml
partOfSpeech: "<part of speech for the adopted sense>"
meaning: "<concise English sense for software development>"
meaningJa: "<Japanese translation for the software development sense>"
description: "<concise English note on professional usage>"
pronunciation: "<US English IPA>"
engineeringSense: "<same sense as meaning; intermediate output>"
sources:
  - role: primaryDictionary
    title: "<Cambridge entry title>"
    url: "<verified URL>"
  - role: crossCheckDictionary
    title: "<Oxford entry title>"
    url: "<verified URL>"
  - role: engineeringPrimary
    title: "<primary source page title>"
    url: "<verified URL>"
    license: "<license>"
    context: "<concise Japanese summary of professional usage>"
confidence: "<High | Medium | Low>"
```

## Confidence

- `High`: part of speech, sense, and IPA agree across both dictionaries and the primary source
- `Medium`: senses agree but notation differs, or the primary-source example is indirect
- `Low`: required information is missing, or inconsistencies cannot be resolved. Do not adopt the entry.

Keep dictionary URLs in intermediate output. Copy only `engineeringPrimary` into Vocabulary `source`.

Copy `meaning` and `description` into Vocabulary front matter.

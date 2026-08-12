# Engineer English

> Japanese: [AGENTS.ja.md](AGENTS.ja.md)

A dataset of English used in day-to-day software engineering work.

## Concept

- Extract words and phrases actually used in software engineering from reliable primary sources. Open-license sources are Google Engineering Practices, explicitly licensed Google SRE CC BY 4.0 materials, and MDN Web Docs. Amazon Jobs Interview Prep is a usage-reference source because no open license has been identified.
- Obtain senses, parts of speech, and US English IPA pronunciation from reliable external dictionaries (primary: Cambridge Dictionary; cross-check: Oxford Advanced Learner's Dictionary).
- Classify difficulty into three levels:
  - **Beginner**: widely known general vocabulary; engineers can infer the meaning easily
  - **Intermediate**: general vocabulary with learning value in professional use, or frequent in technical contexts
  - **Advanced**: uncommon in everyday English; even engineers are unlikely to know the word as English vocabulary
- Write learner-facing content independently. Do not copy, translate, summarize, or adapt source text from usage-reference materials.

## Working Rules

- Create and update Vocabulary entries according to the [vocabulary-markdown rule](.agents/rules/vocabulary-markdown.md).
- Research parts of speech, senses, and pronunciation with the [researching-vocabulary Skill](.agents/skills/researching-vocabulary/SKILL.md).
- Assign difficulty with the [evaluating-difficulty Skill](.agents/skills/evaluating-difficulty/SKILL.md).
- Assign scene with the [evaluating-scene Skill](.agents/skills/evaluating-scene/SKILL.md).
- Evaluate `meaningJa` with the [evaluating-meaningJa Skill](.agents/skills/evaluating-meaningJa/SKILL.md).
- Write and review Japanese text with the [japanese-tech-writing Skill](.agents/skills/japanese-tech-writing/SKILL.md).
- Sort and renumber vocabulary with the [sorting-vocabulary Skill](.agents/skills/sorting-vocabulary/SKILL.md).
- Follow branch and commit conventions with the [git-commit Skill](.agents/skills/git-commit/SKILL.md).

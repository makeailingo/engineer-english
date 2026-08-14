# Vocabulary Markdown

> Japanese: [vocabulary-markdown.ja.md](vocabulary-markdown.ja.md)

Scope: `docs/vocabulary/**/*.md`

- One entry per file. Name files `<id>_<term>.md`. Use lowercase kebab-case for the `term` segment.
- Copy `docs/templates/vocabulary.md` and fill every YAML front matter field.
- Follow the researching-vocabulary Skill for sense, part of speech, and pronunciation.
- Follow the evaluating-difficulty Skill for `difficulty`.
- Follow the evaluating-scene Skill for `scene`.
- Follow the evaluating-meaningJa Skill for `meaningJa`.
- Use unique 4-digit IDs from `"0001"` through `"9999"`. The `id` reflects display and learning order.
- Follow the [sorting-vocabulary Skill](.agents/skills/sorting-vocabulary/SKILL.md) for learning order. Sort entries by Scene (Career / Interview → Implementation / Review → Meetings / Events → Design / Architecture → Incident Response → Technical Writing → Management), then within each Scene by difficulty → learning value → practical frequency, and renumber IDs.
- Set `type` to `word` or `phrase`.
- Choose one value each for `difficulty` and `scene` from the masters below.
- Add only terms that a software engineer has personally heard or seen while working in English.
- Write meanings, descriptions, translations, and usage examples independently.
- Do not copy workplace messages, documents, meeting notes, or conversations. Remove company, product, project, customer, and individual names.
- Keep `meaning`, `description`, `usageExample`, `meaningJa`, `descriptionJa`, `usageExampleJa`, and `scene` semantically aligned.
- Limit `description` to 120 characters.
- Limit `descriptionJa` to 80 characters.
- Limit `usageExample` to 25 words.
- Limit `usageExampleJa` to 80 characters.
- Treat these limits as upper bounds for readability, not targets for truncation. Prefer one natural, complete sentence over cutting words to fit.
- Usage examples must be natural, concrete expressions informed by how the term was actually heard or seen. The target term's meaning must be clear from context.
- Follow the [japanese-tech-writing Skill](.agents/skills/japanese-tech-writing/SKILL.md) when writing or reviewing `usageExampleJa`.
- Check for duplicates against existing Vocabulary before creating a new entry.
- Prefer reusable phrases over one-off PR wording. Each entry should survive a project change: if replacing nouns with `A`, `B`, or a generic role still yields a useful engineering phrase, keep it; if generalization would make it trivial or meaningless, remove or rewrite it instead of copying the original PR sentence.

## Reusability

Ask whether another engineer could reuse the phrase in a different project by swapping nouns for `A`, `B`, or a generic role. Keep phrases at that level of abstraction. Delete or rewrite entries that only make sense in one original PR or ticket.

## Field Order

1. `id`
2. `term`
3. `type`
4. `partOfSpeech`
5. `pronunciation`
6. `description`
7. `descriptionJa`
8. `meaning`
9. `meaningJa`
10. `usageExample`
11. `usageExampleJa`
12. `difficulty`
13. `scene`

The Jekyll layout renders bilingual section headings from these fields. Do not duplicate field values in the Markdown body.

## Difficulty Master

| English | Japanese | Guideline |
| --- | --- | --- |
| Beginner | 初級 | Widely known general vocabulary; engineers can infer the meaning easily |
| Intermediate | 中級 | General vocabulary with learning value in professional use, or frequent in technical contexts |
| Advanced | 上級 | Uncommon in everyday English; even engineers are unlikely to know the word as English vocabulary |

Follow the [evaluating-difficulty Skill](.agents/skills/evaluating-difficulty/SKILL.md) for `difficulty`.

Follow the [evaluating-scene Skill](.agents/skills/evaluating-scene/SKILL.md) for `scene`.

Follow the [evaluating-meaningJa Skill](.agents/skills/evaluating-meaningJa/SKILL.md) for `meaningJa`.

## Reviewing usageExampleJa

When creating, editing, or reviewing `usageExampleJa`, read the [japanese-tech-writing Skill](.agents/skills/japanese-tech-writing/SKILL.md) and revise accordingly.

At minimum, check:

- The Japanese matches `usageExample`. Polysemous English terms (`commit`, `drain`, `prune`, etc.) are not mistranslated.
- The 80-character limit is met without noun chains missing particles (e.g. 「API不可時」).
- Request and question tone matches English (`Please` / `Could you` are not flattened to 「〜してください」 alone).
- Established translations are used (`cooldown` → クールダウン, `liveness probe` → ライブネスプローブ, `footprint` → フットプリント, etc.).
- Terminology is consistent within the dataset (レイテンシ / レイテンシー, デプロイ / 配備, etc.).
- There are no LLM-style filler phrases, em dashes, middle-dot lists, or isolated イ-adjective + 「です」 sentences.

## Scene Master

| English | Japanese |
| --- | --- |
| Career / Interview | 転職・面接 |
| Implementation / Review | 実装・コードレビュー |
| Meetings / Events | 会議・イベント |
| Design / Architecture | 設計・アーキテクチャ |
| Incident Response | 障害対応 |
| Technical Writing | テクニカルライティング |
| Management | マネジメント |

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
- Record one verified primary source in `source` using the Source Schema below.
- Write Japanese translations, explanations, and usage examples independently. Do not copy or adapt source text.
- Keep `meaning`, `description`, `usageExample`, `meaningJa`, `descriptionJa`, `usageExampleJa`, `scene`, and `source.context` semantically aligned.
- Limit `description` to 80 characters.
- Limit `descriptionJa` to 40 characters.
- Limit `usageExample` to 10 words.
- Limit `usageExampleJa` to 40 characters.
- Usage examples must be natural, concrete professional expressions where the target term's meaning is clear from context.
- Follow the [japanese-tech-writing Skill](.agents/skills/japanese-tech-writing/SKILL.md) when writing or reviewing `usageExampleJa`.
- Check for duplicates against existing Vocabulary before creating a new entry.

## Field Order

YAML front matter is the single source of truth. Use this field order:

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
14. `source`

The Jekyll layout renders bilingual section headings from these fields. Do not duplicate field values in the Markdown body.

## Source Schema

`source` is a single object with four required attributes:

| Attribute | Content |
| --- | --- |
| `title` | Official page title of the primary source |
| `url` | Public URL where usage of the target term was verified |
| `license` | License name stated on the primary source, or `No open license identified` when no open license is identified |
| `context` | Concise Japanese summary of the software development context in which the term appears |

Do not quote the source at length in `context`. Include enough detail to judge why the entry was accepted.

## Primary Sources

Primary sources are divided into two categories according to their licenses.

### A. Open-license materials

| Provider | Official URL | Main use | License | Handling |
| --- | --- | --- | --- | --- |
| Google Engineering Practices | https://google.github.io/eng-practices/ | Code review, design, development communication | CC BY 3.0 | Reusable. Attribute the source and license. |
| Google Developer Documentation Style Guide | https://developers.google.com/style/ | Technical writing, documentation structure, wording | CC BY 4.0 | Reusable. Attribute the source and license. |
| Google SRE CC BY 4.0 materials | https://sre.google/classroom/ | Incident, reliability, operations, SLO | CC BY 4.0 | Confirm each material's license notice and attribute Google as the author. Example: [The Art of SLOs](https://sre.google/resources/practices-and-processes/art-of-slos/) |
| MDN Web Docs | https://developer.mozilla.org/en-US/docs/ | Frontend, web, API, debugging, team workflows | Generally CC BY-SA 2.5 or later | Use only to confirm usage. Do not copy or adapt body text. |

For Google SRE, do not treat the whole SRE site as CC BY 4.0. Use only materials explicitly marked CC BY 4.0. The SRE Workbook is CC BY-NC-ND 4.0 and is not a primary source for this dataset. Because reusing MDN body text triggers share-alike obligations, this dataset uses MDN only to confirm usage.

### B. Usage-reference materials

| Provider | Official pages | Main use | License | Handling |
| --- | --- | --- | --- | --- |
| Amazon Jobs Interview Prep | [Software development interview topics](https://www.amazon.jobs/content/en/how-we-hire/interview-prep/software-development-topics), [SDE II Interview Prep](https://www.amazon.jobs/content/en/how-we-hire/sde-ii-interview-prep), [SDE III/Sr. SDE Interview Prep](https://www.amazon.jobs/content/en/how-we-hire/sde-iii-interview-prep) | Technical interview, system design, career and interview | No open license identified | Use only to verify that a term appears in an engineering context. |

For usage-reference materials, do not copy, translate, summarize, or adapt source body text, examples, or questions into Vocabulary. Write `meaning`, `description`, `usageExample`, `meaningJa`, `descriptionJa`, and `usageExampleJa` independently from the source.

For an Amazon Jobs source, set `source.license` to `No open license identified`. Write `source.context` independently as a concise adoption rationale that identifies the engineering interview context. Do not reproduce or translate the original wording.

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
- The 40-character limit is met without noun chains missing particles (e.g. 「API不可時」).
- Request and question tone matches English (`Please` / `Could you` are not flattened to 「〜してください」 alone).
- Established translations are used (`cooldown` → クールダウン, `liveness probe` → ライブネスプローブ, `footprint` → フットプリント, etc.).
- Terminology is consistent within the dataset (レイテンシ / レイテンシー, デプロイ / 配備, etc.).
- There are no LLM-style filler phrases, em dashes, middle-dot lists, or isolated イ-adjective + 「です」 sentences.

## Scene Master

| English | Japanese |
| --- | --- |
| Career / Interview | 転職・面接 |
| Implementation / Review | 実装・レビュー |
| Meetings / Events | 会議・イベント |
| Design / Architecture | 設計・アーキテクチャ |
| Incident Response | 障害対応 |
| Technical Writing | テクニカルライティング |
| Management | マネジメント |

## Example

Completed example using the template: `docs/vocabulary/0217_clarify.md`

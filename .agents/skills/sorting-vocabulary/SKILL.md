---
name: sorting-vocabulary
description: Sort Engineer English vocabulary by Scene and update IDs, filenames, and references. Use when reordering, renumbering, or reclassifying vocabulary.
---

# Sorting Vocabulary

> Japanese: [SKILL.ja.md](SKILL.ja.md)

Sort Engineer English vocabulary into a learner-friendly order and update IDs, filenames, and related references.

Scope: `docs/vocabulary/**/*.md`

Perform sorting directly according to this Skill.
Do not create automation scripts in Python or other languages.

## 1. Scenes

Assign every entry to exactly one Scene according to the
[evaluating-scene Skill](../evaluating-scene/SKILL.md).

## 2. Scene Order

Always use this order:

1. Career / Interview
2. Implementation / Review
3. Meetings / Events
4. Design / Architecture
5. Incident Response
6. Technical Writing
7. Management

## 3. Decide Scene Assignment Before Within-Scene Sorting

Always work in this order:

1. Decide which Scene each entry belongs to from its meaning and usage example
2. Sort within each Scene only
3. Concatenate the seven Scenes in the fixed order
4. Renumber IDs

Do not assign Scene from the term alone. Technical Writing is for examples whose
primary work is creating or maintaining engineering documentation; documentation
used only as part of an incident or review does not automatically belong there.

## 4. Within-Scene Sorting

Within each Scene, place entries earlier when they rank higher on:

1. Difficulty: Beginner → Intermediate → Advanced
2. Learning value for Japanese engineers
3. Practical frequency in professional work

Place Beginner entries toward the front of each Scene so learners can start with
easier vocabulary in every context.

Within the same difficulty, prioritize expressions that are hard for Japanese
learners to infer even when built from simple words, such as:

- wrap up
- follow up
- point out
- hold off
- sort out

## 5. Renumbering IDs

After sorting is complete, assign IDs in final learning order:

- First: `0001`
- Next: `0002`
- ...
- Last: total vocabulary count

Old IDs do not need to be preserved.

## 6. Renaming Files

Rename vocabulary files to match the new ID.

Example:

Old:
`0042_wrap-up.md`

If it becomes the 15th entry in learning order:

`0015_wrap-up.md`

Do not change the `term` segment.

## 7. Updating Content

Update the `id` in each file's YAML front matter to the new ID.

During sorting, do not change:

- term
- type
- partOfSpeech
- pronunciation
- meaning
- meaningJa
- description
- descriptionJa
- difficulty
- scene
- usageExample
- usageExampleJa

## 8. Updating References

Update every reference to old IDs or filenames to the new ID and filename.

Examples:

- Markdown links
- Jekyll internal links
- tests
- fixtures
- snapshots
- README
- documentation

Do not change places that reference only `term` and do not depend on ID.

## 9. Verification

After sorting, confirm:

- Every entry belongs to one of the seven Scenes
- Scene order is correct
- Every entry appears exactly once
- No entries were added or removed
- IDs run continuously from 0001
- There are no duplicate or missing IDs
- Filenames match front matter IDs
- No references to old IDs remain
- Terms, meanings, and examples were not changed unintentionally
- Jekyll build and existing tests succeed

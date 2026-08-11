---
name: sorting-vocabulary
description: Sort Engineer English vocabulary into five learning chapters and update IDs, filenames, and references. Use when reordering, renumbering, or reclassifying vocabulary.
---

# Sorting Vocabulary

> Japanese: [SKILL.ja.md](SKILL.ja.md)

Sort Engineer English vocabulary into a learner-friendly order and update IDs, filenames, and related references.

Scope: `docs/vocabulary/**/*.md`

Perform sorting directly according to this Skill.
Do not create automation scripts in Python or other languages.

## 1. Chapters

Assign every entry to one of the five chapters below.

### Chapter 1: Basic Communication

English for everyday engineering work such as confirmation, requests, sharing, opinions, and alignment.

Examples:
- follow up
- wrap up
- clarify
- reach out
- heads-up

### Chapter 2: Development and Review

English for writing, reviewing, testing, and debugging code.

Examples:
- reproduce
- isolate
- validate
- refactor
- regression

### Chapter 3: Planning and Decision-Making

English for requirements, priorities, estimates, rationale, and trade-offs.

Examples:
- scope
- priority
- estimate
- rationale
- trade-off

### Chapter 4: Operations and Incident Response

English for infrastructure, performance, incidents, and risk in production operations.

Examples:
- mitigate
- rollback
- outage
- latency
- on-call

### Chapter 5: Advanced Technical English

Architecture, technical interviews, advanced discussion, and nuanced expressions.

Examples:
- abstraction
- scalability
- corroborate
- recursion
- time complexity

## 2. Chapter Order

Always use this order:

1. Basic Communication
2. Development and Review
3. Planning and Decision-Making
4. Operations and Incident Response
5. Advanced Technical English

You may use existing `scene` values as hints, but do not map Scene to Chapter mechanically.

## 3. Decide Chapter Assignment Before Within-Chapter Sorting

Always work in this order:

1. Decide which chapter each entry belongs to
2. Sort within each chapter only
3. Concatenate the five chapters
4. Renumber IDs

Do not sort chapters 1–4 first and place the remainder in chapter 5.
Do not send entries that belong elsewhere to chapter 5 because of difficulty or `scene`.

Chapter 5 is not a catch-all.
Include only vocabulary for architecture, technical interviews, advanced technical discussion, and advanced nuance.

Examples that must not go in chapter 5:

- General adverbs such as `currently`, `previously`, `shortly`
  (Chapter 1: Basic Communication)
- Beginner general words such as `alternative`, `approach`, `select`
  (Chapter 3: Planning and Decision-Making, or the appropriate chapter)
- Database operations words such as `migrate`, `swap`
  (Chapter 4: Operations and Incident Response)

Even when `scene` is Architecture, do not put beginner general words or planning/decision vocabulary in chapter 5.
Do not move entries whose `scene` is Daily Communication or Debugging to chapter 5 just because difficulty is Advanced.

### Chapter Assignment Guide

| Chapter | Main `scene` values | Notes |
| --- | --- | --- |
| 1 | Daily Communication | Confirmation, requests, sharing, opinions, alignment |
| 2 | Implementation, Code Review, Debugging, Testing | Reading, writing, and improving code |
| 3 | Sprint Planning, Requirements, Leadership / Management | Planning, requirements, decision-making |
| 4 | Incident Response, Infrastructure / Cloud, Performance, Security, Database | Operations, incidents, performance, security |
| 5 | Architecture (advanced vocabulary), Technical Interview | Advanced technical terms not covered by chapters 1–4 |

For Architecture vocabulary:
- beginner general words → chapter 3
- advanced technical discussion and design vocabulary → chapter 5

## 4. Within-Chapter Sorting

Within each chapter, place entries earlier when they rank higher on:

1. Learning value for Japanese engineers
2. Practical frequency in professional work
3. Difficulty: Beginner → Intermediate → Advanced

Do not sort by difficulty alone.
Even Advanced entries with high learning value and practical use
(`touch base`, `loop in`, `circle back`, etc.)
should come before obvious Beginner general words.

Do not place low-learning-value obvious words such as `update` at the front of a chapter just because they are Beginner.

Prioritize expressions that are hard for Japanese learners to infer even when built from simple words, such as:

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
- source

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

- Every entry belongs to one of the five chapters
- Chapter order is correct
- Every entry appears exactly once
- No entries were added or removed
- IDs run continuously from 0001
- There are no duplicate or missing IDs
- Filenames match front matter IDs
- No references to old IDs remain
- Terms, meanings, and examples were not changed unintentionally
- Jekyll build and existing tests succeed

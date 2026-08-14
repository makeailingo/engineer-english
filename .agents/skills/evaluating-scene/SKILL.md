---
name: evaluating-scene
description: Evaluate whether a Vocabulary scene matches its meaning and usageExample. Use before creating or updating Vocabulary, or when validating scene.
---

# Evaluating Scene

> Japanese: [SKILL.ja.md](SKILL.ja.md)

Evaluate whether Vocabulary `scene` aligns with the adopted meaning and usage example.

Do not assign Scene from the term alone.

## Input

```yaml
term: "router"
meaning: "a device or rule that directs traffic along a path"
meaningJa: "ルーター、経路振分"
usageExample: "..."
currentScene: "Meetings / Events"
```

## Scene Master

* Career / Interview
* Implementation / Review
* Meetings / Events
* Design / Architecture
* Incident Response
* Technical Writing
* Management

## Evaluation Principle

Scene answers:

> "What work is the engineer doing in this usage example?"

not:

> "What topic does this word relate to?"

Do not choose Scene just because keywords such as `review`, `server`, `error`, or `database` appear.

## Workflow

### 1. Fix the adopted sense

Identify the sense used in this Vocabulary entry from `meaning`, `meaningJa`, and `usageExample`.

Do not use a different sense as evidence for Scene.

### 2. Identify the action in the usage example

Summarize briefly:

* who
* does what
* for what purpose

Example:

> "Escalate unresolved disagreements to the engineering manager."

→ Asking a senior decision-maker to resolve a technical disagreement.

### 3. Map to Scene Master

Choose the one Scene that most directly matches.

## Scene Definitions

### Career / Interview

Job searches, applications, interview preparation, and interview evaluation.

### Implementation / Review

Writing, changing, testing, debugging, or reviewing code and features.

### Meetings / Events

Consultation, discussion, planning, presentations, workshops, and team events.

### Design / Architecture

Defining requirements and making decisions about system structure, data,
infrastructure, performance, or security.

### Incident Response

Detecting, mitigating, recovering from, or escalating production incidents.

### Technical Writing

Creating, editing, structuring, or maintaining engineering documentation.

### Management

Handling mentoring, responsibility, organizational coordination, decision-making, and management.

## Conflict Resolution

When multiple Scenes seem possible, use the **primary purpose in usageExample**,
not the word's general category.

Examples:

"Review the query before merging this change."

* query → not Design / Architecture
* merging / review is the primary purpose
  → Implementation / Review

"Optimize this query to reduce response latency."

* query is Database-related
* the primary purpose is performance improvement
  → Design / Architecture

"Restore the database after the production outage."

* database appears
* the primary purpose is incident recovery
  → Incident Response

## Evaluation

Compare `currentScene` with the expected result.

```yaml
result: PASS # PASS | FAIL
currentScene: "Meetings / Events"
expectedScene: "Design / Architecture"
reason: "The example concerns network routing, not a meeting or event."
```

PASS when Scene matches.

If not, return FAIL and `expectedScene`.

## Output

For validation:

```yaml
term: "router"
actionSummary: "Updating router rules before a traffic migration."
expectedScene: "Design / Architecture"
currentScene: "Meetings / Events"
result: FAIL
reason: "The primary purpose is traffic routing on deployment infrastructure, not a meeting."
confidence: High
```

For creation or update:

```yaml
term: "router"
actionSummary: "Updating router rules before a traffic migration."
scene: "Design / Architecture"
confidence: High
notes: "The example describes infrastructure operations rather than implementation."
```

Write `actionSummary` first, then `scene` or `expectedScene`.

## Confidence

- `High`: the example has one clear primary purpose and maps directly to one Scene
- `Medium`: primary purpose is identifiable, but near a boundary between Scenes
- `Low`: primary purpose is ambiguous from the example

Even when `confidence` is Low, choose one Scene from Scene Master and record uncertainty in `notes`.

## Applying Results to Vocabulary

Copy the resulting `scene` into the Vocabulary YAML front matter.
You may keep `actionSummary` as intermediate output, but do not include it in the Vocabulary entry.

When validation FAILs, update Vocabulary `scene` to `expectedScene`.

## Rules

* Do not assign Scene from the term alone.
* Do not assign Scene from katakana technical category alone.
* Do not assign Scene from nouns in `usageExample` alone.
* Prioritize the **primary work or purpose** in `usageExample`.
* Always choose exactly one Scene from Scene Master.

## Wording

Avoid uncommon specialist jargon in this Skill.

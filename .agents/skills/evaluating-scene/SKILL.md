---
name: evaluating-scene
description: Evaluate whether a Vocabulary scene matches usageExample and source context. Use before creating or updating Vocabulary, or when validating scene.
---

# Evaluating Scene

> Japanese: [SKILL.ja.md](SKILL.ja.md)

Evaluate whether Vocabulary `scene` aligns with the adopted sense,
usage example, and engineering context verified in the primary source.

Do not assign Scene from the term alone.

## Input

```yaml
term: "router"
meaning: "a device or rule that directs traffic along a path"
meaningJa: "ルーター、経路振分"
usageExample: "..."
source:
  title: "..."
  url: "..."
  context: "..."
currentScene: "Sprint Planning"
```

## Scene Master

* Daily Communication
* Technical Interview
* Implementation
* Code Review
* Debugging
* Testing
* Sprint Planning
* Requirements
* Incident Response
* Architecture
* Database
* Infrastructure / Cloud
* Performance
* Security
* Leadership / Management

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

### 3. Confirm primary-source context

Open `source.url` and read the surrounding text where the term appears.

Do not decide from search-result snippets alone.

Confirm which activity the source discusses, such as:

* code review
* incident handling
* system design
* implementation
* testing

### 4. Map to Scene Master

Choose the one Scene that most directly matches.

## Scene Definitions

### Daily Communication

Everyday consultation, requests, opinion exchange, and alignment.

### Technical Interview

Explaining design, algorithms, or technical judgment in an interview.

### Implementation

Writing, changing, or running code; implementing APIs or features.

### Code Review

Reviewing code changes and commenting on quality, design, or readability.

### Debugging

Investigating and identifying the cause of an existing defect.

### Testing

Verifying expected results; creating or running tests.

### Sprint Planning

Handling tasks, priorities, effort, deadlines, and sprint planning.

### Requirements

Defining requirements, specifications, scope, and acceptance criteria.

### Incident Response

Detecting, mitigating, recovering from, or escalating production incidents.

### Architecture

Handling system structure, responsibilities, boundaries, dependencies, and design decisions.

### Database

Handling data storage, retrieval, integrity, and DB-specific operations or structure.

### Infrastructure / Cloud

Handling runtime environments, networks, cloud platforms, and deployment infrastructure.

### Performance

Improving or measuring speed, latency, CPU, memory, or load.

### Security

Handling authentication, authorization, attacks, defenses, and confidentiality.

### Leadership / Management

Handling mentoring, responsibility, organizational coordination, decision-making, and management.

## Conflict Resolution

When multiple Scenes seem possible, use the **primary purpose in usageExample**,
not the word's general category.

Examples:

"Review the query before merging this change."

* query → not Database
* merging / review is the primary purpose
  → Code Review

"Optimize this query to reduce response latency."

* query is Database-related
* the primary purpose is performance improvement
  → Performance

"Restore the database after the production outage."

* database appears
* the primary purpose is incident recovery
  → Incident Response

## Evaluation

Compare `currentScene` with the expected result.

```yaml
result: PASS # PASS | FAIL
currentScene: "Sprint Planning"
expectedScene: "Infrastructure / Cloud"
reason: "The example concerns network routing, not sprint planning."
```

PASS when Scene matches.

If not, return FAIL and `expectedScene`.

## Output

For validation:

```yaml
term: "router"
actionSummary: "Updating router rules before a traffic migration."
expectedScene: "Infrastructure / Cloud"
currentScene: "Sprint Planning"
result: FAIL
reason: "The primary purpose is traffic routing on deployment infrastructure, not sprint planning."
confidence: High
```

For creation or update:

```yaml
term: "router"
actionSummary: "Updating router rules before a traffic migration."
scene: "Infrastructure / Cloud"
confidence: High
notes: "The source discusses Express deployment, but the action is infrastructure operations."
```

Write `actionSummary` first, then `scene` or `expectedScene`.

## Confidence

- `High`: primary purpose in the example and source activity align; one Scene is clear
- `Medium`: primary purpose is identifiable, but near a boundary between Scenes
- `Low`: primary purpose is ambiguous from the example alone, or the source diverges

Even when `confidence` is Low, choose one Scene from Scene Master and record uncertainty in `notes`.

## Applying Results to Vocabulary

Copy the resulting `scene` into the Vocabulary YAML front matter.
You may keep `actionSummary` as intermediate output, but do not include it in the Vocabulary entry.

When validation FAILs, update Vocabulary `scene` to `expectedScene`.

## Rules

* Do not assign Scene from the term alone.
* Do not assign Scene from katakana technical category alone.
* Do not assign Scene from nouns in `usageExample` alone.
* Do not copy `source` category to Scene unconditionally.
* Prioritize the **primary work or purpose** in `usageExample`.
* Always choose exactly one Scene from Scene Master.

## Wording

Avoid uncommon specialist jargon in this Skill.

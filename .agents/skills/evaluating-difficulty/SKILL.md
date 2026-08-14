---
name: evaluating-difficulty
description: Assign Vocabulary difficulty using two evaluation axes and fixed decision rules. Use before creating or updating Vocabulary entries.
---

# Evaluating Difficulty

> Japanese: [SKILL.ja.md](SKILL.ja.md)

Assign Vocabulary `difficulty` from two evaluation axes and the decision rules below.
Do not use external vocabulary lists such as CEFR or TOEIC as the deciding standard.

## Difficulty Definitions

| Difficulty | Guideline |
| --- | --- |
| Beginner | Widely known general vocabulary; engineers can infer the meaning easily |
| Intermediate | General vocabulary with learning value in professional use, or frequent in technical contexts |
| Advanced | Uncommon in everyday English; even engineers are unlikely to know the word as English vocabulary |

## Evaluation Axes

Rate each axis as **low**, **medium**, or **high**.

| Axis | Question |
| --- | --- |
| `generalFamiliarity` | As general English, is the meaning easy to infer? |
| `engineerFamiliarity` | Are Japanese software engineers likely to know the word as English vocabulary? |

## Decision Rules

After rating the axes, choose Difficulty using only these rules. **Do not interpret exceptions.**

| Condition | Difficulty |
| --- | --- |
| `generalFamiliarity` = high **and** `engineerFamiliarity` ≠ low | Beginner |
| `generalFamiliarity` = low **and** `engineerFamiliarity` = low | Advanced |
| All other cases | Intermediate |

## Reference Examples

Reference examples guide axis ratings only. Do not assign Difficulty directly from them.

### generalFamiliarity

| Value | Examples |
| --- | --- |
| high | `feedback`, `deadline`, `replace` |
| medium | `clarify`, `mandatory`, `defer` |
| low | `courteous`, `scrutiny`, `discretion` |

Do not include borderline terms such as `trade-off` in reference examples.

## Workflow

1. Rate `generalFamiliarity` using reference examples
2. Rate `engineerFamiliarity` using reference examples
3. Choose Difficulty with the decision rules
4. Assign `confidence`
5. Optionally record `contextualLearningNeeded` (not used for Difficulty)

Write `reasoning` first, then `difficulty`.

## contextualLearningNeeded

Not used for Difficulty. Record only for future learning-value or prioritization notes.

## Input

```yaml
term: "feedback"
type: "word" # word | phrase
```

## Output

```yaml
term: "feedback"
type: "word"
reasoning:
  generalFamiliarity: high
  engineerFamiliarity: high
  contextualLearningNeeded: low
difficulty: Beginner
confidence: High
notes: "Widely known general vocabulary and easy to understand in engineering contexts."
```

```yaml
term: "clarify"
type: "word"
reasoning:
  generalFamiliarity: medium
  engineerFamiliarity: medium
  contextualLearningNeeded: medium
difficulty: Intermediate
confidence: High
notes: "General vocabulary with learning value in professional use."
```

```yaml
term: "courteous"
type: "word"
reasoning:
  generalFamiliarity: low
  engineerFamiliarity: low
  contextualLearningNeeded: high
difficulty: Advanced
confidence: High
notes: "Uncommon in everyday conversation; nuance matters for appropriate use."
```

## Confidence

- `High`: both axes are clear from reference examples
- `Medium`: one axis is borderline, but the decision rules still decide Difficulty
- `Low`: axis ratings themselves are uncertain

Even when `confidence` is Low, still output Difficulty from the decision rules and record uncertainty in `notes`.

## Applying Results to Vocabulary

Copy the resulting `difficulty` into the Vocabulary YAML front matter.
You may keep `reasoning` as intermediate output, but do not include it in the Vocabulary entry.

## Prohibited Actions

- Using external vocabulary lists as ground truth
- Assigning Difficulty directly from similarity to reference examples
- Using `contextualLearningNeeded` in Difficulty decisions
- Choosing the higher level when uncertain

## Wording

Avoid uncommon specialist jargon in this Skill (for example, "fixed decision table", "uncommon").

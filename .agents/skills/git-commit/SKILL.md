---
name: git-commit
description: Choose commit messages and branch names that follow conventional branching. Use when committing, drafting messages before push, or naming branches.
---

# Git Commit

> Japanese: [SKILL.ja.md](SKILL.ja.md)

This repository follows conventional branching.
Use only these four prefixes: `feat`, `bugfix`, `docs`, and `chore`.

| Prefix | Use |
| --- | --- |
| `feat` | New features, new vocabulary, user-facing additions |
| `bugfix` | Bug fixes, translation or wording corrections, behavior fixes |
| `docs` | Documentation and README updates |
| `chore` | Skills, rules, tools, configuration, dependencies, refactors with no behavior change |

Do not use `fix`, `refactor`, `style`, `test`, or any other prefix.

## Branch Names

```
<feat|bugfix|docs|chore>/<short-description>
```

- `<short-description>` uses lowercase English and hyphens (kebab-case)
- Examples: `feat/add-vocabulary-0501`, `bugfix/consensus-usage-example`, `docs/jekyll-local-dev`

## Commit Messages

English, one line only. No body.

```
<feat|bugfix|docs|chore>: <summary>
```

- **summary**: Aim for 50 characters or fewer in English; state what changed clearly
- Pass via HEREDOC to avoid shell escaping issues

## Decision Order

When unsure, decide in this order:

1. Fixing an existing error or defect → `bugfix`
2. Adding new content or capability → `feat`
3. Documentation-only change → `docs`
4. Skills, rules, configuration, or other maintenance → `chore`

## Examples

```
bugfix: fix usageExampleJa for consensus and respectful
feat: add vocabulary 0501
docs: add Jekyll local development setup
chore: add git-commit skill
```

## Pre-commit Checks

- Review targets with `git status` and `git diff`
- Do not include unrelated changes in the same commit
- Do not include secrets (`.env`, keys)
- Do not commit unless the user explicitly asks for a commit

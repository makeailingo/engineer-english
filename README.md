# Software Engineer English Vocabulary

> Japanese: [README.ja.md](README.ja.md)

A dataset designed to improve software engineers' English skills, built from words and phrases personally heard or seen by software engineers in workplaces where English is the working language.

## Concept

- Each entry must be something a software engineer has personally heard or seen while working in English.
- Entries may come from meetings, implementation, code review, interviews, written communication, lunch, after-work gatherings, and other interactions around engineering work.
- We include vocabulary useful across roles and technology stacks, rather than terminology specific to one technology, role, or domain.
- Meanings, parts of speech, and English IPA are checked in Cambridge Dictionary and cross-checked in Oxford Advanced Learner's Dictionary. Descriptions and usage examples are written independently, informed by how each term was actually heard or seen.
- Difficulty is classified into three levels:

| Difficulty | Guideline |
| --- | --- |
| Beginner | Widely known general vocabulary; engineers can infer the meaning easily |
| Intermediate | General vocabulary with learning value in professional use, or frequent in technical contexts |
| Advanced | Uncommon in everyday English; even engineers are unlikely to know the word as English vocabulary |

## Learning Order (ID)

Each vocabulary `id` (0001 onward) reflects learning order across seven Scenes in this sequence:

| Order | Scene |
| --- | --- |
| 1 | Career / Interview |
| 2 | Implementation / Review |
| 3 | Meetings / Events |
| 4 | Design / Architecture |
| 5 | Incident Response |
| 6 | Technical Writing |
| 7 | Management |

Within each Scene, entries are ordered by **difficulty → learning value → practical frequency**.
See the [sorting-vocabulary Skill](.agents/skills/sorting-vocabulary/SKILL.md) for details.

## Local Development

### Prerequisites

- Ruby installed via [Homebrew](https://brew.sh/)

```bash
brew install ruby
```

Prefer Homebrew Ruby in your shell (add to `~/.zshrc`):

```bash
export PATH="/opt/homebrew/opt/ruby/bin:$PATH"
```

### Setup

```bash
cd docs
bundle install
```

### Serve

```bash
cd docs
bundle exec jekyll serve --baseurl ""
```

Open http://127.0.0.1:4000/ in a browser.

`--baseurl ""` removes the GitHub Pages `/engineer-english` prefix so the site is served from the root locally.

### Build only

```bash
cd docs
bundle exec jekyll build --baseurl ""
```

Output is written to `docs/_site/`.

## License

AGPL-3.0-only. See [LICENSE](LICENSE).

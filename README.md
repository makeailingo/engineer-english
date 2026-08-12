# Engineer English

> Japanese: [README.ja.md](README.ja.md)

An open dataset of English used in day-to-day software engineering work.

## Concept

- We include words and phrases that engineers repeatedly encounter regardless of role or tech stack—career and interviewing, meetings, implementation, code review, design, incident response, technical writing, management, and similar cross-cutting work. We exclude specialized terminology whose meaning depends on a particular technology, role, or domain.
- We extract words and phrases actually used in software engineering from reliable primary sources.
- We obtain senses, parts of speech, and pronunciation (US English IPA) from reliable external dictionaries (Cambridge Dictionary as the primary source; Oxford Advanced Learner's Dictionary for cross-checking).
- Difficulty is classified into three levels:

| Difficulty | Guideline |
| --- | --- |
| Beginner | Widely known general vocabulary; engineers can infer the meaning easily |
| Intermediate | General vocabulary with learning value in professional use, or frequent in technical contexts |
| Advanced | Uncommon in everyday English; even engineers are unlikely to know the word as English vocabulary |

- Learner-facing content is written independently.

## Primary Source Usage

Primary sources are handled according to their licenses.

- **Open-license materials:** Google Engineering Practices, Google Developer Documentation Style Guide, explicitly licensed Google SRE CC BY 4.0 materials, and MDN Web Docs. Each source is used according to its license. MDN body text is not reused because doing so would trigger share-alike obligations.
- **Usage-reference materials:** Amazon Jobs Interview Prep. No open license has been identified, so these pages are used only to verify that a term appears in an engineering context:
  - [Software development interview topics](https://www.amazon.jobs/content/en/how-we-hire/interview-prep/software-development-topics)
  - [SDE II Interview Prep](https://www.amazon.jobs/content/en/how-we-hire/sde-ii-interview-prep)
  - [SDE III/Sr. SDE Interview Prep](https://www.amazon.jobs/content/en/how-we-hire/sde-iii-interview-prep)

Amazon Jobs body text, examples, and questions are not copied, translated, summarized, or adapted into the dataset. Meanings, explanations, usage examples, translations, and source-context descriptions are written independently.

## Learning Order (ID)

Each vocabulary `id` (0001 onward) reflects learning order across seven Scenes in this sequence:

| Order | Scene | ID range (1,000 entries) |
| --- | --- | --- |
| 1 | Career / Interview | 0001–0079 |
| 2 | Implementation / Review | 0080–0399 |
| 3 | Meetings / Events | 0400–0546 |
| 4 | Design / Architecture | 0547–0849 |
| 5 | Incident Response | 0850–0929 |
| 6 | Technical Writing | 0930–0969 |
| 7 | Management | 0970–1000 |

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

MIT. See [LICENSE](LICENSE).

This license covers content in this repository, not linked third-party source pages. Those pages remain subject to their respective licenses and terms.

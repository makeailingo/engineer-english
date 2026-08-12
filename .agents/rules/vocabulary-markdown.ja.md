# Vocabulary Markdown

> English: [vocabulary-markdown.md](vocabulary-markdown.md)

対象: `docs/vocabulary/**/*.md`

- 1ファイルにつき1件とし、ファイル名は`<id>_<term>.md`とする。`term`部分は小文字のkebab-caseにする。
- `docs/templates/vocabulary.md`を複製し、YAML Front Matterの全属性を記載する。
- YAML Front Matter を唯一の正本とする。項目の表示見出し（日英併記）は Jekyll レイアウトが生成する。Markdown 本文にフィールド値を複製しない。
- フィールド順序は `id`, `term`, `type`, `partOfSpeech`, `pronunciation`, `description`, `descriptionJa`, `meaning`, `meaningJa`, `usageExample`, `usageExampleJa`, `difficulty`, `scene`, `source` とする。
- 語義・品詞・発音は researching-vocabulary Skill に従う。
- `difficulty`は evaluating-difficulty Skill に従う。
- `scene`は evaluating-scene Skill に従う。
- `meaningJa`は evaluating-meaningJa Skill に従う。
- `id`は`"0001"`から`"9999"`までの重複のない4桁連番とする。`id`は表示順・学習順を表す。
- 学習順は [sorting-vocabulary Skill](.agents/skills/sorting-vocabulary/SKILL.md) に従う。Scene（転職・面接 → 実装・レビュー → 会議・イベント → 設計・アーキテクチャ → 障害対応 → テクニカルライティング → マネジメント）の順に分類し、各 Scene 内では難易度 → 学習価値 → 実用性の順で並べ、IDを振り直す。
- `type`は`word`または`phrase`とする。
- `difficulty`と`scene`は下記マスタからそれぞれ1つだけ選ぶ。
- `source`には、実在と用法を確認した一次情報を1件、下記Source Schemaで記載する。
- 日本語訳、説明、使用例、使用例訳は独自に作成し、出典本文をコピー・翻案しない。
- 語義、説明、使用例、使用例訳、`scene`、`source`の文脈を意味的に一致させる。
- `description`は80文字以内にする。
- `descriptionJa`は40文字以内にする。
- `usageExample`は10語以内、`usageExampleJa`は40文字以内にする。
- 使用例は対象語の意味が文脈から判断できる、自然で具体的な実務表現にする。
- `usageExampleJa`の作成・修正・レビューは [japanese-tech-writing Skill](.agents/skills/japanese-tech-writing/SKILL.md) に従う。
- 作成前に既存Vocabularyとの重複を確認する。

## Source Schema

`source`は単一オブジェクトとし、次の4属性を必須とする。

| 属性 | 内容 |
| --- | --- |
| `title` | 一次資料の正式なページタイトル |
| `url` | 対象語の用法を実際に確認した公開ページのURL |
| `license` | 一次資料に明記されたライセンス名。オープンライセンスを確認できない場合は `No open license identified` |
| `context` | 対象語が使われているソフトウェア開発上の文脈をまとめた簡潔な日本語 |

`context`は原文を長く引用せず、採用根拠が判断できる内容にする。

## 一次資料

一次資料は、ライセンスに応じて次の2種類に分ける。

### A. オープンライセンス資料

| 提供元 | 公式URL | 主な用途 | ライセンス | 取り扱い |
| --- | --- | --- | --- | --- |
| Google Engineering Practices | https://google.github.io/eng-practices/ | Code Review、設計、開発コミュニケーション | CC BY 3.0 | 再利用可能。出典とライセンスを明記する。 |
| Google Developer Documentation Style Guide | https://developers.google.com/style/ | テクニカルライティング、文書構成、用語 | CC BY 4.0 | 再利用可能。出典とライセンスを明記する。 |
| Google SREのCC BY 4.0資料 | https://sre.google/classroom/ | Incident、Reliability、Operations、SLO | CC BY 4.0 | 各資料のライセンス表示を確認し、Googleを原著者として明記する。例: [The Art of SLOs](https://sre.google/resources/practices-and-processes/art-of-slos/) |
| MDN Web Docs | https://developer.mozilla.org/en-US/docs/ | Frontend、Web、API、Debugging、チームワークフロー | 原則CC BY-SA 2.5以降 | 単語の採用根拠として使用する。本文のコピーや翻案は行わない。 |

Google SREでは、SREサイト全体をCC BY 4.0とみなさず、CC BY 4.0と明記された教材だけを使用する。SRE WorkbookはCC BY-NC-ND 4.0であり、本データセットの一次資料には含めない。MDNで本文を再利用すると継承ライセンスの条件が生じるため、本データセットでは用法の確認に限って使用する。

### B. 用法参照資料

| 提供元 | 公式ページ | 主な用途 | ライセンス | 取り扱い |
| --- | --- | --- | --- | --- |
| Amazon Jobs Interview Prep | [Software development interview topics](https://www.amazon.jobs/content/en/how-we-hire/interview-prep/software-development-topics)、[SDE II Interview Prep](https://www.amazon.jobs/content/en/how-we-hire/sde-ii-interview-prep)、[SDE III/Sr. SDE Interview Prep](https://www.amazon.jobs/content/en/how-we-hire/sde-iii-interview-prep) | Technical Interview、System Design、Career / Interview | No open license identified | 対象語がエンジニアリングの文脈で使われていることの確認に限って使用する。 |

用法参照資料の本文、例文、質問文は、Vocabularyへコピー、翻訳、要約、翻案しない。`meaning`、`description`、`usageExample`、`meaningJa`、`descriptionJa`、`usageExampleJa`は一次資料から独立して作成する。

Amazon Jobsを出典とする場合、`source.license`には`No open license identified`と記載する。`source.context`には、対象語が使われているエンジニア面接の文脈と採用根拠を独自の文章で簡潔に記載し、原文の転載や翻訳は行わない。

## Difficulty Master

| English | 日本語 | 目安 |
| --- | --- | --- |
| Beginner | 初級 | 一般語として広く知られ、エンジニアも意味を推測しやすい |
| Intermediate | 中級 | 一般語だが実務での用法に学習価値がある、または技術文脈で頻出する |
| Advanced | 上級 | 一般英語として日常的に使われず、エンジニアも英単語としては馴染みが薄い |

`difficulty`は [evaluating-difficulty Skill](.agents/skills/evaluating-difficulty/SKILL.md) に従う。

`scene`は [evaluating-scene Skill](.agents/skills/evaluating-scene/SKILL.md) に従う。

`meaningJa`は [evaluating-meaningJa Skill](.agents/skills/evaluating-meaningJa/SKILL.md) に従う。

## usageExampleJa のレビュー

`usageExampleJa`を新規作成・修正するとき、またはレビューを依頼されたときは、必ず [japanese-tech-writing Skill](.agents/skills/japanese-tech-writing/SKILL.md) を読み、そのルールに沿って推敲する。

レビューでは、少なくとも次を確認する。

- `usageExample`の意味と一致しているか。英語の多義語（`commit`、`drain`、`prune` など）を誤訳していないか。
- 40文字以内の制約を守りつつ、助詞不足の名詞連結（「API不可時」など）になっていないか。
- 依頼・疑問のトーンが英語と揃っているか（`Please` / `Could you` → 「〜してください」だけにしない）。
- 定訳・慣用語を使っているか（`cooldown` → クールダウン、`liveness probe` → ライブネスプローブ、`footprint` → フットプリント など）。
- 同一語彙セット内で表記がぶれていないか（レイテンシ / レイテンシー、デプロイ / 配備 など）。
- LLM 口調の空句、em ダッシュ、中黒並列、イ形容詞 + 「です」の孤立文がないか。

## Scene Master

| English | 日本語 |
| --- | --- |
| Career / Interview | 転職・面接 |
| Implementation / Review | 実装・レビュー |
| Meetings / Events | 会議・イベント |
| Design / Architecture | 設計・アーキテクチャ |
| Incident Response | 障害対応 |
| Technical Writing | テクニカルライティング |
| Management | マネジメント |

## 作成例

テンプレートを使用した完成例: `docs/vocabulary/0207_clarify.md`

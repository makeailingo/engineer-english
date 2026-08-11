# Vocabulary Markdown

対象: `docs/vocabulary/**/*.md`

- 1ファイルにつき1件とし、ファイル名は`<id>_<term>.md`とする。`term`部分は小文字のkebab-caseにする。
- `docs/templates/vocabulary.md`を複製し、YAML Front Matterの全属性を記載する。
- 語義・品詞・発音は researching-vocabulary Skill に従う。
- `difficulty`は evaluating-difficulty Skill に従う。
- `scene`は evaluating-scene Skill に従う。
- `id`は`"0001"`から始まる重複のない4桁連番とし、既存の最大値に1を加えて採番する。
- `type`は`word`または`phrase`とする。
- `difficulty`と`scene`は下記マスタからそれぞれ1つだけ選ぶ。
- `source`には、実在と用法を確認した一次情報を1件、下記Source Schemaで記載する。
- 日本語訳、説明、使用例、使用例訳は独自に作成し、出典本文をコピー・翻案しない。
- 語義、説明、使用例、使用例訳、`scene`、`source`の文脈を意味的に一致させる。
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
| `license` | 一次資料に明記されたライセンス名 |
| `context` | 対象語が使われているソフトウェア開発上の文脈をまとめた簡潔な日本語 |

`context`は原文を長く引用せず、採用根拠が判断できる内容にする。

## 一次資料

Vocabularyの採用根拠には、次の3つに含まれる公開資料だけを使用する。

| 提供元 | 公式URL | 主な用途 | ライセンス | 取り扱い |
| --- | --- | --- | --- | --- |
| Google Engineering Practices | https://google.github.io/eng-practices/ | Code Review、設計、開発コミュニケーション | CC BY 3.0 | 再利用可能。出典とライセンスを明記する。 |
| Google SREのCC BY 4.0資料 | https://sre.google/classroom/ | Incident、Reliability、Operations、SLO | CC BY 4.0 | 各資料のライセンス表示を確認し、Googleを原著者として明記する。例: [The Art of SLOs](https://sre.google/resources/practices-and-processes/art-of-slos/) |
| MDN Web Docs | https://developer.mozilla.org/en-US/docs/ | Frontend、Web、API、Debugging | 原則CC BY-SA 2.5以降 | 単語の採用根拠として使用する。本文のコピーや翻案は行わない。 |

Google SREでは、SREサイト全体をCC BY 4.0とみなさず、CC BY 4.0と明記された教材だけを使用する。MDNで本文を再利用すると継承ライセンスの条件が生じるため、本データセットでは用法の確認に限って使用する。

## Difficulty Master

| English | 日本語 | 目安 |
| --- | --- | --- |
| Beginner | 初級 | 一般語として広く知られ、エンジニアも意味を推測しやすい |
| Intermediate | 中級 | 一般語だが実務での用法に学習価値がある、または技術文脈で頻出する |
| Advanced | 上級 | 一般英語として日常的に使われず、エンジニアも英単語としては馴染みが薄い |

`difficulty`は [evaluating-difficulty Skill](.agents/skills/evaluating-difficulty/SKILL.md) に従う。

`scene`は [evaluating-scene Skill](.agents/skills/evaluating-scene/SKILL.md) に従う。

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
| Daily Communication | 日常会話 |
| Technical Interview | 技術面接 |
| Implementation | 実装 |
| Code Review | コードレビュー |
| Debugging | デバッグ |
| Testing | テスト |
| Sprint Planning | スプリントプランニング |
| Requirements | 要件定義 |
| Incident Response | インシデント対応 |
| Architecture | アーキテクチャ |
| Database | データベース |
| Infrastructure / Cloud | インフラストラクチャ / クラウド |
| Performance | パフォーマンス |
| Security | セキュリティ |
| Leadership / Management | リーダーシップ / マネジメント |

## 作成例

テンプレートを使用した完成例: `docs/vocabulary/0001_clarify.md`

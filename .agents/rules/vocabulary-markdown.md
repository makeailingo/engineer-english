# Vocabulary Markdown

対象: `docs/vocabulary/**/*.md`

- 1ファイルにつき1件とし、ファイル名は`<id>_<term>.md`とする。`term`部分は小文字のkebab-caseにする。
- `docs/templates/vocabulary.md`を複製し、YAML Front Matterの全属性を記載する。
- 語義・品詞・発音は researching-vocabulary Skill に従う。
- `difficulty`は evaluating-difficulty Skill に従い、CEFR と JMdict 外来語定着度から判定する。
- `id`は`"0001"`から始まる重複のない4桁連番とし、既存の最大値に1を加えて採番する。
- `type`は`word`または`phrase`とする。
- `difficulty`と`scene`は下記マスタからそれぞれ1つだけ選ぶ。
- `source`には、実在と用法を確認した一次情報を1件、下記Source Schemaで記載する。
- 日本語訳、説明、使用例、使用例訳は独自に作成し、出典本文をコピー・翻案しない。
- 語義、説明、使用例、使用例訳、`scene`、`source`の文脈を意味的に一致させる。
- `descriptionJa`は40文字以内にする。
- `usageExample`は10語以内、`usageExampleJa`は40文字以内にする。
- 使用例は対象語の意味が文脈から判断できる、自然で具体的な実務表現にする。
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

| English | 日本語 | 判定基準 |
| --- | --- | --- |
| Beginner | 初級 | TOEIC 600前後でも理解しやすく、一般的な意味のまま実務で使える語句 |
| Intermediate | 中級 | 一般語だが、エンジニア文脈での意味や定型的な使い方の習得が必要な語句 |
| Advanced | 上級 | 抽象度が高い、専門知識を要する、または文脈によってニュアンスが変わる語句 |

`difficulty`は [evaluating-difficulty Skill](.agents/skills/evaluating-difficulty/SKILL.md) に従い、CEFR と JMdict 外来語定着度から機械的に判定する。

## Difficulty Eval

1. Cambridge Dictionary、Oxford 3000 / 5000からCEFRを取得する。
2. CEFRを以下に変換する。
   - A1-A2: Beginner
   - B1-B2: Intermediate
   - C1-C2: Advanced
3. [JMdict](https://www.edrdg.org/jmdict/j_jmdict.html)に、その英単語に対応する日本語の外来語が登録されている場合、Difficultyを1段階下げる。
4. Beginnerより下にはしない。

| 対象 | CEFR 参照ソース |
| --- | --- |
| word | Cambridge Dictionary → Oxford 3000 / 5000 |
| phrase | Oxford Phrase List → Cambridge Dictionary |

CEFR 取得時、複数の CEFR が付いている場合、または語義ごとにレベルが異なる場合は、理解に必要な知識が最も多い Difficulty を選ぶ。CEFR がどちらにもない場合のみ推測する。

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

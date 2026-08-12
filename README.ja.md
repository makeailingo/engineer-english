# Engineer English

> English: [README.md](README.md)

ソフトウェアエンジニアが実務で使う英語のデータセットです。

## コンセプト

- 転職・面接、会議、実装、コードレビュー、設計、障害対応、テクニカルライティング、マネジメントなど、職種や技術スタックを問わず繰り返し遭遇する英単語・フレーズを収録します。一方で、特定の技術・職種・ドメインを理解するための専門用語そのものは対象外とします。
- 信頼性の高い一次資料から、ソフトウェアエンジニアリングの文脈で実際に使われる単語やフレーズを抽出しています。
- 語義・品詞・発音記号は、信頼性の高い外部の辞書（Cambridge Dictionary を一次情報とし、Oxford Advanced Learner's Dictionary で照合）から取得しています。
- 難易度は次の3段階で分類しています。

| 難易度 | 目安 |
| --- | --- |
| Beginner（初級） | 一般語として広く知られ、エンジニアも意味を推測しやすい |
| Intermediate（中級） | 一般語だが実務での用法に学習価値がある、または技術文脈で頻出する |
| Advanced（上級） | 一般英語として日常的に使われず、エンジニアも英単語としては馴染みが薄い |

- 学習用コンテンツは独自に作成しています。

## 一次資料の利用区分

一次資料はライセンスに応じて扱いを分けています。

- **オープンライセンス資料**：Google Engineering Practices、CC BY 4.0と明記されたGoogle SRE資料、MDN Web Docs。各資料のライセンス条件に従います。MDNの本文は、再利用によって継承ライセンスの条件が生じるため使用しません。
- **用法参照資料**：Amazon Jobs Interview Prep。オープンライセンスを確認できないため、対象語がエンジニアリングの文脈で使われていることの確認に限って、次のページを使用します。
  - [Software development interview topics](https://www.amazon.jobs/content/en/how-we-hire/interview-prep/software-development-topics)
  - [SDE II Interview Prep](https://www.amazon.jobs/content/en/how-we-hire/sde-ii-interview-prep)
  - [SDE III/Sr. SDE Interview Prep](https://www.amazon.jobs/content/en/how-we-hire/sde-iii-interview-prep)

Amazon Jobsの本文、例文、質問文は、データセットへコピー、翻訳、要約、翻案しません。
語義、説明、使用例、日本語訳、出典の文脈説明は独自に作成します。

## 学習順（ID）

語彙の `id`（0001 から連番）は、次の7つのSceneをこの順に並べた学習順を表します。

| 順序 | Scene | ID 範囲（1,063語時点） |
| --- | --- | --- |
| 1 | 転職・面接 | 0001–0086 |
| 2 | 実装・レビュー | 0087–0417 |
| 3 | 会議・イベント | 0418–0579 |
| 4 | 設計・アーキテクチャ | 0580–0896 |
| 5 | 障害対応 | 0897–0984 |
| 6 | テクニカルライティング | 0985–1025 |
| 7 | マネジメント | 1026–1063 |

Scene分類を先に確定し、各Scene内では **難易度 → 学習価値 → 実用性** の順で並べます。
詳細は [sorting-vocabulary Skill](.agents/skills/sorting-vocabulary/SKILL.md) を参照してください。

## ローカル開発

### 前提

- [Homebrew](https://brew.sh/) で Ruby をインストール済みであること

```bash
brew install ruby
```

シェルで Homebrew の Ruby を優先する（`~/.zshrc` に追記）:

```bash
export PATH="/opt/homebrew/opt/ruby/bin:$PATH"
```

### セットアップ

```bash
cd docs
bundle install
```

### 起動

```bash
cd docs
bundle exec jekyll serve --baseurl ""
```

ブラウザで http://127.0.0.1:4000/ を開く。

`--baseurl ""` は GitHub Pages 用の `/engineer-english` プレフィックスを外し、ローカルではルートから表示するための指定。

### ビルドのみ

```bash
cd docs
bundle exec jekyll build --baseurl ""
```

生成物は `docs/_site/` に出力される。

## ライセンス

MIT. See [LICENSE](LICENSE).

このライセンスはリポジトリ内のコンテンツに適用され、リンク先の第三者資料には適用されません。
リンク先の資料には、それぞれのライセンスと利用条件が適用されます。

# Engineer English

> English: [README.md](README.md)

ソフトウェアエンジニアの英語力向上を目的に、英語を共通言語とする環境で働くソフトウェアエンジニア自身が、実際に見聞きした英単語・フレーズを収録するデータセットです。

## コンセプト

- ソフトウェアエンジニア自身が実際に見聞きした英単語・フレーズだけを収録する。
- 転職、面接、実装、コードレビュー、テクニカルライティング、アーキテクチャの設計など、ソフトウェアエンジニアとして働く中で交わされる英語を対象とする。
- 特定の技術、職種、ドメインだけで使われる専門用語ではなく、幅広いソフトウェアエンジニアに役立つ語彙を収録する。
- 意味・品詞・発音記号は Cambridge Dictionary で確認し、Oxford Advanced Learner's Dictionary で照合する。
- 難易度は次の3段階で分類しています。

| 難易度 | 目安 |
| --- | --- |
| Beginner（初級） | 一般語として広く知られ、エンジニアも意味を推測しやすい |
| Intermediate（中級） | 一般語だが実務での用法に学習価値がある、または技術文脈で頻出する |
| Advanced（上級） | 一般英語として日常的に使われず、エンジニアも英単語としては馴染みが薄い |

## 学習順（ID）

語彙の `id`（0001 から連番）は、次の7つのSceneをこの順に並べた学習順を表します。

| 順序 | Scene |
| --- | --- |
| 1 | 転職・面接 |
| 2 | 実装・コードレビュー |
| 3 | 会議・イベント |
| 4 | 設計・アーキテクチャ |
| 5 | 障害対応 |
| 6 | テクニカルライティング |
| 7 | マネジメント |

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

AGPL-3.0-only. See [LICENSE](LICENSE).

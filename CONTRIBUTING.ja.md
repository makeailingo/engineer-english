# コントリビューション

> English: [CONTRIBUTING.md](CONTRIBUTING.md)

Engineer Englishは、ソフトウェアエンジニアの英語力向上を目的に、英語で働くソフトウェアエンジニア自身が実際に見聞きした英単語・フレーズを収録します。

## 収録する語彙

- 自身が英語で働く中で実際に見聞きした語彙だけを投稿する。
- 会議、実装、コードレビュー、面接、文章でのやり取り、ランチ、仕事後の集まりなど、ソフトウェアエンジニアとして働く中で交わされた語彙を対象とする。
- 特定の技術、職種、ドメインだけで使われる専門用語ではなく、幅広いソフトウェアエンジニアに役立つ語彙を優先する。
- 同じ語彙が同じ意味ですでに収録されていないか確認する。

## 職場の情報を守る

- 社内のメッセージ、文書、議事録、会話を転載しない。
- 会社名、製品名、プロジェクト名、顧客名、個人名を含めない。
- 実際に見聞きした使われ方を参考に、一般化した使用例を独自に作成する。

## 語彙を追加する

1. [`docs/templates/vocabulary.md`](docs/templates/vocabulary.md) をコピーする。
2. [Vocabulary Markdownルール](.agents/rules/vocabulary-markdown.ja.md) に従う。
3. [researching-vocabulary Skill](.agents/skills/researching-vocabulary/SKILL.ja.md) に従い、意味・品詞・英語の発音記号を確認する。
4. 各Skillに従って難易度とSceneを判定する。
5. Jekyllサイトが正常にビルドできることを確認する。

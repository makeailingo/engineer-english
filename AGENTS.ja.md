# Engineer English

> English: [AGENTS.md](AGENTS.md)

ソフトウェアエンジニアの英語力向上を目的に、英語を共通言語とする環境で働くソフトウェアエンジニア自身が、実際に見聞きした英単語・フレーズを収録するデータセット。

## コンセプト

- ソフトウェアエンジニア自身が実際に見聞きした英単語・フレーズだけを収録する。
- 転職、面接、実装、コードレビュー、テクニカルライティング、アーキテクチャの設計など、ソフトウェアエンジニアとして働く中で交わされる英語を対象とする。
- 特定の技術、職種、ドメインだけで使われる専門用語ではなく、幅広いソフトウェアエンジニアに役立つ語彙を収録する。
- 意味・品詞・発音記号は Cambridge Dictionary で確認し、Oxford Advanced Learner's Dictionary で照合する。
- 難易度は次の3段階で分類する。
  - **Beginner**: 一般語として広く知られ、エンジニアも意味を推測しやすい
  - **Intermediate**: 一般語だが実務での用法に学習価値がある、または技術文脈で頻出する
  - **Advanced**: 一般英語として日常的に使われず、エンジニアも英単語としては馴染みが薄い
- 説明と使用例は、実際に見聞きした使われ方を参考に独自に作成する。

## 作業ルール

- Vocabularyの作成・更新は [vocabulary-markdown ルール](.agents/rules/vocabulary-markdown.md) に従う。
- 語義・品詞・発音の調査は [researching-vocabulary Skill](.agents/skills/researching-vocabulary/SKILL.md) に従う。
- 難易度の判定は [evaluating-difficulty Skill](.agents/skills/evaluating-difficulty/SKILL.md) に従う。
- シーンの判定は [evaluating-scene Skill](.agents/skills/evaluating-scene/SKILL.md) に従う。
- `meaningJa` の評価は [evaluating-meaningJa Skill](.agents/skills/evaluating-meaningJa/SKILL.md) に従う。
- 日本語文の作成・レビューは [japanese-tech-writing Skill](.agents/skills/japanese-tech-writing/SKILL.md) に従う。
- 語彙の並べ替え・再採番は [sorting-vocabulary Skill](.agents/skills/sorting-vocabulary/SKILL.md) に従う。

# Engineer English

> English: [AGENTS.md](AGENTS.md)

ソフトウェアエンジニアが実務で使う英語のデータセット。

## コンセプト

- 信頼性の高い一次情報（Google Engineering Practices、Google SREのCC BY 4.0資料、MDN Web Docs）から、ソフトウェアエンジニアリングの文脈で実際に使われる単語・フレーズを抽出する。
- 語義・品詞・発音記号（米国英語のIPA）は、信頼性の高い外部の辞書（一次: Cambridge Dictionary、照合: Oxford Advanced Learner's Dictionary）から取得する。
- 難易度は次の3段階で分類する。
  - **Beginner**: 一般語として広く知られ、エンジニアも意味を推測しやすい
  - **Intermediate**: 一般語だが実務での用法に学習価値がある、または技術文脈で頻出する
  - **Advanced**: 一般英語として日常的に使われず、エンジニアも英単語としては馴染みが薄い
- 日本語訳・説明・使用例は独自に作成し、出典本文をコピー・翻案しない。

## 作業ルール

- Vocabularyの作成・更新は [vocabulary-markdown ルール](.agents/rules/vocabulary-markdown.md) に従う。
- 語義・品詞・発音の調査は [researching-vocabulary Skill](.agents/skills/researching-vocabulary/SKILL.md) に従う。
- 難易度の判定は [evaluating-difficulty Skill](.agents/skills/evaluating-difficulty/SKILL.md) に従う。
- シーンの判定は [evaluating-scene Skill](.agents/skills/evaluating-scene/SKILL.md) に従う。
- `meaningJa` の評価は [evaluating-meaningJa Skill](.agents/skills/evaluating-meaningJa/SKILL.md) に従う。
- 日本語文の作成・レビューは [japanese-tech-writing Skill](.agents/skills/japanese-tech-writing/SKILL.md) に従う。
- 語彙の並べ替え・再採番は [sorting-vocabulary Skill](.agents/skills/sorting-vocabulary/SKILL.md) に従う。

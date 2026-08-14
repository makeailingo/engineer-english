# Vocabulary Markdown

> English: [vocabulary-markdown.md](vocabulary-markdown.md)

対象: `docs/vocabulary/**/*.md`

- 1ファイルにつき1件とし、ファイル名は`<id>_<term>.md`とする。`term`部分は小文字のkebab-caseにする。
- `docs/templates/vocabulary.md`を複製し、YAML Front Matterの全属性を記載する。
- YAML Front Matter を唯一の正本とする。項目の表示見出し（日英併記）は Jekyll レイアウトが生成する。Markdown 本文にフィールド値を複製しない。
- フィールド順序は `id`, `term`, `type`, `partOfSpeech`, `pronunciation`, `description`, `descriptionJa`, `meaning`, `meaningJa`, `usageExample`, `usageExampleJa`, `difficulty`, `scene` とする。
- 意味・品詞・発音は researching-vocabulary Skill に従う。
- `difficulty`は evaluating-difficulty Skill に従う。
- `scene`は evaluating-scene Skill に従う。
- `meaningJa`は evaluating-meaningJa Skill に従う。
- `id`は`"0001"`から`"9999"`までの重複のない4桁連番とする。`id`は表示順・学習順を表す。
- 学習順は [sorting-vocabulary Skill](.agents/skills/sorting-vocabulary/SKILL.md) に従う。Scene（転職・面接 → 実装・コードレビュー → 会議・イベント → 設計・アーキテクチャ → 障害対応 → テクニカルライティング → マネジメント）の順に分類し、各 Scene 内では難易度 → 学習価値 → 実用性の順で並べ、IDを振り直す。
- `type`は`word`または`phrase`とする。
- `difficulty`と`scene`は下記マスタからそれぞれ1つだけ選ぶ。
- ソフトウェアエンジニア自身が英語で働く中で実際に見聞きした語彙だけを追加する。
- 意味、日本語訳、説明、使用例、使用例訳は独自に作成する。
- 社内のメッセージ、文書、議事録、会話を転載しない。会社名、製品名、プロジェクト名、顧客名、個人名を含めない。
- 意味、説明、使用例、使用例訳、`scene`を意味的に一致させる。
- `description`は120文字以内にする。
- `descriptionJa`は80文字以内にする。
- `usageExample`は25語以内、`usageExampleJa`は80文字以内にする。
- これらの上限は可読性のための目安であり、短く切り詰めるための目標ではない。語数や文字数に合わせて不自然に削らず、自然で完結した1文を優先する。
- 使用例は、実際に見聞きした使われ方を参考に独自に作成する。対象語の意味が文脈から判断できる、自然で具体的な表現にする。
- `usageExampleJa`の作成・修正・レビューは [japanese-tech-writing Skill](.agents/skills/japanese-tech-writing/SKILL.md) に従う。
- 作成前に既存Vocabularyとの重複を確認する。
- 再利用できる表現を優先する。各エントリはプロジェクトが変わっても使えること。名詞を `A` や `B`、一般的な役割名に置き換えても実務で使えるフレーズなら採用する。一般化すると当たり前すぎる、意味が消える場合は、元PRの文をそのまま残さず削除または書き直す。

## 再利用性

別プロジェクトでも、名詞を `A` や `B`、一般的な役割名に置き換えて使えるフレーズかを確認する。その抽象度で残す。元のPRやチケットにしか通用しない表現は、削除するか書き直す。

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
- 80文字以内の制約を守りつつ、助詞不足の名詞連結（「API不可時」など）になっていないか。
- 依頼・疑問のトーンが英語と揃っているか（`Please` / `Could you` → 「〜してください」だけにしない）。
- 定訳・慣用語を使っているか（`cooldown` → クールダウン、`liveness probe` → ライブネスプローブ、`footprint` → フットプリント など）。
- 同一語彙セット内で表記がぶれていないか（レイテンシ / レイテンシー、デプロイ / 配備 など）。
- LLM 口調の空句、em ダッシュ、中黒並列、イ形容詞 + 「です」の孤立文がないか。

## Scene Master

| English | 日本語 |
| --- | --- |
| Career / Interview | 転職・面接 |
| Implementation / Review | 実装・コードレビュー |
| Meetings / Events | 会議・イベント |
| Design / Architecture | 設計・アーキテクチャ |
| Incident Response | 障害対応 |
| Technical Writing | テクニカルライティング |
| Management | マネジメント |

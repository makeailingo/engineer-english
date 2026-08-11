---
name: sorting-vocabulary
description: Engineer English の語彙を5章の学習順に並べ替え、ID・ファイル名・参照を更新する。語彙の並べ替え、再採番、章分類を依頼されたときに使用する。
---

# Sorting Vocabulary

Engineer English の語彙を学習しやすい順序に並べ替え、
ID・ファイル名・関連参照を更新する。

対象: `docs/vocabulary/**/*.md`

## 1. 章

すべての語彙を以下の5章のいずれかに分類する。

### 第1章 基本コミュニケーション

確認・依頼・共有・意見・認識合わせなど、
日常的なエンジニア業務で使う英語。

例:
- follow up
- wrap up
- clarify
- reach out
- heads-up

### 第2章 開発とレビュー

実装・コードレビュー・テスト・デバッグなど、
コードを読み書きし改善する場面で使う英語。

例:
- reproduce
- isolate
- validate
- refactor
- regression

### 第3章 計画と意思決定

要件・優先順位・見積もり・根拠・トレードオフなど、
何をどう作るか決める場面で使う英語。

例:
- scope
- priority
- estimate
- rationale
- trade-off

### 第4章 運用と障害対応

インフラ・性能・インシデント・リスクなど、
サービスを運用する場面で使う英語。

例:
- mitigate
- rollback
- outage
- latency
- on-call

### 第5章 高度な技術英語

アーキテクチャ・技術面接・高度な議論・
ニュアンスの難しい表現。

例:
- abstraction
- scalability
- corroborate
- recursion
- time complexity

## 2. 章の順序

必ず以下の順序にする。

1. 基本コミュニケーション
2. 開発とレビュー
3. 計画と意思決定
4. 運用と障害対応
5. 高度な技術英語

既存の `scene` は章分類の参考にしてよいが、
Sceneを機械的にChapterへ変換してはいけない。

## 3. 章分類を章内ソートより先に確定する

作業の順序は必ず次のとおりとする。

1. 全語彙を5章のどこに属するか決定する
2. 各章の中だけを並べ替える
3. 5章を連結する
4. IDを再採番する

1〜4章を先に並べ、残りを第5章へ置く処理は禁止する。
難易度や `scene` を理由に、
本来別の章に属する語を第5章へ送ってはいけない。

第5章は「残った語を入れる章」ではない。
第5章に含めるのは、
アーキテクチャ・技術面接・高度な技術議論・
高度なニュアンスを持つ語彙に限定する。

第5章に入れてはいけない例:

- `currently`、`previously`、`shortly` などの一般副詞
  （第1章 基本コミュニケーション）
- `alternative`、`approach`、`select` などの初級一般語
  （第3章 計画と意思決定、または該当する章）
- `migrate`、`swap` などのデータベース実務語
  （第4章 運用と障害対応）

`scene` が Architecture でも、
初級の一般語や計画・意思決定の語彙は第5章に入れない。
`scene` が Daily Communication や Debugging の語彙を、
難易度が Advanced だからといって第5章へ送らない。

### 章分類の目安

| 章 | 主な `scene` | 補足 |
| --- | --- | --- |
| 第1章 | Daily Communication | 確認・依頼・共有・意見・認識合わせ |
| 第2章 | Implementation, Code Review, Debugging, Testing | コードの読み書きと改善 |
| 第3章 | Sprint Planning, Requirements, Leadership / Management | 計画・要件・意思決定 |
| 第4章 | Incident Response, Infrastructure / Cloud, Performance, Security, Database | 運用・障害・性能・セキュリティ |
| 第5章 | Architecture（高度な語彙）, Technical Interview | 上記4章に属さない高度な技術語のみ |

Architecture の語彙は、
初級一般語は第3章、
高度な技術議論・設計の語彙は第5章とする。

## 4. 章内の並べ替え

各章では、以下の優先順位で前に配置する。

1. 日本人エンジニアにとって学習価値が高い
2. 実務で遭遇・使用する頻度が高い（実用性）
3. Beginner → Intermediate → Advanced（難易度）

難易度だけでは決めない。
上級ラベルでも、Engineer English として学習価値・実用性が高い語彙
（`touch base`、`loop in`、`circle back` など）は
初級の一般語より前に置く。

例えば `update` のように意味が明白で
学習価値の低い語を、Beginnerという理由だけで
章の先頭に配置しない。

一方、

- wrap up
- follow up
- point out
- hold off
- sort out

のような、簡単な単語から構成されていても
日本人学習者には意味を推測しづらい表現は優先する。

## 5. IDの再採番

すべての並べ替えが完了した後、
最終的な学習順に従ってIDを振り直す。

- 最初: `0001`
- 次: `0002`
- ...
- 最後: 全語彙数

旧IDを維持する必要はない。

## 6. ファイル名の変更

語彙ファイル名は新しいIDに合わせて変更する。

例:

旧:
`0042_wrap-up.md`

新しい学習順で15番目になった場合:

`0015_wrap-up.md`

term部分は変更しない。

## 7. コンテンツの更新

各MarkdownファイルのFront Matterにある `id` を
新しいIDへ更新する。

並べ替え作業では以下は変更しない。

- term
- type
- difficulty
- scene
- meaningJa
- descriptionJa
- usageExample
- usageExampleJa
- source

## 8. 参照の更新

旧IDまたは旧ファイル名を参照している箇所がある場合、
すべて新しいID・ファイル名へ更新する。

対象例:

- Markdownリンク
- Jekyll内部リンク
- テスト
- fixtures
- snapshot
- README
- ドキュメント

termだけを参照しておりIDに依存しない箇所は変更しない。

## 9. 検証

作業完了後、必ず以下を確認する。

- 全語彙が5章のいずれかに属する
- 章の順序が正しい
- 全語彙が1回だけ存在する
- 語彙の追加・削除がない
- IDが0001から連続している
- IDの重複・欠番がない
- ファイル名とFront MatterのIDが一致する
- 旧IDへの参照が残っていない
- termや意味、例文などが意図せず変更されていない
- Jekyllのbuildと既存テストが成功する

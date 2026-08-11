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

## 3. 章内の並べ替え

各章では、以下を優先して前に配置する。

1. 実務で遭遇・使用する頻度が高い
2. 日本人エンジニアにとって学習価値が高い
3. 複数の場面で応用できる
4. 意味・使い方が理解しやすい
5. Beginner → Intermediate → Advanced

難易度だけでは決めない。

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

## 4. IDの再採番

すべての並べ替えが完了した後、
最終的な学習順に従ってIDを振り直す。

- 最初: `0001`
- 次: `0002`
- ...
- 最後: 全語彙数

旧IDを維持する必要はない。

## 5. ファイル名の変更

語彙ファイル名は新しいIDに合わせて変更する。

例:

旧:
`0042_wrap-up.md`

新しい学習順で15番目になった場合:

`0015_wrap-up.md`

term部分は変更しない。

## 6. コンテンツの更新

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

## 7. 参照の更新

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

## 8. 検証

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

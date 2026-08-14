---
name: sorting-vocabulary
description: Engineer English の語彙をScene順に並べ替え、ID・ファイル名・参照を更新する。語彙の並べ替え、再採番、Scene分類を依頼されたときに使用する。
---
# Sorting Vocabulary

> English: [SKILL.md](SKILL.md)

Engineer English の語彙を学習しやすい順序に並べ替え、
ID・ファイル名・関連参照を更新する。

対象: `docs/vocabulary/**/*.md`

並べ替えは本 Skill に従って直接行う。
Python などの自動化スクリプトは作成しない。

## 1. Scene

すべての語彙を [evaluating-scene Skill](../evaluating-scene/SKILL.ja.md)
に従い、いずれか1つのSceneへ分類する。

## 2. Sceneの順序

必ず以下の順序にする。

1. Career / Interview
2. Implementation / Review
3. Meetings / Events
4. Design / Architecture
5. Incident Response
6. Technical Writing
7. Management

## 3. Scene分類をScene内ソートより先に確定する

作業の順序は必ず次のとおりとする。

1. 意味と使用例から各語彙のSceneを決定する
2. 各Sceneの中だけを並べ替える
3. 7つのSceneを所定の順序で連結する
4. IDを再採番する

termだけでSceneを決めない。Technical Writingは技術文書の作成・保守が
主目的の使用例に付ける。障害対応やレビューで文書を参照するだけなら、
機械的にTechnical Writingへ分類しない。

## 4. Scene内の並べ替え

各Sceneでは、以下の優先順位で前に配置する。

1. Beginner → Intermediate → Advanced（難易度）
2. 日本人エンジニアにとって学習価値が高い
3. 実際に見聞きする頻度が高い（実用性）

各Sceneの前半には初級語を置き、文脈ごとに学習を始めやすくする。

同じ難易度内では、

- wrap up
- follow up
- point out
- hold off
- sort out

のような、簡単な単語から構成されていても
日本人学習者には意味を推測しづらい表現を優先する。

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
- partOfSpeech
- pronunciation
- meaning
- meaningJa
- description
- descriptionJa
- difficulty
- scene
- usageExample
- usageExampleJa

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

- 全語彙が7つのSceneのいずれかに属する
- Sceneの順序が正しい
- 全語彙が1回だけ存在する
- 語彙の追加・削除がない
- IDが0001から連続している
- IDの重複・欠番がない
- ファイル名とFront MatterのIDが一致する
- 旧IDへの参照が残っていない
- termや意味、例文などが意図せず変更されていない
- Jekyllのbuildと既存テストが成功する

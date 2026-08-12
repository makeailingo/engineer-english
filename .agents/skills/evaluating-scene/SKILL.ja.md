---
name: evaluating-scene
description: usageExample と source context から Vocabulary の scene が整合しているか評価する。Vocabulary の作成・更新前、または scene の検証時に使用する。
---
# Evaluating Scene

> English: [SKILL.md](SKILL.md)

Vocabulary の `scene` が、その語義・使用例・一次資料で確認した
エンジニアリング文脈と整合しているか評価する。

Scene は term 単体では判定しない。

## Input

```yaml
term: "router"
meaningJa: "ルーター、経路振分"
usageExample: "..."
source:
  title: "..."
  url: "..."
  context: "..."
currentScene: "Meetings / Events"
```

## Scene Master

* Career / Interview
* Implementation / Review
* Meetings / Events
* Design / Architecture
* Incident Response
* Technical Writing
* Management

## Evaluation Principle

Scene は、

> 「この単語は何に関係するか」

ではなく、

> 「この用例で、エンジニアは何の仕事をしているか」

で決定する。

例えば `review`, `server`, `error`, `database` などの
キーワードが含まれているだけでは Scene の根拠にしない。

## Workflow

### 1. 語義を固定する

`meaningJa` と `usageExample` から、
この Vocabulary で採用している語義を特定する。

別語義を根拠に Scene を判定しない。

### 2. 使用例の行為を特定する

使用例について、

* 誰が
* 何を
* 何の目的でしているか

を短く要約する。

例:

> "Escalate unresolved disagreements to the engineering manager."

→ 解決できない技術的対立について上位者に判断を求めている。

### 3. 一次資料の文脈を確認する

`source.url` を開き、実際にその term が使われている周辺を確認する。

検索結果の要約だけで判定しない。

一次資料上で、

* code review
* incident handling
* system design
* implementation
* testing

など、どの活動について述べられているか確認する。

### 4. Scene Master に対応させる

以下の定義に最も直接一致する Scene を1つ選ぶ。

## Scene Definitions

### Career / Interview

転職活動、応募、面接準備、面接での評価を扱う。

### Implementation / Review

コードや機能の実装、変更、テスト、デバッグ、レビューを行う。

### Meetings / Events

相談、議論、計画、発表、ワークショップ、チームイベントを扱う。

### Design / Architecture

要件を定義し、システム構造、データ、インフラ、性能、
セキュリティに関する設計判断を行う。

### Incident Response

本番障害を検知・緩和・復旧・エスカレーションする。

### Technical Writing

技術文書を作成、編集、構成、保守する。

### Management

育成、責任、組織調整、意思決定、マネジメントを扱う。

## Conflict Resolution

複数 Scene に該当しそうな場合は、
単語の一般的な所属ではなく **usageExample で行われている主目的**
を採用する。

例:

"Review the query before merging this change."

* query → Design / Architecture ではない
* merging / review が主目的
  → Implementation / Review

"Optimize this query to reduce response latency."

* query は Database
* 行為の主目的は性能改善
  → Design / Architecture

"Restore the database after the production outage."

* database が含まれる
* 主目的は障害復旧
  → Incident Response

## Evaluation

`currentScene` と判定結果を比較する。

```yaml
result: PASS # PASS | FAIL
currentScene: "Meetings / Events"
expectedScene: "Design / Architecture"
reason: "The example concerns network routing, not a meeting or event."
```

Scene が一致していれば PASS。

一致しなければ FAIL とし、
`expectedScene` を返す。

## Output

検証時:

```yaml
term: "router"
actionSummary: "トラフィック移行前にルーター規則を更新している。"
expectedScene: "Design / Architecture"
currentScene: "Meetings / Events"
result: FAIL
reason: "主目的はデプロイ基盤上のトラフィック振分であり、会議ではない。"
confidence: High
```

新規作成・更新時:

```yaml
term: "router"
actionSummary: "トラフィック移行前にルーター規則を更新している。"
scene: "Design / Architecture"
confidence: High
notes: "source は Express デプロイ文脈だが、行為はインフラ運用。"
```

`actionSummary` を先に書き、その後 `scene` または `expectedScene` を書く。

## Confidence

- `High`: 使用例の主目的と一次資料の活動が一致し、Scene が1つに定まる
- `Medium`: 主目的は特定できるが、複数 Scene の境界付近である
- `Low`: 使用例だけでは主目的が曖昧、または一次資料と乖離がある

`confidence` が Low でも、Scene Master から1つ選ぶ。`notes` に迷いを記録する。

## Vocabulary への反映

評価結果の `scene` を Vocabulary の YAML Front Matter に転記する。
`actionSummary` は中間出力として残してよいが、Vocabulary 本体には載せない。

FAIL の場合は `expectedScene` で Vocabulary の `scene` を修正する。

## Rules

* term 単体で Scene を決めない。
* カタカナ技術用語のカテゴリだけで決めない。
* usageExample に登場する名詞だけで決めない。
* `source` のカテゴリを無条件に Scene にコピーしない。
* usageExample の **主たる仕事・目的** を最優先する。
* 必ず Scene Master から1つだけ選ぶ。

## 文言

Skill 本文では、一般的でない専門用語を使わない。

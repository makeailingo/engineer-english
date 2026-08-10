---
name: evaluating-difficulty
description: Cambridge Dictionary と Oxford Learner's Dictionaries の公開 CEFR 情報から Vocabulary の difficulty を機械的に判定する。Vocabulary の作成・更新前に使用する。
---

# Evaluating Difficulty

ネット上で機械的に参照できる公開ソースでないと、再現可能な Eval にはしづらい。その前提で、Difficulty Eval は Cambridge Dictionary の CEFR 表示と Oxford Learner's Dictionaries の語彙リストを使う。

## 参照ソース

| 対象 | 第一候補 | 補助 |
| --- | --- | --- |
| word | [Cambridge Dictionary](https://dictionary.cambridge.org/dictionary/english/) | [Oxford 3000 / 5000](https://www.oxfordlearnersdictionaries.com/about/wordlists/) |
| phrase | [Oxford Phrase List](https://www.oxfordlearnersdictionaries.com/about/wordlists/oxford-phrase-list) | Cambridge Dictionary（CEFR がある場合） |

- Cambridge Dictionary: 語ごとに CEFR（A1〜C2）が明示されている場合がある。例: `courteous` は **C2**。(https://dictionary.cambridge.org/dictionary/english/courteous)
- Oxford 3000 / 5000: 各語に CEFR レベルが付いている。Oxford 3000 は A1〜B2、Oxford 5000 は追加の B2〜C1 語彙。(https://www.oxfordlearnersdictionaries.com/about/wordlists/)
- Oxford Phrase List: フレーズごとに A1〜C1 の CEFR が付いている。(https://www.oxfordlearnersdictionaries.com/about/wordlists/oxford-phrase-list)

ローカル教材（金フレ等）の載載位置には依存しない。毎回ネット検索して再現できる Eval とする。

## Input

```yaml
term: "courteous"
type: "word" # word | phrase
```

## Workflow

### word の場合

1. Cambridge Dictionary で CEFR を取得する。
2. Oxford 3000 / 5000 で CEFR を取得する。
3. 両方ある場合は一致を確認する。
4. 片方しかない場合はその値を採用する。
5. どちらにも CEFR がない場合は推測する。

### phrase の場合

1. Oxford Phrase List で CEFR を取得する。
2. 見つからない場合は Cambridge Dictionary で CEFR を確認する。
3. どちらにも CEFR がない場合は推測する。

検索結果の要約だけで判断せず、各ページを開いて確認する。

## CEFR → Difficulty 変換

```text
A1-A2 → Beginner
B1-B2 → Intermediate
C1-C2 → Advanced
```

複数の CEFR が付いている場合、または語義ごとにレベルが異なる場合は、**最も高い CEFR** を採用して Difficulty に変換する。これは [Difficulty Master](.agents/rules/vocabulary-markdown.md) の「理解に必要な知識が最も多い Difficulty を選ぶ」に合わせる。

## Output

```yaml
term: "courteous"
type: "word"
difficulty: "Advanced"
cefr:
  cambridge: "C2"
  oxford: null
  adopted: "C2"
  method: "cambridge-only" # both | cambridge-only | oxford-only | inferred
sources:
  - role: cefrPrimary
    title: "COURTEOUS | English meaning - Cambridge Dictionary"
    url: "https://dictionary.cambridge.org/dictionary/english/courteous"
  - role: cefrCrossCheck
    title: null
    url: null
confidence: "High" # High | Medium | Low
notes: "Cambridge C2 → Advanced"
```

## Confidence

- `High`: Cambridge と Oxford の CEFR が一致している、または片方のみで CEFR が明示されている。
- `Medium`: 片方のみで CEFR があり、もう一方は未掲載。または CEFR 範囲（例: B1-B2）から変換した。
- `Low`: 公開ソースに CEFR がなく推測に頼った。理由を `notes` に記録する。

## 例

### courteous（word）

```text
Cambridge: C2
→ Advanced
```

`Beginner` は CEFR と矛盾するため不自然。

### trade-off（phrase）

1. Oxford Phrase List で CEFR を確認する。
2. 見つかればその CEFR から Difficulty に変換する。
3. 見つからなければ Cambridge で確認し、なければ推測する。

## Vocabulary への反映

Eval 結果の `difficulty` を Vocabulary の Front Matter に転記する。Eval 用の `sources` と `cefr` は調査の中間出力として残し、Vocabulary の `source` には引き続き Engineering 一次資料のみを記録する（[researching-vocabulary](.agents/skills/researching-vocabulary/SKILL.md) に従う）。

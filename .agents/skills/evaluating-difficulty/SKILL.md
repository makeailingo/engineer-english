---
name: evaluating-difficulty
description: CEFR（Cambridge / Oxford）から Vocabulary の difficulty を機械的に判定する。Vocabulary の作成・更新前に使用する。
---

# Evaluating Difficulty

再現性を持たせるため、Difficulty Eval は **CEFR のみ** から行う。

## 参照ソース

| 用途 | ソース |
| --- | --- |
| CEFR（word） | [Cambridge Dictionary](https://dictionary.cambridge.org/dictionary/english/) → [Oxford 3000 / 5000](https://www.oxfordlearnersdictionaries.com/about/wordlists/) |
| CEFR（phrase） | [Oxford Phrase List](https://www.oxfordlearnersdictionaries.com/about/wordlists/oxford-phrase-list) → Cambridge Dictionary |

ローカル教材（金フレ等）には依存しない。毎回公開ソースを参照して再現できる Eval とする。

## Input

```yaml
term: "feedback"
type: "word" # word | phrase
```

## Difficulty Eval

1. Cambridge Dictionary、Oxford 3000 / 5000からCEFRを取得する。
2. CEFRをDifficultyに変換する:
   - A1-B1: Beginner
   - B2-C1: Intermediate
   - C2: Advanced

```text
CEFR → Difficulty
```

### Step 1: CEFR の取得

#### word

1. Cambridge Dictionary で CEFR を取得する（`class="epp-xref dxref …"`）。
2. Oxford Learner's Dictionaries で CEFR を取得する（`cefr="…"`）。
3. 両方ある場合は一致を確認する。片方しかない場合はその値を採用する。
4. どちらにも CEFR がない場合は推測する。

#### phrase

1. Oxford Phrase List で CEFR を確認する。
2. 見つからない場合は Cambridge Dictionary で CEFR を確認する。
3. どちらにも CEFR がない場合は推測する。

複数の CEFR が付いている場合、または語義ごとにレベルが異なる場合は、**最も高い CEFR** を採用する。

検索結果の要約だけで判断せず、各ページを開いて確認する。

## 判定例

| Term | CEFR | Difficulty |
| --- | --- | --- |
| feedback | B2 | **Intermediate** |
| courteous | C2 | **Advanced** |
| priority | B2 | **Intermediate** |
| consensus | C1 | **Intermediate** |
| clarify | C1 | **Intermediate** |
| scrutiny | C2 | **Advanced** |
| critique | C1 | **Intermediate** |
| isolate | C1 | **Intermediate** |
| assertion | C1 | **Intermediate** |
| coverage | B2 | **Intermediate** |
| reliability | B2 | **Intermediate** |
| availability | B2 | **Intermediate** |
| capacity | B2 | **Intermediate** |
| ownership | B2 | **Intermediate** |

### feedback

```text
Cambridge: B2
→ Intermediate
```

### courteous

```text
Cambridge: C2
→ Advanced
```

### clarify

```text
Cambridge: C1
→ Intermediate
```

## Output

```yaml
term: "feedback"
type: "word"
difficulty: "Intermediate"
cefr:
  cambridge: "B2"
  oxford: "B2"
  adopted: "B2"
  method: "both"
sources:
  - role: cefrPrimary
    title: "FEEDBACK | English meaning - Cambridge Dictionary"
    url: "https://dictionary.cambridge.org/dictionary/english/feedback"
  - role: cefrCrossCheck
    title: "feedback verb - Oxford Learners Dictionaries"
    url: "https://www.oxfordlearnersdictionaries.com/definition/english/feedback"
confidence: "High"
notes: "B2 → Intermediate"
```

## Confidence

- `High`: CEFR が Cambridge または Oxford で確認できた。
- `Medium`: CEFR は片方のみ、または CEFR がなく推測した。
- `Low`: CEFR が確認できず推測に頼った。理由を `notes` に記録する。

## アルゴリズム検証

新規ルール導入時は、個々の単語を人間判定するのではなく、代表語20件程度でアルゴリズム自体の妥当性を検証する。

検証用語の例: `feedback`, `scope`, `deploy`, `clarify`, `courteous`, `scrutiny`, `priority`, `consensus`

## 日本人エンジニアへの馴染みについて

「日本人エンジニアには簡単」という観点は Difficulty とは別軸です。将来的に `familiarityJa` などの別属性として扱うことを想定しています。

## Vocabulary への反映

Eval 結果の `difficulty` を Vocabulary の Front Matter に転記する。Eval 用の `cefr` は調査の中間出力として残し、Vocabulary の `source` には引き続き Engineering 一次資料のみを記録する（[researching-vocabulary](.agents/skills/researching-vocabulary/SKILL.md) に従う）。

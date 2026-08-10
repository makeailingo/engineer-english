---
name: evaluating-difficulty
description: CEFR（Cambridge / Oxford）と JMdict の外来語定着度から Vocabulary の difficulty を機械的に判定する。Vocabulary の作成・更新前に使用する。
---

# Evaluating Difficulty

再現性を持たせるため、Difficulty Eval は **CEFR + 日本語への定着度** の2段階で行う。

## 参照ソース

| 用途 | ソース |
| --- | --- |
| CEFR（word） | [Cambridge Dictionary](https://dictionary.cambridge.org/dictionary/english/) → [Oxford 3000 / 5000](https://www.oxfordlearnersdictionaries.com/about/wordlists/) |
| CEFR（phrase） | [Oxford Phrase List](https://www.oxfordlearnersdictionaries.com/about/wordlists/oxford-phrase-list) → Cambridge Dictionary |
| 外来語定着 | [JMdict](https://www.edrdg.org/jmdict/j_jmdict.html)（機械利用可能な日英辞書データ） |

ローカル教材（金フレ等）には依存しない。毎回公開ソースを参照して再現できる Eval とする。

## Input

```yaml
term: "feedback"
type: "word" # word | phrase
```

## Difficulty Eval

1. Cambridge Dictionary、Oxford 3000 / 5000からCEFRを取得する。
2. CEFRを以下に変換する。
   - A1-B1: Beginner
   - B2-C1: Intermediate
   - C2: Advanced
3. JMdictに、その英単語に対応する日本語の外来語が登録されている場合、Difficultyを1段階下げる。
4. Beginnerより下にはしない。

```text
CEFR Difficulty
      ↓
JMdictに対応する外来語あり？
      ↓ YES
1段階下げる
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

### Step 2: JMdict 外来語チェック

[JMdict](https://www.edrdg.org/jmdict/j_jmdict.html) で、対象の英単語に対応する**カタカナ表記の外来語**が登録されているか確認する。

- 外来語あり → CEFR から変換した Difficulty を **1段階下げる**
- 外来語なし → CEFR から変換した Difficulty をそのまま採用する
- Beginner より下にはしない

## 判定例

| Term | CEFR | CEFR Difficulty | JMdict外来語 | Final |
| --- | --- | --- | --- | --- |
| feedback | B2 | Intermediate | フィードバック ✅ | **Beginner** |
| courteous | C2 | Advanced | なし | **Advanced** |
| priority | B2 | Intermediate | プライオリティ ✅ | **Beginner** |
| consensus | C1 | Intermediate | コンセンサス ✅ | **Beginner** |
| clarify | C1 | Intermediate | なし | **Intermediate** |
| scrutiny | C2 | Advanced | なし | **Advanced** |

### feedback

```text
Cambridge: B2
→ Intermediate

JMdict:
フィードバック = feedback
→ 1 level down

Final: Beginner
```

### courteous

```text
Cambridge: C2
→ Advanced

JMdict:
対応外来語なし

Final: Advanced
```

### clarify

```text
Cambridge: C1
→ Intermediate

JMdict:
対応外来語なし

Final: Intermediate
```

## Output

```yaml
term: "feedback"
type: "word"
difficulty: "Beginner"
cefr:
  cambridge: "B2"
  oxford: "B2"
  adopted: "B2"
  cefrDifficulty: "Intermediate"
  method: "both"
jmdict:
  loanword: "フィードバック"
  found: true
  adjusted: true
sources:
  - role: cefrPrimary
    title: "FEEDBACK | English meaning - Cambridge Dictionary"
    url: "https://dictionary.cambridge.org/dictionary/english/feedback"
  - role: cefrCrossCheck
    title: "feedback verb - Oxford Learners Dictionaries"
    url: "https://www.oxfordlearnersdictionaries.com/definition/english/feedback"
  - role: jmdict
    title: "JMdict"
    url: "https://www.edrdg.org/jmdict/j_jmdict.html"
confidence: "High"
notes: "B2 → Intermediate → JMdict フィードバック → Beginner"
```

## Confidence

- `High`: CEFR が Cambridge または Oxford で確認でき、JMdict の外来語有無も確認できた。
- `Medium`: CEFR は片方のみ、または CEFR がなく推測した。JMdict は確認できた。
- `Low`: CEFR も JMdict も確認できず推測に頼った。理由を `notes` に記録する。

## アルゴリズム検証

新規ルール導入時は、個々の単語を人間判定するのではなく、代表語20件程度でアルゴリズム自体の妥当性を検証する。

検証用語の例: `feedback`, `scope`, `deploy`, `clarify`, `courteous`, `scrutiny`, `priority`, `consensus`

## Vocabulary への反映

Eval 結果の `difficulty` を Vocabulary の Front Matter に転記する。Eval 用の `cefr` と `jmdict` は調査の中間出力として残し、Vocabulary の `source` には引き続き Engineering 一次資料のみを記録する（[researching-vocabulary](.agents/skills/researching-vocabulary/SKILL.md) に従う）。

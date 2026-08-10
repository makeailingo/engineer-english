# Difficulty Eval POC 結果

実施日: 2026-08-10  
スクリプト: `poc_reproducibility.py`

## 結論

**100% 再現可能な Eval 仕組みは、現時点では未成立。**

先に Eval 本体の実装・提案は行わない。参照データ取得パイプラインの POC を追加で通す必要がある。

---

## 検証したこと

| # | 検証内容 | 結果 |
|---|----------|------|
| 1 | ライブ取得（Cambridge + Oxford ページ）を同一語で2回実行 → CEFR 一致 | **PASS** (15/15) |
| 2 | 凍結 JSON から Eval → 2回同一結果 | **PASS** |
| 3 | 自動取得 CEFR が Skill 記載値と一致 | **FAIL** (7/12 = 58%) |
| 4 | ユーザー指摘の replace vs invoke を ordering inversion で検出 | **FAIL** |
| 5 | ユーザー指摘の C1 語群を same-CEFR split で検出 | **PASS** |
| 6 | Oxford 3000/5000 wordlist の run 間一致 | **PASS** (2979 entries) |
| 7 | Oxford wordlist の 100語カバー率 | **FAIL** (22/100) |

---

## 詳細

### 1. ライブスクレイピングは「同じ結果」だが「正しい参照」ではない

15語 × 2回取得で run 間不一致は 0 件。HTML が同じならパース結果も同じ。

しかし Skill に明記された CEFR と自動取得値の一致率は **58%**。

| term | Skill 記載 | 自動取得 (adopted) | 一致 |
|------|-----------|-------------------|------|
| feedback | B2 | B2 | OK |
| courteous | C2 | C2 | OK |
| clarify | C1 | C1 | OK |
| scrutiny | C2 | C2 | OK |
| critique | C1 | C1 | OK |
| isolate | C1 | C1 | OK |
| assertion | C1 | C1 | OK |
| coverage | **B2** | **C1** | NG |
| availability | **B2** | **C1** | NG |
| reliability | **B2** | **C1** | NG |
| capacity | **B2** | **C1** | NG |
| ownership | **B2** | **C1** | NG |

主な原因:

- **「ページ内最高 CEFR 採用」ルール** — `replace` は Cambridge で B1（CHANGE FOR）と C2（PUT BACK）があり、自動取得は C2 を採用。実務語義は B1。
- **Cambridge CEFR 欠落** — critique / isolate / assertion / invoke は Cambridge に CEFR なし。Oxford Topics の `c1` パースに依存。
- **ソース間不一致の max 採用** — availability は Cambridge B2、Oxford C1 → C1 採用。Skill は B2。

### 2. ordering inversion 単体では replace=Advanced を検出できない

自動取得 CEFR:

```
replace   → C2 (Cambridge C2 が max に入る)
invoke    → C1
```

現行 difficulty:

```
replace   → Advanced  (rank 3)
invoke    → Intermediate (rank 2)
```

CEFR 順と difficulty 順が一致しているため、**inversion にはならない**。
ユーザーが「replace=Advanced は高すぎる」と感じるケースを、このチェックだけでは拾えない。

### 3. same-CEFR split は部分的成功

C1 語群で Beginner / Intermediate が混在:

```
Beginner:     critique, isolate, assertion, coverage, availability, reliability, capacity, ownership
Intermediate: clarify, invoke
```

ユーザー指摘の「critique=Beginner なのに clarify=Intermediate」は検出可能。
ただし **参照 CEFR が正しいことが前提**。C1 以外（B2 語群の Beginner 化）も Skill 基準では多数あるが、自動 CEFR では B2 判定できない語がある。

### 4. Oxford 3000/5000 wordlist は再現性高いがカバー不足

- 2979 語、2回取得で完全一致
- 100語中 **22語しか収録なし**（critique, invoke, coverage, availability 等は未収録）
- 単独参照ソースにはなれない

### 5. Skill 記載 CEFR を参照にした場合（上限ベンチマーク）

人手確認済み参照を使うと:

- ユーザー指摘 10語: absolute mismatch で **10/10 検出**
- replace vs invoke: ordering inversion で **検出**
- ただしこれは **自動再現ではない**（Skill 記載値のメンテナンスが必要）

---

## 再現性の分解

| レイヤ | 再現可能か | 備考 |
|--------|-----------|------|
| Eval ロジック（凍結入力 → 出力） | **Yes** | 決定的 |
| ライブ HTML 取得 → パース | **Same-day Yes** | 同一 HTML なら同一結果 |
| ライブ取得 → Skill 準拠 CEFR | **No** | 58% 一致 |
| Oxford wordlist 単独 | **No** | カバー 22% |
| 100語全自動・外部データのみ | **No** | 上記の合算で未達 |

---

## 次に POC すべきこと（Eval 実装前）

1. **CEFR 参照ソースの確定**
   - Cambridge 語義別 CEFR vs Oxford wordlist vs Oxford 個別ページ — どれを正とするか
   - 「最高 CEFR 採用」 vs 「主要語義 CEFR 採用」のルール検証

2. **100語カバー率 100% の参照フィクスチャ**
   - 取得手順を固定し、Git 凍結 + 再取得 diff で更新
   - 各語に `source_url`, `fetched_at`, `method` を記録

3. **検出チェックの有効性ベンチマーク**
   - ユーザー指摘 10語 + アンカー 5語をゴールドセットに
   - 各チェック（absolute / ordering / same-CEFR split）の precision/recall を測定

4. **JMdict 補正の POC**（別途）
   - feedback=Beginner が正アンカーなら、CEFR-only では B2→Intermediate になり fail
   - JMdict 外来語フラグ込みでアンカー 5/5 に近づくか検証

---

## 実行方法

```bash
python3 evals/difficulty/poc_reproducibility.py
```

ネットワーク必要。約 40 秒。

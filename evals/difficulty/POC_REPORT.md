# Difficulty Eval POC v4 — 結果

## 結論: **PASS（15語で再現可能な仕組みを証明）**

本実装前の POC として、シンプルな2段構成を検証した。

---

## 仕組み（人間向け）

### 1. 参照 CEFR（凍結 JSON、Eval 中ネットワーク不要）

優先順位:

1. **Oxford 3000/5000 wordlist**（リポジトリ内 JSON に凍結）
2. なければ **min(Cambridge 語義 CEFR, Oxford ページ CEFR)** — 基本語義寄り
3. 辞書に載らないフレーズ（`trade-off`）のみ **manual B2**（出典メモ付き）

### 2. 検出（2チェックのみ）

**Check A — 順序逆転**  
CEFR が高い語の Difficulty が、CEFR が低い語より下なら報告。

例: `replace` (A2, Advanced) vs `invoke` (C1, Intermediate) → 逆転

**Check B — アンカー校正**  
同一 CEFR で、アンカー語が **1種類の Difficulty しか持たない** とき、  
その Difficulty と違う語を報告。アンカー語自身は除外。

例: C1 のアンカー `scrutiny=Advanced` のみ → C1 の `critique=Beginner` を報告

**Check B をスキップする場合**  
同一 CEFR に複数のアンカー Difficulty があるとき（例: B2 に `feedback=Beginner` と `trade-off=Intermediate`）→ その CEFR では Check B しない。

---

## POC 成功条件

| 条件 | 結果 |
|------|------|
| 凍結 fixture から Eval が決定的 | PASS |
| CEFR 取得 15/15 | PASS |
| flagged 検出 ≥ 9/10 | PASS (9/10) |
| anchor 誤検出 0/5 | PASS |
| 同一語の fetch 2回一致 | PASS |

未検出: `reproduce`（C1, Advanced — 参照上は整合。ユーザー指摘は「可能性」）

---

## 実行

```bash
# 初回 or 参照更新（ネットワーク必要）
python3 evals/difficulty/poc_v4.py --refresh

# Eval のみ（凍結 fixture、ネットワーク不要）
python3 evals/difficulty/poc_v4.py
```

---

## 本実装への条件

POC v4 が PASS したので、次は以下を本実装する:

1. 100語の `cefr_reference.json` 凍結
2. `run_eval.py`（Check A + B）
3. `verify.py`（決定性 + ゴールドセット）

PR は verify が通ってから出す。

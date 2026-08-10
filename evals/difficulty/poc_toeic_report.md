# TOEIC 3ソース POC 結果

## 結論: **FAIL（Eval 本体には未達）**

再現可能な取得は確認できたが、**100語カバー率 52%** で自動 Eval には不足。

---

## 使ったソース

| # | ソース | 取得方法 | 語数 | 再現性 |
|---|--------|----------|------|--------|
| 1 | [toeic-words.com](https://www.toeic-words.com/words) | HTML 静的パース | 1,376 | ◎ |
| 2 | [かんたんTOEIC](https://kantantoeic.u-ff.com/category/toeic/vocabulary/) | HTML table パース | 3,668 | ◎ |
| 3 | [TSL 1.2 stats](https://www.newgeneralservicelist.com/s/TSL_12_stats.csv) | 公式 CSV | 1,250 | ◎ |

**えいたんごクイズ**: ページが CSR（クライアント描画）のため、静的 fetch では **10語しか取れず不可**。  
同一系統の TSL 公式 CSV をソース3として代替。

---

## TOEIC band → Difficulty マッピング

| TOEIC band | Difficulty |
|------------|------------|
| 600 | Beginner |
| 730 / 730-800 | Intermediate |
| 860 / 800+ | Advanced |

TSL: 頻度 rank 1–400→600, 401–800→730, 801+→860

---

## 100語カバー率

| ヒット数 | 語数 |
|----------|------|
| 0ソース | 48 |
| 1ソース | 34 |
| 2ソース | 13 |
| 3ソース | 5 |
| **1ソース以上** | **52/100 (52%)** |

2ソース以上で Difficulty が一致（consensus）: **10/100**

---

## flagged 10語の検出（現行 ≠ TOEIC採用）

| 語 | 現行 | TOEIC採用 | 検出 |
|----|------|-----------|------|
| replace | Advanced | Beginner | ✓ |
| critique | Beginner | Advanced | ✓ |
| assertion | Beginner | Intermediate | ✓ |
| coverage | Beginner | Intermediate | ✓ |
| reliability | Beginner | Advanced | ✓ |
| ownership | Beginner | Intermediate | ✓ |
| reproduce | Advanced | Advanced | - |
| isolate | Beginner | - | - |
| availability | Beginner | Beginner | - |
| capacity | Beginner | - | - |

**6/10 検出**

---

## anchor 5語

| 語 | anchor | TOEIC採用 | 判定 |
|----|--------|-----------|------|
| feedback | Beginner | Beginner | OK |
| clarify | Intermediate | Intermediate | OK |
| courteous | Advanced | Intermediate | NG |
| scrutiny | Advanced | Intermediate | NG |
| trade-off | Intermediate | - | 未カバー |

---

## ソース間一致（2ソース以上ヒット時）

- Difficulty 一致: 10件
- Difficulty 不一致: 8件

例: `coverage` → toeic-words=730-800, kantantoeic=730 → Intermediate（一致）  
`courteous` → toeic-words=730-800, kantantoeic=730 → Intermediate（アンカー Advanced と矛盾）

---

## 再現性

- 凍結 fixture (`poc_toeic_fixture.json`) から Eval は **決定的** ◎
- `--refresh` で再取得可能 ◎

---

## 示唆

1. **TOEIC リスト単体では Engineer English 100語の半分が未収録**（`deploy`, `schema`, `latency` 等の技術語）
2. **3ソース合意も 10% しかない** — 単一正解ソースは存在しない
3. **replace=Advanced の誤判定は検出できる**（toeic-words 600）
4. **courteous/scrutiny は TOEIC ソースが Intermediate と判定** — アンカー Advanced とのギャップあり
5. Eval に使うなら **TOEIC + 別軸（エンジニア語彙）のハイブリッド** が必要

---

## 実行

```bash
python3 evals/difficulty/poc_toeic.py --refresh  # 初回
python3 evals/difficulty/poc_toeic.py            # 凍結 fixture のみ
```

# Anchor Rubric POC 結果

## 結論: **PASS**

外部データなし。**固定 rubric + アンカー例** で flagged 10/10 を検出、核心アンカー 5/5 を維持。

---

## 方式

```
term
  ↓
3観点評価（low/medium/high）
  generalFamiliarity / engineerFamiliarity / contextualLearningNeeded
  ↓
アンカー群との近さ比較
  ↓
difficulty + reasoning（構造化）
```

- 数値スコア化しない
- 外部 TOEIC/CEFR を正解ラベルにしない
- 回帰 Eval: `anchor_gold.yaml` + `poc_anchor_expected.json`

---

## POC 結果

| 条件 | 結果 |
|------|------|
| rubric 期待値 一致 | 20/20 |
| flagged 検出（現行≠rubric） | **10/10** |
| core anchor 維持 | **5/5** |

### 拡張アンカーで見つかった vocab 不一致

- `discretion`: 現行 Intermediate → rubric Advanced（修正候補）

---

## 実行

```bash
python3 evals/difficulty/poc_anchor.py
```

---

## 次ステップ（本実装）

1. Skill に沿った AI 判定を Vocabulary 更新時に実行
2. `poc_anchor_expected.json` を回帰セットとして拡張（100語）
3. 同一モデル + few-shot で定期回帰

PR は回帰 Eval が 100 語で安定してから。

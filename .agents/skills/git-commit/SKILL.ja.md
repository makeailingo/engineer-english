---
name: git-commit
description: Conventional branching に沿ったコミットメッセージとブランチ名を決める。git commit、コミット作成、push 前のメッセージ起草、ブランチ命名のときに使用する。
---
# Git Commit

> English: [SKILL.md](SKILL.md)

このリポジトリでは conventional branching に従う。
使えるのは `feat`、`bugfix`、`docs`、`chore` の4つだけとする。

| 接頭辞 | 用途 |
| --- | --- |
| `feat` | 新機能、新しいボキャブラリー、ユーザー向けの追加 |
| `bugfix` | バグ修正、誤訳・誤記の是正、既存挙動の修正 |
| `docs` | ドキュメント、README の追加・更新 |
| `chore` | スキル、ルール、ツール、設定、依存、リファクタ（挙動不変） |

`fix`、`refactor`、`style`、`test` など、上記以外は使わない。

## ブランチ名

```
<feat|bugfix|docs|chore>/<短い説明>
```

- `<短い説明>` は英小文字とハイフン（kebab-case）
- 例: `feat/add-vocabulary-0501`、`bugfix/consensus-usage-example`、`docs/jekyll-local-dev`

## コミットメッセージ

英語、1行のみ。本文は書かない。

```
<feat|bugfix|docs|chore>: <summary>
```

- **summary**: 英語50文字以内を目安に、変更内容がわかる句にする
- HEREDOC で渡す（シェルエスケープを避ける）

## 判定

迷ったら次の順で決める。

1. 既存の誤り・不具合を直す → `bugfix`
2. 新しい内容・能力を足す → `feat`
3. ドキュメントだけを変える → `docs`
4. スキル、ルール、設定、その他の保守作業 → `chore`

## 例

```
bugfix: fix usageExampleJa for consensus and respectful
feat: add vocabulary 0501
docs: add Jekyll local development setup
chore: add git-commit skill
```

## コミット前チェック

- `git status` と `git diff` で対象を確認する
- 無関係な変更を同じコミットに含めない
- 秘密情報（`.env`、鍵）を含めない
- ユーザーが commit を明示的に求めていない限り、コミットしない

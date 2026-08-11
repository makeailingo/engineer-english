---
name: researching-vocabulary
description: 英単語・フレーズの品詞、語義、米国英語のIPA、ソフトウェア開発での用法を複数の資料で調査する。Vocabularyの作成・更新前に使用する。
---

# Researching Vocabulary

## 辞書

- 一次情報とする辞書: [Cambridge Dictionary](https://dictionary.cambridge.org/dictionary/english/)
- ダブルチェック用の辞書: [Oxford Advanced Learner's Dictionary](https://www.oxfordlearnersdictionaries.com/definition/english/)

Cambridgeは品詞、語義ごとの定義、米国英語のIPAを同じ項目で確認できる。学習者向けで、コーパスにも基づいているため、辞書情報の一次資料として使用する。Oxfordは一般米語（General American）のIPA、語義、用例を独立して確認できるため、ダブルチェックに使用する。

## Input

```yaml
term: "address"
```

## Workflow

1. Cambridgeで対象語の品詞を確認する。
2. Cambridgeで一般的な語義と、語義ごとの区分を確認する。
3. Cambridgeで米国英語のIPAを確認する。
4. Google Engineering Practices、Google SRE、MDNの一次資料で実務用法を確認する。
5. 辞書に掲載された語義のうち、一次資料のソフトウェア開発文脈で実際に使われているものを特定する。
6. 特定した語義に限定して、自然で簡潔な日本語訳を作成する。
7. Oxfordで品詞、語義、米国英語のIPAを照合し、不一致がないか確認する。
8. 各 Vocabulary を確定する前に、`evaluating-meaningJa` のルールを適用する。

   Before finalizing each vocabulary item, apply the `evaluating-meaningJa` rules.

   In particular:

   - `meaningJa` must explain the English meaning to a Japanese learner.
   - Do not use katakana transliteration alone as the meaning.
   - Katakana may be retained only when accompanied by a useful Japanese explanation.
   - Keep the explanation concise and aligned with the intended sense in `usageExample`.

   Examples:

   NG:
   blocker → ブロッカー
   backlog → バックログ
   on-call → オンコール

   OK:
   blocker → 作業の進行を妨げる問題、ブロッカー
   backlog → 未着手の作業や要望の一覧、バックログ
   on-call → 障害対応のため待機する当番、オンコール

検索結果に表示される要約だけで判断せず、各ページを開いて確認する。不一致を解消できない場合は推測せず、`confidence: Low`として理由を示す。

## Output

```yaml
partOfSpeech: "<採用した語義に対応する品詞>"
meaningJa: "<ソフトウェア開発の文脈に対応する日本語訳>"
pronunciation: "<米国英語のIPA>"
engineeringSense: "<ソフトウェア開発の文脈における簡潔な英語の語義>"
sources:
  - role: primaryDictionary
    title: "<Cambridgeの項目名>"
    url: "<確認したURL>"
  - role: crossCheckDictionary
    title: "<Oxfordの項目名>"
    url: "<確認したURL>"
  - role: engineeringPrimary
    title: "<一次資料のページタイトル>"
    url: "<確認したURL>"
    license: "<ライセンス>"
    context: "<実務用法の簡潔な日本語要約>"
confidence: "<High | Medium | Low>"
```

## Confidence

- `High`: 2つの辞書と一次資料の間で、品詞、語義、IPAに不一致がない。
- `Medium`: 語義は一致しているが、表記に差がある、または一次資料の用例が間接的である。
- `Low`: 必須情報が不足している、または不一致を解消できない。Vocabularyには採用しない。

調査用の辞書URLは中間出力に残す。Vocabularyの`source`には`engineeringPrimary`だけを転記する。

# Engineer English

ソフトウェアエンジニアが実務で使う英語のデータセットです。

## ローカル開発

### 前提

- [Homebrew](https://brew.sh/) で Ruby をインストール済みであること

```bash
brew install ruby
```

シェルで Homebrew の Ruby を優先する（`~/.zshrc` に追記）:

```bash
export PATH="/opt/homebrew/opt/ruby/bin:$PATH"
```

### セットアップ

```bash
cd docs
bundle install
```

### 起動

```bash
cd docs
bundle exec jekyll serve --baseurl ""
```

ブラウザで http://127.0.0.1:4000/ を開く。

`--baseurl ""` は GitHub Pages 用の `/engineer-english` プレフィックスを外し、ローカルではルートから表示するための指定。

### ビルドのみ

```bash
cd docs
bundle exec jekyll build --baseurl ""
```

生成物は `docs/_site/` に出力される。

## ライセンス

MIT. See [LICENSE](LICENSE).

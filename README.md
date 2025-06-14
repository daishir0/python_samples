# サンプルプログラム集

このディレクトリには、様々な機能を実装したサンプルプログラムが含まれています。各サンプルプログラムの概要と使い方を以下に示します。

## 目次

1. [Claude Prompt](#claude-prompt)
2. [OpenAI Prompt](#openai-prompt)
3. [Parallel OpenAI](#parallel-openai)
4. [OpenAI Vision](#openai-vision)
5. [Selenium](#selenium)

## Claude Prompt

### 概要

コマンドラインからClaudeに問い合わせを行うツールです。Anthropic APIを使用してClaudeモデルと対話し、テキストまたはJSON形式でレスポンスを取得します。

### 主な機能

- コマンドライン引数またはファイルからプロンプトを読み込み
- システムプロンプトの設定
- テキストまたはJSONとしての出力
- エラー時の再問合せ機能（リトライ機能）

### 使い方

```bash
# 直接プロンプトを指定
python main.py "あなたは誰ですか？"

# ファイルからプロンプトを読み込み
python main.py -f sample_prompt.txt

# システムプロンプトを指定
python main.py -s "あなたは日本語の専門家です" "「人工知能」について説明してください"

# JSONとして出力
python main.py -j -f sample_json_prompt.txt

# 出力ファイルを指定
python main.py -o output.txt "あなたの名前は？"
```

## OpenAI Prompt

### 概要

コマンドラインからOpenAI GPTモデルに問い合わせを行うツールです。OpenAI APIを使用してGPTモデルと対話し、テキストまたはJSON形式でレスポンスを取得します。

### 主な機能

- コマンドライン引数またはファイルからプロンプトを読み込み
- システムプロンプトの設定
- テキストまたはJSONとしての出力
- エラー時の再問合せ機能（リトライ機能）
- 使用量情報の表示

### 使い方

```bash
# 直接プロンプトを指定
python main.py "あなたは誰ですか？"

# ファイルからプロンプトを読み込み
python main.py -f sample_prompt.txt

# システムプロンプトを指定
python main.py -s "あなたは日本語の専門家です" "「人工知能」について説明してください"

# JSONとして出力
python main.py -j -f sample_json_prompt.txt

# 出力ファイルを指定
python main.py -o output.txt "あなたの名前は？"

# 使用量情報を表示
python main.py -u "短い文章を書いてください"
```

## Parallel OpenAI

### 概要

OpenAIへの並行問い合わせを行うサンプルプログラムです。非同期処理とバッチ処理を使用して、複数の問い合わせを効率的に処理します。

### 主な機能

- 複数の問い合わせを並行処理
- バッチ処理による効率化
- キャッシュ機能によるパフォーマンス向上
- エラー時の自動リトライ
- 結果の集約と管理

### 使い方

```bash
# 単一の問い合わせ
python -m parallel_openai.main query "What is the capital of Japan?"

# ファイルから複数の問い合わせを実行
python -m parallel_openai.main batch queries.txt

# 対話モード
python -m parallel_openai.main interactive

# モデルを指定して実行
python -m parallel_openai.main query "Explain quantum computing" --model gpt-4o-mini

# キャッシュを使用せずに実行
python -m parallel_openai.main query "What is AI?" --no-cache

# バッチサイズを指定して実行
python -m parallel_openai.main batch queries.txt --batch-size 3
```

## OpenAI Vision

### 概要

OpenAI Vision APIを使用して画像分析を行うツールです。単一または複数の画像を分析し、テキスト、JSON、Markdown形式で結果を出力します。

### 主な機能

- 単一または複数の画像を分析
- 画像ファイル、URL、ディレクトリからの画像読み込み
- バッチ処理による効率化
- キャッシュ機能によるパフォーマンス向上
- 結果をテキスト、JSON、Markdownなど様々な形式で出力

### 使い方

```bash
# 単一画像の分析
python main.py path/to/image.jpg

# プロンプトを指定して分析
python main.py path/to/image.jpg -p "この画像に写っている動物は何ですか？"

# 出力形式を指定
python main.py path/to/image.jpg -f json

# 出力ファイルを指定
python main.py path/to/image.jpg -o results.txt

# ディレクトリ内の画像を分析
python main.py -d path/to/images/

# 再帰的にディレクトリを検索
python main.py -d path/to/images/ -r

# バッチサイズを指定
python main.py -d path/to/images/ -b 3
```

## Selenium

### 概要

Chrome WebDriverを使用してWebページにアクセスし、JavaScriptが実行された後のページソースを取得するなどの機能を提供するツールです。

### 主な機能

- 指定されたURLにアクセスしてページの情報を取得
- JavaScriptの実行後にページソースを取得
- スクリーンショットの撮影
- ページからのデータ抽出
- 対話モードでの実行

### 使い方

```bash
# URLを指定して実行
python main.py https://example.com

# 対話モードで実行
python main.py

# 出力ディレクトリを指定
python main.py https://example.com --output results

# デバッグモードを有効化
python main.py https://example.com --debug
```

## 共通の要件

各サンプルプログラムを実行するには、それぞれのディレクトリにある`requirements.txt`ファイルに記載されたパッケージをインストールする必要があります。

```bash
cd <サンプルディレクトリ>
pip install -r requirements.txt
```

また、APIキーなどの設定が必要な場合は、各ディレクトリにある`.env.sample`ファイルを`.env`にコピーして、必要な情報を設定してください。
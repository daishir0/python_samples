# Sample Programs Collection

This directory contains various sample programs implementing different functionalities. Below is an overview and usage instructions for each sample program.

## Table of Contents

1. [Claude Prompt](#claude-prompt)
2. [OpenAI Prompt](#openai-prompt)
3. [Parallel OpenAI](#parallel-openai)
4. [OpenAI Vision](#openai-vision)
5. [Selenium](#selenium)

## Claude Prompt

### Overview

A command-line tool for querying Claude. It uses the Anthropic API to interact with Claude models and retrieve responses in text or JSON format.

### Key Features

- Load prompts from command-line arguments or files
- Set system prompts
- Output as text or JSON
- Automatic retry on errors

### Usage

```bash
# Specify a prompt directly
python main.py "Who are you?"

# Load a prompt from a file
python main.py -f sample_prompt.txt

# Specify a system prompt
python main.py -s "You are a Japanese language expert" "Explain what 'AI' is"

# Output as JSON
python main.py -j -f sample_json_prompt.txt

# Specify an output file
python main.py -o output.txt "What is your name?"
```

## OpenAI Prompt

### Overview

A command-line tool for querying OpenAI GPT models. It uses the OpenAI API to interact with GPT models and retrieve responses in text or JSON format.

### Key Features

- Load prompts from command-line arguments or files
- Set system prompts
- Output as text or JSON
- Automatic retry on errors
- Display usage information

### Usage

```bash
# Specify a prompt directly
python main.py "Who are you?"

# Load a prompt from a file
python main.py -f sample_prompt.txt

# Specify a system prompt
python main.py -s "You are a Japanese language expert" "Explain what 'AI' is"

# Output as JSON
python main.py -j -f sample_json_prompt.txt

# Specify an output file
python main.py -o output.txt "What is your name?"

# Display usage information
python main.py -u "I want to check token usage"
```

## Parallel OpenAI

### Overview

A sample program for making parallel queries to OpenAI. It uses asynchronous processing and batch processing to efficiently handle multiple queries.

### Key Features

- Process multiple queries in parallel
- Batch processing for efficiency
- Cache functionality for improved performance
- Automatic retry on errors
- Result aggregation and management

### Usage

```bash
# Single query
python -m parallel_openai.main query "What is the capital of Japan?"

# Batch queries from a file
python -m parallel_openai.main batch queries.txt

# Interactive mode
python -m parallel_openai.main interactive

# Specify a model
python -m parallel_openai.main query "Explain quantum computing" --model gpt-4o-mini

# Disable cache
python -m parallel_openai.main query "What is AI?" --no-cache

# Specify batch size
python -m parallel_openai.main batch queries.txt --batch-size 3
```

## OpenAI Vision

### Overview

A tool for image analysis using the OpenAI Vision API. It analyzes single or multiple images and outputs results in text, JSON, or Markdown format.

### Key Features

- Analyze single or multiple images
- Load images from files, URLs, or directories
- Batch processing for efficiency
- Cache functionality for improved performance
- Output results in various formats (text, JSON, Markdown)

### Usage

```bash
# Analyze a single image
python main.py path/to/image.jpg

# Specify a prompt
python main.py path/to/image.jpg -p "What animal is in this image?"

# Specify output format
python main.py path/to/image.jpg -f json

# Specify output file
python main.py path/to/image.jpg -o results.txt

# Analyze images in a directory
python main.py -d path/to/images/

# Search directories recursively
python main.py -d path/to/images/ -r

# Specify batch size
python main.py -d path/to/images/ -b 3
```

## Selenium

### Overview

A tool that uses Chrome WebDriver to access web pages and provides features such as retrieving page source after JavaScript execution.

### Key Features

- Access specified URLs and retrieve page information
- Get page source after JavaScript execution
- Take screenshots
- Extract data from pages
- Run in interactive mode

### Usage

```bash
# Run with a specified URL
python main.py https://example.com

# Run in interactive mode
python main.py

# Specify output directory
python main.py https://example.com --output custom_output

# Enable debug mode
python main.py https://example.com --debug
```

## Common Requirements

To run each sample program, you need to install the packages listed in the `requirements.txt` file in each directory.

```bash
cd <sample_directory>
pip install -r requirements.txt
```

Also, if API keys or other settings are required, copy the `.env.sample` file in each directory to `.env` and set the necessary information.

---

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
python main.py -u "トークン使用量を確認したい"
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
# OpenAI Vision API Sample Program

This sample program is a tool for image analysis using the OpenAI Vision API. It analyzes single or multiple images and outputs results in text, JSON, or Markdown format.

## Features

- Analyze single or multiple images
- Load images from files, URLs, or directories
- Batch processing for efficiency
- Cache functionality for improved performance
- Output results in various formats (text, JSON, Markdown)
- Automatic retry on errors (exponential backoff)

## Requirements

- Python 3.7 or higher
- OpenAI API key
- Required packages (listed in requirements.txt)

## Installation

1. Install the required packages:

```bash
pip install -r requirements.txt
```

2. Copy the `config.yaml.sample` file to `config.yaml` and configure it:

```bash
cp config.yaml.sample config.yaml
```

Edit the `config.yaml` file to set your API key and other settings:

```yaml
openai:
  api_key: "your_api_key_here"
  model: "gpt-4o-mini"
  max_tokens: 1000
  temperature: 0.7
  timeout: 30
  retry_count: 3
  retry_delay: 2

cache:
  enabled: true
  directory: "cache"
  expiry_days: 7
```

## Usage

### Basic Usage

```bash
# Analyze a single image
python main.py path/to/image.jpg

# Analyze an image from a URL
python main.py https://example.com/image.jpg
```

### Options

```bash
# Specify a prompt
python main.py path/to/image.jpg -p "What animal is in this image?"

# Specify output format
python main.py path/to/image.jpg -f json

# Specify output file
python main.py path/to/image.jpg -o results.txt

# Specify model
python main.py path/to/image.jpg -m gpt-4o

# Specify API key directly
python main.py path/to/image.jpg -k "your_api_key_here"

# Disable cache
python main.py path/to/image.jpg --no-cache

# Enable verbose logging
python main.py path/to/image.jpg -v
```

### Processing Multiple Images

```bash
# Use an image list file
python main.py -i image_list.txt

# Analyze images in a directory
python main.py -d path/to/images/

# Search directories recursively
python main.py -d path/to/images/ -r

# Process only specific file extensions
python main.py -d path/to/images/ -e jpg,png

# Specify batch size
python main.py -d path/to/images/ -b 3
```

## File Structure

- `main.py` - Main program
- `vision_client.py` - Vision API client class
- `config.py` - Configuration file
- `config.yaml.sample` - Sample configuration file
- `requirements.txt` - List of required packages
- `utils/` - Utility modules
  - `__init__.py` - Utility package initialization file
  - `cache_manager.py` - Cache management module
  - `image_processor.py` - Image processing module

## Image Processing

The `image_processor.py` module provides the following features:

- Load images from local files
- Download images from URLs
- Base64 encode images
- Validate image formats
- Optimize image sizes

## Cache Functionality

This program caches responses for the same image and prompt combination to reduce the number of API requests and improve performance. The cache has the following features:

- Stores cache based on image path and prompt combination
- Configurable expiration (default: 7 days)
- Cache clearing functionality

To disable caching, use the `--no-cache` option or set `cache.enabled` to `false` in the configuration file.

## Output Formats

This program supports the following output formats:

- Text (default): Outputs results in plain text format
- JSON: Outputs results in structured JSON format
- Markdown: Outputs results in Markdown format (including headings, lists, emphasis, etc.)

The output format can be specified using the `-f` or `--format` option.

## Error Handling

The program automatically retries on temporary issues such as API errors or network errors. The number of retries and the interval can be configured in the configuration file. Exponential backoff is used to gradually increase the retry interval.

---

# OpenAI Vision API サンプルプログラム

このサンプルプログラムは、OpenAI Vision APIを使用して画像分析を行うツールです。単一または複数の画像を分析し、テキスト、JSON、Markdown形式で結果を出力します。

## 機能

- 単一または複数の画像を分析
- 画像ファイル、URL、ディレクトリからの画像読み込み
- バッチ処理による効率化
- キャッシュ機能によるパフォーマンス向上
- 結果をテキスト、JSON、Markdownなど様々な形式で出力
- エラー時の自動リトライ（指数バックオフ）

## 必要条件

- Python 3.7以上
- OpenAI APIキー
- 必要なパッケージ（requirements.txtに記載）

## インストール

1. 必要なパッケージをインストールします：

```bash
pip install -r requirements.txt
```

2. `config.yaml.sample`ファイルを`config.yaml`にコピーし、設定を行います：

```bash
cp config.yaml.sample config.yaml
```

`config.yaml`ファイルを編集して、APIキーや他の設定を行います：

```yaml
openai:
  api_key: "your_api_key_here"
  model: "gpt-4o-mini"
  max_tokens: 1000
  temperature: 0.7
  timeout: 30
  retry_count: 3
  retry_delay: 2

cache:
  enabled: true
  directory: "cache"
  expiry_days: 7
```

## 使い方

### 基本的な使い方

```bash
# 単一画像の分析
python main.py path/to/image.jpg

# URLを指定して分析
python main.py https://example.com/image.jpg
```

### オプション

```bash
# プロンプトを指定して分析
python main.py path/to/image.jpg -p "この画像に写っている動物は何ですか？"

# 出力形式を指定
python main.py path/to/image.jpg -f json

# 出力ファイルを指定
python main.py path/to/image.jpg -o results.txt

# モデルを指定
python main.py path/to/image.jpg -m gpt-4o

# APIキーを直接指定
python main.py path/to/image.jpg -k "your_api_key_here"

# キャッシュを無効化
python main.py path/to/image.jpg --no-cache

# 詳細なログを表示
python main.py path/to/image.jpg -v
```

### 複数画像の処理

```bash
# 画像リストファイルを使用
python main.py -i image_list.txt

# ディレクトリ内の画像を分析
python main.py -d path/to/images/

# 再帰的にディレクトリを検索
python main.py -d path/to/images/ -r

# 特定の拡張子のファイルのみを処理
python main.py -d path/to/images/ -e jpg,png

# バッチサイズを指定
python main.py -d path/to/images/ -b 3
```

## ファイル構成

- `main.py` - メインプログラム
- `vision_client.py` - Vision APIクライアントクラス
- `config.py` - 設定ファイル
- `config.yaml.sample` - 設定ファイルのサンプル
- `requirements.txt` - 必要なパッケージのリスト
- `utils/` - ユーティリティモジュール
  - `__init__.py` - ユーティリティパッケージ初期化ファイル
  - `cache_manager.py` - キャッシュ管理モジュール
  - `image_processor.py` - 画像処理モジュール

## 画像処理

`image_processor.py`モジュールは、以下の機能を提供します：

- ローカルファイルからの画像読み込み
- URLからの画像ダウンロード
- 画像のbase64エンコード
- 画像形式の検証
- 画像サイズの最適化

## キャッシュ機能

このプログラムは、同じ画像と同じプロンプトの組み合わせに対するレスポンスをキャッシュすることで、APIリクエストの回数を減らし、パフォーマンスを向上させます。キャッシュは以下の特徴を持っています：

- 画像パスとプロンプトの組み合わせに基づいてキャッシュを保存
- 設定可能な有効期限（デフォルト: 7日）
- キャッシュのクリア機能

キャッシュを無効にするには、`--no-cache`オプションを使用するか、設定ファイルで`cache.enabled`を`false`に設定します。

## 出力形式

このプログラムは、以下の出力形式をサポートしています：

- テキスト（デフォルト）: 通常のテキスト形式で結果を出力
- JSON: 構造化されたJSON形式で結果を出力
- Markdown: Markdown形式で結果を出力（見出し、リスト、強調などの書式を含む）

出力形式は、`-f`または`--format`オプションで指定できます。

## エラーハンドリング

APIエラーやネットワークエラーなどの一時的な問題に対して、自動的にリトライを行います。リトライ回数や間隔は設定ファイルで指定できます。また、指数バックオフを使用して、リトライ間隔を徐々に長くすることもできます。
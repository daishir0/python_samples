# Parallel OpenAI

This sample program is a tool for making parallel queries to OpenAI. It uses asynchronous processing and batch processing to efficiently handle multiple queries.

## Features

- Process multiple queries in parallel
- Batch processing for efficiency
- Cache functionality for improved performance
- Automatic retry on errors
- Result aggregation and management
- Interactive mode

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

parallel:
  batch_size: 5
  max_retries: 3
  retry_delay: 1

cache:
  enabled: true
  directory: "cache"
  expiry_days: 7
```

## Usage

### Basic Usage

```bash
# Run as a module
python -m parallel_openai.main <command> [options]
```

### Commands

#### Single Query

```bash
python -m parallel_openai.main query "What is the capital of Japan?"
```

#### Batch Queries from a File

```bash
python -m parallel_openai.main batch queries.txt
```

Each line in the `queries.txt` file will be processed as a separate query.

#### Interactive Mode

```bash
python -m parallel_openai.main interactive
```

In interactive mode, you'll be prompted to enter queries, which will be processed one at a time. Type "exit" or "quit" to end the session.

### Options

```bash
# Specify a model
python -m parallel_openai.main query "Explain quantum computing" --model gpt-4o-mini

# Disable cache
python -m parallel_openai.main query "What is AI?" --no-cache

# Specify batch size
python -m parallel_openai.main batch queries.txt --batch-size 3

# Specify temperature
python -m parallel_openai.main query "Write a creative story" --temperature 0.9

# Specify maximum tokens
python -m parallel_openai.main query "Summarize this text" --max-tokens 500

# Specify config file
python -m parallel_openai.main query "Hello" --config custom_config.yaml

# Combine multiple options
python -m parallel_openai.main batch queries.txt --model gpt-4o-mini --batch-size 3 --no-cache
```

## File Structure

- `__init__.py` - Package initialization file
- `main.py` - Main entry point
- `parallel_client.py` - Parallel processing client
- `config.yaml.sample` - Sample configuration file
- `requirements.txt` - List of required packages
- `utils/` - Utility modules
  - `__init__.py` - Utility package initialization file
  - `cache_manager.py` - Cache management module
  - `openai_client.py` - OpenAI client module

## Cache Functionality

This program caches responses to the same queries to reduce the number of API requests and improve performance. The cache has the following features:

- Stores cache based on query hash values
- Configurable expiration (default: 7 days)
- Cache clearing functionality
- Metadata management

To disable caching, use the `--no-cache` option or set `cache.enabled` to `false` in the configuration file.

## Asynchronous Processing

This program implements asynchronous processing using `asyncio`. This allows multiple queries to be processed concurrently, efficiently utilizing I/O wait times.

In batch processing, queries are grouped based on the specified batch size, and each batch is processed concurrently. This enables efficient processing of a large number of queries.

## Error Handling

The program automatically retries on temporary issues such as API errors or network errors. The number of retries and the interval can be configured in the configuration file. Exponential backoff is used to gradually increase the retry interval.

---

# Parallel OpenAI

このサンプルプログラムは、OpenAIへの並行問い合わせを行うためのツールです。非同期処理とバッチ処理を使用して、複数の問い合わせを効率的に処理します。

## 機能

- 複数の問い合わせを並行処理
- バッチ処理による効率化
- キャッシュ機能によるパフォーマンス向上
- エラー時の自動リトライ
- 結果の集約と管理
- 対話モードでの実行

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

parallel:
  batch_size: 5
  max_retries: 3
  retry_delay: 1

cache:
  enabled: true
  directory: "cache"
  expiry_days: 7
```

## 使い方

### 基本的な使い方

```bash
# モジュールとして実行
python -m parallel_openai.main <コマンド> [オプション]
```

### コマンド

#### 単一の問い合わせ

```bash
python -m parallel_openai.main query "What is the capital of Japan?"
```

#### ファイルから複数の問い合わせを実行

```bash
python -m parallel_openai.main batch queries.txt
```

ファイル`queries.txt`の各行が1つの問い合わせとして処理されます。

#### 対話モード

```bash
python -m parallel_openai.main interactive
```

対話モードでは、プロンプトが表示され、ユーザーが入力した問い合わせが処理されます。終了するには「exit」または「quit」と入力します。

### オプション

```bash
# モデルを指定して実行
python -m parallel_openai.main query "Explain quantum computing" --model gpt-4o-mini

# キャッシュを使用せずに実行
python -m parallel_openai.main query "What is AI?" --no-cache

# バッチサイズを指定して実行
python -m parallel_openai.main batch queries.txt --batch-size 3

# 温度パラメータを指定
python -m parallel_openai.main query "Write a creative story" --temperature 0.9

# 最大トークン数を指定
python -m parallel_openai.main query "Summarize this text" --max-tokens 500

# 設定ファイルを指定
python -m parallel_openai.main query "Hello" --config custom_config.yaml

# 複数のオプションを組み合わせて使用
python -m parallel_openai.main batch queries.txt --model gpt-4o-mini --batch-size 3 --no-cache
```

## ファイル構成

- `__init__.py` - パッケージ初期化ファイル
- `main.py` - メインエントリーポイント
- `parallel_client.py` - 並行処理クライアント
- `config.yaml.sample` - 設定ファイルのサンプル
- `requirements.txt` - 必要なパッケージのリスト
- `utils/` - ユーティリティモジュール
  - `__init__.py` - ユーティリティパッケージ初期化ファイル
  - `cache_manager.py` - キャッシュ管理モジュール
  - `openai_client.py` - OpenAIクライアントモジュール

## キャッシュ機能

このプログラムは、同じ問い合わせに対するレスポンスをキャッシュすることで、APIリクエストの回数を減らし、パフォーマンスを向上させます。キャッシュは以下の特徴を持っています：

- 問い合わせのハッシュ値に基づいてキャッシュを保存
- 設定可能な有効期限（デフォルト: 7日）
- キャッシュのクリア機能
- メタデータの管理

キャッシュを無効にするには、`--no-cache`オプションを使用するか、設定ファイルで`cache.enabled`を`false`に設定します。

## 非同期処理

このプログラムは、`asyncio`を使用して非同期処理を実装しています。これにより、複数の問い合わせを並行して処理し、I/O待ち時間を効率的に利用することができます。

バッチ処理では、指定されたバッチサイズに基づいて問い合わせをグループ化し、各バッチを並行して処理します。これにより、大量の問い合わせを効率的に処理することができます。

## エラーハンドリング

APIエラーやネットワークエラーなどの一時的な問題に対して、自動的にリトライを行います。リトライ回数や間隔は設定ファイルで指定できます。また、指数バックオフを使用して、リトライ間隔を徐々に長くすることもできます。
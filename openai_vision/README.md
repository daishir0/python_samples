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
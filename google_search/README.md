# Google検索ツール (google_search)

このプログラムは、Google Custom Search APIを使用して検索を実行し、結果のURLをファイルに保存します。

## 使用方法

```bash
# 基本的な使用方法
python main.py "検索クエリ"

# 例: 産経新聞のサイトで「103万円の壁」について検索
python main.py "site:www.sankei.com 103万円の壁"

# 詳細なオプション
python main.py --help
```

## オプション

- `query`: 検索クエリ（必須）
- `--config`: 設定ファイルのパス（デフォルト: config.yaml）
- `--num`: 取得する結果の数（最大100、デフォルト: config.yamlで指定された値または100）

## 設定ファイル

APIキーや検索エンジンIDなどの設定は `config.yaml` ファイルで管理されています。
初回利用時は `config.yaml.sample` をコピーして `config.yaml` を作成し、必要な情報を設定してください。

```yaml
# config.yaml の例
api_key: "YOUR_GOOGLE_API_KEY_HERE"
cx: "YOUR_SEARCH_ENGINE_ID_HERE"
output_dir: "/path/to/output/directory"
num_results: 100
```

## 出力

検索結果は、実行時の日時をファイル名とした（yyyymmdd-hhmmss.txt形式）テキストファイルに保存されます。
ファイルには、検索結果のURLが1行に1つずつ記載されます。

## 必要なライブラリ

- google-api-python-client
- requests
- pyyaml

## インストール方法

```bash
pip install google-api-python-client requests pyyaml
```

## 注意事項

- Google Custom Search APIは、無料枠で1日あたり100クエリまでという制限があります。
- 検索エンジンIDは、Google Programmable Search Engineで作成する必要があります。
  - https://programmablesearchengine.google.com/about/ にアクセス
  - 「Get started」をクリック
  - 「Add」をクリックして新しい検索エンジンを作成
  - 「Sites to search」で検索対象のサイトを指定
  - 作成後、「Control Panel」から検索エンジンIDを取得
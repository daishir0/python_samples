# WordPress投稿サンプルプログラム

このプログラムは、WordPressのREST APIを使用して記事を投稿するシンプルなサンプルです。
Python環境で動作し、WordPressサイトに記事を投稿することができます。

## 機能

- WordPressのREST APIを使用した記事投稿
- 環境変数による設定管理
- タイトル、内容、カテゴリ、タグなどの指定
- ファイルからの記事内容読み込み
- 投稿ステータス（公開、下書きなど）の指定

## 必要条件

- Python 3.6以上
- 以下のPythonパッケージ:
  - requests

## インストール

1. リポジトリをクローンまたはダウンロードします
2. 必要なパッケージをインストールします:

```bash
pip install requests
```

3. 設定ファイルを作成します:

```bash
# config.py.sampleをconfig.pyにコピー
cp config.py.sample config.py

# 必要に応じてconfig.pyを編集
nano config.py  # または任意のエディタで編集
```

## 設定

### 方法1: 環境変数を使用する

環境変数を使用して、WordPressサイトへの接続情報を設定します。
以下の環境変数を設定してください:

```bash
# WordPressサイトのURL
export WP_SITE_URL="https://your-wordpress-site.com"

# WordPressユーザー名
export WP_USERNAME="your_username"

# WordPressアプリケーションパスワード
# https://wordpress.org/documentation/article/application-passwords/ を参照
export WP_APP_PASSWORD="your_app_password"

# デフォルトのカテゴリID
export WP_DEFAULT_CATEGORY_ID="1"

# オプション: デバッグモード
export DEBUG="true"

# オプション: 詳細ログ
export VERBOSE_LOGGING="true"
```

### 方法2: config.pyを直接編集する

`config.py.sample`をコピーして`config.py`を作成し、直接編集することもできます。
`config.py`には以下の設定項目があります:

- WordPress設定（サイトURL、ユーザー名、アプリケーションパスワード、カテゴリID）
- タグ設定（デフォルトのタグ）
- デバッグ設定（デバッグモード、詳細ログ）

**注意**: `config.py`には秘密情報が含まれるため、Gitリポジトリにコミットしないでください。
このプロジェクトには`.gitignore`ファイルが含まれており、`config.py`は自動的に除外されます。

## 使い方

### 基本的な使い方

```bash
python main.py --title "記事タイトル" --content "記事内容"
```

### ファイルから記事内容を読み込む

```bash
python main.py --title "ファイルから読み込む記事" --file content.html
```

### 下書きとして投稿

```bash
python main.py --title "下書き記事" --content "これは下書きです。" --status draft
```

### カテゴリとタグを指定

```bash
python main.py --title "カテゴリとタグ付き記事" --content "記事内容" --category 2 --tags "タグ1,タグ2,タグ3"
```

### 抜粋（excerpt）を指定

```bash
python main.py --title "抜粋付き記事" --content "記事内容" --excerpt "この記事の抜粋です"
```

### デバッグモードで実行

```bash
python main.py --title "デバッグ記事" --content "記事内容" --debug
```

## コマンドラインオプション

| オプション | 説明 | 必須 |
|------------|------|------|
| `--title` | 記事タイトル | はい |
| `--content` | 記事内容 | `--file`と排他 |
| `--file` | 記事内容を読み込むファイルパス | `--content`と排他 |
| `--category` | カテゴリID | いいえ |
| `--status` | 投稿ステータス（publish, draft, private, pending） | いいえ（デフォルト: publish） |
| `--tags` | タグ（カンマ区切り） | いいえ |
| `--excerpt` | 記事の抜粋 | いいえ |
| `--debug` | デバッグモードで実行 | いいえ |

## ファイル構成

- `main.py` - メインの実行スクリプト
- `config.py.sample` - 設定管理モジュールのサンプル（秘密情報なし）
- `config.py` - 実際の設定管理モジュール（秘密情報を含むため、Gitリポジトリから除外）
- `wordpress_poster.py` - WordPress投稿クラス
- `README.md` - 使い方の説明
- `.gitignore` - Gitリポジトリから除外するファイルの設定

## 注意事項

- WordPressのアプリケーションパスワードを使用するため、WordPressサイトでアプリケーションパスワードを発行する必要があります。
- 環境変数を使用して秘密情報を管理しているため、`.env`ファイルなどを使用する場合は、リポジトリにコミットしないよう注意してください。
- `config.py`には秘密情報が含まれるため、Gitリポジトリにコミットしないでください。代わりに`config.py.sample`をコミットしてください。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。
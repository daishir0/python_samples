# WordPress Article Management Tool

This program is a comprehensive tool for managing WordPress articles using the WordPress REST API.
It supports posting, editing, listing, and searching articles in a WordPress site.

# WordPress投稿サンプルプログラム

このプログラムは、WordPressのREST APIを使用して記事を投稿するシンプルなサンプルです。
Python環境で動作し、WordPressサイトに記事を投稿することができます。

## Features

- **Article Publishing**: Post new articles to WordPress using REST API
- **Article Editing**: Update existing articles by ID
- **Article Listing**: Retrieve latest articles with ID information
- **Article Search**: Search articles by keywords
- **Configuration Management**: Manage settings via environment variables
- **Content Management**: Support for titles, content, categories, tags, excerpts
- **File Input**: Read article content from files
- **Publication Status**: Control publication status (publish, draft, private, pending)

## 機能

- WordPressのREST APIを使用した記事投稿
- 既存記事の更新・編集
- 最新記事一覧の取得（ID付き）
- キーワードによる記事検索
- 環境変数による設定管理
- タイトル、内容、カテゴリ、タグなどの指定
- ファイルからの記事内容読み込み
- 投稿ステータス（公開、下書きなど）の指定

## Requirements

- Python 3.6 or higher
- Required Python packages:
  - requests

## Installation

1. Clone or download the repository
2. Install required packages:

```bash
pip install requests
```

3. Set up configuration:

```bash
# Copy sample config to actual config
cp config.py.sample config.py

# Edit config.py as needed
nano config.py  # or use any text editor
```

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

## Configuration

### Method 1: Using Environment Variables

Set up WordPress connection information using environment variables:

```bash
# WordPress site URL
export WP_SITE_URL="https://your-wordpress-site.com"

# WordPress username
export WP_USERNAME="your_username"

# WordPress application password
# See https://wordpress.org/documentation/article/application-passwords/
export WP_APP_PASSWORD="your_app_password"

# Default category ID
export WP_DEFAULT_CATEGORY_ID="1"

# Optional: Debug mode
export DEBUG="true"

# Optional: Verbose logging
export VERBOSE_LOGGING="true"
```

### Method 2: Direct Configuration

You can also copy `config.py.sample` to `config.py` and edit it directly.
The `config.py` file includes the following configuration items:

- WordPress settings (site URL, username, application password, category ID)
- Tag settings (default tags)
- Debug settings (debug mode, verbose logging)

**Note**: `config.py` contains sensitive information, so do not commit it to the Git repository.
This project includes a `.gitignore` file that automatically excludes `config.py`.

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

## Usage

### Basic Usage

```bash
python main.py --title "Article Title" --content "Article content"
```

### Read Content from File

```bash
python main.py --title "Article from File" --file content.html
```

### Post as Draft

```bash
python main.py --title "Draft Article" --content "This is a draft." --status draft
```

### Specify Category and Tags

```bash
python main.py --title "Article with Category and Tags" --content "Article content" --category 2 --tags "tag1,tag2,tag3"
```

### Specify Excerpt

```bash
python main.py --title "Article with Excerpt" --content "Article content" --excerpt "This is the article excerpt"
```

### Run in Debug Mode

```bash
python main.py --title "Debug Article" --content "Article content" --debug
```

### Update Existing Article

```bash
python main.py --update 123 --title "Updated Title" --content "Updated content"
```

### List Latest Articles

```bash
python main.py --list 10
```

### Search Articles by Keyword

```bash
python main.py --search "search keyword"
```

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

### 既存記事を更新

```bash
python main.py --update 123 --title "更新されたタイトル" --content "更新された内容"
```

### 最新記事一覧を表示

```bash
python main.py --list 10
```

### キーワードで記事を検索

```bash
python main.py --search "検索キーワード"
```

## Command Line Options

| Option | Description | Required |
|--------|-------------|----------|
| `--title` | Article title | Required for posting/updating |
| `--content` | Article content | Mutually exclusive with `--file` |
| `--file` | File path to read article content from | Mutually exclusive with `--content` |
| `--category` | Category ID | No |
| `--status` | Publication status (publish, draft, private, pending) | No (default: publish) |
| `--tags` | Tags (comma-separated) | No |
| `--excerpt` | Article excerpt | No |
| `--debug` | Run in debug mode | No |
| `--update` | ID of article to update | No |
| `--list` | Number of latest articles to display | No |
| `--search` | Search articles by keyword | No |

## コマンドラインオプション

| オプション | 説明 | 必須 |
|------------|------|------|
| `--title` | 記事タイトル | 投稿・更新時は必須 |
| `--content` | 記事内容 | `--file`と排他 |
| `--file` | 記事内容を読み込むファイルパス | `--content`と排他 |
| `--category` | カテゴリID | いいえ |
| `--status` | 投稿ステータス（publish, draft, private, pending） | いいえ（デフォルト: publish） |
| `--tags` | タグ（カンマ区切り） | いいえ |
| `--excerpt` | 記事の抜粋 | いいえ |
| `--debug` | デバッグモードで実行 | いいえ |
| `--update` | 更新する記事のID | いいえ |
| `--list` | 最新記事を指定件数表示 | いいえ |
| `--search` | キーワードで記事を検索 | いいえ |

## File Structure

- `main.py` - Main execution script
- `config.py.sample` - Sample configuration module (no sensitive information)
- `config.py` - Actual configuration module (contains sensitive information, excluded from Git repository)
- `wordpress_poster.py` - WordPress posting class
- `README.md` - Usage instructions
- `.gitignore` - Git repository exclusion settings

## Important Notes

- This tool requires WordPress Application Passwords. You need to generate an application password in your WordPress site.
- When using environment variables to manage sensitive information, be careful not to commit `.env` files or similar to the repository.
- `config.py` contains sensitive information, so do not commit it to the Git repository. Instead, commit `config.py.sample`.

## License

This project is released under the MIT License.

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
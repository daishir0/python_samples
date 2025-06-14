# Selenium Sample Program

This sample program is a tool that uses Chrome WebDriver to access web pages and provides features such as retrieving page source after JavaScript execution.

## Features

- Access specified URLs and retrieve page information
- Get page source after JavaScript execution
- Take screenshots
- Extract data from pages
- Run in interactive mode
- Automatic retry on errors

## Requirements

- Python 3.7 or higher
- Chrome browser
- ChromeDriver
- Required packages (listed in requirements.txt)

## Installation

1. Install the required packages:

```bash
pip install -r requirements.txt
```

2. Install Chrome browser (if not already installed).

3. Download ChromeDriver and place it in an appropriate location. The ChromeDriver version must match your installed Chrome version.

4. Edit the `config.py` file to set the Chrome binary path and ChromeDriver path:

```python
# Chrome settings
CHROME_BINARY_PATH = "/path/to/chrome"  # Path to Chrome binary
CHROME_DRIVER_PATH = "/path/to/chromedriver"  # Path to ChromeDriver
```

## Usage

### Basic Usage

```bash
# Run with a specified URL
python main.py https://example.com

# Run in interactive mode (when no URL is specified)
python main.py
```

### Options

```bash
# Specify output directory
python main.py https://example.com --output custom_output

# Enable debug mode
python main.py https://example.com --debug
```

### Interactive Mode

In interactive mode, you'll be prompted to enter URLs, which will be processed one at a time. Type "exit" or "quit" to end the session.

Interactive mode provides the following features:

- URL input and validation
- Page processing and result display
- Retry option on error

## File Structure

- `main.py` - Main program
- `selenium_utils.py` - Selenium utility functions
- `config.py` - Configuration file
- `requirements.txt` - List of required packages

## Selenium Utilities

The `selenium_utils.py` module provides the following features:

### WebDriver Setup

```python
driver, temp_dir = setup_driver()
```

Initializes Chrome WebDriver and creates a temporary directory. Runs in headless mode with various options set.

### Page Loading

```python
success = load_page_with_retry(driver, url)
```

Accesses the specified URL and attempts to load the page. Retries a specified number of times if it fails.

### Element Waiting

```python
element = wait_for_element(driver, By.ID, "element-id")
```

Waits for the specified element to be displayed. Returns None if it times out.

### Get Page Source After JavaScript Execution

```python
page_source = get_page_source_after_js(driver)
```

Gets the page source after JavaScript execution.

### Safe Element Click

```python
success = safe_click(driver, element)
```

Safely clicks an element. If the normal click fails, it attempts to click using JavaScript.

### Take Screenshot

```python
success = take_screenshot(driver, "screenshot.png")
```

Takes a screenshot and saves it.

## Error Handling

This program automatically retries on page loading errors and WebDriver-related errors. The number of retries and the interval can be configured in `config.py`.

## Output

The program generates the following outputs:

1. Page HTML source (after JavaScript execution)
2. Screenshot
3. Extracted data (headings, meta descriptions, link count, etc.)

Output files are saved in the `output` directory by default. Filenames include the domain name, path, and timestamp.

## Notes

- This program runs Chrome in headless mode. If you need a GUI, remove the `--headless=new` option from the `setup_driver` function in `selenium_utils.py`.
- Some websites may restrict access due to bot detection features.
- Sending a large number of requests in a short time may result in your IP being blocked.

---

# Selenium サンプルプログラム

このサンプルプログラムは、Chrome WebDriverを使用してWebページにアクセスし、JavaScriptが実行された後のページソースを取得するなどの機能を提供するツールです。

## 機能

- 指定されたURLにアクセスしてページの情報を取得
- JavaScriptの実行後にページソースを取得
- スクリーンショットの撮影
- ページからのデータ抽出
- 対話モードでの実行
- エラー時の自動リトライ

## 必要条件

- Python 3.7以上
- Chrome ブラウザ
- ChromeDriver
- 必要なパッケージ（requirements.txtに記載）

## インストール

1. 必要なパッケージをインストールします：

```bash
pip install -r requirements.txt
```

2. Chrome ブラウザをインストールします（まだインストールされていない場合）。

3. ChromeDriverをダウンロードし、適切な場所に配置します。ChromeDriverのバージョンは、インストールされているChromeのバージョンと一致している必要があります。

4. `config.py`ファイルを編集して、ChromeのバイナリパスとChromeDriverのパスを設定します：

```python
# Chrome設定
CHROME_BINARY_PATH = "/path/to/chrome"  # Chromeバイナリのパス
CHROME_DRIVER_PATH = "/path/to/chromedriver"  # ChromeDriverのパス
```

## 使い方

### 基本的な使い方

```bash
# URLを指定して実行
python main.py https://example.com

# 対話モードで実行（URLを指定しない場合）
python main.py
```

### オプション

```bash
# 出力ディレクトリを指定
python main.py https://example.com --output custom_output

# デバッグモードを有効化
python main.py https://example.com --debug
```

### 対話モード

対話モードでは、プロンプトが表示され、ユーザーが入力したURLが処理されます。終了するには「exit」または「quit」と入力します。

対話モードでは、以下の機能が利用できます：

- URLの入力と検証
- ページの処理と結果の表示
- エラー発生時の再試行オプション

## ファイル構成

- `main.py` - メインプログラム
- `selenium_utils.py` - Seleniumユーティリティ関数
- `config.py` - 設定ファイル
- `requirements.txt` - 必要なパッケージのリスト

## Seleniumユーティリティ

`selenium_utils.py`モジュールは、以下の機能を提供します：

### WebDriverの設定

```python
driver, temp_dir = setup_driver()
```

Chrome WebDriverを初期化し、一時ディレクトリを作成します。ヘッドレスモードで実行され、様々なオプションが設定されます。

### ページの読み込み

```python
success = load_page_with_retry(driver, url)
```

指定されたURLにアクセスし、ページの読み込みを試みます。失敗した場合は指定回数リトライします。

### 要素の待機

```python
element = wait_for_element(driver, By.ID, "element-id")
```

指定された要素が表示されるまで待機します。タイムアウトした場合はNoneを返します。

### JavaScriptの実行後のページソース取得

```python
page_source = get_page_source_after_js(driver)
```

JavaScriptの実行後にページのソースを取得します。

### 要素の安全なクリック

```python
success = safe_click(driver, element)
```

要素を安全にクリックします。通常のクリックが失敗した場合は、JavaScriptを使用してクリックを試みます。

### スクリーンショットの撮影

```python
success = take_screenshot(driver, "screenshot.png")
```

スクリーンショットを撮影して保存します。

## エラーハンドリング

このプログラムは、ページの読み込みエラーやWebDriver関連のエラーに対して自動的にリトライを行います。リトライ回数や間隔は`config.py`で設定できます。

## 出力

プログラムは以下の出力を生成します：

1. ページのHTMLソース（JavaScriptの実行後）
2. スクリーンショット
3. 抽出されたデータ（見出し、メタ説明、リンク数など）

出力ファイルは、デフォルトでは`output`ディレクトリに保存されます。ファイル名には、ドメイン名、パス、タイムスタンプが含まれます。

## 注意事項

- このプログラムはヘッドレスモードでChromeを実行します。GUIが必要な場合は、`selenium_utils.py`の`setup_driver`関数から`--headless=new`オプションを削除してください。
- 一部のWebサイトでは、ボットの検出機能によりアクセスが制限される場合があります。
- 大量のリクエストを短時間に送信すると、IPがブロックされる可能性があります。
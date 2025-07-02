# Gmailメール送信ツール

コマンドラインからGmailでメールを送信するシンプルなPythonプログラムです。

## 機能

- Gmailを使用したメール送信
- 複数の宛先（CC、BCC）に対応
- 添付ファイル対応
- HTMLメール対応
- エラー時の自動リトライ機能

## 準備

1. 必要なパッケージをインストールします。

```bash
pip install -r requirements.txt
```

2. `.env.sample`ファイルを`.env`にコピーし、実際の認証情報を設定します。

```bash
cp .env.sample .env
```

3. `.env`ファイルを編集して、以下の情報を設定します。

```
EMAIL_USER=your-email@gmail.com
EMAIL_PASS=your-app-password
EMAIL_FROM=your-email@gmail.com
```

※ `EMAIL_PASS`には、Googleアカウントのアプリパスワードを設定してください。通常のパスワードではなく、アプリパスワードが必要です。アプリパスワードの取得方法は[こちら](https://support.google.com/accounts/answer/185833)を参照してください。

## 使い方

### 基本的な使い方

```bash
python main.py recipient@example.com -s "件名" -b "本文"
```

### 複数の宛先に送信

```bash
python main.py recipient@example.com -c "cc1@example.com,cc2@example.com" -d "bcc@example.com"
```

### ファイルから本文を読み込む

```bash
python main.py recipient@example.com -s "件名" -f body.txt
```

### 添付ファイル付きメール

```bash
python main.py recipient@example.com -s "件名" -b "本文" -a "file1.pdf,file2.jpg"
```

### HTMLメール

```bash
python main.py recipient@example.com -s "件名" -b "<h1>HTMLメール</h1><p>これはHTMLメールです。</p>" --html
```

### 標準入力から本文を読み込む

```bash
python main.py recipient@example.com -s "件名"
```

（入力後、Ctrl+Dで終了）

## オプション

- `-s`, `--subject`: 件名
- `-b`, `--body`: 本文
- `-f`, `--file`: 本文ファイル（指定した場合はbody引数は無視される）
- `-c`, `--cc`: CC（カンマ区切りで複数指定可能）
- `-d`, `--bcc`: BCC（カンマ区切りで複数指定可能）
- `-a`, `--attachments`: 添付ファイル（カンマ区切りで複数指定可能）
- `--html`: HTMLメールとして送信
- `-v`, `--verbose`: 詳細なログを出力

## 注意事項

- このプログラムを使用するには、Gmailのアプリパスワードが必要です。
- 添付ファイルのパスは、絶対パスまたは実行ディレクトリからの相対パスで指定してください。
- 大量のメール送信には使用しないでください。Gmailの送信制限に達する可能性があります。
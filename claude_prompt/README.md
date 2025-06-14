# Claude Prompt ツール

このサンプルプログラムは、コマンドラインからClaudeに問い合わせを行うツールです。Anthropic APIを使用してClaudeモデルと対話し、テキストまたはJSON形式でレスポンスを取得します。

## 機能

- コマンドライン引数またはファイルからプロンプトを読み込み
- 標準入力からのプロンプト読み込み
- システムプロンプトの設定
- 使用するモデルの指定
- 温度パラメータの調整
- テキストまたはJSONとしての出力
- 出力ファイルへの保存
- エラー時の再問合せ機能（リトライ機能）

## 必要条件

- Python 3.7以上
- Anthropic APIキー

## インストール

1. 必要なパッケージをインストールします：

```bash
pip install -r requirements.txt
```

2. `.env.sample`ファイルを`.env`にコピーし、Anthropic APIキーを設定します：

```bash
cp .env.sample .env
```

`.env`ファイルを編集して、APIキーを設定します：

```
ANTHROPIC_API_KEY=your_api_key_here
DEBUG=False
```

## 使い方

### 基本的な使い方

```bash
# 直接プロンプトを指定
python main.py "あなたは誰ですか？"

# ファイルからプロンプトを読み込み
python main.py -f sample_prompt.txt

# 標準入力からプロンプトを読み込み
echo "あなたは誰ですか？" | python main.py
```

### オプション

```bash
# システムプロンプトを指定
python main.py -s "あなたは日本語の専門家です" "「人工知能」について説明してください"

# モデルを指定
python main.py -m claude-3-5-sonnet-20240620 "量子コンピュータについて説明してください"

# 温度パラメータを指定
python main.py -t 0.5 "創造的な物語を書いてください"

# JSONとして出力
python main.py -j -f sample_json_prompt.txt

# 出力ファイルを指定
python main.py -o output.txt "あなたの名前は？"

# 詳細なログを出力
python main.py -v "デバッグ情報を確認したい"
```

## ファイル構成

- `main.py` - メインプログラム
- `claude_client.py` - Claudeクライアントクラス
- `config.py` - 設定ファイル
- `requirements.txt` - 必要なパッケージのリスト
- `sample_prompt.txt` - サンプルプロンプト
- `sample_json_prompt.txt` - JSONレスポンス用のサンプルプロンプト
- `.env.sample` - 環境変数のサンプルファイル

## サンプルプロンプト

### テキストプロンプト（sample_prompt.txt）

```
以下の質問に日本語で答えてください。

1. あなたは誰ですか？
2. あなたにはどのような機能がありますか？
3. あなたはどのように学習しましたか？

回答は箇条書きで、簡潔にお願いします。
```

### JSONプロンプト（sample_json_prompt.txt）

```
以下の情報をJSON形式で返してください。

名前: 山田太郎
年齢: 35
職業: ソフトウェアエンジニア
スキル: 
  - Python
  - JavaScript
  - Docker
  - AWS
趣味:
  - 読書
  - 旅行
  - 料理

JSONの形式は以下のようにしてください：
{
  "name": "名前",
  "age": 年齢,
  "occupation": "職業",
  "skills": ["スキル1", "スキル2", ...],
  "hobbies": ["趣味1", "趣味2", ...]
}
```

## エラーハンドリング

このツールは、APIエラーやネットワークエラーなどの一時的な問題に対して自動的にリトライを行います。リトライ回数や間隔は`config.py`で設定できます。
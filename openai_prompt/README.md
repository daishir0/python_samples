# OpenAI Prompt Tool

This sample program is a command-line tool for querying OpenAI GPT models. It uses the OpenAI API to interact with GPT models and retrieve responses in text or JSON format.

## Features

- Load prompts from command-line arguments or files
- Read prompts from standard input
- Set system prompts
- Specify the model to use
- Adjust temperature parameter
- Set maximum token count
- Output as text or JSON
- Save output to files
- Automatic retry on errors
- Display usage information

## Requirements

- Python 3.7 or higher
- OpenAI API key

## Installation

1. Install the required packages:

```bash
pip install -r requirements.txt
```

2. Copy the `.env.sample` file to `.env` and set your OpenAI API key:

```bash
cp .env.sample .env
```

Edit the `.env` file to set your API key:

```
OPENAI_API_KEY=your_api_key_here
DEBUG=False
```

## Usage

### Basic Usage

```bash
# Specify a prompt directly
python main.py "Who are you?"

# Load a prompt from a file
python main.py -f sample_prompt.txt

# Read a prompt from standard input
echo "Who are you?" | python main.py
```

### Options

```bash
# Specify a system prompt
python main.py -s "You are a Japanese language expert" "Explain what 'AI' is"

# Specify a model
python main.py -m gpt-4o "Explain quantum computing"

# Adjust the temperature parameter
python main.py -t 0.5 "Write a creative story"

# Set maximum token count
python main.py -x 500 "Write a short story"

# Output as JSON
python main.py -j -f sample_json_prompt.txt

# Specify an output file
python main.py -o output.txt "What is your name?"

# Enable verbose logging
python main.py -v "I want to see debug information"

# Display usage information
python main.py -u "I want to check token usage"
```

## File Structure

- `main.py` - Main program
- `openai_client.py` - OpenAI client class
- `config.py` - Configuration file
- `requirements.txt` - List of required packages
- `sample_prompt.txt` - Sample prompt
- `sample_json_prompt.txt` - Sample prompt for JSON response
- `.env.sample` - Sample environment variables file

## Sample Prompts

### Text Prompt (sample_prompt.txt)

```
Please answer the following questions in Japanese.

1. Who are you?
2. What features do you have?
3. How were you trained?

Please provide your answers in bullet points, concisely.
```

### JSON Prompt (sample_json_prompt.txt)

```
Please return the following information in JSON format.

Name: Taro Yamada
Age: 35
Occupation: Software Engineer
Skills: 
  - Python
  - JavaScript
  - Docker
  - AWS
Hobbies:
  - Reading
  - Travel
  - Cooking

Please format the JSON as follows:
{
  "name": "name",
  "age": age,
  "occupation": "occupation",
  "skills": ["skill1", "skill2", ...],
  "hobbies": ["hobby1", "hobby2", ...]
}
```

## Error Handling

This tool automatically retries on temporary issues such as API errors or network errors. The number of retries and the interval can be configured in `config.py`. A backoff factor is used to gradually increase the retry interval.

## Usage Information

Using the `-u` or `--usage` option displays token usage information for the API request. This includes:

- Prompt token count
- Completion token count
- Total token count

This information is useful for monitoring API usage and managing costs.

---

# OpenAI Prompt ツール

このサンプルプログラムは、コマンドラインからOpenAI GPTモデルに問い合わせを行うツールです。OpenAI APIを使用してGPTモデルと対話し、テキストまたはJSON形式でレスポンスを取得します。

## 機能

- コマンドライン引数またはファイルからプロンプトを読み込み
- 標準入力からのプロンプト読み込み
- システムプロンプトの設定
- 使用するモデルの指定
- 温度パラメータの調整
- 最大トークン数の指定
- テキストまたはJSONとしての出力
- 出力ファイルへの保存
- エラー時の再問合せ機能（リトライ機能）
- 使用量情報の表示

## 必要条件

- Python 3.7以上
- OpenAI APIキー

## インストール

1. 必要なパッケージをインストールします：

```bash
pip install -r requirements.txt
```

2. `.env.sample`ファイルを`.env`にコピーし、OpenAI APIキーを設定します：

```bash
cp .env.sample .env
```

`.env`ファイルを編集して、APIキーを設定します：

```
OPENAI_API_KEY=your_api_key_here
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
python main.py -m gpt-4o "量子コンピュータについて説明してください"

# 温度パラメータを指定
python main.py -t 0.5 "創造的な物語を書いてください"

# 最大トークン数を指定
python main.py -x 500 "短い物語を書いてください"

# JSONとして出力
python main.py -j -f sample_json_prompt.txt

# 出力ファイルを指定
python main.py -o output.txt "あなたの名前は？"

# 詳細なログを出力
python main.py -v "デバッグ情報を確認したい"

# 使用量情報を表示
python main.py -u "トークン使用量を確認したい"
```

## ファイル構成

- `main.py` - メインプログラム
- `openai_client.py` - OpenAIクライアントクラス
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

このツールは、APIエラーやネットワークエラーなどの一時的な問題に対して自動的にリトライを行います。リトライ回数や間隔は`config.py`で設定できます。バックオフ係数を使用して、リトライ間隔を徐々に長くすることもできます。

## 使用量情報

`-u`または`--usage`オプションを使用すると、APIリクエストで使用されたトークン数の情報が表示されます。これには以下の情報が含まれます：

- プロンプトトークン数
- 完了トークン数
- 合計トークン数

この情報は、APIの使用量を監視し、コストを管理するのに役立ちます。
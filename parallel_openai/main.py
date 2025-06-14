"""
OpenAI 並行問い合わせサンプル - メイン実行ファイル
==================================================

このプログラムは、OpenAIへの並行問い合わせを行うサンプルです。
非同期処理とバッチ処理を使用して、複数の問い合わせを効率的に処理します。

使い方:
------
```bash
python -m parallel_openai.main <コマンド> [オプション]
```

コマンド:
--------
query <テキスト>     : 単一の問い合わせを実行
batch <ファイル>     : ファイルから複数の問い合わせを読み込んで実行
interactive         : 対話モードで実行

オプション:
---------
--model <モデル名>   : 使用するモデルを指定（デフォルト: 設定ファイルの値）
--no-cache          : キャッシュを使用しない
--batch-size <数値> : バッチサイズを指定（デフォルト: 設定ファイルの値）
--config <ファイル>  : 設定ファイルのパスを指定（デフォルト: config.yaml）
--temperature <数値>: 温度パラメータを指定（デフォルト: 0.7）
--max-tokens <数値> : 最大トークン数を指定

コマンド例:
---------
# 単一の問い合わせ
python -m parallel_openai.main query "What is the capital of Japan?"

# ファイルから複数の問い合わせを実行
python -m parallel_openai.main batch queries.txt

# 対話モード
python -m parallel_openai.main interactive

# モデルを指定して実行
python -m parallel_openai.main query "Explain quantum computing" --model gpt-4o-mini

# キャッシュを使用せずに実行
python -m parallel_openai.main query "What is AI?" --no-cache

# バッチサイズを指定して実行
python -m parallel_openai.main batch queries.txt --batch-size 3

# 複数のオプションを組み合わせて使用
python -m parallel_openai.main batch queries.txt --model gpt-4o-mini --batch-size 3 --no-cache
"""

import sys
import os
import logging
import asyncio
import argparse
from typing import List, Dict, Any

# 内部モジュールのインポート
from parallel_client import ParallelOpenAIClient

# ロガーの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def load_queries_from_file(file_path: str) -> List[str]:
    """ファイルから問い合わせを読み込む"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            # 空行を除外して各行を問い合わせとして読み込む
            return [line.strip() for line in f if line.strip()]
    except Exception as e:
        logger.error(f"ファイルの読み込みに失敗しました: {str(e)}")
        sys.exit(1)

def print_response(query: str, response: Dict):
    """応答を表示"""
    print("\n" + "=" * 80)
    print(f"問い合わせ: {query}")
    print("-" * 80)
    
    if "error" in response:
        print(f"エラー: {response['error']}")
    else:
        print(f"応答: {response['content']}")
        print(f"\nモデル: {response['model']}")
        print(f"トークン使用量: {response['usage']['total_tokens']} (プロンプト: {response['usage']['prompt_tokens']}, 完了: {response['usage']['completion_tokens']})")
    
    print("=" * 80)

async def run_query_async(client: ParallelOpenAIClient, query: str, model: str = None, temperature: float = 0.7, max_tokens: int = None):
    """単一の問い合わせを非同期で実行"""
    response = await client.query_async(query, model, temperature, max_tokens)
    print_response(query, response)
    return response

async def run_batch_async(client: ParallelOpenAIClient, queries: List[str], model: str = None, temperature: float = 0.7, max_tokens: int = None):
    """複数の問い合わせを非同期でバッチ処理"""
    logger.info(f"{len(queries)}個の問い合わせを処理します...")
    responses = await client.query_batch_async(queries, model, temperature, max_tokens)
    
    for query, response in zip(queries, responses):
        print_response(query, response)
    
    logger.info(f"すべての問い合わせが完了しました")
    return responses

async def run_interactive_async(client: ParallelOpenAIClient, model: str = None, temperature: float = 0.7, max_tokens: int = None):
    """対話モードで実行"""
    print("\nOpenAI 並行問い合わせサンプル - 対話モード")
    print("終了するには 'exit' または 'quit' と入力してください\n")
    
    while True:
        try:
            query = input("問い合わせ> ")
            if query.lower() in ['exit', 'quit']:
                break
            
            if not query.strip():
                continue
            
            response = await client.query_async(query, model, temperature, max_tokens)
            print("\n" + "-" * 80)
            if "error" in response:
                print(f"エラー: {response['error']}")
            else:
                print(f"{response['content']}")
            print("-" * 80 + "\n")
            
        except KeyboardInterrupt:
            print("\n終了します...")
            break
        except Exception as e:
            logger.error(f"エラーが発生しました: {str(e)}")
    
    print("対話モードを終了します")

def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(description='OpenAI 並行問い合わせサンプル')
    
    # サブコマンドの設定
    subparsers = parser.add_subparsers(dest='command', help='実行するコマンド')
    
    # queryコマンド
    query_parser = subparsers.add_parser('query', help='単一の問い合わせを実行')
    query_parser.add_argument('text', help='問い合わせるテキスト')
    
    # batchコマンド
    batch_parser = subparsers.add_parser('batch', help='ファイルから複数の問い合わせを実行')
    batch_parser.add_argument('file', help='問い合わせが記載されたファイルのパス')
    
    # interactiveコマンド
    interactive_parser = subparsers.add_parser('interactive', help='対話モードで実行')
    
    # 共通オプション
    for subparser in [query_parser, batch_parser, interactive_parser]:
        subparser.add_argument('--model', help='使用するモデル')
        subparser.add_argument('--no-cache', action='store_true', help='キャッシュを使用しない')
        subparser.add_argument('--batch-size', type=int, help='バッチサイズ')
        subparser.add_argument('--config', default='config.yaml', help='設定ファイルのパス')
        subparser.add_argument('--temperature', type=float, default=0.7, help='温度パラメータ')
        subparser.add_argument('--max-tokens', type=int, help='最大トークン数')
    
    # ヘルプの表示
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    
    args = parser.parse_args()
    
    # クライアントの初期化
    client = ParallelOpenAIClient(
        config_path=args.config,
        use_cache=not args.no_cache,
        batch_size=args.batch_size
    )
    
    # コマンドに応じた処理
    if args.command == 'query':
        asyncio.run(run_query_async(client, args.text, args.model, args.temperature, args.max_tokens))
    
    elif args.command == 'batch':
        queries = load_queries_from_file(args.file)
        asyncio.run(run_batch_async(client, queries, args.model, args.temperature, args.max_tokens))
    
    elif args.command == 'interactive':
        asyncio.run(run_interactive_async(client, args.model, args.temperature, args.max_tokens))
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
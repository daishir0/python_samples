#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenAIプロンプトツール

コマンドラインからOpenAI GPTモデルに問い合わせを行うツール
"""

import os
import sys
import argparse
import json
import logging
from typing import Dict, List, Optional, Any

from openai_client import OpenAIClient
from config import DEBUG, MAX_TOKENS, TEMPERATURE

# ロガーの設定
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_arguments():
    """コマンドライン引数をパースする"""
    parser = argparse.ArgumentParser(description='OpenAIプロンプトツール')
    
    # 必須引数
    parser.add_argument('prompt', nargs='?', help='プロンプト（指定しない場合は標準入力から読み込む）')
    
    # オプション引数
    parser.add_argument('-f', '--file', help='プロンプトファイル（指定した場合はprompt引数は無視される）')
    parser.add_argument('-s', '--system', help='システムプロンプト')
    parser.add_argument('-m', '--model', help='使用するモデル')
    parser.add_argument('-t', '--temperature', type=float, default=TEMPERATURE, help=f'温度（デフォルト: {TEMPERATURE}）')
    parser.add_argument('-x', '--max-tokens', type=int, default=MAX_TOKENS, help=f'最大トークン数（デフォルト: {MAX_TOKENS}）')
    parser.add_argument('-o', '--output', help='出力ファイル（指定しない場合は標準出力に出力）')
    parser.add_argument('-j', '--json', action='store_true', help='JSONとして出力')
    parser.add_argument('-v', '--verbose', action='store_true', help='詳細なログを出力')
    parser.add_argument('-u', '--usage', action='store_true', help='使用量情報を表示')
    
    return parser.parse_args()


def read_prompt_from_file(file_path: str) -> str:
    """ファイルからプロンプトを読み込む"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"プロンプトファイルの読み込みに失敗しました: {e}")
        sys.exit(1)


def read_prompt_from_stdin() -> str:
    """標準入力からプロンプトを読み込む"""
    logger.info("標準入力からプロンプトを読み込みます。入力後、Ctrl+Dで終了してください。")
    try:
        return sys.stdin.read()
    except KeyboardInterrupt:
        logger.info("入力が中断されました。")
        sys.exit(0)


def write_output(output: str, file_path: Optional[str] = None):
    """出力を書き込む"""
    if file_path:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(output)
            logger.info(f"出力を {file_path} に書き込みました。")
        except Exception as e:
            logger.error(f"出力ファイルの書き込みに失敗しました: {e}")
            sys.exit(1)
    else:
        print(output)


def main():
    """メイン関数"""
    # コマンドライン引数をパース
    args = parse_arguments()
    
    # 詳細ログの設定
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # プロンプトの取得
    prompt = None
    if args.file:
        prompt = read_prompt_from_file(args.file)
    elif args.prompt:
        prompt = args.prompt
    else:
        prompt = read_prompt_from_stdin()
    
    if not prompt:
        logger.error("プロンプトが指定されていません。")
        sys.exit(1)
    
    # OpenAIクライアントの初期化
    try:
        client = OpenAIClient(model=args.model)
    except ValueError as e:
        logger.error(f"クライアントの初期化に失敗しました: {e}")
        sys.exit(1)
    
    # OpenAI GPTモデルに問い合わせ
    try:
        response = client.ask(
            prompt=prompt,
            system=args.system,
            max_tokens=args.max_tokens,
            temperature=args.temperature
        )
        
        # 使用量情報の表示
        if args.usage:
            usage = client.get_usage(response)
            logger.info(f"使用量情報: プロンプト {usage['prompt_tokens']} トークン, "
                       f"レスポンス {usage['completion_tokens']} トークン, "
                       f"合計 {usage['total_tokens']} トークン")
        
        # 出力の処理
        if args.json:
            # JSONとして出力
            json_data = client.extract_json(response)
            output = json.dumps(json_data, ensure_ascii=False, indent=2)
        else:
            # テキストとして出力
            output = client.extract_text(response)
        
        # 出力の書き込み
        write_output(output, args.output)
        
    except Exception as e:
        logger.error(f"問い合わせに失敗しました: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
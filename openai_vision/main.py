#!/usr/bin/env python3
"""
OpenAI Vision API サンプルプログラム - メインモジュール
====================================================

このモジュールは、コマンドライン引数を処理し、Vision APIを使用して
画像分析を実行するメインエントリーポイントです。
"""

import os
import sys
import json
import logging
import argparse
import asyncio
from typing import List, Dict, Any, Optional

from config import Config
from vision_client import VisionClient
from utils.cache_manager import CacheManager
from utils.image_processor import ImageProcessor

# ロガーの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

def parse_arguments():
    """コマンドライン引数を解析します。"""
    parser = argparse.ArgumentParser(description='OpenAI Vision APIを使用して画像を分析します。')
    
    # 必須引数
    parser.add_argument('image', nargs='?', help='分析する画像のパスまたはURL')
    
    # オプション引数
    parser.add_argument('-c', '--config', help='設定ファイルのパス')
    parser.add_argument('-p', '--prompt', help='分析のためのプロンプト')
    parser.add_argument('-f', '--format', choices=['text', 'json', 'markdown'], 
                        help='出力形式（text, json, markdown）')
    parser.add_argument('-o', '--output', help='結果を保存するファイルパス')
    parser.add_argument('-m', '--model', help='使用するモデル（デフォルト: gpt-4o-mini）')
    parser.add_argument('-k', '--api-key', help='OpenAI APIキー')
    parser.add_argument('--no-cache', action='store_true', help='キャッシュを無効にする')
    parser.add_argument('-b', '--batch', type=int, default=1, 
                        help='バッチサイズ（複数画像処理時）')
    parser.add_argument('-i', '--images-file', help='画像パスのリストを含むファイル（1行に1つのパスまたはURL）')
    parser.add_argument('-d', '--image-dir', help='画像ファイルを含むディレクトリ')
    parser.add_argument('-r', '--recursive', action='store_true', 
                        help='ディレクトリを再帰的に検索する')
    parser.add_argument('-e', '--extensions', default='jpg,jpeg,png,webp', 
                        help='処理する画像の拡張子（カンマ区切り）')
    parser.add_argument('-v', '--verbose', action='store_true', help='詳細なログを表示')
    
    return parser.parse_args()

def setup_logging(verbose: bool):
    """ロギングレベルを設定します。"""
    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("詳細ログモードが有効になりました")
    else:
        logging.getLogger().setLevel(logging.INFO)

def get_image_paths(args) -> List[str]:
    """
    コマンドライン引数から画像パスのリストを取得します。
    
    Args:
        args: コマンドライン引数
        
    Returns:
        画像パスのリスト
    """
    image_paths = []
    
    # 単一画像
    if args.image:
        image_paths.append(args.image)
    
    # 画像リストファイル
    if args.images_file and os.path.exists(args.images_file):
        try:
            with open(args.images_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        image_paths.append(line)
            logger.info(f"画像リストファイルから{len(image_paths)}個の画像パスを読み込みました")
        except Exception as e:
            logger.error(f"画像リストファイルの読み込みに失敗しました: {str(e)}")
    
    # 画像ディレクトリ
    if args.image_dir and os.path.isdir(args.image_dir):
        extensions = [f".{ext.lower().strip()}" for ext in args.extensions.split(',')]
        
        for root, _, files in os.walk(args.image_dir):
            if not args.recursive and root != args.image_dir:
                continue
                
            for file in files:
                if any(file.lower().endswith(ext) for ext in extensions):
                    image_paths.append(os.path.join(root, file))
        
        logger.info(f"ディレクトリから{len(image_paths)}個の画像ファイルを見つけました")
    
    return image_paths

def get_default_prompt() -> str:
    """デフォルトのプロンプトを取得します。"""
    return "この画像について詳細に説明してください。何が写っているか、特徴的な要素は何か、画像から読み取れる情報を教えてください。"

async def process_images(config: Config, args, image_paths: List[str]):
    """
    画像を処理します。
    
    Args:
        config: 設定
        args: コマンドライン引数
        image_paths: 画像パスのリスト
    """
    if not image_paths:
        logger.error("処理する画像がありません")
        return
    
    # キャッシュマネージャーの初期化
    cache_manager = None
    if not args.no_cache and config.get('cache.enabled', True):
        cache_dir = config.get('cache.directory', 'cache')
        cache_expiry = config.get('cache.expiry_days', 7)
        cache_manager = CacheManager(cache_dir, cache_expiry)
    
    # Vision APIクライアントの初期化
    api_key = args.api_key or config.get('openai.api_key')
    if not api_key:
        logger.error("OpenAI APIキーが設定されていません")
        return
    
    model = args.model or config.get('openai.model', 'gpt-4o-mini')
    max_tokens = config.get('openai.max_tokens', 1000)
    temperature = config.get('openai.temperature', 0.7)
    timeout = config.get('openai.timeout', 30)
    retry_count = config.get('openai.retry_count', 3)
    retry_delay = config.get('openai.retry_delay', 2)
    
    vision_client = VisionClient(
        api_key=api_key,
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        timeout=timeout,
        retry_count=retry_count,
        retry_delay=retry_delay,
        cache_manager=cache_manager
    )
    
    # プロンプトの設定
    prompt = args.prompt or get_default_prompt()
    
    # 出力形式の設定
    output_format = args.format
    
    # 複数画像の処理
    if len(image_paths) > 1:
        logger.info(f"{len(image_paths)}個の画像を処理します（バッチサイズ: {args.batch}）")
        results = await vision_client.analyze_multiple_images_async(
            image_paths=image_paths,
            prompt=prompt,
            output_format=output_format,
            batch_size=args.batch
        )
    else:
        # 単一画像の処理
        logger.info(f"画像を処理します: {image_paths[0]}")
        result = await vision_client.analyze_image_async(
            image_path=image_paths[0],
            prompt=prompt,
            output_format=output_format
        )
        results = [result]
    
    # 結果の出力
    output_results(results, args.output, args.format)

def output_results(results: List[Dict[str, Any]], output_file: Optional[str], output_format: Optional[str]):
    """
    結果を出力します。
    
    Args:
        results: 分析結果のリスト
        output_file: 出力ファイルパス（省略時は標準出力）
        output_format: 出力形式
    """
    # 出力内容の準備
    if output_format == 'json':
        output_content = json.dumps(results, ensure_ascii=False, indent=2)
    else:
        output_content = ""
        for i, result in enumerate(results):
            if i > 0:
                output_content += "\n" + "-" * 80 + "\n\n"
                
            if "error" in result:
                output_content += f"エラー: {result['error']}\n"
            elif "content" in result:
                output_content += result["content"] + "\n"
            else:
                output_content += json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    
    # 出力先の決定
    if output_file:
        try:
            # ディレクトリが存在しない場合は作成
            os.makedirs(os.path.dirname(os.path.abspath(output_file)), exist_ok=True)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output_content)
            logger.info(f"結果をファイルに保存しました: {output_file}")
        except Exception as e:
            logger.error(f"結果の保存に失敗しました: {str(e)}")
            print(output_content)
    else:
        print(output_content)

async def main_async():
    """非同期メイン関数"""
    # コマンドライン引数の解析
    args = parse_arguments()
    
    # ロギングの設定
    setup_logging(args.verbose)
    
    # 設定の読み込み
    config = Config(args.config)
    
    # 画像パスの取得
    image_paths = get_image_paths(args)
    
    # 画像の処理
    await process_images(config, args, image_paths)

def main():
    """メイン関数"""
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        logger.info("ユーザーによって処理が中断されました")
        sys.exit(1)
    except Exception as e:
        logger.error(f"予期しないエラーが発生しました: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WordPressへの投稿サンプルプログラム

このプログラムは、WordPressのREST APIを使用して記事を投稿するサンプルです。
タイトル、内容、カテゴリなどを指定して記事を投稿できます。

使い方:
    python main.py --title "記事タイトル" --content "記事内容" [options]

オプション:
    --title: 記事タイトル（必須）
    --content: 記事内容（必須）
    --file: 記事内容をファイルから読み込む場合のファイルパス
    --category: カテゴリID（デフォルト: 設定ファイルの値）
    --status: 投稿ステータス（publish, draft, private, pending）
    --tags: タグ（カンマ区切り）
    --excerpt: 抜粋
    --debug: デバッグモード

例:
    python main.py --title "テスト記事" --content "これはテスト記事です。"
    python main.py --title "ファイルから読み込む記事" --file content.html
    python main.py --title "下書き記事" --content "これは下書きです。" --status draft
"""

import sys
import os
import argparse
import logging
from pathlib import Path
from typing import Dict, Any, List

# 自作モジュールのインポート
import config
from wordpress_poster import WordPressPoster

def setup_logging(debug_mode: bool = False) -> logging.Logger:
    """
    ロギングの設定
    
    Args:
        debug_mode: デバッグモードの有効/無効
        
    Returns:
        ロガーオブジェクト
    """
    log_level = logging.DEBUG if debug_mode else logging.INFO
    
    # ロガーの設定
    logger = logging.getLogger()
    logger.setLevel(log_level)
    
    # 既存のハンドラをクリア
    for handler in logger.handlers:
        logger.removeHandler(handler)
    
    # コンソールハンドラを追加
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    
    # フォーマッタを設定
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger

def setup_argument_parser() -> argparse.ArgumentParser:
    """コマンドライン引数のパーサーを設定"""
    parser = argparse.ArgumentParser(
        description='WordPressへの投稿サンプルプログラム',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用例:
  python main.py --title "テスト記事" --content "これはテスト記事です。"
  python main.py --title "ファイルから読み込む記事" --file content.html
  python main.py --title "下書き記事" --content "これは下書きです。" --status draft
        """
    )
    
    parser.add_argument(
        '--title',
        help='記事タイトル'
    )
    
    content_group = parser.add_mutually_exclusive_group()
    content_group.add_argument(
        '--content',
        help='記事内容'
    )
    content_group.add_argument(
        '--file',
        help='記事内容を読み込むファイルパス'
    )
    
    parser.add_argument(
        '--category',
        type=int,
        help='カテゴリID'
    )
    
    parser.add_argument(
        '--status',
        choices=['publish', 'draft', 'private', 'pending'],
        default='publish',
        help='投稿ステータス'
    )
    
    parser.add_argument(
        '--tags',
        help='タグ（カンマ区切り）'
    )
    
    parser.add_argument(
        '--excerpt',
        help='記事の抜粋'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        help='デバッグモードで実行'
    )
    
    parser.add_argument(
        '--update',
        type=int,
        help='更新する記事のID'
    )
    
    parser.add_argument(
        '--list',
        type=int,
        metavar='COUNT',
        help='最新の記事をCOUNT件表示する'
    )
    
    parser.add_argument(
        '--search',
        type=str,
        help='キーワードで記事を検索する'
    )
    
    return parser

def read_content_from_file(file_path: str) -> str:
    """
    ファイルから記事内容を読み込む
    
    Args:
        file_path: ファイルパス
        
    Returns:
        ファイルの内容
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        raise Exception(f"ファイルの読み込みに失敗しました: {e}")

def main():
    """メイン関数"""
    # コマンドライン引数の解析
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    # ログ設定
    logger = setup_logging(args.debug)
    
    logger.info("=== WordPressへの投稿サンプルプログラム 開始 ===")
    
    try:
        # 設定ファイルの読み込み
        logger.info("設定ファイルを読み込み中...")
        cfg = config.load_config()
        
        # デバッグモードの設定を上書き
        if args.debug:
            cfg['debug']['enabled'] = True
            cfg['debug']['verbose_logging'] = True
            logger.info("デバッグモードが有効になりました")
        
        # 設定の検証
        if not config.validate_config(cfg):
            logger.error("設定が不完全です。環境変数を確認してください。")
            config.print_env_help()
            sys.exit(1)
        
        # 記事内容の取得
        content = ""
        if args.content:
            content = args.content
        elif args.file:
            logger.info(f"ファイルから記事内容を読み込み中: {args.file}")
            content = read_content_from_file(args.file)
        
        # タグの処理
        tags = []
        if args.tags:
            tags = [tag.strip() for tag in args.tags.split(',')]
        
        # 記事データの準備
        article = {
            'title': args.title,
            'content': content,
            'status': args.status
        }
        
        # オプションパラメータの追加
        if args.category:
            article['category_id'] = args.category
        
        if tags:
            article['tags'] = tags
        
        if args.excerpt:
            article['excerpt'] = args.excerpt
        
        # WordPress投稿器の初期化
        logger.info("WordPress投稿器を初期化中...")
        wordpress_poster = WordPressPoster(cfg)
        
        # WordPress接続テスト
        if not wordpress_poster.test_connection():
            logger.error("WordPressとの接続に失敗しました")
            sys.exit(1)
        logger.info("WordPress接続テスト成功")
        
        # 記事一覧表示の場合
        if args.list:
            articles = wordpress_poster.get_latest_articles(args.list)
            if articles:
                print(f"\n最新の記事 {len(articles)}件:")
                print("=" * 80)
                for i, article in enumerate(articles, 1):
                    print(f"{i}. ID: {article['id']}")
                    print(f"   タイトル: {article['title']}")
                    print(f"   日付: {article['date']}")
                    print(f"   URL: {article['link']}")
                    print("-" * 80)
            else:
                print("記事が見つかりませんでした")
            sys.exit(0)
        
        # 記事検索の場合
        if args.search:
            articles = wordpress_poster.search_articles(args.search)
            if articles:
                print(f"\n'{args.search}' の検索結果 {len(articles)}件:")
                print("=" * 80)
                for i, article in enumerate(articles, 1):
                    print(f"{i}. ID: {article['id']}")
                    print(f"   タイトル: {article['title']}")
                    print(f"   日付: {article['date']}")
                    print(f"   抜粋: {article['excerpt']}")
                    print(f"   URL: {article['link']}")
                    print("-" * 80)
            else:
                print(f"'{args.search}' に一致する記事が見つかりませんでした")
            sys.exit(0)
        
        # タイトルと内容が必要な操作の場合はチェック
        if not args.list and not args.search and not args.title:
            logger.error("タイトルが指定されていません")
            sys.exit(1)
        
        if not args.list and not args.search and not args.content and not args.file:
            logger.error("記事内容が指定されていません（--content または --file が必要）")
            sys.exit(1)
        
        # 記事を投稿または更新
        if args.update:
            logger.info(f"記事を更新中: ID={args.update}, タイトル={article['title']}")
            result = wordpress_poster.update_article(args.update, article)
            
            if result:
                logger.info(f"更新成功: ID={result['id']}")
                logger.info(f"記事URL: {result['link']}")
            else:
                logger.error("更新に失敗しました")
                sys.exit(1)
        else:
            logger.info(f"記事を投稿中: {article['title']}")
            result = wordpress_poster.post_article(article)
            
            if result:
                logger.info(f"投稿成功: ID={result['id']}")
                logger.info(f"記事URL: {result['link']}")
            else:
                logger.error("投稿に失敗しました")
                sys.exit(1)
        
        logger.info("=== 処理完了 ===")
        
    except KeyboardInterrupt:
        logger.info("ユーザーによって処理が中断されました")
        sys.exit(1)
    except Exception as e:
        logger.error(f"予期しないエラーが発生しました: {e}")
        if args.debug:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
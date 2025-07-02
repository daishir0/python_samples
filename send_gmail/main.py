#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gmailメール送信ツール

コマンドラインからGmailでメールを送信するツール
"""

import os
import sys
import argparse
import logging
from typing import Dict, List, Optional, Any

from gmail_client import GmailClient
from config import DEBUG

# ロガーの設定
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_arguments():
    """コマンドライン引数をパースする"""
    parser = argparse.ArgumentParser(description='Gmailメール送信ツール')
    
    # 必須引数
    parser.add_argument('to', nargs='?', help='宛先メールアドレス（指定しない場合は標準入力から読み込む）')
    
    # オプション引数
    parser.add_argument('-s', '--subject', help='件名')
    parser.add_argument('-b', '--body', help='本文')
    parser.add_argument('-f', '--file', help='本文ファイル（指定した場合はbody引数は無視される）')
    parser.add_argument('-c', '--cc', help='CC（カンマ区切りで複数指定可能）')
    parser.add_argument('-d', '--bcc', help='BCC（カンマ区切りで複数指定可能）')
    parser.add_argument('-a', '--attachments', help='添付ファイル（カンマ区切りで複数指定可能）')
    parser.add_argument('--html', action='store_true', help='HTMLメールとして送信')
    parser.add_argument('-v', '--verbose', action='store_true', help='詳細なログを出力')
    
    return parser.parse_args()


def read_body_from_file(file_path: str) -> str:
    """ファイルから本文を読み込む"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        logger.error(f"本文ファイルの読み込みに失敗しました: {e}")
        sys.exit(1)


def read_body_from_stdin() -> str:
    """標準入力から本文を読み込む"""
    logger.info("標準入力から本文を読み込みます。入力後、Ctrl+Dで終了してください。")
    try:
        return sys.stdin.read()
    except KeyboardInterrupt:
        logger.info("入力が中断されました。")
        sys.exit(0)


def main():
    """メイン関数"""
    # コマンドライン引数をパース
    args = parse_arguments()
    
    # 詳細ログの設定
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # 宛先の取得
    to = None
    if args.to:
        to = args.to
    else:
        logger.error("宛先が指定されていません。")
        sys.exit(1)
    
    # 件名の取得
    subject = args.subject or "件名なし"
    
    # 本文の取得
    body = None
    if args.file:
        body = read_body_from_file(args.file)
    elif args.body:
        body = args.body
    else:
        body = read_body_from_stdin()
    
    if not body:
        logger.error("本文が指定されていません。")
        sys.exit(1)
    
    # CCの処理
    cc = []
    if args.cc:
        cc = [addr.strip() for addr in args.cc.split(",")]
    
    # BCCの処理
    bcc = []
    if args.bcc:
        bcc = [addr.strip() for addr in args.bcc.split(",")]
    
    # 添付ファイルの処理
    attachments = []
    if args.attachments:
        attachments = [path.strip() for path in args.attachments.split(",")]
    
    # Gmailクライアントの初期化
    try:
        client = GmailClient()
    except ValueError as e:
        logger.error(f"クライアントの初期化に失敗しました: {e}")
        sys.exit(1)
    
    # メールの送信
    try:
        success = client.send_email(
            to=to,
            subject=subject,
            body=body,
            cc=cc,
            bcc=bcc,
            attachments=attachments,
            is_html=args.html
        )
        
        if success:
            logger.info("メールの送信が完了しました。")
        else:
            logger.error("メールの送信に失敗しました。")
            sys.exit(1)
        
    except Exception as e:
        logger.error(f"メールの送信中にエラーが発生しました: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
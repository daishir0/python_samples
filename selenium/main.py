#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chrome WebDriverを使用した汎用的なサンプルプログラム

このプログラムは、Chrome WebDriverを使用して特定のWebページにアクセスし、
JavaScriptが実行された後のページソースを取得するなどの機能を提供します。
エラー処理と再問い合わせの機能、APIキーの外部ファイルからの読み込みにも対応しています。

使用方法:
    python main.py [URL]
    
    または、URLを指定せずに実行すると対話モードになります:
    python main.py
"""

import sys
import os
import time
import json
import argparse
import logging
from typing import Dict, Any, Optional, List, Tuple
from urllib.parse import urlparse

from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException

from selenium_utils import (
    setup_driver,
    cleanup_temp_dir,
    load_page_with_retry,
    wait_for_element,
    get_page_source_after_js,
    safe_click,
    take_screenshot
)
from config import API_KEY, DEBUG, MAX_RETRIES

# ロガーの設定
logger = logging.getLogger(__name__)
if DEBUG:
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
else:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )


def validate_url(url: str) -> bool:
    """
    URLが有効かどうかを検証します。
    
    Args:
        url (str): 検証するURL
    
    Returns:
        bool: URLが有効な場合はTrue、無効な場合はFalse
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def get_user_input(prompt: str, validator=None, error_message: str = None) -> str:
    """
    ユーザーからの入力を取得し、オプションでバリデーションを行います。
    
    Args:
        prompt (str): ユーザーに表示するプロンプト
        validator (callable, optional): 入力を検証する関数
        error_message (str, optional): バリデーションエラー時のメッセージ
    
    Returns:
        str: ユーザーの入力
    """
    while True:
        user_input = input(prompt)
        
        if validator is None or validator(user_input):
            return user_input
        
        if error_message:
            print(error_message)


def save_page_content(content: str, url: str, output_dir: str = "output") -> str:
    """
    ページの内容をファイルに保存します。
    
    Args:
        content (str): 保存するコンテンツ
        url (str): ページのURL
        output_dir (str, optional): 出力ディレクトリ
    
    Returns:
        str: 保存したファイルのパス
    """
    # 出力ディレクトリが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # URLからファイル名を生成
    parsed_url = urlparse(url)
    domain = parsed_url.netloc.replace(".", "_")
    path = parsed_url.path.replace("/", "_")
    if not path:
        path = "index"
    
    # タイムスタンプを追加
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    
    # ファイル名を生成
    filename = f"{domain}{path}_{timestamp}.html"
    filepath = os.path.join(output_dir, filename)
    
    # コンテンツを保存
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    
    logger.info(f"ページの内容を保存しました: {filepath}")
    return filepath


def extract_data_from_page(driver, selectors: Dict[str, Tuple[By, str]]) -> Dict[str, Any]:
    """
    ページから指定されたセレクタに基づいてデータを抽出します。
    
    Args:
        driver: WebDriverインスタンス
        selectors: セレクタの辞書 {名前: (検索方法, 値)}
    
    Returns:
        Dict[str, Any]: 抽出されたデータ
    """
    result = {}
    
    for name, (by, value) in selectors.items():
        try:
            element = wait_for_element(driver, by, value)
            if element:
                result[name] = element.text
            else:
                result[name] = None
        except Exception as e:
            logger.error(f"データの抽出中にエラーが発生しました ({name}): {e}")
            result[name] = None
    
    return result


def process_url(url: str) -> Dict[str, Any]:
    """
    指定されたURLにアクセスし、ページの情報を処理します。
    
    Args:
        url (str): アクセスするURL
    
    Returns:
        Dict[str, Any]: 処理結果
    """
    driver = None
    temp_dir = None
    result = {
        "success": False,
        "url": url,
        "title": None,
        "content_file": None,
        "screenshot_file": None,
        "extracted_data": None,
        "error": None
    }
    
    try:
        # WebDriverの初期化
        driver, temp_dir = setup_driver()
        
        # ページにアクセス
        if not load_page_with_retry(driver, url):
            result["error"] = "ページの読み込みに失敗しました"
            return result
        
        # ページのタイトルを取得
        result["title"] = driver.title
        
        # JavaScriptの実行後にページソースを取得
        page_source = get_page_source_after_js(driver)
        
        # ページの内容を保存
        result["content_file"] = save_page_content(page_source, url)
        
        # スクリーンショットを撮影
        screenshot_filename = os.path.splitext(result["content_file"])[0] + ".png"
        if take_screenshot(driver, screenshot_filename):
            result["screenshot_file"] = screenshot_filename
        
        # 例として、ページからいくつかのデータを抽出
        selectors = {
            "main_heading": (By.TAG_NAME, "h1"),
            "meta_description": (By.CSS_SELECTOR, "meta[name='description']"),
            "links_count": (By.TAG_NAME, "a")
        }
        
        extracted_data = extract_data_from_page(driver, selectors)
        
        # リンクの数を数える
        if driver.find_elements(By.TAG_NAME, "a"):
            extracted_data["links_count"] = len(driver.find_elements(By.TAG_NAME, "a"))
        
        result["extracted_data"] = extracted_data
        result["success"] = True
        
    except WebDriverException as e:
        logger.error(f"WebDriverエラーが発生しました: {e}")
        result["error"] = f"WebDriverエラー: {str(e)}"
    except Exception as e:
        logger.error(f"予期しないエラーが発生しました: {e}")
        result["error"] = f"予期しないエラー: {str(e)}"
    finally:
        # WebDriverを終了
        if driver:
            try:
                driver.quit()
            except Exception as e:
                logger.warning(f"WebDriverの終了中にエラーが発生しました: {e}")
        
        # 一時ディレクトリを削除
        if temp_dir:
            cleanup_temp_dir(temp_dir)
    
    return result


def interactive_mode() -> None:
    """
    対話モードでプログラムを実行します。
    """
    print("=== Chrome WebDriver サンプルプログラム - 対話モード ===")
    print("終了するには 'exit' または 'quit' と入力してください。")
    
    while True:
        url = get_user_input(
            "\nURLを入力してください: ",
            validator=validate_url,
            error_message="無効なURLです。正しいURLを入力してください。"
        )
        
        if url.lower() in ['exit', 'quit']:
            print("プログラムを終了します。")
            break
        
        print(f"\n{url} を処理しています...")
        result = process_url(url)
        
        if result["success"]:
            print("\n=== 処理結果 ===")
            print(f"URL: {result['url']}")
            print(f"タイトル: {result['title']}")
            print(f"コンテンツファイル: {result['content_file']}")
            print(f"スクリーンショット: {result['screenshot_file'] or 'なし'}")
            
            if result["extracted_data"]:
                print("\n抽出されたデータ:")
                for key, value in result["extracted_data"].items():
                    if key == "links_count":
                        print(f"  リンク数: {value}")
                    elif key == "main_heading" and value:
                        print(f"  メインの見出し: {value}")
                    elif key == "meta_description" and value:
                        print(f"  メタ説明: {value}")
        else:
            print(f"\nエラーが発生しました: {result['error']}")
            retry = get_user_input(
                "再試行しますか？ (y/n): ",
                validator=lambda x: x.lower() in ['y', 'yes', 'n', 'no'],
                error_message="'y' または 'n' を入力してください。"
            )
            
            if retry.lower() in ['y', 'yes']:
                print(f"\n{url} を再処理しています...")
                result = process_url(url)
                # 結果の表示は省略（上記と同じ処理になるため）


def main() -> None:
    """
    メイン関数
    """
    parser = argparse.ArgumentParser(description='Chrome WebDriverを使用したWebページ処理プログラム')
    parser.add_argument('url', nargs='?', help='処理するURL')
    parser.add_argument('--output', '-o', default='output', help='出力ディレクトリ')
    parser.add_argument('--debug', '-d', action='store_true', help='デバッグモードを有効にする')
    
    args = parser.parse_args()
    
    # APIキーの確認
    if not API_KEY and DEBUG:
        logger.warning("API_KEYが設定されていません。一部の機能が制限される可能性があります。")
    
    if args.url:
        # URLが指定された場合は直接処理
        if not validate_url(args.url):
            logger.error(f"無効なURL: {args.url}")
            sys.exit(1)
        
        result = process_url(args.url)
        
        if result["success"]:
            print(f"処理が完了しました。結果は {result['content_file']} に保存されました。")
            if result["screenshot_file"]:
                print(f"スクリーンショットは {result['screenshot_file']} に保存されました。")
        else:
            print(f"エラーが発生しました: {result['error']}")
            sys.exit(1)
    else:
        # URLが指定されていない場合は対話モード
        try:
            interactive_mode()
        except KeyboardInterrupt:
            print("\nプログラムが中断されました。")
            sys.exit(0)


if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Selenium ユーティリティモジュール
Chrome WebDriverの設定や共通機能を提供します。
"""

import os
import time
import tempfile
import shutil
import logging
from typing import Tuple, Optional, Dict, Any

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, 
    WebDriverException, 
    NoSuchElementException,
    StaleElementReferenceException
)

from config import (
    CHROME_BINARY_PATH, 
    CHROME_DRIVER_PATH, 
    DEBUG, 
    PAGE_LOAD_TIMEOUT, 
    IMPLICIT_WAIT,
    MAX_RETRIES,
    RETRY_DELAY
)

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


def setup_driver() -> Tuple[webdriver.Chrome, str]:
    """
    Chrome WebDriverを設定して返します。
    
    Returns:
        Tuple[webdriver.Chrome, str]: WebDriverインスタンスと一時ディレクトリのパス
    """
    options = Options()
    options.binary_location = CHROME_BINARY_PATH
    options.add_argument("--window-size=1366,768")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-infobars')
    options.add_argument('--headless=new')
    options.add_argument('--disable-setuid-sandbox')
    
    # DevToolsActivePort問題を解決するための引数
    options.add_argument('--no-first-run')
    options.add_argument('--no-default-browser-check')
    options.add_argument('--disable-background-networking')
    options.add_argument('--disable-prompt-on-repost')
    options.add_argument('--disable-sync')
    
    # Chromeデータ用の専用一時ディレクトリを使用
    temp_dir = tempfile.mkdtemp()
    options.add_argument(f'--user-data-dir={temp_dir}')
    options.add_argument('--data-path=' + os.path.join(temp_dir, 'data'))
    options.add_argument('--homedir=' + os.path.join(temp_dir, 'home'))
    options.add_argument('--disk-cache-dir=' + os.path.join(temp_dir, 'cache'))
    
    try:
        service = Service(executable_path=CHROME_DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=options)
        
        # タイムアウト設定
        driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
        driver.implicitly_wait(IMPLICIT_WAIT)
        
        logger.info("Chrome WebDriverを正常に初期化しました")
        return driver, temp_dir
    except Exception as e:
        logger.error(f"Chrome WebDriverの初期化に失敗しました: {e}")
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
        raise


def cleanup_temp_dir(temp_dir: str) -> None:
    """
    WebDriver終了後に一時ディレクトリを削除します。
    
    Args:
        temp_dir (str): 削除する一時ディレクトリのパス
    """
    try:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
            logger.info(f"一時ディレクトリを削除しました: {temp_dir}")
    except Exception as e:
        logger.warning(f"一時ディレクトリの削除に失敗しました: {e}")


def load_page_with_retry(driver: webdriver.Chrome, url: str) -> Tuple[bool, bool]:
    """
    指定されたURLにアクセスし、ページの読み込みを試みます。
    失敗した場合は指定回数リトライします。
    タイムアウトが発生した場合でも部分的なHTMLを取得できる場合があります。
    
    Args:
        driver (webdriver.Chrome): WebDriverインスタンス
        url (str): アクセスするURL
    
    Returns:
        Tuple[bool, bool]: (成功したかどうか, 部分的なHTMLが取得できたかどうか)
    """
    partial_html_available = False
    
    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"ページにアクセスしています: {url} (試行 {attempt + 1}/{MAX_RETRIES})")
            
            # try-except-finallyブロックを使用してdriver.getを実行
            try:
                driver.get(url)
                
                # ページが完全に読み込まれるまで待機
                WebDriverWait(driver, PAGE_LOAD_TIMEOUT).until(
                    lambda d: d.execute_script('return document.readyState') == 'complete'
                )
                
                logger.info(f"ページの読み込みに成功しました: {url}")
                return True, True  # 完全に成功
            except TimeoutException as e:
                logger.warning(f"ページの読み込みがタイムアウトしました: {url}")
                # タイムアウトが発生しても、部分的なHTMLが取得できる可能性がある
                if driver.page_source and len(driver.page_source) > 100:  # 最低限のHTMLがあるか確認
                    logger.info("タイムアウトが発生しましたが、部分的なHTMLを取得しました")
                    partial_html_available = True
                raise e  # 例外を再度発生させて外側のcatchブロックで処理
            except Exception as e:
                logger.error(f"ページの読み込み中にエラーが発生しました: {e}")
                # その他のエラーでも部分的なHTMLが取得できる可能性がある
                if driver.page_source and len(driver.page_source) > 100:
                    logger.info("エラーが発生しましたが、部分的なHTMLを取得しました")
                    partial_html_available = True
                raise e
        except TimeoutException:
            # すでに内側のtry-exceptで処理済み
            pass
        except WebDriverException as e:
            logger.error(f"ページの読み込み中にWebDriverエラーが発生しました: {e}")
        
        # 最後の試行でなければ待機してリトライ
        if attempt < MAX_RETRIES - 1:
            logger.info(f"{RETRY_DELAY}秒後にリトライします...")
            time.sleep(RETRY_DELAY)
    
    logger.error(f"ページの読み込みに失敗しました（{MAX_RETRIES}回試行）: {url}")
    if partial_html_available:
        logger.info("ただし、部分的なHTMLは取得できています")
    
    return False, partial_html_available


def wait_for_element(driver: webdriver.Chrome, by: By, value: str, timeout: int = None) -> Optional[webdriver.remote.webelement.WebElement]:
    """
    指定された要素が表示されるまで待機します。
    
    Args:
        driver (webdriver.Chrome): WebDriverインスタンス
        by (By): 要素の検索方法（By.ID, By.XPATHなど）
        value (str): 検索する値
        timeout (int, optional): タイムアウト時間（秒）。Noneの場合はデフォルト値を使用
    
    Returns:
        Optional[WebElement]: 見つかった要素。タイムアウトした場合はNone
    """
    if timeout is None:
        timeout = IMPLICIT_WAIT
    
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located((by, value))
        )
        return element
    except TimeoutException:
        logger.warning(f"要素が見つかりませんでした: {by}={value}")
        return None
    except Exception as e:
        logger.error(f"要素の待機中にエラーが発生しました: {e}")
        return None


def get_page_source_after_js(driver: webdriver.Chrome, wait_time: int = 2) -> str:
    """
    JavaScriptの実行後にページのソースを取得します。
    
    Args:
        driver (webdriver.Chrome): WebDriverインスタンス
        wait_time (int, optional): JavaScriptの実行を待つ時間（秒）
    
    Returns:
        str: ページのソース
    """
    # JavaScriptの実行を待つ
    time.sleep(wait_time)
    
    # ページのソースを取得
    return driver.page_source


def safe_click(driver: webdriver.Chrome, element) -> bool:
    """
    要素を安全にクリックします。エラーが発生した場合はJavaScriptを使用してクリックを試みます。
    
    Args:
        driver (webdriver.Chrome): WebDriverインスタンス
        element: クリックする要素
    
    Returns:
        bool: 成功した場合はTrue、失敗した場合はFalse
    """
    try:
        element.click()
        return True
    except (StaleElementReferenceException, NoSuchElementException) as e:
        logger.warning(f"通常のクリックに失敗しました: {e}")
        try:
            # JavaScriptを使用してクリック
            driver.execute_script("arguments[0].click();", element)
            return True
        except Exception as js_e:
            logger.error(f"JavaScriptを使用したクリックにも失敗しました: {js_e}")
            return False
    except Exception as e:
        logger.error(f"要素のクリック中にエラーが発生しました: {e}")
        return False


def take_screenshot(driver: webdriver.Chrome, filename: str) -> bool:
    """
    スクリーンショットを撮影して保存します。
    
    Args:
        driver (webdriver.Chrome): WebDriverインスタンス
        filename (str): 保存するファイル名
    
    Returns:
        bool: 成功した場合はTrue、失敗した場合はFalse
    """
    try:
        driver.save_screenshot(filename)
        logger.info(f"スクリーンショットを保存しました: {filename}")
        return True
    except Exception as e:
        logger.error(f"スクリーンショットの撮影に失敗しました: {e}")
        return False
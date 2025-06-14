#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
設定ファイル
Chrome WebDriverのパスやAPIキーなどの設定を管理します。
"""

import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# Chrome WebDriverの設定
CHROME_BINARY_PATH = os.getenv('CHROME_BINARY_PATH', '/usr/bin/google-chrome')
CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH', '/usr/local/bin/chromedriver')

# APIキーの設定
API_KEY = os.getenv('API_KEY', '')

# デバッグモード
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# リトライ設定
MAX_RETRIES = int(os.getenv('MAX_RETRIES', '3'))
RETRY_DELAY = int(os.getenv('RETRY_DELAY', '2'))

# タイムアウト設定（秒）
PAGE_LOAD_TIMEOUT = int(os.getenv('PAGE_LOAD_TIMEOUT', '30'))
IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', '10'))
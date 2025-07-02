#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gmailメール送信ツール設定ファイル
"""

import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# Gmail認証情報
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_FROM = os.getenv("EMAIL_FROM")

# SMTPサーバー設定
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# リトライ設定
MAX_RETRIES = 3
RETRY_DELAY = 2  # 秒
BACKOFF_FACTOR = 2  # バックオフ係数

# ログ設定
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
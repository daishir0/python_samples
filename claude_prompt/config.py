#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claudeプロンプトツール設定ファイル
"""

import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

# Anthropic APIキー
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# デフォルトのモデル
DEFAULT_MODEL = "claude-3-5-sonnet-20240620"

# リトライ設定
MAX_RETRIES = 3
RETRY_DELAY = 2  # 秒

# ログ設定
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "t")
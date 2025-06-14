"""
OpenAI 並行問い合わせサンプル - ユーティリティモジュール
==================================================

このパッケージは、OpenAIへの並行問い合わせを行うための
ユーティリティクラスとヘルパー関数を提供します。

主なモジュール:
-----------
- cache_manager: キャッシュ管理機能
- openai_client: OpenAI APIクライアント
"""

from .cache_manager import CacheManager
from .openai_client import OpenAIClient

__all__ = ['CacheManager', 'OpenAIClient']
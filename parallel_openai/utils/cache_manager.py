"""
OpenAI 並行問い合わせサンプル - キャッシュ管理モジュール
==================================================

このモジュールは、OpenAIへの問い合わせ結果をキャッシュし、
アプリケーションのパフォーマンスを向上させる機能を提供します。

主な機能:
-------
- 問い合わせ結果のキャッシュと取得
- キャッシュの有効期限管理
- メタデータの管理

使用方法:
-------
```python
from parallel_openai.utils.cache_manager import CacheManager

# キャッシュマネージャーの初期化
cache_manager = CacheManager(
    cache_dir='./cache',  # キャッシュディレクトリのパス
    cache_expiry_days=7   # キャッシュの有効期限（日数）
)

# 問い合わせ結果をキャッシュ
query = "What is the capital of Japan?"
response = {"content": "The capital of Japan is Tokyo."}
cache_manager.cache_response(query, response)

# キャッシュから問い合わせ結果を取得
cached_response = cache_manager.get_response(query)

# キャッシュをクリア（特定のクエリまたはすべて）
cache_manager.clear_cache(query)  # 特定のクエリのキャッシュをクリア
cache_manager.clear_cache()       # すべてのキャッシュをクリア
```
"""

import os
import json
import logging
import hashlib
from datetime import datetime, timedelta

# ロガーの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class CacheManager:
    def __init__(self, cache_dir='cache', cache_expiry_days=7):
        """キャッシュマネージャーの初期化"""
        self.cache_dir = cache_dir
        self.response_cache_dir = os.path.join(cache_dir, 'responses')
        self.metadata_file = os.path.join(cache_dir, 'metadata.json')
        self.cache_expiry = timedelta(days=cache_expiry_days)
        
        # キャッシュディレクトリの作成
        os.makedirs(self.response_cache_dir, exist_ok=True)
        
        # メタデータの読み込み
        self.metadata = self._load_metadata()
    
    def _load_metadata(self):
        """メタデータの読み込み"""
        if os.path.exists(self.metadata_file):
            try:
                with open(self.metadata_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                logger.error(f"メタデータの読み込みに失敗しました: {str(e)}")
                return {}
        return {}
    
    def _save_metadata(self):
        """メタデータの保存"""
        try:
            with open(self.metadata_file, 'w', encoding='utf-8') as f:
                json.dump(self.metadata, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"メタデータの保存に失敗しました: {str(e)}")
    
    def _get_query_hash(self, query):
        """クエリからハッシュ値を生成"""
        # クエリが辞書の場合はJSON文字列に変換
        if isinstance(query, dict):
            query = json.dumps(query, sort_keys=True)
        return hashlib.md5(query.encode('utf-8')).hexdigest()
    
    def is_response_cached(self, query):
        """クエリの応答がキャッシュされているか確認"""
        query_hash = self._get_query_hash(query)
        
        # メタデータに存在するか確認
        if query_hash not in self.metadata:
            return False
        
        # キャッシュファイルが存在するか確認
        response_cache_path = os.path.join(self.response_cache_dir, f"{query_hash}.json")
        
        if not os.path.exists(response_cache_path):
            return False
        
        # キャッシュの有効期限を確認
        cache_time = datetime.fromisoformat(self.metadata[query_hash]['timestamp'])
        if datetime.now() - cache_time > self.cache_expiry:
            logger.info(f"応答キャッシュの有効期限切れ: {query_hash}")
            return False
        
        return True
    
    def cache_response(self, query, response_data):
        """問い合わせ応答をキャッシュ"""
        query_hash = self._get_query_hash(query)
        response_cache_path = os.path.join(self.response_cache_dir, f"{query_hash}.json")
        
        try:
            with open(response_cache_path, 'w', encoding='utf-8') as f:
                json.dump(response_data, f, ensure_ascii=False, indent=2)
            
            # メタデータを更新
            self.metadata[query_hash] = {
                'query': query if isinstance(query, str) else json.dumps(query, sort_keys=True),
                'timestamp': datetime.now().isoformat(),
                'type': 'response'
            }
            self._save_metadata()
            
            logger.info(f"応答をキャッシュしました: {query_hash}")
            return True
        except Exception as e:
            logger.error(f"応答のキャッシュに失敗しました: {str(e)}")
            return False
    
    def get_response(self, query):
        """キャッシュから問い合わせ応答を取得"""
        if not self.is_response_cached(query):
            return None
        
        query_hash = self._get_query_hash(query)
        response_cache_path = os.path.join(self.response_cache_dir, f"{query_hash}.json")
        
        try:
            with open(response_cache_path, 'r', encoding='utf-8') as f:
                response_data = json.load(f)
            
            logger.info(f"キャッシュから応答を読み込みました: {query_hash}")
            return response_data
        except Exception as e:
            logger.error(f"キャッシュからの応答読み込みに失敗しました: {str(e)}")
            return None
    
    def clear_cache(self, query=None):
        """キャッシュをクリア"""
        if query:
            # 特定のクエリのキャッシュをクリア
            query_hash = self._get_query_hash(query)
            response_cache_path = os.path.join(self.response_cache_dir, f"{query_hash}.json")
            
            if os.path.exists(response_cache_path):
                os.remove(response_cache_path)
            
            if query_hash in self.metadata:
                del self.metadata[query_hash]
                self._save_metadata()
            
            logger.info(f"キャッシュをクリアしました: {query_hash}")
        else:
            # すべてのキャッシュをクリア
            for filename in os.listdir(self.response_cache_dir):
                os.remove(os.path.join(self.response_cache_dir, filename))
            
            self.metadata = {}
            self._save_metadata()
            
            logger.info("すべてのキャッシュをクリアしました")
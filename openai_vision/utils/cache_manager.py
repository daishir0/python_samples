"""
OpenAI Vision API サンプルプログラム - キャッシュマネージャー
==========================================================

このモジュールは、API呼び出しの結果をキャッシュするための機能を提供します。
キャッシュを使用することで、同じ画像に対する重複したAPI呼び出しを防ぎ、
コストとレスポンス時間を削減できます。
"""

import os
import json
import time
import hashlib
import logging
from typing import Optional, Dict, Any

# ロガーの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class CacheManager:
    """APIレスポンスのキャッシュを管理するクラス"""
    
    def __init__(self, cache_dir: str = 'cache', expiry_days: int = 7):
        """
        キャッシュマネージャーを初期化します。
        
        Args:
            cache_dir: キャッシュファイルを保存するディレクトリ
            expiry_days: キャッシュの有効期限（日数）
        """
        self.cache_dir = cache_dir
        self.expiry_seconds = expiry_days * 24 * 60 * 60  # 日数を秒に変換
        
        # キャッシュディレクトリが存在しない場合は作成
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir, exist_ok=True)
            logger.info(f"キャッシュディレクトリを作成しました: {cache_dir}")
    
    def _get_cache_key(self, url: str, params: Optional[Dict] = None) -> str:
        """
        URLとパラメータからキャッシュキーを生成します。
        
        Args:
            url: 画像またはAPIのURL
            params: APIリクエストの追加パラメータ
            
        Returns:
            生成されたキャッシュキー（ハッシュ値）
        """
        # URLとパラメータを結合してハッシュ化
        key_data = url
        if params:
            key_data += json.dumps(params, sort_keys=True)
        
        return hashlib.md5(key_data.encode('utf-8')).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> str:
        """
        キャッシュキーからファイルパスを取得します。
        
        Args:
            cache_key: キャッシュキー
            
        Returns:
            キャッシュファイルのパス
        """
        return os.path.join(self.cache_dir, f"{cache_key}.json")
    
    def get(self, url: str, params: Optional[Dict] = None) -> Optional[Dict]:
        """
        キャッシュからデータを取得します。
        
        Args:
            url: 画像またはAPIのURL
            params: APIリクエストの追加パラメータ
            
        Returns:
            キャッシュされたデータ（存在しない場合はNone）
        """
        cache_key = self._get_cache_key(url, params)
        cache_path = self._get_cache_path(cache_key)
        
        # キャッシュファイルが存在するか確認
        if not os.path.exists(cache_path):
            return None
        
        try:
            # キャッシュファイルを読み込む
            with open(cache_path, 'r', encoding='utf-8') as f:
                cache_data = json.load(f)
            
            # キャッシュの有効期限をチェック
            timestamp = cache_data.get('timestamp', 0)
            if time.time() - timestamp > self.expiry_seconds:
                logger.info(f"キャッシュの有効期限が切れています: {url}")
                return None
            
            logger.info(f"キャッシュからデータを取得しました: {url}")
            return cache_data.get('data')
            
        except Exception as e:
            logger.warning(f"キャッシュの読み込みに失敗しました: {str(e)}")
            return None
    
    def set(self, url: str, data: Any, params: Optional[Dict] = None) -> None:
        """
        データをキャッシュに保存します。
        
        Args:
            url: 画像またはAPIのURL
            data: キャッシュするデータ
            params: APIリクエストの追加パラメータ
        """
        cache_key = self._get_cache_key(url, params)
        cache_path = self._get_cache_path(cache_key)
        
        try:
            # タイムスタンプを含めてデータを保存
            cache_data = {
                'timestamp': time.time(),
                'data': data
            }
            
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
                
            logger.info(f"データをキャッシュに保存しました: {url}")
            
        except Exception as e:
            logger.warning(f"キャッシュの保存に失敗しました: {str(e)}")
    
    def clear_expired(self) -> int:
        """
        期限切れのキャッシュファイルを削除します。
        
        Returns:
            削除されたファイルの数
        """
        count = 0
        current_time = time.time()
        
        for filename in os.listdir(self.cache_dir):
            if not filename.endswith('.json'):
                continue
                
            file_path = os.path.join(self.cache_dir, filename)
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                
                timestamp = cache_data.get('timestamp', 0)
                if current_time - timestamp > self.expiry_seconds:
                    os.remove(file_path)
                    count += 1
                    
            except Exception as e:
                logger.warning(f"キャッシュファイルの処理中にエラーが発生しました: {str(e)}")
        
        if count > 0:
            logger.info(f"{count}個の期限切れキャッシュファイルを削除しました")
            
        return count
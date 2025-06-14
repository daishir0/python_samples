"""
OpenAI Vision API サンプルプログラム - 画像プロセッサー
====================================================

このモジュールは、画像の処理と準備のための機能を提供します。
ローカルファイルやURLからの画像の読み込み、base64エンコードなどを行います。
"""

import os
import base64
import requests
import logging
from typing import Optional, Union, Dict, Any
from urllib.parse import urlparse

# ロガーの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class ImageProcessor:
    """画像処理のためのクラス"""
    
    def __init__(self, timeout: int = 10):
        """
        画像プロセッサーを初期化します。
        
        Args:
            timeout: 画像ダウンロード時のタイムアウト秒数
        """
        self.timeout = timeout
    
    def is_url(self, path: str) -> bool:
        """
        指定されたパスがURLかどうかを判定します。
        
        Args:
            path: 判定するパス
            
        Returns:
            URLの場合はTrue、そうでない場合はFalse
        """
        parsed = urlparse(path)
        return bool(parsed.scheme and parsed.netloc)
    
    def get_image_data(self, image_path: str) -> Optional[Dict[str, Any]]:
        """
        画像データを取得し、OpenAI Vision APIに適した形式に変換します。
        
        Args:
            image_path: 画像のパスまたはURL
            
        Returns:
            OpenAI Vision API用の画像データ辞書、エラー時はNone
        """
        try:
            if self.is_url(image_path):
                return {"type": "url", "url": image_path}
            else:
                # ローカルファイルの場合はbase64エンコード
                return {"type": "base64", "data": self.encode_image(image_path)}
        except Exception as e:
            logger.error(f"画像データの取得に失敗しました: {str(e)}")
            return None
    
    def encode_image(self, image_path: str) -> str:
        """
        ローカル画像ファイルをbase64エンコードします。
        
        Args:
            image_path: 画像ファイルのパス
            
        Returns:
            base64エンコードされた画像データ
            
        Raises:
            FileNotFoundError: 画像ファイルが見つからない場合
            Exception: その他のエラーが発生した場合
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"画像ファイルが見つかりません: {image_path}")
        
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def download_image(self, image_url: str, save_path: Optional[str] = None) -> Optional[bytes]:
        """
        URLから画像をダウンロードします。
        
        Args:
            image_url: 画像のURL
            save_path: 保存先のパス（指定しない場合は保存しない）
            
        Returns:
            ダウンロードした画像のバイナリデータ、エラー時はNone
        """
        try:
            response = requests.get(image_url, timeout=self.timeout)
            response.raise_for_status()  # エラーレスポンスの場合は例外を発生
            
            image_data = response.content
            
            # 保存先が指定されている場合は保存
            if save_path:
                os.makedirs(os.path.dirname(os.path.abspath(save_path)), exist_ok=True)
                with open(save_path, 'wb') as f:
                    f.write(image_data)
                logger.info(f"画像を保存しました: {save_path}")
            
            return image_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"画像のダウンロードに失敗しました: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"画像の処理中にエラーが発生しました: {str(e)}")
            return None
    
    def get_image_format(self, image_path: str) -> Optional[str]:
        """
        画像ファイルの形式を取得します。
        
        Args:
            image_path: 画像ファイルのパス
            
        Returns:
            画像形式（jpg, png, webp など）、不明な場合はNone
        """
        try:
            _, ext = os.path.splitext(image_path)
            if ext:
                return ext.lower()[1:]  # 先頭の'.'を除去
            return None
        except Exception:
            return None
"""
OpenAI Vision API サンプルプログラム - 設定管理
==============================================

このモジュールは、APIキーや他の設定パラメータを管理します。
環境変数、.envファイル、または設定ファイルから設定を読み込みます。
"""

import os
import yaml
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# ロガーの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class Config:
    """設定を管理するクラス"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        設定マネージャーを初期化します。
        
        Args:
            config_path: 設定ファイルのパス（省略可）
        """
        # .envファイルがあれば読み込む
        load_dotenv()
        
        # デフォルト設定
        self.default_config = {
            'openai': {
                'api_key': os.environ.get('OPENAI_API_KEY', ''),
                'model': 'gpt-4o-mini',
                'max_tokens': 1000,
                'temperature': 0.7,
                'timeout': 30,
                'retry_count': 3,
                'retry_delay': 2
            },
            'cache': {
                'enabled': True,
                'directory': 'cache',
                'expiry_days': 7
            },
            'logging': {
                'level': 'INFO',
                'file': None
            }
        }
        
        # 設定ファイルから読み込む
        self.config = self.load_config(config_path)
        
        # APIキーが設定されているか確認
        if not self.get('openai.api_key'):
            logger.warning("OpenAI APIキーが設定されていません。環境変数OPENAI_API_KEYまたは設定ファイルで指定してください。")
    
    def load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """
        設定ファイルを読み込みます。
        
        Args:
            config_path: 設定ファイルのパス
            
        Returns:
            読み込んだ設定（デフォルト設定とマージ済み）
        """
        config = self.default_config.copy()
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    file_config = yaml.safe_load(f)
                
                if file_config:
                    # 設定をマージ（ネストされた辞書も適切にマージ）
                    self._merge_config(config, file_config)
                    logger.info(f"設定ファイルを読み込みました: {config_path}")
            except Exception as e:
                logger.error(f"設定ファイルの読み込みに失敗しました: {str(e)}")
        else:
            if config_path:
                logger.warning(f"設定ファイル {config_path} が見つかりません。デフォルト設定を使用します。")
            else:
                logger.info("設定ファイルが指定されていません。デフォルト設定を使用します。")
        
        return config
    
    def _merge_config(self, target: Dict[str, Any], source: Dict[str, Any]) -> None:
        """
        設定を再帰的にマージします。
        
        Args:
            target: マージ先の辞書
            source: マージ元の辞書
        """
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                # 両方が辞書の場合は再帰的にマージ
                self._merge_config(target[key], value)
            else:
                # それ以外の場合は上書き
                target[key] = value
    
    def get(self, key_path: str, default: Any = None) -> Any:
        """
        ドット区切りのキーパスで設定値を取得します。
        
        Args:
            key_path: ドット区切りのキーパス（例: 'openai.api_key'）
            default: キーが存在しない場合のデフォルト値
            
        Returns:
            設定値、キーが存在しない場合はデフォルト値
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any) -> None:
        """
        ドット区切りのキーパスで設定値を設定します。
        
        Args:
            key_path: ドット区切りのキーパス（例: 'openai.api_key'）
            value: 設定する値
        """
        keys = key_path.split('.')
        target = self.config
        
        # 最後のキー以外をたどる
        for key in keys[:-1]:
            if key not in target or not isinstance(target[key], dict):
                target[key] = {}
            target = target[key]
        
        # 最後のキーに値を設定
        target[keys[-1]] = value
    
    def save(self, config_path: str) -> bool:
        """
        現在の設定をファイルに保存します。
        
        Args:
            config_path: 保存先のファイルパス
            
        Returns:
            保存に成功した場合はTrue、失敗した場合はFalse
        """
        try:
            # ディレクトリが存在しない場合は作成
            os.makedirs(os.path.dirname(os.path.abspath(config_path)), exist_ok=True)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)
            
            logger.info(f"設定をファイルに保存しました: {config_path}")
            return True
            
        except Exception as e:
            logger.error(f"設定の保存に失敗しました: {str(e)}")
            return False
    
    def to_dict(self) -> Dict[str, Any]:
        """
        現在の設定を辞書として取得します。
        
        Returns:
            設定の辞書
        """
        return self.config.copy()
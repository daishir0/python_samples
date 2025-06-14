"""
OpenAI 並行問い合わせサンプル - メインクラス
==================================================

このファイルは、OpenAIへの並行問い合わせを行うメインクラスを定義しています。
非同期処理とバッチ処理を使用して、複数の問い合わせを効率的に処理します。

主な機能:
-------
- 複数の問い合わせを並行処理
- バッチ処理による効率化
- キャッシュ機能によるパフォーマンス向上
- エラー時の自動リトライ
- 結果の集約と管理

使用方法:
-------
```python
from parallel_openai.parallel_client import ParallelOpenAIClient

# クライアントの初期化
client = ParallelOpenAIClient(
    config_path='config.yaml',  # 設定ファイルのパス
    use_cache=True,             # キャッシュを使用するかどうか
    batch_size=5                # バッチサイズ
)

# 単一の問い合わせ
response = client.query("What is the capital of Japan?")
print(response["content"])

# 複数の問い合わせ
queries = [
    "What is the capital of Japan?",
    "What is the capital of France?",
    "What is the capital of Germany?"
]
responses = client.query_batch(queries)
for query, response in zip(queries, responses):
    print(f"Query: {query}")
    print(f"Response: {response['content']}")

# 非同期での問い合わせ
import asyncio

async def main():
    response = await client.query_async("What is the capital of Japan?")
    print(response["content"])
    
    responses = await client.query_batch_async(queries)
    for query, response in zip(queries, responses):
        print(f"Query: {query}")
        print(f"Response: {response['content']}")

asyncio.run(main())
```
"""

import os
import yaml
import logging
import asyncio
from typing import List, Dict, Any, Optional, Union

# 内部モジュールのインポート
from utils.cache_manager import CacheManager
from utils.openai_client import OpenAIClient

# ロガーの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class ParallelOpenAIClient:
    def __init__(self, config_path: str = 'config.yaml', use_cache: bool = True, batch_size: Optional[int] = None):
        """初期化"""
        logger.info("ParallelOpenAIClientを初期化中...")
        self.config = self.load_config(config_path)
        self.use_cache = use_cache
        self.batch_size = batch_size or self.config.get('parallel', {}).get('batch_size', 5)
        
        # キャッシュマネージャーの初期化
        if self.use_cache:
            cache_dir = self.config.get('cache', {}).get('directory', 'cache')
            cache_expiry = self.config.get('cache', {}).get('expiry_days', 7)
            self.cache_manager = CacheManager(cache_dir, cache_expiry)
        else:
            self.cache_manager = None
        
        # OpenAIクライアントの初期化
        self.openai_client = OpenAIClient(
            api_key=self.config['openai']['api_key'],
            model=self.config['openai']['model'],
            max_retries=self.config.get('parallel', {}).get('max_retries', 3),
            retry_delay=self.config.get('parallel', {}).get('retry_delay', 1)
        )
        
        logger.info("初期化完了")
    
    def load_config(self, config_path: str) -> dict:
        """設定ファイルを読み込む"""
        logger.info(f"設定ファイルを読み込み中: {config_path}")
        
        # モジュールディレクトリを取得
        module_dir = os.path.dirname(os.path.abspath(__file__))
        
        # デフォルト設定
        default_config = {
            'openai': {
                'api_key': os.environ.get('OPENAI_API_KEY', ''),
                'model': 'gpt-4o-mini'
            },
            'parallel': {
                'batch_size': 5,
                'max_retries': 3,
                'retry_delay': 1
            },
            'cache': {
                'enabled': True,
                'directory': os.path.join(module_dir, 'cache'),
                'expiry_days': 7
            }
        }
        
        # 相対パスの場合、モジュールのディレクトリからの相対パスとして解釈
        if not os.path.isabs(config_path):
            module_config_path = os.path.join(module_dir, config_path)
            
            if os.path.exists(module_config_path):
                config_path = module_config_path
                logger.info(f"モジュールディレクトリ内の設定ファイルを使用: {config_path}")
        
        # 設定ファイルが存在する場合は読み込む
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    config = yaml.safe_load(f)
                logger.info("設定ファイルの読み込みが完了")
            except Exception as e:
                logger.warning(f"設定ファイルの読み込みに失敗しました: {str(e)}")
                logger.info("デフォルト設定を使用します")
                config = default_config
        else:
            logger.warning(f"設定ファイル {config_path} が見つかりません")
            logger.info("デフォルト設定を使用します")
            config = default_config
        
        # 環境変数からAPIキーを取得（設定ファイルよりも優先）
        if 'OPENAI_API_KEY' in os.environ:
            config.setdefault('openai', {})['api_key'] = os.environ['OPENAI_API_KEY']
        
        # 必須設定の確認
        if not config.get('openai', {}).get('api_key'):
            logger.warning("OpenAI APIキーが設定されていません。環境変数OPENAI_API_KEYを設定するか、設定ファイルで指定してください。")
        
        return config
    
    async def query_async(self, 
                         query: Union[str, Dict], 
                         model: Optional[str] = None,
                         temperature: float = 0.7,
                         max_tokens: Optional[int] = None) -> Dict:
        """単一の問い合わせを非同期で実行"""
        return await self.openai_client.query_async(
            query, 
            self.cache_manager, 
            model, 
            temperature, 
            max_tokens
        )
    
    def query(self, 
             query: Union[str, Dict], 
             model: Optional[str] = None,
             temperature: float = 0.7,
             max_tokens: Optional[int] = None) -> Dict:
        """単一の問い合わせを実行（同期版）"""
        return asyncio.run(self.query_async(query, model, temperature, max_tokens))
    
    async def query_batch_async(self, 
                               queries: List[Union[str, Dict]], 
                               model: Optional[str] = None,
                               temperature: float = 0.7,
                               max_tokens: Optional[int] = None) -> List[Dict]:
        """複数の問い合わせを非同期でバッチ処理"""
        return await self.openai_client.query_batch_async(
            queries, 
            self.cache_manager, 
            self.batch_size, 
            model, 
            temperature, 
            max_tokens
        )
    
    def query_batch(self, 
                   queries: List[Union[str, Dict]], 
                   model: Optional[str] = None,
                   temperature: float = 0.7,
                   max_tokens: Optional[int] = None) -> List[Dict]:
        """複数の問い合わせをバッチ処理（同期版）"""
        return asyncio.run(self.query_batch_async(queries, model, temperature, max_tokens))
    
    def clear_cache(self, query=None):
        """キャッシュをクリア"""
        if self.cache_manager:
            self.cache_manager.clear_cache(query)
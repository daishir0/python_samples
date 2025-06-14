"""
OpenAI 並行問い合わせサンプル - OpenAIクライアントモジュール
==================================================

このモジュールは、OpenAI APIを使用して問い合わせを行うための機能を提供します。
非同期処理とリトライ機能を使用して、安定した問い合わせを実現します。

主な機能:
-------
- OpenAI APIを使用した問い合わせ
- 非同期処理による並列実行
- エラー時の自動リトライ
- キャッシュ機能によるパフォーマンス向上

使用方法:
-------
```python
from parallel_openai.utils.openai_client import OpenAIClient
from parallel_openai.utils.cache_manager import CacheManager

# キャッシュマネージャーの初期化
cache_manager = CacheManager()

# OpenAIクライアントの初期化
client = OpenAIClient(
    api_key='your_openai_api_key',
    model='gpt-4o-mini',
    max_retries=3
)

# 単一の問い合わせ（非同期）
response = await client.query_async(
    "What is the capital of Japan?",
    cache_manager=cache_manager
)

# 複数の問い合わせをバッチ処理（非同期）
queries = [
    "What is the capital of Japan?",
    "What is the capital of France?",
    "What is the capital of Germany?"
]
responses = await client.query_batch_async(queries, cache_manager=cache_manager)
```
"""

import json
import logging
import asyncio
import time
from typing import Dict, List, Any, Optional, Union
from openai import AsyncOpenAI, OpenAI
from openai.types.chat import ChatCompletion

# ロガーの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self, api_key: str, model: str = "gpt-4o-mini", max_retries: int = 3, retry_delay: int = 1):
        """OpenAIクライアントの初期化"""
        self.async_client = AsyncOpenAI(api_key=api_key)
        self.sync_client = OpenAI(api_key=api_key)
        self.model = model
        self.max_retries = max_retries
        self.retry_delay = retry_delay
    
    async def query_async(self, 
                         query: Union[str, Dict], 
                         cache_manager=None, 
                         model: Optional[str] = None,
                         temperature: float = 0.7,
                         max_tokens: Optional[int] = None) -> Dict:
        """OpenAI APIに非同期で問い合わせ（キャッシュ対応）"""
        # キャッシュが有効で、問い合わせ結果がキャッシュされている場合
        if cache_manager and cache_manager.is_response_cached(query):
            logger.info(f"キャッシュから応答を使用: {query if isinstance(query, str) else '(複合クエリ)'}")
            cached_response = cache_manager.get_response(query)
            if cached_response:
                return cached_response
        
        # クエリの種類に応じてメッセージを構築
        if isinstance(query, str):
            messages = [{"role": "user", "content": query}]
        elif isinstance(query, dict):
            if "messages" in query:
                messages = query["messages"]
            else:
                messages = [query]
        else:
            error_msg = f"サポートされていないクエリ形式: {type(query)}"
            logger.error(error_msg)
            return self._create_error_response(error_msg)
        
        # 使用するモデルを決定
        use_model = model if model else self.model
        
        logger.info(f"OpenAI APIに問い合わせ中: {query if isinstance(query, str) else '(複合クエリ)'}")
        
        for retry in range(self.max_retries):
            try:
                if retry > 0:
                    logger.info(f"リトライ {retry}/{self.max_retries-1}: {query if isinstance(query, str) else '(複合クエリ)'}")
                    # リトライ前に少し待機
                    await asyncio.sleep(self.retry_delay * retry)
                
                # APIリクエストのパラメータを構築
                request_params = {
                    "model": use_model,
                    "messages": messages,
                    "temperature": temperature,
                }
                
                if max_tokens:
                    request_params["max_tokens"] = max_tokens
                
                # APIリクエストを実行
                response = await self.async_client.chat.completions.create(**request_params)
                
                # レスポンスを整形
                result = self._format_response(response)
                
                logger.info(f"問い合わせが完了しました: {query if isinstance(query, str) else '(複合クエリ)'}")
                
                # キャッシュが有効な場合は応答をキャッシュ
                if cache_manager:
                    cache_manager.cache_response(query, result)
                    
                return result
                
            except Exception as e:
                if retry < self.max_retries - 1:
                    logger.warning(f"API呼び出しエラー、リトライします: {str(e)}")
                    continue
                else:
                    logger.error(f"問い合わせ中にエラーが発生: {str(e)}")
                    return self._create_error_response(f"API呼び出しエラー: {str(e)}")
        
        # すべてのリトライが失敗した場合
        return self._create_error_response("最大リトライ回数を超えました")
    
    def query(self, 
             query: Union[str, Dict], 
             cache_manager=None, 
             model: Optional[str] = None,
             temperature: float = 0.7,
             max_tokens: Optional[int] = None) -> Dict:
        """同期版の問い合わせメソッド"""
        return asyncio.run(self.query_async(query, cache_manager, model, temperature, max_tokens))
    
    async def query_batch_async(self, 
                               queries: List[Union[str, Dict]], 
                               cache_manager=None, 
                               batch_size: int = 5,
                               model: Optional[str] = None,
                               temperature: float = 0.7,
                               max_tokens: Optional[int] = None) -> List[Dict]:
        """複数の問い合わせを非同期でバッチ処理"""
        results = []
        total = len(queries)
        
        # バッチ処理
        for i in range(0, total, batch_size):
            batch = queries[i:i+batch_size]
            batch_tasks = []
            
            logger.info(f"バッチ処理開始: {i+1}～{min(i+batch_size, total)}/{total}")
            
            # 各問い合わせの処理タスクを作成
            for query in batch:
                task = self.query_async(query, cache_manager, model, temperature, max_tokens)
                batch_tasks.append(task)
            
            # バッチ内のタスクを並列実行
            batch_results = await asyncio.gather(*batch_tasks)
            
            # 結果を追加
            results.extend(batch_results)
            
            logger.info(f"バッチ処理完了: {i+1}～{min(i+batch_size, total)}/{total}")
        
        return results
    
    def query_batch(self, 
                   queries: List[Union[str, Dict]], 
                   cache_manager=None, 
                   batch_size: int = 5,
                   model: Optional[str] = None,
                   temperature: float = 0.7,
                   max_tokens: Optional[int] = None) -> List[Dict]:
        """同期版のバッチ処理メソッド"""
        return asyncio.run(self.query_batch_async(queries, cache_manager, batch_size, model, temperature, max_tokens))
    
    def _format_response(self, response: ChatCompletion) -> Dict:
        """APIレスポンスを整形"""
        try:
            return {
                "content": response.choices[0].message.content,
                "model": response.model,
                "id": response.id,
                "created": response.created,
                "finish_reason": response.choices[0].finish_reason,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens
                }
            }
        except Exception as e:
            logger.error(f"レスポンスの整形中にエラーが発生: {str(e)}")
            return self._create_error_response(f"レスポンス整形エラー: {str(e)}")
    
    def _create_error_response(self, error_message: str) -> Dict:
        """エラーレスポンスを生成"""
        return {
            "error": error_message,
            "content": None,
            "model": self.model,
            "id": None,
            "created": int(time.time()),
            "finish_reason": "error",
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }
        }
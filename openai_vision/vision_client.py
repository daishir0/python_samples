"""
OpenAI Vision API サンプルプログラム - Vision APIクライアント
==========================================================

このモジュールは、OpenAI Vision APIとの通信を担当します。
画像分析のリクエスト送信、レスポンス処理、エラーハンドリングを行います。
"""

import time
import json
import logging
import asyncio
from typing import Dict, List, Any, Optional, Union, Tuple

import openai
from openai import OpenAI, AsyncOpenAI
from openai.types.chat import ChatCompletion

from utils.cache_manager import CacheManager
from utils.image_processor import ImageProcessor

# ロガーの設定
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class VisionClient:
    """OpenAI Vision APIクライアント"""
    
    def __init__(
        self, 
        api_key: str, 
        model: str = "gpt-4o-mini",
        max_tokens: int = 1000,
        temperature: float = 0.7,
        timeout: int = 30,
        retry_count: int = 3,
        retry_delay: int = 2,
        cache_manager: Optional[CacheManager] = None
    ):
        """
        Vision APIクライアントを初期化します。
        
        Args:
            api_key: OpenAI APIキー
            model: 使用するモデル名
            max_tokens: 生成する最大トークン数
            temperature: 生成の多様性（0.0～2.0）
            timeout: APIリクエストのタイムアウト秒数
            retry_count: エラー時の再試行回数
            retry_delay: 再試行間の待機秒数
            cache_manager: キャッシュマネージャー（省略可）
        """
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.timeout = timeout
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.cache_manager = cache_manager
        
        # OpenAIクライアントの初期化
        self.client = OpenAI(api_key=api_key, timeout=timeout)
        self.async_client = AsyncOpenAI(api_key=api_key, timeout=timeout)
        
        # 画像プロセッサーの初期化
        self.image_processor = ImageProcessor(timeout=timeout)
        
        logger.info(f"Vision APIクライアントを初期化しました（モデル: {model}）")
    
    def analyze_image(
        self, 
        image_path: str, 
        prompt: str,
        output_format: Optional[str] = None,
        additional_instructions: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        画像を分析します（同期版）。
        
        Args:
            image_path: 画像のパスまたはURL
            prompt: 分析のためのプロンプト
            output_format: 出力形式（json, markdown, textなど）
            additional_instructions: 追加の指示
            
        Returns:
            分析結果の辞書
        """
        try:
            # キャッシュをチェック
            if self.cache_manager:
                cache_params = {
                    "prompt": prompt,
                    "model": self.model,
                    "output_format": output_format,
                    "additional_instructions": additional_instructions
                }
                cached_result = self.cache_manager.get(image_path, cache_params)
                if cached_result:
                    logger.info(f"キャッシュから結果を取得しました: {image_path}")
                    return cached_result
            
            # 画像データを取得
            image_data = self.image_processor.get_image_data(image_path)
            if not image_data:
                return {"error": f"画像データの取得に失敗しました: {image_path}"}
            
            # プロンプトを構築
            messages = self._build_messages(prompt, image_data, output_format, additional_instructions)
            
            # APIリクエストを送信（再試行あり）
            for attempt in range(self.retry_count + 1):
                try:
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        max_tokens=self.max_tokens,
                        temperature=self.temperature
                    )
                    
                    # レスポンスを処理
                    result = self._process_response(response)
                    
                    # 結果をキャッシュに保存
                    if self.cache_manager:
                        self.cache_manager.set(image_path, result, cache_params)
                    
                    return result
                    
                except Exception as e:
                    if attempt < self.retry_count:
                        wait_time = self.retry_delay * (2 ** attempt)  # 指数バックオフ
                        logger.warning(f"APIリクエストに失敗しました（{attempt+1}/{self.retry_count+1}）: {str(e)}")
                        logger.info(f"{wait_time}秒後に再試行します...")
                        time.sleep(wait_time)
                    else:
                        logger.error(f"APIリクエストが{self.retry_count+1}回失敗しました: {str(e)}")
                        return {"error": f"APIリクエストに失敗しました: {str(e)}"}
                        
        except Exception as e:
            logger.error(f"画像分析中にエラーが発生しました: {str(e)}")
            return {"error": f"画像分析中にエラーが発生しました: {str(e)}"}
    
    async def analyze_image_async(
        self, 
        image_path: str, 
        prompt: str,
        output_format: Optional[str] = None,
        additional_instructions: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        画像を分析します（非同期版）。
        
        Args:
            image_path: 画像のパスまたはURL
            prompt: 分析のためのプロンプト
            output_format: 出力形式（json, markdown, textなど）
            additional_instructions: 追加の指示
            
        Returns:
            分析結果の辞書
        """
        try:
            # キャッシュをチェック
            if self.cache_manager:
                cache_params = {
                    "prompt": prompt,
                    "model": self.model,
                    "output_format": output_format,
                    "additional_instructions": additional_instructions
                }
                cached_result = self.cache_manager.get(image_path, cache_params)
                if cached_result:
                    logger.info(f"キャッシュから結果を取得しました: {image_path}")
                    return cached_result
            
            # 画像データを取得
            image_data = self.image_processor.get_image_data(image_path)
            if not image_data:
                return {"error": f"画像データの取得に失敗しました: {image_path}"}
            
            # プロンプトを構築
            messages = self._build_messages(prompt, image_data, output_format, additional_instructions)
            
            # APIリクエストを送信（再試行あり）
            for attempt in range(self.retry_count + 1):
                try:
                    response = await self.async_client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        max_tokens=self.max_tokens,
                        temperature=self.temperature
                    )
                    
                    # レスポンスを処理
                    result = self._process_response(response)
                    
                    # 結果をキャッシュに保存
                    if self.cache_manager:
                        self.cache_manager.set(image_path, result, cache_params)
                    
                    return result
                    
                except Exception as e:
                    if attempt < self.retry_count:
                        wait_time = self.retry_delay * (2 ** attempt)  # 指数バックオフ
                        logger.warning(f"APIリクエストに失敗しました（{attempt+1}/{self.retry_count+1}）: {str(e)}")
                        logger.info(f"{wait_time}秒後に再試行します...")
                        await asyncio.sleep(wait_time)
                    else:
                        logger.error(f"APIリクエストが{self.retry_count+1}回失敗しました: {str(e)}")
                        return {"error": f"APIリクエストに失敗しました: {str(e)}"}
                        
        except Exception as e:
            logger.error(f"画像分析中にエラーが発生しました: {str(e)}")
            return {"error": f"画像分析中にエラーが発生しました: {str(e)}"}
    
    def _build_messages(
        self, 
        prompt: str, 
        image_data: Dict[str, Any],
        output_format: Optional[str] = None,
        additional_instructions: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        APIリクエスト用のメッセージを構築します。
        
        Args:
            prompt: 分析のためのプロンプト
            image_data: 画像データ（URLまたはbase64）
            output_format: 出力形式
            additional_instructions: 追加の指示
            
        Returns:
            メッセージのリスト
        """
        # システムメッセージを構築
        system_message = "あなたは画像分析の専門家です。提供された画像を詳細に分析し、質問に答えてください。"
        
        if output_format:
            if output_format.lower() == "json":
                system_message += " 回答はJSON形式で提供してください。"
            elif output_format.lower() == "markdown":
                system_message += " 回答はMarkdown形式で提供してください。"
        
        if additional_instructions:
            system_message += f" {additional_instructions}"
        
        # メッセージリストを構築
        messages = [
            {"role": "system", "content": system_message},
            {
                "role": "user", 
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": image_data}
                ]
            }
        ]
        
        return messages
    
    def _process_response(self, response: ChatCompletion) -> Dict[str, Any]:
        """
        APIレスポンスを処理します。
        
        Args:
            response: OpenAI APIからのレスポンス
            
        Returns:
            処理された結果の辞書
        """
        try:
            content = response.choices[0].message.content
            
            # JSONレスポンスの場合はパース
            try:
                if content.strip().startswith('{') and content.strip().endswith('}'):
                    return json.loads(content)
            except json.JSONDecodeError:
                pass
            
            # 通常のテキストレスポンス
            return {"content": content}
            
        except Exception as e:
            logger.error(f"レスポンスの処理中にエラーが発生しました: {str(e)}")
            return {"error": f"レスポンスの処理中にエラーが発生しました: {str(e)}"}
    
    async def analyze_multiple_images_async(
        self, 
        image_paths: List[str], 
        prompt: str,
        output_format: Optional[str] = None,
        additional_instructions: Optional[str] = None,
        batch_size: int = 5
    ) -> List[Dict[str, Any]]:
        """
        複数の画像を非同期で分析します。
        
        Args:
            image_paths: 画像のパスまたはURLのリスト
            prompt: 分析のためのプロンプト
            output_format: 出力形式
            additional_instructions: 追加の指示
            batch_size: 同時に処理するバッチサイズ
            
        Returns:
            分析結果の辞書のリスト
        """
        results = []
        
        # バッチ処理
        for i in range(0, len(image_paths), batch_size):
            batch = image_paths[i:i+batch_size]
            batch_tasks = []
            
            logger.info(f"バッチ処理開始: {i+1}～{min(i+batch_size, len(image_paths))}/{len(image_paths)}")
            
            # 各画像の処理タスクを作成
            for image_path in batch:
                task = self.analyze_image_async(
                    image_path, 
                    prompt, 
                    output_format, 
                    additional_instructions
                )
                batch_tasks.append(task)
            
            # バッチ内のタスクを並列実行
            batch_results = await asyncio.gather(*batch_tasks)
            results.extend(batch_results)
            
            logger.info(f"バッチ処理完了: {i+1}～{min(i+batch_size, len(image_paths))}/{len(image_paths)}")
        
        return results
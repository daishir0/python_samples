#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Claudeクライアント

Anthropic APIを使用してClaudeに問い合わせを行うクライアントクラス
"""

import time
import json
import logging
from typing import Dict, List, Optional, Union, Any

import anthropic
from anthropic.types import MessageParam
from anthropic.types.message import Message
from anthropic.types.message_create_params import MessageCreateParams

from config import ANTHROPIC_API_KEY, DEFAULT_MODEL, MAX_RETRIES, RETRY_DELAY, DEBUG

# ロガーの設定
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ClaudeClient:
    """
    Claudeクライアントクラス
    
    Anthropic APIを使用してClaudeに問い合わせを行うクライアントクラス
    エラー時の再問合せ機能を実装
    """
    
    def __init__(
        self, 
        api_key: Optional[str] = None, 
        model: Optional[str] = None,
        max_retries: int = MAX_RETRIES,
        retry_delay: int = RETRY_DELAY
    ):
        """
        初期化
        
        Args:
            api_key: Anthropic APIキー（Noneの場合はconfig.pyから読み込む）
            model: 使用するモデル（Noneの場合はconfig.pyから読み込む）
            max_retries: 最大リトライ回数
            retry_delay: リトライ間隔（秒）
        """
        self.api_key = api_key or ANTHROPIC_API_KEY
        if not self.api_key:
            raise ValueError("APIキーが設定されていません。環境変数ANTHROPIC_API_KEYを設定するか、初期化時にapi_keyを指定してください。")
        
        self.model = model or DEFAULT_MODEL
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Anthropicクライアントの初期化
        self.client = anthropic.Anthropic(api_key=self.api_key)
        
        logger.debug(f"ClaudeClientを初期化しました。モデル: {self.model}")
    
    def ask(
        self, 
        prompt: str, 
        system: Optional[str] = None,
        max_tokens: int = 4000,
        temperature: float = 0.7,
        messages: Optional[List[Dict[str, str]]] = None,
        **kwargs
    ) -> Message:
        """
        Claudeに問い合わせを行う
        
        Args:
            prompt: プロンプト
            system: システムプロンプト
            max_tokens: 最大トークン数
            temperature: 温度
            messages: メッセージ履歴（指定した場合はpromptは無視される）
            **kwargs: その他のパラメータ
            
        Returns:
            Message: レスポンス
        """
        retry_count = 0
        last_error = None
        
        # メッセージの準備
        if messages is None:
            messages = [{"role": "user", "content": prompt}]
        
        while retry_count <= self.max_retries:
            try:
                logger.debug(f"Claudeに問い合わせを行います。リトライ回数: {retry_count}")
                
                # パラメータの準備
                params: MessageCreateParams = {
                    "model": self.model,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "messages": messages,
                }
                
                # システムプロンプトが指定されている場合は追加
                if system:
                    params["system"] = system
                
                # その他のパラメータを追加
                for key, value in kwargs.items():
                    params[key] = value
                
                # 問い合わせを実行
                response = self.client.messages.create(**params)
                
                logger.debug("問い合わせが成功しました。")
                return response
                
            except anthropic.APIError as e:
                # APIエラーの場合
                logger.warning(f"APIエラーが発生しました: {e}")
                last_error = e
                
                # レート制限エラーの場合は少し長めに待機
                if e.status_code == 429:
                    wait_time = self.retry_delay * (2 ** retry_count)
                    logger.info(f"レート制限に達しました。{wait_time}秒待機します。")
                    time.sleep(wait_time)
                else:
                    time.sleep(self.retry_delay)
                
            except anthropic.APIConnectionError as e:
                # 接続エラーの場合
                logger.warning(f"接続エラーが発生しました: {e}")
                last_error = e
                time.sleep(self.retry_delay)
                
            except Exception as e:
                # その他のエラーの場合
                logger.error(f"予期しないエラーが発生しました: {e}")
                last_error = e
                time.sleep(self.retry_delay)
            
            retry_count += 1
        
        # 最大リトライ回数を超えた場合
        logger.error(f"最大リトライ回数（{self.max_retries}回）を超えました。")
        if last_error:
            raise last_error
        else:
            raise Exception("不明なエラーが発生しました。")
    
    def extract_text(self, response: Message) -> str:
        """
        レスポンスからテキストを抽出する
        
        Args:
            response: レスポンス
            
        Returns:
            str: 抽出されたテキスト
        """
        if not response or not response.content:
            return ""
        
        # テキストを抽出
        text_parts = []
        for content in response.content:
            if content.type == "text":
                text_parts.append(content.text)
        
        return "".join(text_parts)
    
    def extract_json(self, response: Message) -> Dict[str, Any]:
        """
        レスポンスからJSONを抽出する
        
        Args:
            response: レスポンス
            
        Returns:
            Dict[str, Any]: 抽出されたJSON
        """
        text = self.extract_text(response)
        
        # JSONを抽出
        try:
            # JSONブロックを探す
            json_start = text.find("{")
            json_end = text.rfind("}") + 1
            
            if json_start >= 0 and json_end > json_start:
                json_str = text[json_start:json_end]
                return json.loads(json_str)
            else:
                logger.warning("JSONが見つかりませんでした。")
                return {}
                
        except json.JSONDecodeError as e:
            logger.error(f"JSONのデコードに失敗しました: {e}")
            return {}
        except Exception as e:
            logger.error(f"JSONの抽出中に予期しないエラーが発生しました: {e}")
            return {}
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WordPress投稿モジュール

WordPress REST APIを使用して記事を投稿する機能を提供します。
"""

import logging
import requests
import time
from requests.auth import HTTPBasicAuth
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class WordPressPoster:
    """WordPress投稿クラス"""
    
    def __init__(self, config: Dict[str, Any]):
        """
        初期化
        
        Args:
            config: 設定データ
        """
        self.config = config
        self.wp_config = config['wordpress']
        
        # WordPress設定
        self.site_url = self.wp_config['site_url'].rstrip('/')
        self.username = self.wp_config['username']
        self.app_password = self.wp_config['app_password']
        self.default_category_id = self.wp_config['default_category_id']
        
        # API エンドポイント
        self.api_base = f"{self.site_url}/wp-json/wp/v2"
        self.posts_endpoint = f"{self.api_base}/posts"
        self.media_endpoint = f"{self.api_base}/media"
        
        # 認証設定
        self.auth = HTTPBasicAuth(self.username, self.app_password)
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # デバッグ設定
        self.debug_enabled = config['debug']['enabled']
        
        logger.info(f"WordPress投稿器を初期化: {self.site_url}")
    
    def test_connection(self) -> bool:
        """
        WordPress接続をテストする
        
        Returns:
            接続成功の真偽値
        """
        logger.info("WordPress接続をテスト中...")
        
        try:
            response = requests.get(
                self.api_base,
                auth=self.auth,
                headers={'Accept': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                logger.info("WordPress接続テスト成功")
                return True
            else:
                logger.error(f"WordPress接続テスト失敗: {response.status_code}")
                logger.error(f"レスポンス: {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            logger.error(f"WordPress接続エラー: {e}")
            return False
    
    def post_article(self, article: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        記事をWordPressに投稿する
        
        Args:
            article: 記事データ
            
        Returns:
            投稿結果、失敗時はNone
        """
        logger.info(f"記事を投稿中: {article['title']}")
        
        try:
            # 投稿データを準備
            post_data = self._prepare_post_data(article)
            
            if self.debug_enabled:
                logger.debug(f"投稿データ: {post_data}")
            
            # 記事を投稿
            response = requests.post(
                self.posts_endpoint,
                auth=self.auth,
                headers=self.headers,
                json=post_data,
                timeout=60
            )
            
            if response.status_code == 201:
                result = response.json()
                logger.info(f"投稿成功: ID={result['id']}, URL={result['link']}")
                return result
            else:
                logger.error(f"投稿失敗: {response.status_code}")
                logger.error(f"レスポンス: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"投稿エラー: {e}")
            return None
        except Exception as e:
            logger.error(f"予期しないエラー: {e}")
            return None
    
    def _prepare_post_data(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """
        投稿用データを準備する
        
        Args:
            article: 記事データ
            
        Returns:
            WordPress投稿用データ
        """
        # スラッグを生成
        slug = self._generate_slug(article['title'])
        
        # カテゴリIDを決定
        category_ids = [article.get('category_id', self.default_category_id)]
        
        # タグを生成
        tags = article.get('tags', [])
        if 'tags' not in article and 'default_tags' in self.config.get('tags', {}):
            tags = self.config['tags']['default_tags']
        
        post_data = {
            'title': article['title'],
            'content': article['content'],
            'status': article.get('status', 'publish'),
            'slug': slug,
            'categories': category_ids,
            'tags': tags
        }
        
        # メタ説明がある場合
        if article.get('excerpt'):
            post_data['excerpt'] = article['excerpt']
        
        return post_data
    
    def _generate_slug(self, title: str) -> str:
        """
        タイトルからスラッグを生成する
        
        Args:
            title: 記事タイトル
            
        Returns:
            URL用スラッグ
        """
        # 日本語文字を除去し、英数字とハイフンのみにする
        slug = title.lower()
        
        # 特殊文字を除去
        import re
        slug = re.sub(r'[^\w\s-]', '', slug)
        slug = re.sub(r'[-\s]+', '-', slug)
        slug = slug.strip('-')
        
        # 長すぎる場合は切り詰める
        if len(slug) > 50:
            slug = slug[:50].rstrip('-')
        
        # 空の場合はデフォルト値
        if not slug:
            slug = f"wordpress-article-{int(time.time())}"
        
        return slug
    
    def get_article(self, post_id: int) -> Optional[Dict[str, Any]]:
        """
        記事を取得する
        
        Args:
            post_id: 投稿ID
            
        Returns:
            記事データ、失敗時はNone
        """
        try:
            response = requests.get(
                f"{self.posts_endpoint}/{post_id}",
                auth=self.auth,
                headers={'Accept': 'application/json'},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"記事取得失敗: {response.status_code}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"記事取得エラー: {e}")
            return None
    
    def list_articles(self, per_page: int = 10, page: int = 1) -> List[Dict[str, Any]]:
        """
        記事一覧を取得する
        
        Args:
            per_page: 1ページあたりの記事数
            page: ページ番号
            
        Returns:
            記事一覧
        """
        try:
            params = {
                'per_page': per_page,
                'page': page,
                'status': 'publish'
            }
            
            response = requests.get(
                self.posts_endpoint,
                auth=self.auth,
                headers={'Accept': 'application/json'},
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"記事一覧取得失敗: {response.status_code}")
                return []
                
        except requests.exceptions.RequestException as e:
            logger.error(f"記事一覧取得エラー: {e}")
            return []

def test_wordpress_connection(config: Dict[str, Any]) -> bool:
    """
    WordPress接続をテストする便利関数
    
    Args:
        config: 設定データ
        
    Returns:
        接続成功の真偽値
    """
    poster = WordPressPoster(config)
    return poster.test_connection()

if __name__ == "__main__":
    # テスト用
    import config as cfg
    
    # 設定を読み込む
    config = cfg.load_config()
    
    if not cfg.validate_config(config):
        print("設定が不完全です。環境変数を確認してください。")
        cfg.print_env_help()
        exit(1)
    
    # 接続テスト
    if test_wordpress_connection(config):
        print("WordPress接続テスト成功")
    else:
        print("WordPress接続テスト失敗")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
WordPress投稿モジュール

WordPress REST APIを使用して記事を投稿する機能を提供します。
"""

import logging
import requests
import time
import re
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
        
        # Markdownリンクを自動でHTMLに変換
        content_html = self._convert_markdown_links_to_html(article['content'])
        
        post_data = {
            'title': article['title'],
            'content': content_html,
            'status': article.get('status', 'publish'),
            'slug': slug,
            'categories': category_ids
        }
        
        # タグが文字列の場合は除外（WordPressはタグIDを期待するため）
        if tags and all(isinstance(tag, int) for tag in tags):
            post_data['tags'] = tags
        
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
    
    def update_article(self, post_id: int, article: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        既存記事を更新する
        
        Args:
            post_id: 投稿ID
            article: 更新する記事データ
            
        Returns:
            更新結果、失敗時はNone
        """
        logger.info(f"記事を更新中: ID={post_id}, タイトル={article.get('title', '(タイトル未指定)')}")
        
        try:
            # 更新データを準備
            update_data = self._prepare_post_data(article)
            
            if self.debug_enabled:
                logger.debug(f"更新データ: {update_data}")
            
            # 記事を更新
            response = requests.post(
                f"{self.posts_endpoint}/{post_id}",
                auth=self.auth,
                headers=self.headers,
                json=update_data,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                logger.info(f"更新成功: ID={result['id']}, URL={result['link']}")
                return result
            else:
                logger.error(f"更新失敗: {response.status_code}")
                logger.error(f"レスポンス: {response.text}")
                return None
                
        except requests.exceptions.RequestException as e:
            logger.error(f"更新エラー: {e}")
            return None
        except Exception as e:
            logger.error(f"予期しないエラー: {e}")
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
    
    def get_latest_articles(self, count: int = 5) -> List[Dict[str, Any]]:
        """
        最新の記事一覧をIDと共に取得する
        
        Args:
            count: 取得する記事数
            
        Returns:
            最新記事一覧（ID、タイトル、日付等を含む）
        """
        logger.info(f"最新の記事{count}件を取得中...")
        
        try:
            params = {
                'per_page': count,
                'orderby': 'date',
                'order': 'desc',
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
                articles = response.json()
                result = []
                for article in articles:
                    result.append({
                        'id': article['id'],
                        'title': article['title']['rendered'],
                        'date': article['date'],
                        'link': article['link'],
                        'status': article['status']
                    })
                logger.info(f"最新記事{len(result)}件を取得成功")
                return result
            else:
                logger.error(f"最新記事取得失敗: {response.status_code}")
                return []
                
        except requests.exceptions.RequestException as e:
            logger.error(f"最新記事取得エラー: {e}")
            return []
    
    def search_articles(self, search_term: str, count: int = 10) -> List[Dict[str, Any]]:
        """
        キーワードで記事を検索する
        
        Args:
            search_term: 検索キーワード
            count: 取得する記事数の上限
            
        Returns:
            検索にマッチした記事一覧（ID、タイトル、日付等を含む）
        """
        logger.info(f"キーワード '{search_term}' で記事を検索中...")
        
        try:
            params = {
                'search': search_term,
                'per_page': count,
                'orderby': 'relevance',
                'order': 'desc'
            }
            
            response = requests.get(
                self.posts_endpoint,
                auth=self.auth,
                headers={'Accept': 'application/json'},
                params=params,
                timeout=30
            )
            
            if response.status_code == 200:
                articles = response.json()
                result = []
                for article in articles:
                    result.append({
                        'id': article['id'],
                        'title': article['title']['rendered'],
                        'date': article['date'],
                        'link': article['link'],
                        'status': article['status'],
                        'excerpt': article['excerpt']['rendered'][:100] + '...' if article['excerpt']['rendered'] else ''
                    })
                logger.info(f"検索結果{len(result)}件を取得成功")
                return result
            else:
                logger.error(f"記事検索失敗: {response.status_code}")
                return []
                
        except requests.exceptions.RequestException as e:
            logger.error(f"記事検索エラー: {e}")
            return []
    
    def _convert_markdown_links_to_html(self, content: str) -> str:
        """
        MarkdownのリンクをHTMLのaタグに変換する（リンクのみ）
        
        Args:
            content: Markdown形式のコンテンツ
            
        Returns:
            リンクのみHTMLに変換されたコンテンツ
        """
        # [テキスト](URL) → <a href="URL">テキスト</a> に変換
        def replace_link(match):
            text = match.group(1)
            url = match.group(2)
            return f'<a href="{url}" target="_blank">{text}</a>'
        
        # Markdownリンクパターンをマッチして変換
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        content = re.sub(link_pattern, replace_link, content)
        
        logger.info("Markdownリンクのみをaタグに変換完了")
        return content

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
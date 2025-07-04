#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Google検索ツール (google_search)

このプログラムはGoogle Custom Search APIを使用して検索を実行し、
検索結果のURLをテキストファイルに保存します。

使い方:
    基本:
        python main.py "検索クエリ"
    
    オプション:
        --config: 設定ファイルのパス
                 デフォルト: config.yaml
        
        --num: 取得する結果の数（最大100）
               デフォルト: config.yamlで指定された値または100
               注意: Google Custom Search APIの制限により、実際には最大100件までしか取得できません

例:
    基本的な使用例:
        python main.py "人工知能"
        python main.py "機械学習" --num 50
        python main.py "ディープラーニング" --config custom_config.yaml
    
    特殊な検索クエリの例:
        # 特定のサイト内検索（site:構文）
        python main.py "site:www.asahi.com 103万円の壁"
        
        # 複数の検索条件を組み合わせる場合
        python main.py "site:www.nikkei.com (AI OR 人工知能) -コロナ"
        
        # 特殊文字を含む検索の場合はシングルクォートで囲む
        python main.py 'site:example.com "完全一致フレーズ"'
        
    注意:
        * 検索クエリに特殊文字やスペースが含まれる場合は、必ずクォーテーション（" "または' '）で囲んでください
        * シェルによる特殊文字の解釈を避けるため、特に複雑な検索クエリではシングルクォート（' '）の使用を推奨します
        * 検索クエリ内でダブルクォート（"）を使用する場合は、外側をシングルクォート（'）で囲むと良いでしょう
        * Google Custom Search APIの制限により、最大100件までしか検索結果を取得できません
"""

import sys
import datetime
import json
import requests
import argparse
import yaml
import os
from googleapiclient.discovery import build

def load_config(config_path):
    """
    設定ファイルを読み込みます。
    
    Args:
        config_path: 設定ファイルのパス
    
    Returns:
        設定情報を含む辞書
    """
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        return config
    except Exception as e:
        print(f"設定ファイルの読み込みエラー: {e}", file=sys.stderr)
        print(f"設定ファイル {config_path} が存在するか確認してください。", file=sys.stderr)
        print("config.yaml.sample を参考に config.yaml を作成してください。", file=sys.stderr)
        sys.exit(1)

def search_google(query, api_key, cx, num_results=100):
    """
    Google Custom Search APIを使用して検索を実行し、指定された数の結果を取得します。
    
    Args:
        query: 検索クエリ
        api_key: Google Custom Search APIキー
        cx: 検索エンジンID
        num_results: 取得する結果の数（最大100）
    
    Returns:
        検索結果のURLリスト
    """
    # Google Custom Search APIでは一度に最大10件しか取得できないため、
    # 複数回のリクエストが必要
    service = build("customsearch", "v1", developerKey=api_key)
    
    urls = []
    # 最大100件の結果を取得するために、10件ずつ10回リクエスト
    for i in range(0, min(num_results, 100), 10):
        try:
            result = service.cse().list(
                q=query,
                cx=cx,
                start=i+1,  # 1-based indexing
                num=10
            ).execute()
            
            if 'items' in result:
                for item in result['items']:
                    urls.append(item['link'])
            else:
                print(f"警告: 開始位置 {i+1} の検索結果にアイテムがありません。", file=sys.stderr)
                if i == 0:
                    # 最初のリクエストで結果がない場合、詳細情報を表示
                    print(f"検索結果の詳細: {json.dumps(result, indent=2, ensure_ascii=False)}", file=sys.stderr)
        except Exception as e:
            print(f"検索エラー (開始位置 {i+1}): {e}", file=sys.stderr)
            # 最初のリクエストでエラーが発生した場合は、詳細情報を表示して終了
            if i == 0:
                raise
            break
    
    return urls

def search_google_alternative(query, api_key, cx, num_results=100):
    """
    Google Custom Search APIを使用して検索を実行する代替方法（requestsライブラリを使用）
    
    Args:
        query: 検索クエリ
        api_key: Google Custom Search APIキー
        cx: 検索エンジンID
        num_results: 取得する結果の数（最大100）
    
    Returns:
        検索結果のURLリスト
    """
    urls = []
    # 最大100件の結果を取得するために、10件ずつ10回リクエスト
    for i in range(0, min(num_results, 100), 10):
        try:
            params = {
                'key': api_key,
                'cx': cx,
                'q': query,
                'start': i+1,  # 1-based indexing
                'num': 10
            }
            response = requests.get('https://www.googleapis.com/customsearch/v1', params=params)
            response.raise_for_status()  # HTTPエラーがあれば例外を発生させる
            result = response.json()
            
            if 'items' in result:
                for item in result['items']:
                    urls.append(item['link'])
            else:
                print(f"警告: 開始位置 {i+1} の検索結果にアイテムがありません。", file=sys.stderr)
                if i == 0:
                    # 最初のリクエストで結果がない場合、詳細情報を表示
                    print(f"検索結果の詳細: {json.dumps(result, indent=2, ensure_ascii=False)}", file=sys.stderr)
        except Exception as e:
            print(f"検索エラー (開始位置 {i+1}): {e}", file=sys.stderr)
            # 最初のリクエストでエラーが発生した場合は、詳細情報を表示して終了
            if i == 0:
                if isinstance(e, requests.exceptions.HTTPError):
                    print(f"HTTPエラーの詳細: {e.response.text}", file=sys.stderr)
                raise
            break
    
    return urls

def main():
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description='Google Custom Search APIを使用して検索を実行し、結果をファイルに保存します。')
    parser.add_argument('query', help='検索クエリ')
    parser.add_argument('--config', default="config.yaml", help='設定ファイルのパス')
    parser.add_argument('--num', type=int, help='取得する結果の数（最大100、Google APIの制限による）')
    
    args = parser.parse_args()
    
    try:
        # 設定ファイルの読み込み
        script_dir = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(script_dir, args.config)
        config = load_config(config_path)
        
        # コマンドライン引数が指定されていない場合は設定ファイルの値を使用
        api_key = config.get('api_key')
        cx = config.get('cx')
        output_dir = config.get('output_dir')
        num_results = args.num if args.num is not None else config.get('num_results', 100)
        
        print(f"検索クエリ: {args.query}")
        print(f"検索エンジンID: {cx}")
        
        # Google Custom Search APIを使用して検索
        try:
            # まず googleapiclient を使用した方法を試す
            print("googleapiclientを使用して検索を実行中...")
            urls = search_google(args.query, api_key, cx, num_results)
        except Exception as e:
            print(f"googleapiclientでのリクエストに失敗しました: {e}", file=sys.stderr)
            print("代替方法を試みます...", file=sys.stderr)
            # 失敗した場合は requests を使用した代替方法を試す
            urls = search_google_alternative(args.query, api_key, cx, num_results)
        
        # 現在の日時を取得し、ファイル名を生成
        now = datetime.datetime.now()
        filename = now.strftime("%Y%m%d-%H%M%S") + ".txt"
        
        # 出力ディレクトリが存在しない場合は作成
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        # URLリストをファイルに保存
        with open(filepath, 'w', encoding='utf-8') as f:
            for url in urls:
                f.write(f"{url}\n")
        
        print(f"検索結果を {filepath} に保存しました。")
        print(f"取得したURL数: {len(urls)}")
        
        if len(urls) == 0:
            print("警告: 検索結果が0件です。以下を確認してください：")
            print("1. 検索エンジンID (config.yamlのcx) が正しいか")
            print("2. APIキー (config.yamlのapi_key) が有効か")
            print("3. 検索クエリに一致する結果があるか")
            print("4. API使用量の制限に達していないか")
    
    except Exception as e:
        print(f"エラーが発生しました: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
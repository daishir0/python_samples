"""
OpenAI 並行問い合わせサンプル
==========================

このパッケージは、OpenAIへの並行問い合わせを行うための汎用的なサンプルを提供します。
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
from parallel_openai import ParallelOpenAIClient

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
```

コマンドラインからの使用:
---------------------
```bash
# 単一の問い合わせ
python -m parallel_openai.main query "What is the capital of Japan?"

# ファイルから複数の問い合わせを実行
python -m parallel_openai.main batch queries.txt

# 対話モード
python -m parallel_openai.main interactive
```
"""

from .parallel_client import ParallelOpenAIClient

__version__ = '0.1.0'
__all__ = ['ParallelOpenAIClient']
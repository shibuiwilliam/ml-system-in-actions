# web single pattern

## 目的

Web API として推論器を公開します。

## 前提

- Python 3.8 以上
- Docker

## 使い方

0. カレントディレクトリ

```sh
$ pwd
~/ml-system-in-actions/chapter4_serving_patterns/web_single_pattern
```

1. Docker イメージをビルド

```sh
$ make build_all
# 実行されるコマンド
# docker build \
#     -t shibui/ml-system-in-actions:web_single_pattern_0.0.1 \
#     -f Dockerfile \
#     .
```

2. Docker でサービスを起動

```sh
$ make run
# 実行されるコマンド
# docker run \
#     -d \
#     --name web_single_pattern \
#     -p 8000:8000 \
#     shibui/ml-system-in-actions:web_single_pattern_0.0.1
```

3. 起動した API にクライアントからリクエスト

```sh
# ヘルスチェック
$ curl localhost:8000/health
# 出力
# {
#   "health":"ok"
# }

# メタデータ
$ curl localhost:8000/metadata
# 出力
# {
#   "data_type": "float32",
#   "data_structure": "(1,4)",
#   "data_sample": [
#     [
#       5.1,
#       3.5,
#       1.4,
#       0.2
#     ]
#   ],
#   "prediction_type": "float32",
#   "prediction_structure": "(1,3)",
#   "prediction_sample": [
#     0.97093159,
#     0.01558308,
#     0.01348537
#   ]
# }


# ラベル一覧
$ curl localhost:8000/label
# 出力
# {
#   "0": "setosa",
#   "1": "versicolor",
#   "2": "virginica"
# }


# テストデータで推論リクエスト
$ curl localhost:8000/predict/test
# 出力
# {
#   "prediction": [
#     0.9709315896034241,
#     0.015583082102239132,
#     0.013485366478562355
#   ]
# }


# 推論リクエスト
$ curl \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"data": [[1.0, 2.0, 3.0, 4.0]]}' \
    localhost:8000/predict
# 出力
# {
#   "prediction": [
#     0.3613327741622925,
#     0.2574760615825653,
#     0.3811912536621094
#   ]
# }
```

4. Docker コンテナを停止

```sh
$ make stop
# 実行されるコマンド
# docker rm \
#   -f web_single_pattern
```

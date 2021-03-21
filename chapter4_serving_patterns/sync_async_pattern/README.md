# sync async pattern

## 目的

同期的な推論器と非同期な推論器を組み合わせることで複数の推論の遅延差を補助します。

## 前提

- Python 3.8 以上
- Docker
- Docker compose

## 使い方

0. カレントディレクトリ

```sh
$ pwd
~/ml-system-in-actions/chapter4_serving_patterns/sync_async_pattern
```

1. Docker イメージをビルド

```sh
$ make build_all
# 実行されるコマンド
# docker build \
#     -t shibui/ml-system-in-actions:sync_async_pattern_sync_async_proxy_0.0.1 \
#     -f ./Dockerfile.proxy .
# docker build \
#     -t shibui/ml-system-in-actions:sync_async_pattern_imagenet_mobilenet_v2_0.0.1 \
#     -f ./imagenet_mobilenet_v2/Dockerfile .
# docker build \
#     -t shibui/ml-system-in-actions:sync_async_pattern_imagenet_inception_v3_0.0.1 \
#     -f ./imagenet_inception_v3/Dockerfile .
# docker build \
#     -t shibui/ml-system-in-actions:sync_async_pattern_sync_async_backend_0.0.1 \
#     -f ./Dockerfile.backend .
```

2. Docker compose で各サービスを起動

```sh
$ make c_up
# 実行されるコマンド
# docker-compose \
#     -f ./docker-compose.yml \
#     up -d
```

3. 起動した API にリクエスト

```sh
# ヘルスチェック
$ curl localhost:8000/health
# 出力
# {
#   "health":"ok"
# }

# バックエンドのヘルスチェック
$ curl localhost:8000/health/all
# 出力
# {
#   "mobilenet_v2": "ok",
#   "inception_v3": "ok"
# }


# メタデータ
$ curl localhost:8000/metadata
# 出力
# {
#   "data_type": "str",
#   "data_structure": "(1,1)",
#   "data_sample": "base64 encoded image file",
#   "prediction_type": "float32",
#   "prediction_structure": "(1,1001)",
#   "prediction_sample": "[0.07093159, 0.01558308, 0.01348537, ...]"
# }


# テストデータで推論リクエスト
$ curl localhost:8000/predict/test
# 出力
# {
#   "job_id": "6195b8",
#   "mobilenet_v2": "Persian cat"
# }


# 画像をリクエスト
$ (echo -n '{"image_data": "'; base64 data/cat.jpg; echo '"}') | \
    curl \
    -X POST \
    -H "Content-Type: application/json" \
    -d @- \
    localhost:8000/predict
# 出力
# {
#   "job_id": "9e987f",
#   "mobilenet_v2": "Persian cat"
# }

# 画像リクエストのジョブIDから推論結果をリクエスト
$ curl localhost:8000/job/2f49aa
# 出力
# {
#   "6195b8": {
#     "prediction": "Siamese cat"
#   }
# }
```

4. Docker compose を停止

```sh
$ make c_down
# 実行されるコマンド
# docker-compose \
#     -f ./docker-compose.yml \
#     down
```

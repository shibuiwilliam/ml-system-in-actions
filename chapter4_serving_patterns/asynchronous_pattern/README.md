# asynchronous pattern

## 目的

非同期推論の API を提供します。

## 前提

- Python 3.8 以上
- Docker
- Docker compose

## 使い方

0. カレントディレクトリ

```sh
$ pwd
~/ml-system-in-actions/chapter4_serving_patterns/asynchronous_pattern
```

1. 非同期推論のための Docker イメージをビルド

```sh
$ make build_all
# 実行されるコマンド
# docker build \
#     -t shibui/ml-system-in-actions:asynchronous_pattern_asynchronous_proxy_0.0.1 \
#     -f ./Dockerfile.proxy .
# docker build \
#     -t shibui/ml-system-in-actions:asynchronous_pattern_imagenet_inception_v3_0.0.1 \
#     -f ./imagenet_inception_v3/Dockerfile .
# docker build \
#     -t shibui/ml-system-in-actions:asynchronous_pattern_asynchronous_backend_0.0.1 \
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
# {"health":"ok"}

# メタデータ
$ curl localhost:8000/metadata
# 出力
# {
#   "model_spec": {
#     "name": "inception_v3",
#     "signature_name": "",
#     "version": "0"
#   },
#   "metadata": {
#     "signature_def": {
#       "signature_def": {
#         "serving_default": {
#           "inputs": {
#             "image": {
#               "dtype": "DT_STRING",
#               "tensor_shape": {
#                 "dim": [
#                   {
#                     "size": "-1",
#                     "name": ""
#                   }
#                 ],
#                 "unknown_rank": false
#               },
#               "name": "serving_default_image:0"
#             }
#           },
#           "outputs": {
#             "output_0": {
#               "dtype": "DT_STRING",
#               "tensor_shape": {
#                 "dim": [],
#                 "unknown_rank": true
#               },
#               "name": "StatefulPartitionedCall:0"
#             }
#           },
#           "method_name": "tensorflow/serving:2.6.1/predict"
#         },
#         "__saved_model_init_op": {
#           "inputs": {},
#           "outputs": {
#             "__saved_model_init_op": {
#               "dtype": "DT_INVALID",
#               "tensor_shape": {
#                 "dim": [],
#                 "unknown_rank": true
#               },
#               "name": "NoOp"
#             }
#           },
#           "method_name": ""
#         }
#       }
#     }
#   }
# }

# ラベル一覧
$ curl localhost:8000/label
# 出力
# [
#   "background",
#   "tench",
#   "goldfish",
# ...
#   "bolete",
#   "ear",
#   "toilet tissue"
# ]

# テストデータで推論リクエスト
$ curl localhost:8000/predict/test
# 出力
# {
#   "job_id": "f22689"
# }


# 画像をリクエスト
$ (echo \
    -n '{"image_data": "'; \
    base64 imagenet_inception_v3/data/cat.jpg; \
    echo '"}') | \
   curl \
    -X POST \
    -H "Content-Type: application/json" \
    -d @- \
    localhost:8000/predict
# 出力
# {
#   "job_id":"2f49aa"
# }

# 画像リクエストのジョブIDから推論結果をリクエスト
$ curl localhost:8000/job/2f49aa
# 出力
# {
#   "2f49aa": {
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

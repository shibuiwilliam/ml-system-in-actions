# synchronous prediction pattern

## 目的

リクエストに対して同期的に推論しレスポンスします。

## 前提

- Python 3.8 以上
- Docker

## 使い方

0. カレントディレクトリ

```sh
$ pwd
~/ml-system-in-actions/chapter4_serving_patterns/synchronous_pattern
```

1. Docker イメージをビルド

```sh
$ make build_all
# 実行されるコマンド
# docker build \
#     -t shibui/ml-system-in-actions:synchronous_pattern_imagenet_inception_v3_0.0.1 \
#     -f imagenet_inception_v3/Dockerfile .
```

2. Docker コンテナでサービスを起動

```sh
$ make run
# 実行されるコマンド
# docker run \
#     -d \
#     --name imagenet_inception_v3 \
#     -p 8500:8500 \
#     -p 8501:8501 \
#     shibui/ml-system-in-actions:synchronous_pattern_imagenet_inception_v3_0.0.1
```

3. 起動した API にクライアントからリクエスト

```sh
# メタデータ
$ curl localhost:8501/v1/models/inception_v3/versions/0/metadata
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



# GRPCで画像をリクエスト
$ python \
    -m client.request_inception_v3 \
    --image_file ./cat.jpg \
    --format grpc
# 出力
# Siamese cat


# RESTで画像をリクエスト
$ python \
    -m client.request_inception_v3 \
    --image_file ./cat.jpg \
    --format rest
# 出力
# Siamese cat
```

4. Docker コンテナを停止

```sh
$ make stop
# 実行されるコマンド
# docker rm \
#   -f imagenet_inception_v3
```

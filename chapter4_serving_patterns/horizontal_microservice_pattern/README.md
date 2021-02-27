# horizontal microservice pattern

## 目的

推論器をマイクロサービスとして並列に配置します。

## 前提

- Python 3.8 以上
- Docker
- Docker compose

## 使い方

0. カレントディレクトリ

```sh
$ pwd
~/ml-system-in-actions/chapter4_serving_patterns/horizontal_microservice_pattern
```

1. Docker イメージをビルド

```sh
$ make build_all
# 実行されるコマンド
# docker build \
#     -t shibui/ml-system-in-actions:horizontal_microservice_pattern_setosa_0.0.1 \
#     -f ./Dockerfile.service.setosa \
#     .
# docker build \
#     -t shibui/ml-system-in-actions:horizontal_microservice_pattern_versicolor_0.0.1 \
#     -f ./Dockerfile.service.versicolor \
#     .
# docker build \
#     -t shibui/ml-system-in-actions:horizontal_microservice_pattern_virginica_0.0.1 \
#     -f ./Dockerfile.service.virginica \
#     .
# docker build \
#     -t shibui/ml-system-in-actions:horizontal_microservice_pattern_proxy_0.0.1 \
#     -f ./Dockerfile.proxy \
#     .
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
# proxyにヘルスチェック
$ curl localhost:9000/health
# 出力
# {"health":"ok"}

# 推論器にヘルスチェック
$ curl localhost:9000/health/all
# 出力
# {
#   "setosa": {
#     "health": "ok"
#   },
#   "virginica": {
#     "health": "ok"
#   },
#   "versicolor": {
#     "health": "ok"
#   }
# }

# メタデータ
$ curl localhost:9000/metadata
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
#   "prediction_structure": "(1,2)",
#   "prediction_sample": {
#     "service_setosa": [
#       0.97,
#       0.03
#     ],
#     "service_versicolor": [
#       0.97,
#       0.03
#     ],
#     "service_virginica": [
#       0.97,
#       0.03
#     ]
#   }
# }

# テストデータで推論リクエスト(GET)
$ curl localhost:9000/predict/get/test
# 出力
# {
#   "setosa": {
#     "prediction": [
#       0.9824145436286926,
#       0.017585478723049164
#     ]
#   },
#   "virginica": {
#     "prediction": [
#       0.011562099680304527,
#       0.9884378910064697
#     ]
#   },
#   "versicolor": {
#     "prediction": [
#       0.0046140821650624275,
#       0.9953859448432922
#     ]
#   }
# }

# テストデータで推論リクエスト(POST)
$ curl localhost:9000/predict/post/test
# 出力
# {
#   "setosa": {
#     "prediction": [
#       0.9824145436286926,
#       0.017585478723049164
#     ]
#   },
#   "virginica": {
#     "prediction": [
#       0.011562099680304527,
#       0.9884378910064697
#     ]
#   },
#   "versicolor": {
#     "prediction": [
#       0.0046140821650624275,
#       0.9953859448432922
#     ]
#   }
# }


# POSTリクエスト
$ curl \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"data": [[1.0, 2.0, 3.0, 4.0]]}' \
    localhost:9000/predict
# 出力
# {
#   "setosa": {
#     "prediction": [
#       0.2897033989429474,
#       0.710296630859375
#     ]
#   },
#   "virginica": {
#     "prediction": [
#       0.3042130172252655,
#       0.6957869529724121
#     ]
#   },
#   "versicolor": {
#     "prediction": [
#       0.05282164365053177,
#       0.9471783638000488
#     ]
#   }
# }

# ラベルをリクエスト
$ curl \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"data": [[1.0, 2.0, 3.0, 4.0]]}' \
    localhost:9000/predict/label
# 出力
# {
#   "prediction": {
#     "proba": 0.3042130172252655,
#     "label": "virginica"
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

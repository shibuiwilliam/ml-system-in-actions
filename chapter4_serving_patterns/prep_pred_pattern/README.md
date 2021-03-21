# prep-pred pattern

## 目的

前処理と推論を分割して柔軟性を向上します。

## 前提

- Python 3.8 以上
- Docker
- Docker compose

## 使い方

0. カレントディレクトリ

```sh
$ pwd
~/ml-system-in-actions/chapter4_serving_patterns/prep_pred_pattern
```

1. Docker イメージをビルド

```sh
$ make build_all
# 実行されるコマンド
# docker build \
#     -t shibui/ml-system-in-actions:prep_pred_pattern_prep_0.0.1 \
#     -f ./Dockerfile.prep .
# docker build \
#     -t shibui/ml-system-in-actions:prep_pred_pattern_pred_0.0.1 \
#     -f ./Dockerfile.pred .
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
#   "data_type": "str",
#   "data_structure": "(1,1)",
#   "data_sample": "base64 encoded image file",
#   "prediction_type": "float32",
#   "prediction_structure": "(1,1000)",
#   "prediction_sample": "[0.07093159, 0.01558308, 0.01348537, ...]"
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
$ curl localhost:8000/predict/test/label
# 出力
# {
#   "prediction": "Siamese cat"
# }


# 画像をリクエスト
$ (echo -n '{"data": "'; base64 data/cat.jpg; echo '"}') | \
    curl \
    -X POST \
    -H "Content-Type: application/json" \
    -d @- \
    localhost:8000/predict/label
# 出力
# {
#   "prediction": "Siamese cat"
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

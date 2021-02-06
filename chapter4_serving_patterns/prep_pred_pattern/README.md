# prep-pred pattern

## 目的

前処理と推論を分割して柔軟性を向上します。

## 前提

- Python 3.8以上
- Docker
- Docker compose

## 使い方

1. Dockerイメージをビルド

```sh
$ make build_all

docker build \
    -t shibui/ml-system-in-actions:prep_pred_pattern_prep_0.0.1 \
    -f ./Dockerfile.prep .
docker build \
    -t shibui/ml-system-in-actions:prep_pred_pattern_pred_0.0.1 \
    -f ./Dockerfile.pred .
```

2. Docker composeで各サービスを起動

```sh
$ make c_up

docker-compose \
    -f ./docker-compose.yml \
    up -d
```

3. 起動したAPIにリクエスト

```sh
# ヘルスチェック
$ curl localhost:8000/health
{"health":"ok"}

# メタデータ
$ curl localhost:8000/metadata
{
  "data_type": "str",
  "data_structure": "(1,1)",
  "data_sample": "base64 encoded image file",
  "prediction_type": "float32",
  "prediction_structure": "(1,1000)",
  "prediction_sample": "[0.07093159, 0.01558308, 0.01348537, ...]"
}


# ラベル一覧
$ curl localhost:8000/label
[
  "background",
  "tench",
  "goldfish",
...
  "bolete",
  "ear",
  "toilet tissue"
]


# テストデータで推論リクエスト
$ curl localhost:8000/predict/test
{
  "prediction": "Siamese cat"
}


# 画像をリクエスト
$ (echo -n '{"data": "'; base64 data/cat.jpg; echo '"}') | \
    curl \
    -X POST \
    -H "Content-Type: application/json" \
    -d @- \
    localhost:8000/predict/label
{
  "prediction": "Siamese cat"
}
```

4. Docker composeを停止

```sh
$ make c_down

docker-compose \
    -f ./docker-compose.yml \
    down
```

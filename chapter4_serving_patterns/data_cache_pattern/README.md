# data cache pattern

## 目的

データをキャッシュし、推論速度を改善します。

## 前提

- Python 3.8以上
- Docker
- Docker compose

## 使い方

1. ...

```sh
$ make build_all
docker build \
    -t shibui/ml-system-in-actions:data_cache_pattern_proxy_0.0.1 \
    -f ./Dockerfile.proxy .
docker build \
    -t shibui/ml-system-in-actions:data_cache_pattern_pred_0.0.1 \
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
{
  "health": "ok"
}

# メタデータ
$ curl localhost:8000/metadata
{
  "data_type": "str",
  "data_structure": "(1,1)",
  "data_sample": "0000",
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
$ curl localhost:8000/predict/test/label
{
  "prediction": "Persian cat"
}

# 画像をリクエスト
$ curl \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"data": "0000"}' \
    localhost:8000/predict/label
{
  "prediction": "Persian cat"
}
```

4. Docker composeを停止

```sh
$ make c_down
docker-compose \
		-f ./docker-compose.yml \
		down
```

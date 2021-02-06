# sync async pattern

## 目的

同期的な推論器と非同期な推論器を組み合わせることで複数の推論の遅延差を補助します。

## 前提

- Python 3.8以上
- Docker
- Docker compose

## 使い方

1. Dockerイメージをビルド

```sh
$ make build_all

docker build \
    -t shibui/ml-system-in-actions:sync_async_pattern_sync_async_proxy_0.0.1 \
    -f ./Dockerfile.proxy .
docker build \
    -t shibui/ml-system-in-actions:sync_async_pattern_imagenet_mobilenet_v2_0.0.1 \
    -f ./imagenet_mobilenet_v2/Dockerfile .
docker build \
    -t shibui/ml-system-in-actions:sync_async_pattern_imagenet_inception_v3_0.0.1 \
    -f ./imagenet_inception_v3/Dockerfile .
docker build \
    -t shibui/ml-system-in-actions:sync_async_pattern_sync_async_backend_0.0.1 \
    -f ./Dockerfile.backend .
   
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
  "health":"ok"
}

# バックエンドのヘルスチェック
$ curl localhost:8000/health/all
{
  "mobilenet_v2": "ok",
  "inception_v3": "ok"
}


# メタデータ
$ make metadata
curl localhost:8000/metadata
{
  "data_type": "str",
  "data_structure": "(1,1)",
  "data_sample": "base64 encoded image file",
  "prediction_type": "float32",
  "prediction_structure": "(1,1001)",
  "prediction_sample": "[0.07093159, 0.01558308, 0.01348537, ...]"
}


# テストデータで推論リクエスト
$ curl localhost:8000/predict/test
{
  "job_id": "6195b8",
  "mobilenet_v2": "Persian cat"
}


# 画像をリクエスト
$ (echo -n '{"image_data": "'; base64 data/cat.jpg; echo '"}') | \
    curl \
    -X POST \
    -H "Content-Type: application/json" \
    -d @- \
    localhost:8000/predict
{
  "job_id": "9e987f",
  "mobilenet_v2": "Persian cat"
}

# 画像リクエストのジョブIDから推論結果をリクエスト
$ curl localhost:8000/job/2f49aa
{
  "6195b8": {
    "prediction": "Siamese cat"
  }
}
```

4. Docker composeを停止

```sh
$ make c_down

docker-compose \
    -f ./docker-compose.yml \
    down
```

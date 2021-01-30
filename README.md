# ml-system-in-actions
machine learning system examples


---
テンプレート
# 名称

## 目的

...

## 前提

- Python 3.8以上
- Docker
- Docker compose

## 使い方

1. Dockerイメージをビルド

```sh
$ make build_all


```

2. Docker composeで各サービスを起動

```sh
$ make c_up


```

3. 起動したAPIにリクエスト

```sh
# ヘルスチェック
$ curl localhost:8000/health
{"health":"ok"}

# メタデータ
$ make metadata
curl localhost:8000/metadata



# ラベル一覧
$ curl localhost:8000/label | jq



# テストデータで推論リクエスト
$ curl localhost:8000/predict/test | jq .




# 画像をリクエスト
$ (echo -n '{"image_data": "'; base64 imagenet_inception_v3/data/cat.jpg; echo '"}') | \
    curl \
        -X POST \
        -H "Content-Type: application/json" \
        -d @- \
        localhost:8000/predict



# 画像リクエストのジョブIDから推論結果をリクエスト
$ curl localhost:8000/job/2f49aa


```

4. Docker composeを停止

```sh
$ make c_down


```

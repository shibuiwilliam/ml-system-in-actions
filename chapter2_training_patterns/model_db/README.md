# モデル管理DB

## 目的

モデルを管理するためのデータベースおよびサービス用REST APIの構築

## 前提

- Python 3.8以上
- Docker
- Docker compose

## 使い方

1. モデルDBサービス（REST API）用のDockerイメージのビルド

```sh
$ make build
```

2. Docker composeによるモデルDBの起動

```sh
$ make c_up
```

3. モデルDBサービスの起動確認

`localhost:8000/docs` をブラウザで開き、Swaggerが起動していることを確認します。

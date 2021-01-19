# model load pattern

## 目的

モデル・イン・イメージ・パターンでは学習によってモデルファイルを生成した後にモデルファイル含めて推論サーバイメージをビルドします。推論サーバを配備する際には、サーバイメージを Pull して推論サーバを起動することで本稼働させることができます。

## 前提

- Python 3.8以上
- Docker
- Kubernetesクラスターまたはminikube

## 使い方

1. 推論用Dockerイメージのビルド
   
```sh
$ make build_all
```

2. 推論器をKubernetesクラスターにデプロイ

```sh
$ make deploy
```

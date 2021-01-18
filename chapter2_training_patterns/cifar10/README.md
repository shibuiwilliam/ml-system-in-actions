# Cifar10学習パイプライン

## 目的

MLFlowを用いたCifar10データセットの学習パイプラインです。

## 前提

先に[model_db](../model_db)を構築し、利用可能な状態にしてください。

- Python 3.8以上
- Docker
- MLFlow

## 使い方

1. ライブラリインストール

```sh
$ make dev
```

2. 学習用Dockerイメージのビルド

```sh
$ make d_build
```

3. 学習パイプラインの実行

```sh
$ make train
```

学習が完了するまで、数分から数十分かかることがあります。




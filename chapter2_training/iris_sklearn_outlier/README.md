# Irisデータセットの外れ値検知モデル学習パイプライン

## 目的

MLFlowを用いたIrisデータセットの外れ値検知モデル学習パイプラインです。

## 前提

- Python 3.8以上
- Docker
- MLFlow

## 使い方

1. ライブラリインストール

```sh
$ make dev
pip install -r requirements.txt
```

2. 学習用Dockerイメージのビルド

```sh
$ make d_build
docker build \
    -t shibui/ml-system-in-actions:training_pattern_iris_sklearn_rf_0.0.1 \
    -f Dockerfile .
```

3. 学習パイプラインの実行

```sh
$ make train
mlflow run . --no-conda
```

学習は数分以内に完了します。



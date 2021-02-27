# Iris データセットの外れ値検知モデル学習パイプライン

## 目的

MLFlow を用いた Iris データセットの外れ値検知モデル学習パイプラインです。

## 前提

- Python 3.8 以上
- Docker
- MLFlow

## 使い方

0. カレントディレクトリ

```sh
$ pwd
~/ml-system-in-actions/chapter2_training/iris_sklearn_outlier
```

1. ライブラリインストール
   本プログラムで仕様するライブラリは[requirements.txt](./requirements.txt)に示すとおりです。

```sh
$ make dev
# 実行されるコマンド
# pip install -r requirements.txt
# 出力は省略
```

2. 学習用 Docker イメージのビルド
   学習で使用する Docker イメージをビルドします。

```sh
$ make d_build
# 実行されるコマンド
# docker build \
#     -t shibui/ml-system-in-actions:training_pattern_iris_sklearn_rf_0.0.1 \
#     -f Dockerfile .
# 出力は省略
# dockerイメージとしてshibui/ml-system-in-actions:training_pattern_iris_sklearn_rf_0.0.1がビルドされます。
```

3. 学習パイプラインの実行
   mlflow で学習パイプラインを実行します。

```sh
$ make train
# 実行されるコマンド
# mlflow run . --no-conda
# 出力例
# 2021/02/11 11:23:47 INFO mlflow.projects.docker: === Building docker image iris_sklearn_ocs:6fa928e ===
# 2021/02/11 11:23:55 INFO mlflow.projects.utils: === Created directory /var/folders/v8/bvkzgn8j1ws6y76t4z5nt6280000gn/T/tmpwcy6fg3e for downloading remote URIs passed to arguments of type 'path' ===
# 2021/02/11 11:23:55 INFO mlflow.projects.backend.local: === Running command 'docker run --rm -v ~/book/ml-system-in-actions/chapter2_training/iris_sklearn_outlier/mlruns:/mlflow/tmp/mlruns -v ~/book/ml-system-in-actions/chapter2_training_patterns/iris_sklearn_outlier/mlruns/0/b6521ae70302453e8ab452db2359ad8e/artifacts:~/book/ml-system-in-actions/chapter2_training_patterns/iris_sklearn_outlier/mlruns/0/b6521ae70302453e8ab452db2359ad8e/artifacts -e MLFLOW_RUN_ID=b6521ae70302453e8ab452db2359ad8e -e MLFLOW_TRACKING_URI=file:///mlflow/tmp/mlruns -e MLFLOW_EXPERIMENT_ID=0 iris_sklearn_ocs:6fa928e python -m iris_train' in run with ID 'b6521ae70302453e8ab452db2359ad8e' ===
# 2021/02/11 11:24:01 INFO mlflow.projects: === Run (ID 'b6521ae70302453e8ab452db2359ad8e') succeeded ===
```

学習は数分以内に完了します。

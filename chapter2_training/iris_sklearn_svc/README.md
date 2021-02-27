# Iris データセットの SVM 分類モデル学習パイプライン

## 目的

MLFlow を用いた Iris データセットの SVM 分類モデル学習パイプラインです。

## 前提

- Python 3.8 以上
- Docker
- MLFlow

## 使い方

0. カレントディレクトリ

```sh
$ pwd
~/ml-system-in-actions/chapter2_training/iris_sklearn_svc
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
#     -t shibui/ml-system-in-actions:training_pattern_iris_sklearn_svc_0.0.1 \
#     -f Dockerfile .
# 出力は省略
# dockerイメージとしてshibui/ml-system-in-actions:training_pattern_iris_sklearn_svc_0.0.1がビルドされます。
```

3. 学習パイプラインの実行
   mlflow で学習パイプラインを実行します。

```sh
$ make train
# 実行されるコマンド
# mlflow run . --no-conda
# 出力例
# 2021/02/11 11:29:41 INFO mlflow.projects.docker: === Building docker image iris_sklearn_svc:6fa928e ===
# 2021/02/11 11:29:52 INFO mlflow.projects.utils: === Created directory /var/folders/v8/bvkzgn8j1ws6y76t4z5nt6280000gn/T/tmpdtqjaxok for downloading remote URIs passed to arguments of type 'path' ===
# 2021/02/11 11:29:52 INFO mlflow.projects.backend.local: === Running command 'docker run --rm -v ~/book/ml-system-in-actions/chapter2_training/iris_sklearn_svc/mlruns:/mlflow/tmp/mlruns -v ~/book/ml-system-in-actions/chapter2_training_patterns/iris_sklearn_svc/mlruns/0/c2e44e8158f64352b4f23fb21329693e/artifacts:~/book/ml-system-in-actions/chapter2_training_patterns/iris_sklearn_svc/mlruns/0/c2e44e8158f64352b4f23fb21329693e/artifacts -e MLFLOW_RUN_ID=c2e44e8158f64352b4f23fb21329693e -e MLFLOW_TRACKING_URI=file:///mlflow/tmp/mlruns -e MLFLOW_EXPERIMENT_ID=0 iris_sklearn_svc:6fa928e python -m iris_train \
#   --test_size 0.3 ' in run with ID 'c2e44e8158f64352b4f23fb21329693e' ===
# 2021/02/11 11:29:58 INFO mlflow.projects: === Run (ID 'c2e44e8158f64352b4f23fb21329693e') succeeded ===
```

学習は数分以内に完了します。

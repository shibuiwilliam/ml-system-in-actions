# ml-system-in-actions

machine learning system examples

## tl;dr

- 本レポジトリは 2021 年 XX 月翔泳社出版『機械学習システムデザインパターン』のサンプルコード集です。
- 本レポジトリでは機械学習のモデル学習、リリース、推論器の稼働、運用のためのコードおよび実行環境を用例ごとに提供します。

## 実行環境

- Python 3.8 以上
- Docker
- Docker-compose
- （一部）Kubernetes または minikube
- （一部）Android Studio

本レポジトリではプログラムの実行環境として Docker、Docker-compose、（一部）Kubernetes/minikube、（一部）Android Studio を使用します。
また、コマンドラインとして `kubectl`、`istioctl` を使用します。
各種ミドルウェア、開発環境、コマンドラインは以下公式ドキュメントを参考にインストールしてください。

- [Docker](https://docs.docker.com/get-docker/)
- [Docker-compose](https://docs.docker.jp/compose/toc.html)
- [Kubernetes クラスター構築](https://kubernetes.io/ja/docs/setup/)
- [minikube](https://kubernetes.io/ja/docs/setup/learning-environment/minikube/)
- [kubectl](https://kubernetes.io/ja/docs/tasks/tools/install-kubectl/)
- [istioctl](https://istio.io/latest/docs/setup/getting-started/)
- [Android Studio](https://developer.android.com/studio/install)

### Python の実行環境

本レポジトリで用いる Python のライブラリは`pipenv`で指定しています。以下の手順で pipenv とともにライブラリをインストールしてください。
サンプルコードは Python3.8 以上で実行を検証しています。実行環境の Python バージョンが合わない場合、[pyenv](https://github.com/pyenv/pyenv)等で実行環境を整えてください。

```sh
# Pythonのバージョン
$ python -V
# 出力
Python 3.8.5

# pyenvバージョン
$ pyenv versions
# 出力
  system
* 3.8.5

# pipenvと依存ライブラリをインストールし、シェルをpipenv venvに変更
$ make dev
# 出力例
# pip install pipenv
# Requirement already satisfied: pipenv in ~/.pyenv/versions/3.8.5/lib/python3.8/site-packages (2020.11.15)
# Requirement already satisfied: virtualenv-clone>=0.2.5 in ~/.pyenv/versions/3.8.5/lib/python3.8/site-packages (from pipenv) (0.5.4)
# Requirement already satisfied: certifi in ~/.pyenv/versions/3.8.5/lib/python3.8/site-packages (from pipenv) (2020.12.5)
# Requirement already satisfied: pip>=18.0 in ~/.pyenv/versions/3.8.5/lib/python3.8/site-packages (from pipenv) (20.1.1)
# Requirement already satisfied: virtualenv in ~/.pyenv/versions/3.8.5/lib/python3.8/site-packages (from pipenv) (20.4.2)
# Requirement already satisfied: setuptools>=36.2.1 in ~/.pyenv/versions/3.8.5/lib/python3.8/site-packages (from pipenv) (47.1.0)
# Requirement already satisfied: distlib<1,>=0.3.1 in ~/.pyenv/versions/3.8.5/lib/python3.8/site-packages (from virtualenv->pipenv) (0.3.1)
# Requirement already satisfied: appdirs<2,>=1.4.3 in ~/.pyenv/versions/3.8.5/lib/python3.8/site-packages (from virtualenv->pipenv) (1.4.4)
# Requirement already satisfied: filelock<4,>=3.0.0 in ~/.pyenv/versions/3.8.5/lib/python3.8/site-packages (from virtualenv->pipenv) (3.0.12)
# Requirement already satisfied: six<2,>=1.9.0 in ~/.pyenv/versions/3.8.5/lib/python3.8/site-packages (from virtualenv->pipenv) (1.15.0)
# WARNING: You are using pip version 20.1.1; however, version 21.0.1 is available.
# You should consider upgrading via the '~/.pyenv/versions/3.8.5/bin/python3.8 -m pip install --upgrade pip' command.
# PIPENV_VENV_IN_PROJECT=true pipenv shell
# Creating a virtualenv for this project...
# Pipfile: ~/book/ml-system-in-actions/Pipfile
# Using ~/.pyenv/versions/3.8.5/bin/python3.8 (3.8.5) to create virtualenv...
# ⠧ Creating virtual environment...created virtual environment CPython3.8.5.final.0-64 in 433ms
#   creator CPython3Posix(dest=~/book/ml-system-in-actions/.venv, clear=False, no_vcs_ignore=False, global=False)
#   seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=~/Library/Application Support/virtualenv)
#     added seed packages: pip==21.0.1, setuptools==52.0.0, wheel==0.36.2
#   activators BashActivator,CShellActivator,FishActivator,PowerShellActivator,PythonActivator,XonshActivator

# ✔ Successfully created virtual environment!
# Virtualenv location: ~/book/ml-system-in-actions/.venv
# Launching subshell in virtual environment...
#  . ~/book/ml-system-in-actions/.venv/bin/activate
# [21-02-27 10:03:37] your_name@your_namenoMacBook-Pro:~/book/ml-system-in-actions
# $  . ~/book/ml-system-in-actions/.venv/bin/activate
# (ml-system-in-actions) [21-02-27 10:03:37] your_name@your_namenoMacBook-Pro:~/book/ml-system-in-actions

# pipenv venvを終了
$ exit
```

ただし、一部のサンプルコードでは他のライブラリを使用することがあります。当該サンプルコードのディレクトリで README を参照してください。

## コード一覧

本レポジトリが提供するプログラムは以下に示す各プログラムのディレクトリで実行されることを想定して開発されています。
各プログラムを実行する際は目的のディレクトリに移動してください。
各プログラムの実行方法は各プログラムディレクトリ配下の README に示してあります。

.</br>
├── [chapter2_training](./chapter2_training/)</br>
│   ├── [cifar10](./chapter2_training/cifar10)</br>
│   ├── [iris_binary](./chapter2_training/iris_binary)</br>
│   ├── [iris_sklearn_outlier](./chapter2_training/iris_sklearn_outlier)</br>
│   ├── [iris_sklearn_rf](./chapter2_training/iris_sklearn_rf)</br>
│   ├── [iris_sklearn_svc](./chapter2_training/iris_sklearn_svc)</br>
│   └── [model_db](./chapter2_training/model_db)</br>
├── [chapter3_release_patterns](./chapter3_release_patterns)</br>
│   ├── [model_in_image_pattern](./chapter3_release_patterns/model_in_image_pattern)</br>
│   └── [model_load_pattern](./chapter3_release_patterns/model_load_pattern)</br>
├── [chapter4_serving_patterns](./chapter4_serving_patterns/)</br>
│   ├── [asynchronous_pattern](./chapter4_serving_patterns/asynchronous_pattern)</br>
│   ├── [batch_pattern](./chapter4_serving_patterns/batch_pattern)</br>
│   ├── [data_cache_pattern](./chapter4_serving_patterns/data_cache_pattern)</br>
│   ├── [edge_ai_pattern](./chapter4_serving_patterns/edge_ai_pattern)</br>
│   ├── [horizontal_microservice_pattern](./chapter4_serving_patterns/horizontal_microservice_pattern)</br>
│   ├── [prediction_cache_pattern](./chapter4_serving_patterns/prediction_cache_pattern)</br>
│   ├── [prep_pred_pattern](./chapter4_serving_patterns/prep_pred_pattern)</br>
│   ├── [sync_async_pattern](./chapter4_serving_patterns/sync_async_pattern)</br>
│   ├── [synchronous_pattern](./chapter4_serving_patterns/synchronous_pattern)</br>
│   └── [web_single_pattern](./chapter4_serving_patterns/web_single_pattern)</br>
├── [chapter5_operations](./chapter5_operations/)</br>
│   ├── [prediction_log_pattern](./chapter5_operations/prediction_log_pattern)</br>
│   └── [prediction_monitoring_pattern](./chapter5_operations/prediction_monitoring_pattern)</br>
└── [chapter6_operation_management](./chapter6_operation_management/)</br>
   ├── [circuit_breaker_pattern](./chapter6_operation_management/circuit_breaker_pattern)</br>
   ├── [condition_based_pattern](./chapter6_operation_management/condition_based_pattern)</br>
   ├── [load_test_pattern](./chapter6_operation_management/load_test_pattern)</br>
   ├── [online_ab_pattern](./chapter6_operation_management/online_ab_pattern)</br>
   ├── [paramater_based_pattern](./chapter6_operation_management/paramater_based_pattern)</br>
   └── [shadow_ab_pattern](./chapter6_operation_management/shadow_ab_pattern)</br>

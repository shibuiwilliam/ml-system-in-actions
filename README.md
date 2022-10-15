# ml-system-in-actions

machine learning system examples

## tl;dr

- 本レポジトリは 2021 年 5 月翔泳社出版『AI エンジニアのための機械学習システムデザインパターン』のサンプルコード集です。
- 本レポジトリでは機械学習のモデル学習、リリース、推論器の稼働、運用のためのコードおよび実行環境を用例ごとに提供します。
- 「機械学習システムデザインパターン」の詳細は本書および mercari/ml-system-design-pattern をご参照ください。
  - [AI エンジニアのための機械学習システムデザインパターン](https://www.amazon.co.jp/AI%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%8B%E3%82%A2%E3%81%AE%E3%81%9F%E3%82%81%E3%81%AE%E6%A9%9F%E6%A2%B0%E5%AD%A6%E7%BF%92%E3%82%B7%E3%82%B9%E3%83%86%E3%83%A0%E3%83%87%E3%82%B6%E3%82%A4%E3%83%B3%E3%83%91%E3%82%BF%E3%83%BC%E3%83%B3-%E6%BE%81%E4%BA%95%E9%9B%84%E4%BB%8B-ebook/dp/B08YNMRH4J?crid=387XA7DART8JA&keywords=%E6%A9%9F%E6%A2%B0%E5%AD%A6%E7%BF%92%E3%82%B7%E3%82%B9%E3%83%86%E3%83%A0&qid=1665798135&qu=eyJxc2MiOiIyLjU0IiwicXNhIjoiMi40OCIsInFzcCI6IjIuNDQifQ%3D%3D&sprefix=%2Caps%2C160&sr=8-1&linkCode=ll1&tag=shibuiyusuke-22&linkId=5a0d07b5a18ccd16f6c2e26fab00a106&language=ja_JP&ref_=as_li_ss_tl)
  - [mercari/ml-system-design-pattern](https://github.com/mercari/ml-system-design-pattern)

![img](./hyoshi.jpg)

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

# pipenvをインストールし、シェルをpipenv venvに変更
$ make dev
# 出力例
# pip install pipenv
# Requirement already satisfied: pipenv in ~/.pyenv/versions/3.8.5/lib/python3.8/site-packages (2020.11.15)
# (中略)
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

# 依存ライブラリをインストール
$ make dev_sync
# 出力例
# pipenv sync --dev
# Installing dependencies from Pipfile.lock (a2c081)...
#   🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 93/93 — 00:02:36
# All dependencies are now up-to-date!

##################################
####### 開発、プログラムの実行 #######
##################################


# 開発、プログラムの実行が完了したらpipenv venvシェルを終了
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

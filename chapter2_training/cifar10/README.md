# Cifar10学習パイプライン

## 目的

MLFlowを用いたCifar10データセットの学習パイプラインです。

## 前提

- Python 3.8以上
- Docker
- MLFlow
- Anaconda

本プログラムではcondaコマンドを使用するため、Anaconda/minicondaを使います。
Anaconda/minicondaの実行環境はpyenv等仮想環境で用意することを推奨します。
pyenvで環境構築する方法は以下のとおりです。

```sh
# 2021/02時点最新のanaconda環境を選択
$ pyenv install anaconda3-2020.02
Downloading Anaconda3-2020.02-MacOSX-x86_64.sh...
-> https://repo.continuum.io/archive/Anaconda3-2020.02-MacOSX-x86_64.sh
Installing Anaconda3-2020.02-MacOSX-x86_64...
Installed Anaconda3-2020.02-MacOSX-x86_64 to /Users/shibuiyuusuke/.pyenv/versions/anaconda3-2020.02

# pyenvで仮想環境にanaconda3-2020.02を選択
$ pyenv local anaconda3-2020.02

# 仮想環境がanaconda3-2020.02になっていることを確認
$ pyenv versions
  system
* anaconda3-2020.02 (set by ~/ml-system-in-actions/chapter2_training/cifar10/.python-version)

# 依存ライブラリをインストール
$ pip install -r requirements.txt
```

## 使い方

1. ライブラリインストール

```sh
$ make dev
# 実行されるコマンド
# pip install -r requirements.txt
# 出力は省略
```

2. 学習用Dockerイメージのビルド

```sh
$ make d_build
# 実行されるコマンド
# docker build \
#     -t shibui/ml-system-in-actions:training_pattern_cifar10_0.0.1 \
#     -f Dockerfile .
# 出力は省略
# dockerイメージとしてshibui/ml-system-in-actions:training_pattern_cifar10_0.0.1がビルドされます。
```

3. 学習パイプラインの実行

```sh
$ make train
# 実行されるコマンド
# mlflow run .
```

学習が完了するまで、数分から数十分かかることがあります。

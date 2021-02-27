# template pattern

## 目的

推論器に必要なリソースをディレクトリ構成と jinja2 テンプレートで提供します。

## 前提

- Python 3.8 以上

## 使い方

0. カレントディレクトリ

```sh
$ pwd
~/ml-system-in-actions/chapter4_serving_patterns/template_pattern
```

1. ライブラリのインストール

```sh
$ pip install -r requirements.txt
```

2. テンプレートからサンプルの推論機をビルド

推論器のテンプレートは以下のディレクトリ、ファイル構成となっています。

- template: テンプレートとなるディレクトリ
- template_files: 変数の変換が必要なファイル一式
- correspond_file_path.yaml: template_files 配下のファイルを変換後に配置するファイルパスを指定
- vars.yaml: 変数
- builder.py: テンプレートから推論器プロジェクトを作成するスクリプト

```sh
# テンプレートとなるファイル一覧と変換後のファイルパス
$ cat correspond_file_path.yaml
# Dockerfile.j2: "{}/Dockerfile"
# prediction.py.j2: "{}/src/ml/prediction.py"
# routers.py.j2: "{}/src/app/routers/routers.py"
# deployment.yml.j2: "{}/manifests/deployment.yml"
# namespace.yml.j2: "{}/manifests/namespace.yml"
# makefile.j2: "{}/makefile"
# docker-compose.yml.j2: "{}/docker-compose.yml"

# 変数
$ cat vars.yaml
# name: sample
# model_file_name: iris_svc.onnx
# label_file_name: label.json
# data_type: float32
# data_structure: (1,4)
# data_sample: [[5.1, 3.5, 1.4, 0.2]]
# prediction_type: float32
# prediction_structure: (1,3)
# prediction_sample: [0.97093159, 0.01558308, 0.01348537]

# 推論器プロジェクトをビルド
$ python \
    -m builder \
    --name sample \
    --variable_file vars.yaml \
    --correspond_file_path correspond_file_path.yaml

# これで./sampleディレクトリ配下に推論器のプログラムが出来上がります。
```

3. サンプル推論器プロジェクトの確認

作成されたプログラムは以下のような構成になっています。
モデルとラベルファイルを `sample/models/` ディレクトリに配置すれば完成です。

```sh
$ tree sample
# sample
# ├── Dockerfile
# ├── __init__.py
# ├── docker-compose.yml
# ├── makefile
# ├── manifests
# │   ├── deployment.yml
# │   └── namespace.yml
# ├── models
# ├── requirements.txt
# ├── run.sh
# └── src
#     ├── __init__.py
#     ├── app
#     │   ├── __init__.py
#     │   ├── app.py
#     │   └── routers
#     │       ├── __init__.py
#     │       └── routers.py
#     ├── configurations.py
#     ├── constants.py
#     ├── ml
#     │   ├── __init__.py
#     │   └── prediction.py
#     └── utils
#         ├── __init__.py
#         ├── logging.conf
#         └── profiler.py
```

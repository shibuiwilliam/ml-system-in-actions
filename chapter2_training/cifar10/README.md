# Cifar10 学習パイプライン

## 目的

MLFlow を用いた Cifar10 データセットの学習パイプラインです。

## 前提

- Python 3.8 以上
- Docker
- MLFlow
- Anaconda

本プログラムでは conda コマンドを使用するため、Anaconda/miniconda を使います。
Anaconda/miniconda の実行環境は pyenv 等仮想環境で用意することを推奨します。
pyenv で環境構築する方法は以下のとおりです。

```sh
# 2021/10時点最新のanaconda環境を選択
$ pyenv install anaconda3-2021.05
Downloading Anaconda3-2021.05-MacOSX-x86_64.sh...
-> https://repo.continuum.io/archive/Anaconda3-2021.05-MacOSX-x86_64.sh
Installing Anaconda3-2021.05-MacOSX-x86_64...
Installed Anaconda3-2021.05-MacOSX-x86_64 to /Users/shibuiyuusuke/.pyenv/versions/anaconda3-2021.05

# pyenvで仮想環境にanaconda3-2021.05を選択
$ pyenv local anaconda3-2021.05

# 仮想環境がanaconda3-2020.05になっていることを確認
$ pyenv versions
  system
* anaconda3-2021.05

# 依存ライブラリをインストール
$ pip install -r requirements.txt

# mlflowをインストール
$ pip install mlflow
```

本プログラムは `/tmp/ml-system-in-actions/chapter2_training/cifar10/` ディレクトリで実行することを想定して書かれています。
レポジトリを `/tmp/` ディレクトリにクローンして実行するか、他ディレクトリにある場合は `/tmp/ml-system-in-actions/chapter2_training/cifar10/` にシンボリックリンクを張って実行してください。

## 使い方

1. ライブラリインストール

```sh
$ make dev
# 実行されるコマンド
# pip install -r requirements.txt
# 出力は省略
```

2. 学習用 Docker イメージのビルド

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
# mlflow run . --no-conda
```

学習が完了するまで、数分から数十分かかることがあります。

実行ログ（一部）は以下になります。

<details><summary>ログ</summary><div>

```sh
$ make train
mlflow run . --no-conda
2021/10/09 16:00:32 INFO mlflow.projects.utils: === Created directory /var/folders/v8/bvkzgn8j1ws6y76t4z5nt6280000gn/T/tmp_sq3me5q for downloading remote URIs passed to arguments of type 'path' ===
2021/10/09 16:00:32 INFO mlflow.projects.backend.local: === Running command 'python -m main \
  --preprocess_data cifar10 \
  --preprocess_downstream /opt/data/preprocess/ \
  --preprocess_cached_data_id '' \
  --train_downstream /opt/data/model/ \
  --train_tensorboard /opt/data/tensorboard/ \
  --train_epochs 1 \
  --train_batch_size 32 \
  --train_num_workers 4 \
  --train_learning_rate 0.001 \
  --train_model_type vgg11 \
  --building_dockerfile_path ./Dockerfile \
  --building_model_filename cifar10_0.onnx \
  --building_entrypoint_path ./onnx_runtime_server_entrypoint.sh \
  --evaluate_downstream ./evaluate/
' in run with ID '4966d91cb81040dda0291f1840484c06' ===
2021/10/09 16:00:34 INFO mlflow.projects.docker: === Building docker image cifar10_initial:4fb1b3e ===
2021/10/09 16:00:35 INFO mlflow.projects.utils: === Created directory /var/folders/v8/bvkzgn8j1ws6y76t4z5nt6280000gn/T/tmp23vlfjfu for downloading remote URIs passed to arguments of type 'path' ===
2021/10/09 16:00:35 INFO mlflow.projects.backend.local: === Running command 'docker run --rm -v /private/tmp/ml-system-in-actions/chapter2_training/cifar10/mlruns:/mlflow/tmp/mlruns -v /private/tmp/ml-system-in-actions/chapter2_training/cifar10/mlruns/0/a581fe06ecad4d4cb596db74e4cd2a57/artifacts:/private/tmp/ml-system-in-actions/chapter2_training/cifar10/mlruns/0/a581fe06ecad4d4cb596db74e4cd2a57/artifacts -v $(pwd)/data:/opt/data -v /tmp/ml-system-in-actions/chapter2_training/cifar10/mlruns:/tmp/mlruns -e MLFLOW_RUN_ID=a581fe06ecad4d4cb596db74e4cd2a57 -e MLFLOW_TRACKING_URI=file:///mlflow/tmp/mlruns -e MLFLOW_EXPERIMENT_ID=0 cifar10_initial:4fb1b3e python -m src.preprocess \
  --data cifar10 \
  --downstream /opt/data/preprocess/ \
  --cached_data_id ''
' in run with ID 'a581fe06ecad4d4cb596db74e4cd2a57' ===
100.0%Downloading https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz to /opt/data/preprocess/cifar-10-python.tar.gz
Extracting /opt/data/preprocess/cifar-10-python.tar.gz to /opt/data/preprocess/
Files already downloaded and verified

2021/10/09 16:14:34 INFO mlflow.projects: === Run (ID 'a581fe06ecad4d4cb596db74e4cd2a57') succeeded ===
2021/10/09 16:14:35 INFO mlflow.projects.docker: === Building docker image cifar10_initial:4fb1b3e ===
2021/10/09 16:14:35 INFO mlflow.projects.utils: === Created directory /var/folders/v8/bvkzgn8j1ws6y76t4z5nt6280000gn/T/tmpmp17bac5 for downloading remote URIs passed to arguments of type 'path' ===
2021/10/09 16:14:35 INFO mlflow.projects.backend.local: === Running command 'docker run --rm -v /private/tmp/ml-system-in-actions/chapter2_training/cifar10/mlruns:/mlflow/tmp/mlruns -v /private/tmp/ml-system-in-actions/chapter2_training/cifar10/mlruns/0/bd9f50269f6f40d2a4c5cf832f892384/artifacts:/private/tmp/ml-system-in-actions/chapter2_training/cifar10/mlruns/0/bd9f50269f6f40d2a4c5cf832f892384/artifacts -v $(pwd)/data:/opt/data -v /tmp/ml-system-in-actions/chapter2_training/cifar10/mlruns:/tmp/mlruns -e MLFLOW_RUN_ID=bd9f50269f6f40d2a4c5cf832f892384 -e MLFLOW_TRACKING_URI=file:///mlflow/tmp/mlruns -e MLFLOW_EXPERIMENT_ID=0 cifar10_initial:4fb1b3e python -m src.train \
  --upstream /tmp/mlruns/0/a581fe06ecad4d4cb596db74e4cd2a57/artifacts/downstream_directory \
  --downstream /opt/data/model/ \
  --tensorboard /opt/data/tensorboard/ \
  --epochs 1 \
  --batch_size 32 \
  --num_workers 4 \
  --learning_rate 0.001 \
  --model_type vgg11
' in run with ID 'bd9f50269f6f40d2a4c5cf832f892384' ===
INFO:src.model:loaded: 50000 data
INFO:src.model:loaded: 10000 data
INFO:src.model:start training...
INFO:src.model:starting epoch: 0
INFO:src.model:[0, 199] loss: 2.273090735077858 duration: 91.27972292900085
INFO:src.model:[0, 399] loss: 1.963498272895813 duration: 57.59314465522766
INFO:src.model:[0, 599] loss: 1.9160682064294816 duration: 55.94656205177307
INFO:src.model:[0, 799] loss: 1.8396001029014588 duration: 60.194833278656006
INFO:src.model:[0, 999] loss: 1.7468485635519029 duration: 58.08973455429077
INFO:src.model:[0, 1199] loss: 1.7104253977537156 duration: 56.7458815574646
INFO:src.model:[0, 1399] loss: 1.6527180963754653 duration: 87.19056677818298
INFO:src.model:[0] duration in seconds: 516.8108649253845
INFO:src.model:Accuracy: 37.169999999999995, Loss: 0.048952482640743256
INFO:src.model:save checkpoints: /opt/data/model/epoch_0_loss_0.048952482640743256.pth
INFO:src.model:Accuracy: 37.169999999999995, Loss: 0.048952482640743256
INFO:__main__:Latest performance: Accuracy: 37.169999999999995, Loss: 0.048952482640743256
graph(%input : Float(1, 3, 32, 32, strides=[3072, 1024, 32, 1], requires_grad=0, device=cpu),
      %classifier.0.weight : Float(512, 512, strides=[512, 1], requires_grad=1, device=cpu),
      %classifier.0.bias : Float(512, strides=[1], requires_grad=1, device=cpu),
      %classifier.3.weight : Float(32, 512, strides=[512, 1], requires_grad=1, device=cpu),
      %classifier.3.bias : Float(32, strides=[1], requires_grad=1, device=cpu),
      %classifier.6.weight : Float(10, 32, strides=[32, 1], requires_grad=1, device=cpu),
      %classifier.6.bias : Float(10, strides=[1], requires_grad=1, device=cpu),
      %106 : Float(64, 3, 3, 3, strides=[27, 9, 3, 1], requires_grad=0, device=cpu),
      %107 : Float(64, strides=[1], requires_grad=0, device=cpu),
      %109 : Float(128, 64, 3, 3, strides=[576, 9, 3, 1], requires_grad=0, device=cpu),
      %110 : Float(128, strides=[1], requires_grad=0, device=cpu),
      %112 : Float(256, 128, 3, 3, strides=[1152, 9, 3, 1], requires_grad=0, device=cpu),
      %113 : Float(256, strides=[1], requires_grad=0, device=cpu),
      %115 : Float(256, 256, 3, 3, strides=[2304, 9, 3, 1], requires_grad=0, device=cpu),
      %116 : Float(256, strides=[1], requires_grad=0, device=cpu),
      %118 : Float(512, 256, 3, 3, strides=[2304, 9, 3, 1], requires_grad=0, device=cpu),
      %119 : Float(512, strides=[1], requires_grad=0, device=cpu),
      %121 : Float(512, 512, 3, 3, strides=[4608, 9, 3, 1], requires_grad=0, device=cpu),
      %122 : Float(512, strides=[1], requires_grad=0, device=cpu),
      %124 : Float(512, 512, 3, 3, strides=[4608, 9, 3, 1], requires_grad=0, device=cpu),
      %125 : Float(512, strides=[1], requires_grad=0, device=cpu),
      %127 : Float(512, 512, 3, 3, strides=[4608, 9, 3, 1], requires_grad=0, device=cpu),
      %128 : Float(512, strides=[1], requires_grad=0, device=cpu),
      %129 : Long(1, strides=[1], requires_grad=0, device=cpu)):
  %105 : Float(1, 64, 32, 32, strides=[65536, 1024, 32, 1], requires_grad=1, device=cpu) = onnx::Conv[dilations=[1, 1], group=1, kernel_shape=[3, 3], pads=[1, 1, 1, 1], strides=[1, 1]](%input, %106, %107)
  %65 : Float(1, 64, 32, 32, strides=[65536, 1024, 32, 1], requires_grad=1, device=cpu) = onnx::Relu(%105) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:1296:0
  %66 : Float(1, 64, 16, 16, strides=[16384, 256, 16, 1], requires_grad=1, device=cpu) = onnx::MaxPool[kernel_shape=[2, 2], pads=[0, 0, 0, 0], strides=[2, 2]](%65) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:718:0
  %108 : Float(1, 128, 16, 16, strides=[32768, 256, 16, 1], requires_grad=1, device=cpu) = onnx::Conv[dilations=[1, 1], group=1, kernel_shape=[3, 3], pads=[1, 1, 1, 1], strides=[1, 1]](%66, %109, %110)
  %69 : Float(1, 128, 16, 16, strides=[32768, 256, 16, 1], requires_grad=1, device=cpu) = onnx::Relu(%108) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:1296:0
  %70 : Float(1, 128, 8, 8, strides=[8192, 64, 8, 1], requires_grad=1, device=cpu) = onnx::MaxPool[kernel_shape=[2, 2], pads=[0, 0, 0, 0], strides=[2, 2]](%69) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:718:0
  %111 : Float(1, 256, 8, 8, strides=[16384, 64, 8, 1], requires_grad=1, device=cpu) = onnx::Conv[dilations=[1, 1], group=1, kernel_shape=[3, 3], pads=[1, 1, 1, 1], strides=[1, 1]](%70, %112, %113)
  %73 : Float(1, 256, 8, 8, strides=[16384, 64, 8, 1], requires_grad=1, device=cpu) = onnx::Relu(%111) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:1296:0
  %114 : Float(1, 256, 8, 8, strides=[16384, 64, 8, 1], requires_grad=1, device=cpu) = onnx::Conv[dilations=[1, 1], group=1, kernel_shape=[3, 3], pads=[1, 1, 1, 1], strides=[1, 1]](%73, %115, %116)
  %76 : Float(1, 256, 8, 8, strides=[16384, 64, 8, 1], requires_grad=1, device=cpu) = onnx::Relu(%114) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:1296:0
  %77 : Float(1, 256, 4, 4, strides=[4096, 16, 4, 1], requires_grad=1, device=cpu) = onnx::MaxPool[kernel_shape=[2, 2], pads=[0, 0, 0, 0], strides=[2, 2]](%76) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:718:0
  %117 : Float(1, 512, 4, 4, strides=[8192, 16, 4, 1], requires_grad=1, device=cpu) = onnx::Conv[dilations=[1, 1], group=1, kernel_shape=[3, 3], pads=[1, 1, 1, 1], strides=[1, 1]](%77, %118, %119)
  %80 : Float(1, 512, 4, 4, strides=[8192, 16, 4, 1], requires_grad=1, device=cpu) = onnx::Relu(%117) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:1296:0
  %120 : Float(1, 512, 4, 4, strides=[8192, 16, 4, 1], requires_grad=1, device=cpu) = onnx::Conv[dilations=[1, 1], group=1, kernel_shape=[3, 3], pads=[1, 1, 1, 1], strides=[1, 1]](%80, %121, %122)
  %83 : Float(1, 512, 4, 4, strides=[8192, 16, 4, 1], requires_grad=1, device=cpu) = onnx::Relu(%120) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:1296:0
  %84 : Float(1, 512, 2, 2, strides=[2048, 4, 2, 1], requires_grad=1, device=cpu) = onnx::MaxPool[kernel_shape=[2, 2], pads=[0, 0, 0, 0], strides=[2, 2]](%83) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:718:0
  %123 : Float(1, 512, 2, 2, strides=[2048, 4, 2, 1], requires_grad=1, device=cpu) = onnx::Conv[dilations=[1, 1], group=1, kernel_shape=[3, 3], pads=[1, 1, 1, 1], strides=[1, 1]](%84, %124, %125)
  %87 : Float(1, 512, 2, 2, strides=[2048, 4, 2, 1], requires_grad=1, device=cpu) = onnx::Relu(%123) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:1296:0
  %126 : Float(1, 512, 2, 2, strides=[2048, 4, 2, 1], requires_grad=1, device=cpu) = onnx::Conv[dilations=[1, 1], group=1, kernel_shape=[3, 3], pads=[1, 1, 1, 1], strides=[1, 1]](%87, %127, %128)
  %90 : Float(1, 512, 2, 2, strides=[2048, 4, 2, 1], requires_grad=1, device=cpu) = onnx::Relu(%126) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:1296:0
  %91 : Float(1, 512, 1, 1, strides=[512, 1, 1, 1], requires_grad=1, device=cpu) = onnx::MaxPool[kernel_shape=[2, 2], pads=[0, 0, 0, 0], strides=[2, 2]](%90) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:718:0
  %92 : Long(4, strides=[1], device=cpu) = onnx::Shape(%91)
  %93 : Long(device=cpu) = onnx::Constant[value={0}]()
  %94 : Long(device=cpu) = onnx::Gather[axis=0](%92, %93) # /mlflow/projects/code/src/model.py:137:0
  %96 : Long(1, strides=[1], device=cpu) = onnx::Unsqueeze[axes=[0]](%94)
  %98 : Long(2, strides=[1], device=cpu) = onnx::Concat[axis=0](%96, %129)
  %99 : Float(1, 512, strides=[512, 1], requires_grad=1, device=cpu) = onnx::Reshape(%91, %98) # /mlflow/projects/code/src/model.py:137:0
  %100 : Float(1, 512, strides=[512, 1], requires_grad=1, device=cpu) = onnx::Gemm[alpha=1., beta=1., transB=1](%99, %classifier.0.weight, %classifier.0.bias) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:1847:0
  %101 : Float(1, 512, strides=[512, 1], requires_grad=1, device=cpu) = onnx::Relu(%100) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:1168:0
  %102 : Float(1, 32, strides=[32, 1], requires_grad=1, device=cpu) = onnx::Gemm[alpha=1., beta=1., transB=1](%101, %classifier.3.weight, %classifier.3.bias) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:1847:0
  %103 : Float(1, 32, strides=[32, 1], requires_grad=1, device=cpu) = onnx::Relu(%102) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:1168:0
  %output : Float(1, 10, strides=[10, 1], requires_grad=1, device=cpu) = onnx::Gemm[alpha=1., beta=1., transB=1](%103, %classifier.6.weight, %classifier.6.bias) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:1847:0
  return (%output)

2021/10/09 16:27:24 INFO mlflow.projects: === Run (ID 'bd9f50269f6f40d2a4c5cf832f892384') succeeded ===
2021/10/09 16:27:29 INFO mlflow.utils.conda: === Creating conda environment mlflow-896ad7ba51492e700af933e0b293ec0fc9aface0 ===
Collecting package metadata (repodata.json): done
Solving environment: done


==> WARNING: A newer version of conda exists. <==
  current version: 4.10.1
  latest version: 4.10.3

Please update conda by running

    $ conda update -n base -c defaults conda



Downloading and Extracting Packages
openssl-1.1.1l       | 2.2 MB    | ##################################################################################### | 100%
certifi-2021.5.30    | 139 KB    | ##################################################################################### | 100%
ca-certificates-2021 | 116 KB    | ##################################################################################### | 100%
tk-8.6.11            | 3.0 MB    | ##################################################################################### | 100%
setuptools-58.0.4    | 791 KB    | ##################################################################################### | 100%
pip-21.2.4           | 1.8 MB    | ##################################################################################### | 100%
wheel-0.37.0         | 33 KB     | ##################################################################################### | 100%
sqlite-3.36.0        | 1.1 MB    | ##################################################################################### | 100%
libcxx-12.0.0        | 805 KB    | ##################################################################################### | 100%
python-3.8.11        | 10.3 MB   | ##################################################################################### | 100%
Preparing transaction: done
Verifying transaction: done
Executing transaction: done
Installing pip dependencies: - Ran pip subprocess with arguments:
['/Users/shibuiyuusuke/.pyenv/versions/anaconda3-2021.05/envs/mlflow-896ad7ba51492e700af933e0b293ec0fc9aface0/bin/python', '-m', 'pip', 'install', '-U', '-r', '/private/tmp/ml-system-in-actions/chapter2_training/cifar10/building/condaenv.snzeiirk.requirements.txt']
Pip subprocess output:
Collecting mlflow
  Using cached mlflow-1.20.2-py3-none-any.whl (14.6 MB)
Collecting sqlalchemy
  Downloading SQLAlchemy-1.4.25-cp38-cp38-macosx_10_14_x86_64.whl (1.5 MB)
Collecting click>=7.0
  Using cached click-8.0.2-py3-none-any.whl (97 kB)
Collecting alembic<=1.4.1
  Using cached alembic-1.4.1-py2.py3-none-any.whl
Collecting protobuf>=3.7.0
  Using cached protobuf-3.18.1-cp38-cp38-macosx_10_9_x86_64.whl (1.0 MB)
Collecting Flask
  Downloading Flask-2.0.2-py3-none-any.whl (95 kB)
Collecting prometheus-flask-exporter
  Using cached prometheus_flask_exporter-0.18.3-py3-none-any.whl (17 kB)
Collecting docker>=4.0.0
  Using cached docker-5.0.3-py2.py3-none-any.whl (146 kB)
Collecting entrypoints
  Using cached entrypoints-0.3-py2.py3-none-any.whl (11 kB)
Collecting numpy
  Downloading numpy-1.21.2-cp38-cp38-macosx_10_9_x86_64.whl (16.9 MB)
Collecting pandas
  Downloading pandas-1.3.3-cp38-cp38-macosx_10_9_x86_64.whl (11.4 MB)
Collecting pytz
  Downloading pytz-2021.3-py2.py3-none-any.whl (503 kB)
Collecting gitpython>=2.1.0
  Using cached GitPython-3.1.24-py3-none-any.whl (180 kB)
Collecting sqlparse>=0.3.1
  Using cached sqlparse-0.4.2-py3-none-any.whl (42 kB)
Collecting cloudpickle
  Downloading cloudpickle-2.0.0-py3-none-any.whl (25 kB)
Collecting requests>=2.17.3
  Using cached requests-2.26.0-py2.py3-none-any.whl (62 kB)
Collecting gunicorn
  Using cached gunicorn-20.1.0-py3-none-any.whl (79 kB)
Collecting querystring-parser
  Using cached querystring_parser-1.2.4-py2.py3-none-any.whl (7.9 kB)
Collecting databricks-cli>=0.8.7
  Using cached databricks_cli-0.15.0-py3-none-any.whl
Collecting importlib-metadata!=4.7.0,>=3.7.0
  Using cached importlib_metadata-4.8.1-py3-none-any.whl (17 kB)
Collecting packaging
  Using cached packaging-21.0-py3-none-any.whl (40 kB)
Collecting pyyaml>=5.1
  Using cached PyYAML-5.4.1-cp38-cp38-macosx_10_9_x86_64.whl (253 kB)
Collecting Mako
  Using cached Mako-1.1.5-py2.py3-none-any.whl (75 kB)
Collecting python-editor>=0.3
  Using cached python_editor-1.0.4-py3-none-any.whl (4.9 kB)
Collecting python-dateutil
  Using cached python_dateutil-2.8.2-py2.py3-none-any.whl (247 kB)
Collecting tabulate>=0.7.7
  Using cached tabulate-0.8.9-py3-none-any.whl (25 kB)
Collecting six>=1.10.0
  Using cached six-1.16.0-py2.py3-none-any.whl (11 kB)
Collecting websocket-client>=0.32.0
  Using cached websocket_client-1.2.1-py2.py3-none-any.whl (52 kB)
Collecting gitdb<5,>=4.0.1
  Using cached gitdb-4.0.7-py3-none-any.whl (63 kB)
Collecting typing-extensions>=3.7.4.3
  Using cached typing_extensions-3.10.0.2-py3-none-any.whl (26 kB)
Collecting smmap<5,>=3.0.1
  Using cached smmap-4.0.0-py2.py3-none-any.whl (24 kB)
Collecting zipp>=0.5
  Using cached zipp-3.6.0-py3-none-any.whl (5.3 kB)
Collecting charset-normalizer~=2.0.0
  Using cached charset_normalizer-2.0.6-py3-none-any.whl (37 kB)
Collecting idna<4,>=2.5
  Using cached idna-3.2-py3-none-any.whl (59 kB)
Collecting urllib3<1.27,>=1.21.1
  Downloading urllib3-1.26.7-py2.py3-none-any.whl (138 kB)
Requirement already satisfied: certifi>=2017.4.17 in /Users/shibuiyuusuke/.pyenv/versions/anaconda3-2021.05/envs/mlflow-896ad7ba51492e700af933e0b293ec0fc9aface0/lib/python3.8/site-packages (from requests>=2.17.3->mlflow->-r /private/tmp/ml-system-in-actions/chapter2_training/cifar10/building/condaenv.snzeiirk.requirements.txt (line 1)) (2021.5.30)
Collecting greenlet!=0.4.17
  Downloading greenlet-1.1.2-cp38-cp38-macosx_10_14_x86_64.whl (92 kB)
Collecting Jinja2>=3.0
  Downloading Jinja2-3.0.2-py3-none-any.whl (133 kB)
Collecting Werkzeug>=2.0
  Downloading Werkzeug-2.0.2-py3-none-any.whl (288 kB)
Collecting itsdangerous>=2.0
  Using cached itsdangerous-2.0.1-py3-none-any.whl (18 kB)
Collecting MarkupSafe>=2.0
  Using cached MarkupSafe-2.0.1-cp38-cp38-macosx_10_9_x86_64.whl (13 kB)
Requirement already satisfied: setuptools>=3.0 in /Users/shibuiyuusuke/.pyenv/versions/anaconda3-2021.05/envs/mlflow-896ad7ba51492e700af933e0b293ec0fc9aface0/lib/python3.8/site-packages (from gunicorn->mlflow->-r /private/tmp/ml-system-in-actions/chapter2_training/cifar10/building/condaenv.snzeiirk.requirements.txt (line 1)) (58.0.4)
Collecting pyparsing>=2.0.2
  Using cached pyparsing-2.4.7-py2.py3-none-any.whl (67 kB)
Collecting prometheus-client
  Using cached prometheus_client-0.11.0-py2.py3-none-any.whl (56 kB)
Installing collected packages: MarkupSafe, Werkzeug, urllib3, smmap, six, Jinja2, itsdangerous, idna, greenlet, click, charset-normalizer, zipp, websocket-client, typing-extensions, tabulate, sqlalchemy, requests, pytz, python-editor, python-dateutil, pyparsing, prometheus-client, numpy, Mako, gitdb, Flask, sqlparse, querystring-parser, pyyaml, protobuf, prometheus-flask-exporter, pandas, packaging, importlib-metadata, gunicorn, gitpython, entrypoints, docker, databricks-cli, cloudpickle, alembic, mlflow
Successfully installed Flask-2.0.2 Jinja2-3.0.2 Mako-1.1.5 MarkupSafe-2.0.1 Werkzeug-2.0.2 alembic-1.4.1 charset-normalizer-2.0.6 click-8.0.2 cloudpickle-2.0.0 databricks-cli-0.15.0 docker-5.0.3 entrypoints-0.3 gitdb-4.0.7 gitpython-3.1.24 greenlet-1.1.2 gunicorn-20.1.0 idna-3.2 importlib-metadata-4.8.1 itsdangerous-2.0.1 mlflow-1.20.2 numpy-1.21.2 packaging-21.0 pandas-1.3.3 prometheus-client-0.11.0 prometheus-flask-exporter-0.18.3 protobuf-3.18.1 pyparsing-2.4.7 python-dateutil-2.8.2 python-editor-1.0.4 pytz-2021.3 pyyaml-5.4.1 querystring-parser-1.2.4 requests-2.26.0 six-1.16.0 smmap-4.0.0 sqlalchemy-1.4.25 sqlparse-0.4.2 tabulate-0.8.9 typing-extensions-3.10.0.2 urllib3-1.26.7 websocket-client-1.2.1 zipp-3.6.0

done
#
# To activate this environment, use
#
#     $ conda activate mlflow-896ad7ba51492e700af933e0b293ec0fc9aface0
#
# To deactivate an active environment, use
#
#     $ conda deactivate

2021/10/09 16:28:53 INFO mlflow.projects.utils: === Created directory /var/folders/v8/bvkzgn8j1ws6y76t4z5nt6280000gn/T/tmpt1ru89c1 for downloading remote URIs passed to arguments of type 'path' ===
2021/10/09 16:28:53 INFO mlflow.projects.backend.local: === Running command 'source /Users/shibuiyuusuke/.pyenv/versions/anaconda3-2021.05/bin/../etc/profile.d/conda.sh && conda activate mlflow-896ad7ba51492e700af933e0b293ec0fc9aface0 1>&2 && cp ../mlruns/0/bd9f50269f6f40d2a4c5cf832f892384/artifacts/cifar10_0.onnx ./ && \
docker build \
  -t shibui/ml-system-in-actions:training_pattern_cifar10_evaluate_0 \
  -f ./Dockerfile \
  --build-arg model_filename=cifar10_0.onnx \
  --build-arg model_directory=mlruns/0/bd9f50269f6f40d2a4c5cf832f892384/artifacts \
  --build-arg entrypoint_path=./onnx_runtime_server_entrypoint.sh \
  .' in run with ID '3379a87628b94369af71d5e27cf16389' ===
[+] Building 12.9s (11/11) FINISHED
 => [internal] load build definition from Dockerfile                                                                       0.0s
 => => transferring dockerfile: 564B                                                                                       0.0s
 => [internal] load .dockerignore                                                                                          0.0s
 => => transferring context: 2B                                                                                            0.0s
 => [internal] load metadata for mcr.microsoft.com/onnxruntime/server:latest                                               0.9s
 => [1/6] FROM mcr.microsoft.com/onnxruntime/server:latest@sha256:a23da0977bbc4aca4d3de56ad648ebde86031e61d7a3b7cbe1daae  11.0s
 => => resolve mcr.microsoft.com/onnxruntime/server:latest@sha256:a23da0977bbc4aca4d3de56ad648ebde86031e61d7a3b7cbe1daaeb  0.0s
 => => sha256:0556947b2a78463ec9e30b0da9c52d315074116e376d3e348b333ef854b83cd8 4.77kB / 4.77kB                             0.0s
 => => sha256:04a3282d9c4be54603a46a0828ff0d7a992a72289c242c2301e704f658f00717 531B / 531B                                 0.4s
 => => sha256:a23da0977bbc4aca4d3de56ad648ebde86031e61d7a3b7cbe1daaebbc7f6ad3d 1.99kB / 1.99kB                             0.0s
 => => sha256:a1298f4ce99037bf3099adffe30b6a0096c592788fb611f1a2be2f8a494b8572 44.11MB / 44.11MB                           6.3s
 => => sha256:9b0d3db6dc039e138ede35bcf3a318c5b14545265d8fc6b55da49c5b57ffc32c 840B / 840B                                 0.4s
 => => sha256:8269c605f3f1f60eacd23c11d08771ee696182b7523ed09793980f5d9020ff7c 170B / 170B                                 0.6s
 => => sha256:682bfba003ea35f8102c4d444279a16ca72b8ee93cabf628982edc550cc023cd 123B / 123B                                 0.6s
 => => sha256:800b34ff9c7db72abee7e58387971dfa06cfc81986a2fe983600eeae14d6875b 2.58MB / 2.58MB                             1.7s
 => => sha256:4257e5c2fefd21baaf6c23d4516e3542391b646bf80300fd42d9a0b5ea3986c0 4.09MB / 4.09MB                             1.6s
 => => sha256:273ae94580cc52b890c6ddd9142aac95403d13db72ff2cd08680d931b53985cf 19.01MB / 19.01MB                           5.2s
 => => extracting sha256:a1298f4ce99037bf3099adffe30b6a0096c592788fb611f1a2be2f8a494b8572                                  2.8s
 => => extracting sha256:04a3282d9c4be54603a46a0828ff0d7a992a72289c242c2301e704f658f00717                                  0.0s
 => => extracting sha256:9b0d3db6dc039e138ede35bcf3a318c5b14545265d8fc6b55da49c5b57ffc32c                                  0.0s
 => => extracting sha256:8269c605f3f1f60eacd23c11d08771ee696182b7523ed09793980f5d9020ff7c                                  0.0s
 => => extracting sha256:682bfba003ea35f8102c4d444279a16ca72b8ee93cabf628982edc550cc023cd                                  0.0s
 => => extracting sha256:800b34ff9c7db72abee7e58387971dfa06cfc81986a2fe983600eeae14d6875b                                  0.2s
 => => extracting sha256:4257e5c2fefd21baaf6c23d4516e3542391b646bf80300fd42d9a0b5ea3986c0                                  0.2s
 => => extracting sha256:273ae94580cc52b890c6ddd9142aac95403d13db72ff2cd08680d931b53985cf                                  0.7s
 => [internal] load build context                                                                                          0.7s
 => => transferring context: 38.01MB                                                                                       0.7s
 => [2/6] WORKDIR /cifar10                                                                                                 0.2s
 => [3/6] COPY ./cifar10_0.onnx /cifar10/cifar10_0.onnx                                                                    0.1s
 => [4/6] WORKDIR /onnxruntime/server/                                                                                     0.0s
 => [5/6] COPY ././onnx_runtime_server_entrypoint.sh ./onnx_runtime_server_entrypoint.sh                                   0.0s
 => [6/6] RUN chmod +x onnx_runtime_server_entrypoint.sh                                                                   0.3s
 => exporting to image                                                                                                     0.3s
 => => exporting layers                                                                                                    0.3s
 => => writing image sha256:52b7f63dc167ce71631d669545ef3ff5eebf850b1f197b1b68e769182e4ae7d8                               0.0s
 => => naming to docker.io/shibui/ml-system-in-actions:training_pattern_cifar10_evaluate_0                                 0.0s

Use 'docker scan' to run Snyk tests against images to find vulnerabilities and learn how to fix them
2021/10/09 16:29:07 INFO mlflow.projects: === Run (ID '3379a87628b94369af71d5e27cf16389') succeeded ===
2021/10/09 16:29:09 INFO mlflow.utils.conda: === Creating conda environment mlflow-a5f0c06b2ecebc7d20239baa7c71ce611a46259e ===
Collecting package metadata (repodata.json): done
Solving environment: done


==> WARNING: A newer version of conda exists. <==
  current version: 4.10.1
  latest version: 4.10.3

Please update conda by running

    $ conda update -n base -c defaults conda


Preparing transaction: done
Verifying transaction: done
Executing transaction: done
Installing pip dependencies: | Ran pip subprocess with arguments:
['/Users/shibuiyuusuke/.pyenv/versions/anaconda3-2021.05/envs/mlflow-a5f0c06b2ecebc7d20239baa7c71ce611a46259e/bin/python', '-m', 'pip', 'install', '-U', '-r', '/private/tmp/ml-system-in-actions/chapter2_training/cifar10/evaluate/condaenv.abrmof73.requirements.txt']
Pip subprocess output:
Collecting mlflow
  Using cached mlflow-1.20.2-py3-none-any.whl (14.6 MB)
Collecting grpcio
  Using cached grpcio-1.41.0-cp38-cp38-macosx_10_10_x86_64.whl (3.9 MB)
Collecting Pillow
  Downloading Pillow-8.3.2-cp38-cp38-macosx_10_10_x86_64.whl (3.0 MB)
Collecting scikit-learn
  Downloading scikit_learn-1.0-cp38-cp38-macosx_10_13_x86_64.whl (7.9 MB)
Collecting numpy
  Using cached numpy-1.21.2-cp38-cp38-macosx_10_9_x86_64.whl (16.9 MB)
Collecting alembic<=1.4.1
  Using cached alembic-1.4.1-py2.py3-none-any.whl
Collecting Flask
  Using cached Flask-2.0.2-py3-none-any.whl (95 kB)
Collecting importlib-metadata!=4.7.0,>=3.7.0
  Using cached importlib_metadata-4.8.1-py3-none-any.whl (17 kB)
Collecting click>=7.0
  Using cached click-8.0.2-py3-none-any.whl (97 kB)
Collecting prometheus-flask-exporter
  Using cached prometheus_flask_exporter-0.18.3-py3-none-any.whl (17 kB)
Collecting sqlalchemy
  Using cached SQLAlchemy-1.4.25-cp38-cp38-macosx_10_14_x86_64.whl (1.5 MB)
Collecting gitpython>=2.1.0
  Using cached GitPython-3.1.24-py3-none-any.whl (180 kB)
Collecting protobuf>=3.7.0
  Using cached protobuf-3.18.1-cp38-cp38-macosx_10_9_x86_64.whl (1.0 MB)
Collecting pandas
  Using cached pandas-1.3.3-cp38-cp38-macosx_10_9_x86_64.whl (11.4 MB)
Collecting packaging
  Using cached packaging-21.0-py3-none-any.whl (40 kB)
Collecting gunicorn
  Using cached gunicorn-20.1.0-py3-none-any.whl (79 kB)
Collecting requests>=2.17.3
  Using cached requests-2.26.0-py2.py3-none-any.whl (62 kB)
Collecting entrypoints
  Using cached entrypoints-0.3-py2.py3-none-any.whl (11 kB)
Collecting pytz
  Using cached pytz-2021.3-py2.py3-none-any.whl (503 kB)
Collecting docker>=4.0.0
  Using cached docker-5.0.3-py2.py3-none-any.whl (146 kB)
Collecting cloudpickle
  Using cached cloudpickle-2.0.0-py3-none-any.whl (25 kB)
Collecting databricks-cli>=0.8.7
  Using cached databricks_cli-0.15.0-py3-none-any.whl
Collecting pyyaml>=5.1
  Using cached PyYAML-5.4.1-cp38-cp38-macosx_10_9_x86_64.whl (253 kB)
Collecting querystring-parser
  Using cached querystring_parser-1.2.4-py2.py3-none-any.whl (7.9 kB)
Collecting sqlparse>=0.3.1
  Using cached sqlparse-0.4.2-py3-none-any.whl (42 kB)
Collecting six>=1.5.2
  Using cached six-1.16.0-py2.py3-none-any.whl (11 kB)
Collecting scipy>=1.1.0
  Downloading scipy-1.7.1-cp38-cp38-macosx_10_9_x86_64.whl (32.6 MB)
Collecting joblib>=0.11
  Using cached joblib-1.1.0-py2.py3-none-any.whl (306 kB)
Collecting threadpoolctl>=2.0.0
  Using cached threadpoolctl-3.0.0-py3-none-any.whl (14 kB)
Collecting python-editor>=0.3
  Using cached python_editor-1.0.4-py3-none-any.whl (4.9 kB)
Collecting python-dateutil
  Using cached python_dateutil-2.8.2-py2.py3-none-any.whl (247 kB)
Collecting Mako
  Using cached Mako-1.1.5-py2.py3-none-any.whl (75 kB)
Collecting tabulate>=0.7.7
  Using cached tabulate-0.8.9-py3-none-any.whl (25 kB)
Collecting websocket-client>=0.32.0
  Using cached websocket_client-1.2.1-py2.py3-none-any.whl (52 kB)
Collecting typing-extensions>=3.7.4.3
  Using cached typing_extensions-3.10.0.2-py3-none-any.whl (26 kB)
Collecting gitdb<5,>=4.0.1
  Using cached gitdb-4.0.7-py3-none-any.whl (63 kB)
Collecting smmap<5,>=3.0.1
  Using cached smmap-4.0.0-py2.py3-none-any.whl (24 kB)
Collecting zipp>=0.5
  Using cached zipp-3.6.0-py3-none-any.whl (5.3 kB)
Collecting charset-normalizer~=2.0.0
  Using cached charset_normalizer-2.0.6-py3-none-any.whl (37 kB)
Requirement already satisfied: certifi>=2017.4.17 in /Users/shibuiyuusuke/.pyenv/versions/anaconda3-2021.05/envs/mlflow-a5f0c06b2ecebc7d20239baa7c71ce611a46259e/lib/python3.8/site-packages (from requests>=2.17.3->mlflow->-r /private/tmp/ml-system-in-actions/chapter2_training/cifar10/evaluate/condaenv.abrmof73.requirements.txt (line 1)) (2021.5.30)
Collecting urllib3<1.27,>=1.21.1
  Using cached urllib3-1.26.7-py2.py3-none-any.whl (138 kB)
Collecting idna<4,>=2.5
  Using cached idna-3.2-py3-none-any.whl (59 kB)
Collecting greenlet!=0.4.17
  Using cached greenlet-1.1.2-cp38-cp38-macosx_10_14_x86_64.whl (92 kB)
Collecting Werkzeug>=2.0
  Using cached Werkzeug-2.0.2-py3-none-any.whl (288 kB)
Collecting itsdangerous>=2.0
  Using cached itsdangerous-2.0.1-py3-none-any.whl (18 kB)
Collecting Jinja2>=3.0
  Using cached Jinja2-3.0.2-py3-none-any.whl (133 kB)
Collecting MarkupSafe>=2.0
  Using cached MarkupSafe-2.0.1-cp38-cp38-macosx_10_9_x86_64.whl (13 kB)
Requirement already satisfied: setuptools>=3.0 in /Users/shibuiyuusuke/.pyenv/versions/anaconda3-2021.05/envs/mlflow-a5f0c06b2ecebc7d20239baa7c71ce611a46259e/lib/python3.8/site-packages (from gunicorn->mlflow->-r /private/tmp/ml-system-in-actions/chapter2_training/cifar10/evaluate/condaenv.abrmof73.requirements.txt (line 1)) (58.0.4)
Collecting pyparsing>=2.0.2
  Using cached pyparsing-2.4.7-py2.py3-none-any.whl (67 kB)
Collecting prometheus-client
  Using cached prometheus_client-0.11.0-py2.py3-none-any.whl (56 kB)
Installing collected packages: MarkupSafe, Werkzeug, urllib3, smmap, six, Jinja2, itsdangerous, idna, greenlet, click, charset-normalizer, zipp, websocket-client, typing-extensions, tabulate, sqlalchemy, requests, pytz, python-editor, python-dateutil, pyparsing, prometheus-client, numpy, Mako, gitdb, Flask, threadpoolctl, sqlparse, scipy, querystring-parser, pyyaml, protobuf, prometheus-flask-exporter, pandas, packaging, joblib, importlib-metadata, gunicorn, gitpython, entrypoints, docker, databricks-cli, cloudpickle, alembic, scikit-learn, Pillow, mlflow, grpcio
Successfully installed Flask-2.0.2 Jinja2-3.0.2 Mako-1.1.5 MarkupSafe-2.0.1 Pillow-8.3.2 Werkzeug-2.0.2 alembic-1.4.1 charset-normalizer-2.0.6 click-8.0.2 cloudpickle-2.0.0 databricks-cli-0.15.0 docker-5.0.3 entrypoints-0.3 gitdb-4.0.7 gitpython-3.1.24 greenlet-1.1.2 grpcio-1.41.0 gunicorn-20.1.0 idna-3.2 importlib-metadata-4.8.1 itsdangerous-2.0.1 joblib-1.1.0 mlflow-1.20.2 numpy-1.21.2 packaging-21.0 pandas-1.3.3 prometheus-client-0.11.0 prometheus-flask-exporter-0.18.3 protobuf-3.18.1 pyparsing-2.4.7 python-dateutil-2.8.2 python-editor-1.0.4 pytz-2021.3 pyyaml-5.4.1 querystring-parser-1.2.4 requests-2.26.0 scikit-learn-1.0 scipy-1.7.1 six-1.16.0 smmap-4.0.0 sqlalchemy-1.4.25 sqlparse-0.4.2 tabulate-0.8.9 threadpoolctl-3.0.0 typing-extensions-3.10.0.2 urllib3-1.26.7 websocket-client-1.2.1 zipp-3.6.0

done
#
# To activate this environment, use
#
#     $ conda activate mlflow-a5f0c06b2ecebc7d20239baa7c71ce611a46259e
#
# To deactivate an active environment, use
#
#     $ conda deactivate

2021/10/09 16:30:05 INFO mlflow.projects.utils: === Created directory /var/folders/v8/bvkzgn8j1ws6y76t4z5nt6280000gn/T/tmpsdxheliz for downloading remote URIs passed to arguments of type 'path' ===
2021/10/09 16:30:05 INFO mlflow.projects.backend.local: === Running command 'source /Users/shibuiyuusuke/.pyenv/versions/anaconda3-2021.05/bin/../etc/profile.d/conda.sh && conda activate mlflow-a5f0c06b2ecebc7d20239baa7c71ce611a46259e 1>&2 && docker run \
  -it -d \
  --name training_pattern_cifar10_evaluate_0 \
  -p 50051:50051 shibui/ml-system-in-actions:training_pattern_cifar10_evaluate_0 && \
python -m src.evaluate \
  --upstream ../mlruns/0/bd9f50269f6f40d2a4c5cf832f892384/artifacts \
  --downstream ./evaluate/ \
  --test_data_directory ../mlruns/0/a581fe06ecad4d4cb596db74e4cd2a57/artifacts/downstream_directory/test
  ' in run with ID '801df0a55ee945518f884a08f398d740' ===
782de7a6f1c67b40275afe91312dd5f18befcf50400a53b841e76753579473b8
INFO:__main__:predict proba [[0.29046037793159485, 0.07903019338846207, 0.05096588656306267, 0.021699633449316025, 0.031009187921881676, 0.013215476647019386, 0.012070787139236927, 0.03407438471913338, 0.3405143618583679, 0.12695972621440887]]
INFO:__main__:predict label 8
INFO:__main__:../mlruns/0/a581fe06ecad4d4cb596db74e4cd2a57/artifacts/downstream_directory/test/9/tipper_truck_s_000048.png label: 9 predicted: 8 duration: 0.015868186950683594 seconds
INFO:__main__:predict proba [[0.015559987165033817, 0.5181851983070374, 0.002052417490631342, 0.0005123076261952519, 0.0001863305369624868, 0.0003374455845914781, 0.002682535210624337, 0.00034050876274704933, 0.020900070667266846, 0.4392431974411011]]
INFO:__main__:predict label 1

###########
### 中略 ###
###########


INFO:__main__:../mlruns/0/a581fe06ecad4d4cb596db74e4cd2a57/artifacts/downstream_directory/test/5/toy_dog_s_000013.png label: 5 predicted: 4 duration: 0.011266946792602539 seconds
INFO:__main__:predict proba [[0.005290620028972626, 0.0010339220752939582, 0.20407144725322723, 0.12005537748336792, 0.21151918172836304, 0.16939151287078857, 0.18023692071437836, 0.10347509384155273, 0.0013741046423092484, 0.0035517578944563866]]
INFO:__main__:predict label 4
INFO:__main__:../mlruns/0/a581fe06ecad4d4cb596db74e4cd2a57/artifacts/downstream_directory/test/5/maltese_s_000126.png label: 5 predicted: 4 duration: 0.011644124984741211 seconds
2021/10/09 16:31:58 INFO mlflow.projects: === Run (ID '801df0a55ee945518f884a08f398d740') succeeded ===
2021/10/09 16:31:58 INFO mlflow.projects: === Run (ID '4966d91cb81040dda0291f1840484c06') succeeded ===
```

</div></details>

4. 推論用コンテナの削除

```sh
# mlflowで起動される推論用のコンテナを削除します。
$ docker rm -f training_pattern_cifar10_evaluate_0
```

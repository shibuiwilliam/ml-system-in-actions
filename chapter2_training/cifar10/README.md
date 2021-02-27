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
# 2021/02時点最新のanaconda環境を選択
$ pyenv install anaconda3-5.3.1
Downloading Anaconda3-5.3.1-MacOSX-x86_64.sh.sh...
-> https://repo.continuum.io/archive/Anaconda3-5.3.1-MacOSX-x86_64.sh
Installing Anaconda3-5.3.1-MacOSX-x86_64.sh...
Installed Anaconda3-5.3.1-MacOSX-x86_64.sh to ~/.pyenv/versions/anaconda3-5.3.1

# pyenvで仮想環境にanaconda3-2020.02を選択
$ pyenv local anaconda3-5.3.1

# 仮想環境がanaconda3-2020.02になっていることを確認
$ pyenv versions
  system
* anaconda3-5.3.1

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
2021/02/11 07:07:41 INFO mlflow.projects.utils: === Created directory /tmp/tmpwp6xeymy for downloading remote URIs passed to arguments of type 'path' ===
2021/02/11 07:07:41 INFO mlflow.projects.backend.local: === Running command 'python -m main \
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
' in run with ID '16ca2fc7a707438fb999ffcc2ca0cc5f' ===
2021/02/11 07:08:27 INFO mlflow.projects.docker: === Building docker image cifar10_initial:2d89748 ===
2021/02/11 07:08:54 INFO mlflow.projects.utils: === Created directory /tmp/tmpqrouv_eh for downloading remote URIs passed to arguments of type 'path' ===
2021/02/11 07:08:54 INFO mlflow.projects.backend.local: === Running command 'docker run --rm -v /tmp/ml-system-in-actions/chapter2_training/cifar10/mlruns:/mlflow/tmp/mlruns -v /tmp/ml-system-in-actions/chapter2_training/cifar10/mlruns/0/d2ec649ed0254e99a9713e75da3dced9/artifacts:/tmp/ml-system-in-actions/chapter2_training/cifar10/mlruns/0/d2ec649ed0254e99a9713e75da3dced9/artifacts -v $(pwd)/data:/opt/data -v /tmp/ml-system-in-actions/chapter2_training/cifar10/mlruns:/tmp/mlruns -e MLFLOW_RUN_ID=d2ec649ed0254e99a9713e75da3dced9 -e MLFLOW_TRACKING_URI=file:///mlflow/tmp/mlruns -e MLFLOW_EXPERIMENT_ID=0 cifar10_initial:2d89748 python -m src.preprocess \
  --data cifar10 \
  --downstream /opt/data/preprocess/ \
  --cached_data_id ''
' in run with ID 'd2ec649ed0254e99a9713e75da3dced9' ===
Files already downloaded and verified
Files already downloaded and verified
2021/02/11 07:09:38 INFO mlflow.projects: === Run (ID 'd2ec649ed0254e99a9713e75da3dced9') succeeded ===
2021/02/11 07:09:49 INFO mlflow.projects.docker: === Building docker image cifar10_initial:2d89748 ===
2021/02/11 07:09:55 INFO mlflow.projects.utils: === Created directory /tmp/tmp4z7k8vf_ for downloading remote URIs passed to arguments of type 'path' ===
2021/02/11 07:09:55 INFO mlflow.projects.backend.local: === Running command 'docker run --rm -v /tmp/ml-system-in-actions/chapter2_training/cifar10/mlruns:/mlflow/tmp/mlruns -v /tmp/ml-system-in-actions/chapter2_training/cifar10/mlruns/0/597633d3c4f5494898559b4b1889d457/artifacts:/tmp/ml-system-in-actions/chapter2_training/cifar10/mlruns/0/597633d3c4f5494898559b4b1889d457/artifacts -v $(pwd)/data:/opt/data -v /tmp/ml-system-in-actions/chapter2_training/cifar10/mlruns:/tmp/mlruns -e MLFLOW_RUN_ID=597633d3c4f5494898559b4b1889d457 -e MLFLOW_TRACKING_URI=file:///mlflow/tmp/mlruns -e MLFLOW_EXPERIMENT_ID=0 cifar10_initial:2d89748 python -m src.train \
  --upstream /tmp/mlruns/0/d2ec649ed0254e99a9713e75da3dced9/artifacts/downstream_directory \
  --downstream /opt/data/model/ \
  --tensorboard /opt/data/tensorboard/ \
  --epochs 1 \
  --batch_size 32 \
  --num_workers 4 \
  --learning_rate 0.001 \
  --model_type vgg11
' in run with ID '597633d3c4f5494898559b4b1889d457' ===
/usr/local/lib/python3.8/site-packages/torch/cuda/__init__.py:52: UserWarning: CUDA initialization: Found no NVIDIA driver on your system. Please check that you have an NVIDIA GPU and installed a driver from http://www.nvidia.com/Download/index.aspx (Triggered internally at  /pytorch/c10/cuda/CUDAFunctions.cpp:100.)
  return torch._C._cuda_getDeviceCount() > 0
INFO:src.model:loaded: 50000 data
INFO:src.model:loaded: 10000 data
INFO:src.model:start training...
INFO:src.model:starting epoch: 0
INFO:src.model:[0, 199] loss: 2.312226449251175 duration: 54.222291231155396
INFO:src.model:[0, 399] loss: 2.3037538850307464 duration: 54.138527393341064
INFO:src.model:[0, 599] loss: 2.30290598988533 duration: 54.571797609329224
INFO:src.model:[0, 799] loss: 2.3030105102062226 duration: 61.33693838119507
INFO:src.model:[0, 999] loss: 2.303100422620773 duration: 61.62240767478943
INFO:src.model:[0, 1199] loss: 2.3030186557769774 duration: 60.76185894012451
INFO:src.model:[0, 1399] loss: 2.302838541269302 duration: 60.42561101913452
INFO:src.model:[0] duration in seconds: 456.4304406642914
INFO:src.model:Accuracy: 10.0, Loss: 0.07207702845335007
INFO:src.model:save checkpoints: /opt/data/model/epoch_0_loss_0.07207702845335007.pth
INFO:src.model:Accuracy: 10.0, Loss: 0.07207702845335007
INFO:__main__:Latest performance: Accuracy: 10.0, Loss: 0.07207702845335007
graph(%input : Float(1:3072, 3:1024, 32:32, 32:1, requires_grad=0, device=cpu),
      %classifier.0.weight : Float(512:512, 512:1, requires_grad=1, device=cpu),
      %classifier.0.bias : Float(512:1, requires_grad=1, device=cpu),
      %classifier.3.weight : Float(32:512, 512:1, requires_grad=1, device=cpu),
      %classifier.3.bias : Float(32:1, requires_grad=1, device=cpu),
      %classifier.6.weight : Float(10:32, 32:1, requires_grad=1, device=cpu),
      %classifier.6.bias : Float(10:1, requires_grad=1, device=cpu),
      %106 : Float(64:27, 3:9, 3:3, 3:1, requires_grad=0, device=cpu),
      %107 : Float(64:1, requires_grad=0, device=cpu),
      %109 : Float(128:576, 64:9, 3:3, 3:1, requires_grad=0, device=cpu),
      %110 : Float(128:1, requires_grad=0, device=cpu),
      %112 : Float(256:1152, 128:9, 3:3, 3:1, requires_grad=0, device=cpu),
      %113 : Float(256:1, requires_grad=0, device=cpu),
      %115 : Float(256:2304, 256:9, 3:3, 3:1, requires_grad=0, device=cpu),
      %116 : Float(256:1, requires_grad=0, device=cpu),
      %118 : Float(512:2304, 256:9, 3:3, 3:1, requires_grad=0, device=cpu),
      %119 : Float(512:1, requires_grad=0, device=cpu),
      %121 : Float(512:4608, 512:9, 3:3, 3:1, requires_grad=0, device=cpu),
      %122 : Float(512:1, requires_grad=0, device=cpu),
      %124 : Float(512:4608, 512:9, 3:3, 3:1, requires_grad=0, device=cpu),
      %125 : Float(512:1, requires_grad=0, device=cpu),
      %127 : Float(512:4608, 512:9, 3:3, 3:1, requires_grad=0, device=cpu),
      %128 : Float(512:1, requires_grad=0, device=cpu),
      %129 : Long(1:1, requires_grad=0, device=cpu)):
  %105 : Float(1:65536, 64:1024, 32:32, 32:1, requires_grad=1, device=cpu) = onnx::Conv[dilations=[1, 1], group=1, kernel_shape=[3, 3], pads=[1, 1, 1, 1], strides=[1, 1]](%input, %106, %107)
  %65 : Float(1:65536, 64:1024, 32:32, 32:1, requires_grad=1, device=cpu) = onnx::Relu(%105) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:1134:0
  %66 : Float(1:16384, 64:256, 16:16, 16:1, requires_grad=1, device=cpu) = onnx::MaxPool[kernel_shape=[2, 2], pads=[0, 0, 0, 0], strides=[2, 2]](%65) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:585:0
  %108 : Float(1:32768, 128:256, 16:16, 16:1, requires_grad=1, device=cpu) = onnx::Conv[dilations=[1, 1], group=1, kernel_shape=[3, 3], pads=[1, 1, 1, 1], strides=[1, 1]](%66, %109, %110)
  %69 : Float(1:32768, 128:256, 16:16, 16:1, requires_grad=1, device=cpu) = onnx::Relu(%108) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:1134:0
  %70 : Float(1:8192, 128:64, 8:8, 8:1, requires_grad=1, device=cpu) = onnx::MaxPool[kernel_shape=[2, 2], pads=[0, 0, 0, 0], strides=[2, 2]](%69) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:585:0
  %111 : Float(1:16384, 256:64, 8:8, 8:1, requires_grad=1, device=cpu) = onnx::Conv[dilations=[1, 1], group=1, kernel_shape=[3, 3], pads=[1, 1, 1, 1], strides=[1, 1]](%70, %112, %113)
  %73 : Float(1:16384, 256:64, 8:8, 8:1, requires_grad=1, device=cpu) = onnx::Relu(%111) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:1134:0
  %114 : Float(1:16384, 256:64, 8:8, 8:1, requires_grad=1, device=cpu) = onnx::Conv[dilations=[1, 1], group=1, kernel_shape=[3, 3], pads=[1, 1, 1, 1], strides=[1, 1]](%73, %115, %116)
  %76 : Float(1:16384, 256:64, 8:8, 8:1, requires_grad=1, device=cpu) = onnx::Relu(%114) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:1134:0
  %77 : Float(1:4096, 256:16, 4:4, 4:1, requires_grad=1, device=cpu) = onnx::MaxPool[kernel_shape=[2, 2], pads=[0, 0, 0, 0], strides=[2, 2]](%76) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:585:0
  %117 : Float(1:8192, 512:16, 4:4, 4:1, requires_grad=1, device=cpu) = onnx::Conv[dilations=[1, 1], group=1, kernel_shape=[3, 3], pads=[1, 1, 1, 1], strides=[1, 1]](%77, %118, %119)
  %80 : Float(1:8192, 512:16, 4:4, 4:1, requires_grad=1, device=cpu) = onnx::Relu(%117) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:1134:0
  %120 : Float(1:8192, 512:16, 4:4, 4:1, requires_grad=1, device=cpu) = onnx::Conv[dilations=[1, 1], group=1, kernel_shape=[3, 3], pads=[1, 1, 1, 1], strides=[1, 1]](%80, %121, %122)
  %83 : Float(1:8192, 512:16, 4:4, 4:1, requires_grad=1, device=cpu) = onnx::Relu(%120) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:1134:0
  %84 : Float(1:2048, 512:4, 2:2, 2:1, requires_grad=1, device=cpu) = onnx::MaxPool[kernel_shape=[2, 2], pads=[0, 0, 0, 0], strides=[2, 2]](%83) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:585:0
  %123 : Float(1:2048, 512:4, 2:2, 2:1, requires_grad=1, device=cpu) = onnx::Conv[dilations=[1, 1], group=1, kernel_shape=[3, 3], pads=[1, 1, 1, 1], strides=[1, 1]](%84, %124, %125)
  %87 : Float(1:2048, 512:4, 2:2, 2:1, requires_grad=1, device=cpu) = onnx::Relu(%123) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:1134:0
  %126 : Float(1:2048, 512:4, 2:2, 2:1, requires_grad=1, device=cpu) = onnx::Conv[dilations=[1, 1], group=1, kernel_shape=[3, 3], pads=[1, 1, 1, 1], strides=[1, 1]](%87, %127, %128)
  %90 : Float(1:2048, 512:4, 2:2, 2:1, requires_grad=1, device=cpu) = onnx::Relu(%126) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:1134:0
  %91 : Float(1:512, 512:1, 1:1, 1:1, requires_grad=1, device=cpu) = onnx::MaxPool[kernel_shape=[2, 2], pads=[0, 0, 0, 0], strides=[2, 2]](%90) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:585:0
  %92 : Tensor = onnx::Shape(%91)
  %93 : Tensor = onnx::Constant[value={0}]()
  %94 : Long(device=cpu) = onnx::Gather[axis=0](%92, %93) # /mlflow/projects/code/src/model.py:137:0
  %96 : Tensor = onnx::Unsqueeze[axes=[0]](%94)
  %98 : Tensor = onnx::Concat[axis=0](%96, %129)
  %99 : Float(1:512, 512:1, requires_grad=1, device=cpu) = onnx::Reshape(%91, %98) # /mlflow/projects/code/src/model.py:137:0
  %100 : Float(1:512, 512:1, requires_grad=1, device=cpu) = onnx::Gemm[alpha=1., beta=1., transB=1](%99, %classifier.0.weight, %classifier.0.bias) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:1690:0
  %101 : Float(1:512, 512:1, requires_grad=1, device=cpu) = onnx::Relu(%100) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:983:0
  %102 : Float(1:32, 32:1, requires_grad=1, device=cpu) = onnx::Gemm[alpha=1., beta=1., transB=1](%101, %classifier.3.weight, %classifier.3.bias) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:1690:0
  %103 : Float(1:32, 32:1, requires_grad=1, device=cpu) = onnx::Relu(%102) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:983:0
  %output : Float(1:10, 10:1, requires_grad=1, device=cpu) = onnx::Gemm[alpha=1., beta=1., transB=1](%103, %classifier.6.weight, %classifier.6.bias) # /usr/local/lib/python3.8/site-packages/torch/nn/functional.py:1690:0
  return (%output)

2021/02/11 07:18:39 INFO mlflow.projects: === Run (ID '597633d3c4f5494898559b4b1889d457') succeeded ===
2021/02/11 07:18:40 INFO mlflow.projects.utils: === Created directory /tmp/tmpza722aed for downloading remote URIs passed to arguments of type 'path' ===
2021/02/11 07:18:40 INFO mlflow.projects.backend.local: === Running command 'source activate mlflow-896ad7ba51492e700af933e0b293ec0fc9aface0 1>&2 && cp ../mlruns/0/597633d3c4f5494898559b4b1889d457/artifacts/cifar10_0.onnx ./ && \
docker build \
  -t shibui/ml-system-in-actions:training_pattern_cifar10_evaluate_0 \
  -f ./Dockerfile \
  --build-arg model_filename=cifar10_0.onnx \
  --build-arg model_directory=mlruns/0/597633d3c4f5494898559b4b1889d457/artifacts \
  --build-arg entrypoint_path=./onnx_runtime_server_entrypoint.sh \
  .
' in run with ID '6272918d214242f48e7c85c71b82a883' ===
Sending build context to Docker daemon  38.01MB
Step 1/12 : FROM mcr.microsoft.com/onnxruntime/server:latest
 ---> 0556947b2a78
Step 2/12 : ARG model_filename=cifar10_0.onnx
 ---> Using cache
 ---> 071d7f5e1856
Step 3/12 : ARG model_directory=./
 ---> Using cache
 ---> 57525f62cf29
Step 4/12 : ARG entrypoint_path=./building/onnx_runtime_server_entrypoint.sh
 ---> Using cache
 ---> fca089050d44
Step 5/12 : ENV PROJECT_DIR cifar10
 ---> Using cache
 ---> 9ee2694b77ca
Step 6/12 : WORKDIR /${PROJECT_DIR}
 ---> Using cache
 ---> 951c3b34d3f2
Step 7/12 : COPY ./${model_filename} /${PROJECT_DIR}/${model_filename}
 ---> bf6e03ba9587
Step 8/12 : ENV MODEL_PATH /${PROJECT_DIR}/${model_filename}
 ---> Running in 74f18b7d2300
Removing intermediate container 74f18b7d2300
 ---> 8ae5eaaf33e0
Step 9/12 : WORKDIR /onnxruntime/server/
 ---> Running in 5271c610f35f
Removing intermediate container 5271c610f35f
 ---> 72280ba14a1d
Step 10/12 : COPY ./${entrypoint_path} ./onnx_runtime_server_entrypoint.sh
 ---> acfe6f939227
Step 11/12 : RUN chmod +x onnx_runtime_server_entrypoint.sh
 ---> Running in 644202b28f1b
Removing intermediate container 644202b28f1b
 ---> 17a01ac73e80
Step 12/12 : ENTRYPOINT ["./onnx_runtime_server_entrypoint.sh"]
 ---> Running in bad1e2601f2a
Removing intermediate container bad1e2601f2a
 ---> ad282fcbcfe9
Successfully built ad282fcbcfe9
Successfully tagged shibui/ml-system-in-actions:training_pattern_cifar10_evaluate_0
2021/02/11 07:18:42 INFO mlflow.projects: === Run (ID '6272918d214242f48e7c85c71b82a883') succeeded ===
2021/02/11 07:18:44 INFO mlflow.utils.conda: === Creating conda environment mlflow-a5f0c06b2ecebc7d20239baa7c71ce611a46259e ===
Solving environment: done


==> WARNING: A newer version of conda exists. <==
  current version: 4.5.11
  latest version: 4.9.2

Please update conda by running

    $ conda update -n base -c defaults conda


Preparing transaction: done
Verifying transaction: done
Executing transaction: done
Collecting grpcio
  Downloading grpcio-1.35.0-cp38-cp38-manylinux2014_x86_64.whl (4.1 MB)
     |████████████████████████████████| 4.1 MB 23.9 MB/s
Collecting six>=1.5.2
  Using cached six-1.15.0-py2.py3-none-any.whl (10 kB)
Collecting mlflow
  Using cached mlflow-1.13.1-py3-none-any.whl (14.1 MB)
Collecting alembic<=1.4.1
  Using cached alembic-1.4.1-py2.py3-none-any.whl
Collecting azure-storage-blob>=12.0.0
  Using cached azure_storage_blob-12.7.1-py2.py3-none-any.whl (339 kB)
Collecting azure-core<2.0.0,>=1.10.0
  Using cached azure_core-1.11.0-py2.py3-none-any.whl (127 kB)
Collecting click>=7.0
  Using cached click-7.1.2-py2.py3-none-any.whl (82 kB)
Collecting cryptography>=2.1.4
  Using cached cryptography-3.4.4-cp36-abi3-manylinux2014_x86_64.whl (3.2 MB)
Collecting cffi>=1.12
  Using cached cffi-1.14.4-cp38-cp38-manylinux1_x86_64.whl (411 kB)
Collecting databricks-cli>=0.8.7
  Using cached databricks_cli-0.14.1-py3-none-any.whl
Collecting docker>=4.0.0
  Using cached docker-4.4.1-py2.py3-none-any.whl (146 kB)
Collecting gitpython>=2.1.0
  Using cached GitPython-3.1.13-py3-none-any.whl (159 kB)
Collecting gitdb<5,>=4.0.1
  Using cached gitdb-4.0.5-py3-none-any.whl (63 kB)
Collecting msrest>=0.6.18
  Using cached msrest-0.6.21-py2.py3-none-any.whl (85 kB)
Requirement already satisfied: certifi>=2017.4.17 in /root/.pyenv/versions/anaconda3-5.3.1/envs/mlflow-a5f0c06b2ecebc7d20239baa7c71ce611a46259e/lib/python3.8/site-packages (from msrest>=0.6.18->azure-storage-blob>=12.0.0->mlflow->-r /tmp/ml-system-in-actions/chapter2_training/cifar10/evaluate/condaenv.xd7xzphu.requirements.txt (line 1)) (2020.12.5)
Collecting isodate>=0.6.0
  Using cached isodate-0.6.0-py2.py3-none-any.whl (45 kB)
Collecting protobuf>=3.6.0
  Using cached protobuf-3.14.0-cp38-cp38-manylinux1_x86_64.whl (1.0 MB)
Collecting python-editor>=0.3
  Using cached python_editor-1.0.4-py3-none-any.whl (4.9 kB)
Collecting requests>=2.17.3
  Using cached requests-2.25.1-py2.py3-none-any.whl (61 kB)
Collecting chardet<5,>=3.0.2
  Using cached chardet-4.0.0-py2.py3-none-any.whl (178 kB)
Collecting idna<3,>=2.5
  Using cached idna-2.10-py2.py3-none-any.whl (58 kB)
Collecting requests-oauthlib>=0.5.0
  Using cached requests_oauthlib-1.3.0-py2.py3-none-any.whl (23 kB)
Collecting oauthlib>=3.0.0
  Using cached oauthlib-3.1.0-py2.py3-none-any.whl (147 kB)
Collecting smmap<4,>=3.0.1
  Using cached smmap-3.0.5-py2.py3-none-any.whl (25 kB)
Collecting sqlalchemy
  Using cached SQLAlchemy-1.3.23-cp38-cp38-manylinux2010_x86_64.whl (1.3 MB)
Collecting sqlparse>=0.3.1
  Using cached sqlparse-0.4.1-py3-none-any.whl (42 kB)
Collecting tabulate>=0.7.7
  Using cached tabulate-0.8.7-py3-none-any.whl (24 kB)
Collecting urllib3<1.27,>=1.21.1
  Using cached urllib3-1.26.3-py2.py3-none-any.whl (137 kB)
Collecting websocket-client>=0.32.0
  Using cached websocket_client-0.57.0-py2.py3-none-any.whl (200 kB)
Collecting numpy
  Using cached numpy-1.20.1-cp38-cp38-manylinux2010_x86_64.whl (15.4 MB)
Collecting Pillow
  Downloading Pillow-8.1.0-cp38-cp38-manylinux1_x86_64.whl (2.2 MB)
     |████████████████████████████████| 2.2 MB 56.5 MB/s
Collecting scikit-learn
  Downloading scikit_learn-0.24.1-cp38-cp38-manylinux2010_x86_64.whl (24.9 MB)
     |████████████████████████████████| 24.9 MB 60.2 MB/s
Collecting joblib>=0.11
  Downloading joblib-1.0.1-py3-none-any.whl (303 kB)
     |████████████████████████████████| 303 kB 62.6 MB/s
Collecting scipy>=0.19.1
  Downloading scipy-1.6.0-cp38-cp38-manylinux1_x86_64.whl (27.2 MB)
     |████████████████████████████████| 27.2 MB 57.9 MB/s
Collecting threadpoolctl>=2.0.0
  Downloading threadpoolctl-2.1.0-py3-none-any.whl (12 kB)
Collecting cloudpickle
  Using cached cloudpickle-1.6.0-py3-none-any.whl (23 kB)
Collecting entrypoints
  Using cached entrypoints-0.3-py2.py3-none-any.whl (11 kB)
Collecting Flask
  Using cached Flask-1.1.2-py2.py3-none-any.whl (94 kB)
Collecting itsdangerous>=0.24
  Using cached itsdangerous-1.1.0-py2.py3-none-any.whl (16 kB)
Collecting Jinja2>=2.10.1
  Using cached Jinja2-2.11.3-py2.py3-none-any.whl (125 kB)
Collecting MarkupSafe>=0.23
  Using cached MarkupSafe-1.1.1-cp38-cp38-manylinux2010_x86_64.whl (32 kB)
Collecting Werkzeug>=0.15
  Using cached Werkzeug-1.0.1-py2.py3-none-any.whl (298 kB)
Collecting gunicorn
  Using cached gunicorn-20.0.4-py2.py3-none-any.whl (77 kB)
Requirement already satisfied: setuptools>=3.0 in /root/.pyenv/versions/anaconda3-5.3.1/envs/mlflow-a5f0c06b2ecebc7d20239baa7c71ce611a46259e/lib/python3.8/site-packages (from gunicorn->mlflow->-r /tmp/ml-system-in-actions/chapter2_training/cifar10/evaluate/condaenv.xd7xzphu.requirements.txt (line 1)) (52.0.0.post20210125)
Collecting Mako
  Using cached Mako-1.1.4-py2.py3-none-any.whl
Collecting pandas
  Using cached pandas-1.2.2-cp38-cp38-manylinux1_x86_64.whl (9.7 MB)
Collecting python-dateutil
  Using cached python_dateutil-2.8.1-py2.py3-none-any.whl (227 kB)
Collecting pytz>=2017.3
  Using cached pytz-2021.1-py2.py3-none-any.whl (510 kB)
Collecting prometheus-flask-exporter
  Using cached prometheus_flask_exporter-0.18.1-py3-none-any.whl
Collecting prometheus-client
  Using cached prometheus_client-0.9.0-py2.py3-none-any.whl (53 kB)
Collecting pycparser
  Using cached pycparser-2.20-py2.py3-none-any.whl (112 kB)
Collecting pyyaml
  Using cached PyYAML-5.4.1-cp38-cp38-manylinux1_x86_64.whl (662 kB)
Collecting querystring-parser
  Using cached querystring_parser-1.2.4-py2.py3-none-any.whl (7.9 kB)
Installing collected packages: urllib3, idna, chardet, six, requests, pycparser, oauthlib, MarkupSafe, Werkzeug, smmap, requests-oauthlib, Jinja2, itsdangerous, isodate, click, cffi, websocket-client, tabulate, sqlalchemy, pytz, python-editor, python-dateutil, prometheus-client, numpy, msrest, Mako, gitdb, Flask, cryptography, azure-core, threadpoolctl, sqlparse, scipy, querystring-parser, pyyaml, protobuf, prometheus-flask-exporter, pandas, joblib, gunicorn, gitpython, entrypoints, docker, databricks-cli, cloudpickle, azure-storage-blob, alembic, scikit-learn, Pillow, mlflow, grpcio
Successfully installed Flask-1.1.2 Jinja2-2.11.3 Mako-1.1.4 MarkupSafe-1.1.1 Pillow-8.1.0 Werkzeug-1.0.1 alembic-1.4.1 azure-core-1.11.0 azure-storage-blob-12.7.1 cffi-1.14.4 chardet-4.0.0 click-7.1.2 cloudpickle-1.6.0 cryptography-3.4.4 databricks-cli-0.14.1 docker-4.4.1 entrypoints-0.3 gitdb-4.0.5 gitpython-3.1.13 grpcio-1.35.0 gunicorn-20.0.4 idna-2.10 isodate-0.6.0 itsdangerous-1.1.0 joblib-1.0.1 mlflow-1.13.1 msrest-0.6.21 numpy-1.20.1 oauthlib-3.1.0 pandas-1.2.2 prometheus-client-0.9.0 prometheus-flask-exporter-0.18.1 protobuf-3.14.0 pycparser-2.20 python-dateutil-2.8.1 python-editor-1.0.4 pytz-2021.1 pyyaml-5.4.1 querystring-parser-1.2.4 requests-2.25.1 requests-oauthlib-1.3.0 scikit-learn-0.24.1 scipy-1.6.0 six-1.15.0 smmap-3.0.5 sqlalchemy-1.3.23 sqlparse-0.4.1 tabulate-0.8.7 threadpoolctl-2.1.0 urllib3-1.26.3 websocket-client-0.57.0
#
# To activate this environment, use:
# > source activate mlflow-a5f0c06b2ecebc7d20239baa7c71ce611a46259e
#
# To deactivate an active environment, use:
# > source deactivate
#

2021/02/11 07:19:36 INFO mlflow.projects.utils: === Created directory /tmp/tmp9mqcz7ye for downloading remote URIs passed to arguments of type 'path' ===
2021/02/11 07:19:36 INFO mlflow.projects.backend.local: === Running command 'source activate mlflow-a5f0c06b2ecebc7d20239baa7c71ce611a46259e 1>&2 && docker run \
  -it -d \
  --name training_pattern_cifar10_evaluate_0 \
  -p 50051:50051 shibui/ml-system-in-actions:training_pattern_cifar10_evaluate_0 && \
python -m src.evaluate \
  --upstream ../mlruns/0/597633d3c4f5494898559b4b1889d457/artifacts \
  --downstream ./evaluate/ \
  --test_data_directory ../mlruns/0/d2ec649ed0254e99a9713e75da3dced9/artifacts/downstream_directory/test

' in run with ID '9e5f8813e150424fba85d66ad7aea1d9' ===
bac2ff7cc319ab9ba19f5ca639a0eedfbbb9e5d96e31c30bd11afe4d8c73e01f
INFO:__main__:predict proba [[0.09882650524377823, 0.09837666898965836, 0.10054934769868851, 0.10118967294692993, 0.10194174945354462, 0.10157361626625061, 0.10137040168046951, 0.0949874073266983, 0.10158077627420425, 0.09960377961397171]]
INFO:__main__:predict label 4
INFO:__main__:../mlruns/0/d2ec649ed0254e99a9713e75da3dced9/artifacts/downstream_directory/test/9/tipper_s_001370.png label: 9 predicted: 4 duration: 0.020441532135009766 seconds
INFO:__main__:predict proba [[0.09882650524377823, 0.09837666898965836, 0.10054934769868851, 0.10118967294692993, 0.10194174945354462, 0.10157361626625061, 0.10137040168046951, 0.0949874073266983, 0.10158077627420425, 0.09960377961397171]]
INFO:__main__:predict label 4
INFO:__main__:../mlruns/0/d2ec649ed0254e99a9713e75da3dced9/artifacts/downstream_directory/test/9/trailer_truck_s_000002.png label: 9 predicted: 4 duration: 0.0063266754150390625 seconds
INFO:__main__:predict proba [[0.09882650524377823, 0.09837666898965836, 0.10054934769868851, 0.10118967294692993, 0.10194174945354462, 0.10157361626625061, 0.10137040168046951, 0.0949874073266983, 0.10158077627420425, 0.09960377961397171]]

###########
### 中略 ###
###########


INFO:__main__:../mlruns/0/d2ec649ed0254e99a9713e75da3dced9/artifacts/downstream_directory/test/5/puppy_s_002220.png label: 5 predicted: 4 duration: 0.005832672119140625 seconds
INFO:__main__:predict proba [[0.09882650524377823, 0.09837666898965836, 0.10054934769868851, 0.10118967294692993, 0.10194174945354462, 0.10157361626625061, 0.10137040168046951, 0.0949874073266983, 0.10158077627420425, 0.09960377961397171]]
INFO:__main__:predict label 4
INFO:__main__:../mlruns/0/d2ec649ed0254e99a9713e75da3dced9/artifacts/downstream_directory/test/5/toy_spaniel_s_001503.png label: 5 predicted: 4 duration: 0.0055751800537109375 seconds
2021/02/11 07:20:40 INFO mlflow.projects: === Run (ID '9e5f8813e150424fba85d66ad7aea1d9') succeeded ===
2021/02/11 07:20:41 INFO mlflow.projects: === Run (ID '16ca2fc7a707438fb999ffcc2ca0cc5f') succeeded ===
```

</div></details>

4. 推論用コンテナの削除

```sh
# mlflowで起動される推論用のコンテナを削除します。
$ docker rm -f training_pattern_cifar10_evaluate_0
```

# model in image pattern

## 目的

モデル・イン・イメージ・パターンでは学習によってモデルファイルを生成した後にモデルファイル含めて推論サーバイメージをビルドします。推論サーバを配備する際には、サーバイメージを Pull して推論サーバを起動することで本稼働させることができます。

## 前提

- Python 3.8 以上
- Docker
- Kubernetes クラスターまたは minikube

本プログラムでは Kubernetes クラスターまたは minikube が必要になります。
Kubernetes クラスターは独自に構築するか、各クラウドのマネージドサービス（GCP GKE、AWS EKS、MS Azure AKS 等）をご利用ください。
なお、作者は GCP GKE クラスターで稼働確認を取っております。

- [Kubernetes クラスター構築](https://kubernetes.io/ja/docs/setup/)
- [minikube](https://kubernetes.io/ja/docs/setup/learning-environment/minikube/)

## 使い方

0. カレントディレクトリ

```sh
$ pwd
~/ml-system-in-actions/chapter3_release_patterns/model_in_image_pattern
```

1. 推論用 Docker イメージのビルド

```sh
$ make build_all
# 実行されるコマンド
# docker build \
#     -t shibui/ml-system-in-actions:model_in_image_pattern_0.0.1 \
#     -f Dockerfile \
#     .
```

2. 推論器を Kubernetes クラスターにデプロイ

```sh
$ make deploy
# 実行されるコマンド
# kubectl apply -f manifests/namespace.yml
# kubectl apply -f manifests/deployment.yml

# デプロイの確認
$ kubectl -n model-in-image get pods,deploy,svc
# NAME                                  READY   STATUS    RESTARTS   AGE
# pod/model-in-image-5c64988c5d-5phxn   1/1     Running   0          28s
# pod/model-in-image-5c64988c5d-lljmg   1/1     Running   0          28s
# pod/model-in-image-5c64988c5d-qhpms   1/1     Running   0          28s
# pod/model-in-image-5c64988c5d-rgwlx   1/1     Running   0          28s

# NAME                             READY   UP-TO-DATE   AVAILABLE   AGE
# deployment.apps/model-in-image   4/4     4            4           28s

# NAME                     TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)    AGE
# service/model-in-image   ClusterIP   10.84.9.167   <none>        8000/TCP   28s
```

3. Kubernetes の model-in-image を削除

```sh
$ make delete
# 実行されるコマンド
# kubectl delete ns model-in-image
```

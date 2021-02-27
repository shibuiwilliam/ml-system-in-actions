# model load pattern

## 目的

モデル・ロード・パターンでは推論サーバを配備する際、サーバイメージを Pull した後に推論サーバを起動し、その後にモデルファイルをロードして推論サーバを本稼働させます。モデルファイルのロード元を変数等で変更することによって、推論サーバで稼働するモデルを柔軟に変更することも可能です。

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
~/ml-system-in-actions/chapter3_release_patterns/model_load_pattern
```

1. 推論用 Docker イメージおよびモデルロード用 Docker イメージのビルド

```sh
$ make build_all
# 実行されるコマンド
# docker build \
#     -t shibui/ml-system-in-actions:model_load_pattern_api_0.0.1 \
#     -f Dockerfile \
#     .
# docker build \
#     -t shibui/ml-system-in-actions:model_load_pattern_loader_0.0.1 \
#     -f model_loader/Dockerfile \
#     .
```

2. 推論器とサイドカーを Kubernetes クラスターにデプロイ

```sh
$ make deploy
# 実行されるコマンド
# kubectl apply -f manifests/namespace.yml
# kubectl apply -f manifests/deployment.yml

# デプロイの確認
$ kubectl -n model-load get pods,deploy,svc
# NAME                              READY   STATUS    RESTARTS   AGE
# pod/model-load-6b4bb6f96c-b95f2   1/1     Running   0          33s
# pod/model-load-6b4bb6f96c-kntxk   1/1     Running   0          33s
# pod/model-load-6b4bb6f96c-s8zjx   1/1     Running   0          33s
# pod/model-load-6b4bb6f96c-zdwqj   1/1     Running   0          33s

# NAME                         READY   UP-TO-DATE   AVAILABLE   AGE
# deployment.apps/model-load   4/4     4            4           33s

# NAME                 TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
# service/model-load   ClusterIP   10.84.11.108   <none>        8000/TCP   33s
```

3. Kubernetes の model-load を削除

```sh
$ make delete
# 実行されるコマンド
# kubectl delete ns model-load
```

# model load pattern

## 目的

モデル・ロード・パターンでは推論サーバを配備する際、サーバイメージを Pull した後に推論サーバを起動し、その後にモデルファイルをロードして推論サーバを本稼働させます。モデルファイルのロード元を変数等で変更することによって、推論サーバで稼働するモデルを柔軟に変更することも可能です。

## 前提

- Python 3.8以上
- Docker
- Kubernetesクラスターまたはminikube

本プログラムではKubernetesクラスターまたはminikubeが必要になります。
Kubernetesクラスターは独自に構築するか、各クラウドのマネージドサービス（GCP GKE、AWS EKS、MS Azure AKS等）をご利用ください。
なお、作者はGCP GKEクラスターで稼働確認を取っております。

- [Kubernetesクラスター構築](https://kubernetes.io/ja/docs/setup/)
- [minikube](https://kubernetes.io/ja/docs/setup/learning-environment/minikube/)


## 使い方

1. 推論用Dockerイメージおよびモデルロード用Dockerイメージのビルド
   
```sh
$ make build_all
docker build \
    -t shibui/ml-system-in-actions:model_load_pattern_api_0.0.1 \
    -f Dockerfile \
    .
docker build \
    -t shibui/ml-system-in-actions:model_load_pattern_loader_0.0.1 \
    -f model_loader/Dockerfile \
    .
```

2. 推論器とサイドカーをKubernetesクラスターにデプロイ

```sh
$ make deploy
kubectl apply -f manifests/namespace.yml
kubectl apply -f manifests/deployment.yml
```

3. Kubernetesのmodel-loadを削除

```sh
$ make delete
kubectl delete ns model-load
```

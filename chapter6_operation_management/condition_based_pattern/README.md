# condition based prediction pattern

## 目的

状況によって推論のリクエスト先を変えるパターン。

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
~/ml-system-in-actions/chapter6_operation_management/condition_based_pattern
```

1. Docker イメージをビルド

```sh
$ make build_all
# 実行されるコマンド
# docker build \
# 	-t shibui/ml-system-in-actions:condition_based_pattern_proxy_0.0.1 \
# 	-f ./Dockerfile.proxy \
# 	.
# docker build \
# 	-t shibui/ml-system-in-actions:condition_based_pattern_imagenet_mobilenet_v2_0.0.1 \
# 	-f ./imagenet_mobilenet_v2/Dockerfile \
# 	.
# docker build \
# 	-t shibui/ml-system-in-actions:condition_based_pattern_plant_0.0.1 \
# 	-f ./plant/Dockerfile \
# 	.
# docker build \
# 	-t shibui/ml-system-in-actions:condition_based_pattern_client_0.0.1 \
# 	-f Dockerfile.client \
# 	.
```

2. Kubernetes でサービスを起動

```sh
$ make deploy
# 実行されるコマンド
# istioctl install -y
# kubectl apply -f manifests/namespace.yml
# kubectl apply -f manifests/

# 稼働確認
$ kubectl -n condition-based-serving get all
# 出力
# NAME                                     READY   STATUS    RESTARTS   AGE
# pod/client                               2/2     Running   0          59s
# pod/mobilenet-v2-c9dc95c89-66dn9         2/2     Running   0          58s
# pod/mobilenet-v2-c9dc95c89-985sq         2/2     Running   0          58s
# pod/mobilenet-v2-c9dc95c89-qs5ht         2/2     Running   0          58s
# pod/mobilenet-v2-proxy-59d9f899c-7bpbb   1/2     Running   0          57s
# pod/mobilenet-v2-proxy-59d9f899c-blwz9   2/2     Running   0          57s
# pod/mobilenet-v2-proxy-59d9f899c-c2mlz   2/2     Running   0          57s
# pod/plant-9766f44d7-d9wwb                2/2     Running   0          58s
# pod/plant-9766f44d7-jn6m2                2/2     Running   0          58s
# pod/plant-9766f44d7-lnn48                2/2     Running   0          58s
# pod/plant-proxy-558877db5c-d8wvz         2/2     Running   0          57s
# pod/plant-proxy-558877db5c-fwtsh         1/2     Running   0          57s
# pod/plant-proxy-558877db5c-qpxmz         2/2     Running   0          57s

# NAME                   TYPE        CLUSTER-IP    EXTERNAL-IP   PORT(S)             AGE
# service/mobilenet-v2   ClusterIP   10.4.8.216    <none>        8500/TCP,8501/TCP   58s
# service/plant          ClusterIP   10.4.9.128    <none>        9500/TCP,9501/TCP   57s
# service/proxy          ClusterIP   10.4.11.158   <none>        8000/TCP            57s

# NAME                                 READY   UP-TO-DATE   AVAILABLE   AGE
# deployment.apps/mobilenet-v2         3/3     3            3           59s
# deployment.apps/mobilenet-v2-proxy   2/3     3            2           58s
# deployment.apps/plant                3/3     3            3           59s
# deployment.apps/plant-proxy          2/3     3            2           58s

# NAME                                           DESIRED   CURRENT   READY   AGE
# replicaset.apps/mobilenet-v2-c9dc95c89         3         3         3       59s
# replicaset.apps/mobilenet-v2-proxy-59d9f899c   3         3         2       58s
# replicaset.apps/plant-9766f44d7                3         3         3       59s
# replicaset.apps/plant-proxy-558877db5c         3         3         2       58s
```

3. 起動した API にリクエスト

```sh
# クライアントに接続
$ kubectl -n condition-based-serving exec -it pod/client bash

# ヘルスチェック
$ curl proxy.condition-based-serving.svc.cluster.local:8000/health
# 出力
# {
#   "health":"ok"
# }

# メタデータ
$ curl proxy.condition-based-serving.svc.cluster.local:8000/metadata
# 出力
# {
#   "data_type": "str",
#   "data_structure": "(1,1)",
#   "data_sample": "base64 encoded image file",
#   "prediction_type": "float32",
#   "prediction_structure": "(1,1001)",
#   "prediction_sample": "[0.07093159, 0.01558308, 0.01348537, ...]"
# }

# ラベル一覧
$ curl proxy.condition-based-serving.svc.cluster.local:8000/label
# 出力
# [
#   "background",
#   "tench",
#   "goldfish",
# ...
#   "bolete",
#   "ear",
#   "toilet tissue"
# ]


# テストデータで推論リクエスト
$ curl proxy.condition-based-serving.svc.cluster.local:8000/predict/test
# 出力
# "Persian cat"


# ネコ画像をImageNet推論器にリクエスト
$ (echo -n '{"image_data": "'; base64 cat.jpg; echo '"}') | \
	curl \
	-X POST \
	-H "Content-Type: application/json" \
	-d @- \
	proxy.condition-based-serving.svc.cluster.local:8000/predict
# 出力
# "Persian cat"


# アヤメ画像を植物推論器にリクエスト
$ (echo -n '{"image_data": "'; base64 iris.jpg; echo '"}') | \
	curl \
	-X POST \
	-H "Content-Type: application/json" \
	-H "target: mountain" \
	-d @- \
	proxy.condition-based-serving.svc.cluster.local:8000/predict
# 出力
# "Iris versicolor"


# ネコ画像を植物推論器にリクエストすると、backgroundと分類される
$ (echo -n '{"image_data": "'; base64 cat.jpg; echo '"}') | \
	curl \
	-X POST \
	-H "Content-Type: application/json" \
	-H "target: mountain" \
	-d @- \
	proxy.condition-based-serving.svc.cluster.local:8000/predict
# 出力
# "background"

# アヤメ画像をImageNet推論器にリクエストすると、beeと分類される
$ (echo -n '{"image_data": "'; base64 iris.jpg; echo '"}') | \
	curl \
	-X POST \
	-H "Content-Type: application/json" \
	-d @- \
	proxy.condition-based-serving.svc.cluster.local:8000/predict
# 出力
# "bee"
```

4. Kubernetes からサービスを削除

```sh
$ kubectl delete ns condition-based-serving
$ istioctl x uninstall --purge -y
$ kubectl delete ns istio-system
```

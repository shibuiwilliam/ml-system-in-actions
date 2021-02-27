# online ab test pattern

## 目的

オンラインで A/B テストを実施します。

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
~/ml-system-in-actions/chapter6_operation_management/online_ab_pattern
```

1. Docker イメージをビルド

```sh
$ make build_all
# 実行されるコマンド
# docker build \
# 	-t shibui/ml-system-in-actions:online_ab_pattern_api_0.0.1 \
# 	-f Dockerfile \
# 	.
# docker build \
# 	-t shibui/ml-system-in-actions:online_ab_pattern_loader_0.0.1 \
# 	-f model_loader/Dockerfile \
# 	.
# docker build \
# 	-t shibui/ml-system-in-actions:online_ab_pattern_client_0.0.1 \
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
$ kubectl -n online-ab get all
# 出力
# NAME                            READY   STATUS    RESTARTS   AGE
# pod/client                      2/2     Running   0          70s
# pod/iris-rf-f9b9d8b98-5rpms     2/2     Running   0          70s
# pod/iris-rf-f9b9d8b98-m8h4j     2/2     Running   0          70s
# pod/iris-rf-f9b9d8b98-ws7x9     2/2     Running   0          70s
# pod/iris-svc-85c897f9f4-78n69   2/2     Running   0          70s
# pod/iris-svc-85c897f9f4-ccs69   2/2     Running   0          70s
# pod/iris-svc-85c897f9f4-rmqct   2/2     Running   0          70s

# NAME           TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
# service/iris   ClusterIP   10.4.7.184   <none>        8000/TCP   69s

# NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
# deployment.apps/iris-rf    3/3     3            3           70s
# deployment.apps/iris-svc   3/3     3            3           71s

# NAME                                  DESIRED   CURRENT   READY   AGE
# replicaset.apps/iris-rf-f9b9d8b98     3         3         3       71s
# replicaset.apps/iris-svc-85c897f9f4   3         3         3       71s

# NAME                                           REFERENCE             TARGETS         MINPODS   MAXPODS   REPLICAS   AGE
# horizontalpodautoscaler.autoscaling/iris-rf    Deployment/iris-rf    <unknown>/70%   3         10        3          70s
# horizontalpodautoscaler.autoscaling/iris-svc   Deployment/iris-svc   <unknown>/70%   3         10        3          70s
```

3. 起動した API にリクエスト

```sh
# クライアントに接続
$ kubectl -n online-ab exec -it pod/client bash

# 同じエンドポイントに複数回リクエストを送り、2種類のレスポンスが得られることを確認
$ curl http://iris.online-ab.svc.cluster.local:8000/predict/test
# {"prediction":[0.9709315896034241,0.015583082102239132,0.013485366478562355],"mode":"iris_svc.onnx"}
$ curl http://iris.online-ab.svc.cluster.local:8000/predict/test
# {"prediction":[0.9709315896034241,0.015583082102239132,0.013485366478562355],"mode":"iris_svc.onnx"}
$ curl http://iris.online-ab.svc.cluster.local:8000/predict/test
# {"prediction":[0.9709315896034241,0.015583082102239132,0.013485366478562355],"mode":"iris_svc.onnx"}
$ curl http://iris.online-ab.svc.cluster.local:8000/predict/test
# {"prediction":[0.9709315896034241,0.015583082102239132,0.013485366478562355],"mode":"iris_svc.onnx"}
$ curl http://iris.online-ab.svc.cluster.local:8000/predict/test
# {"prediction":[0.9999999403953552,0.0,0.0],"mode":"iris_rf.onnx"}
$ curl http://iris.online-ab.svc.cluster.local:8000/predict/test
# {"prediction":[0.9999999403953552,0.0,0.0],"mode":"iris_rf.onnx"}
$ curl http://iris.online-ab.svc.cluster.local:8000/predict/test
# {"prediction":[0.9999999403953552,0.0,0.0],"mode":"iris_rf.onnx"}
```

4. Kubernetes からサービスを削除

```sh
$ kubectl delete ns online-ab
$ istioctl x uninstall --purge -y
$ kubectl delete ns istio-system
```

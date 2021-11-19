# circuit breaker pattern

## 目的

サーキットブレーカーによって高負荷に対処します。

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
~/ml-system-in-actions/chapter6_operation_management/circuit_breaker_pattern
```

1. Docker イメージをビルド

```sh
$ make build_all
# 実行されるコマンド
# docker build \
# 	-t shibui/ml-system-in-actions:circuit_breaker_pattern_api_0.0.1 \
# 	-f Dockerfile \
# 	.
# docker build \
# 	-t shibui/ml-system-in-actions:circuit_breaker_pattern_loader_0.0.1 \
# 	-f model_loader/Dockerfile \
# 	.
# docker build \
# 	-t shibui/ml-system-in-actions:circuit_breaker_pattern_client_0.0.1 \
# 	-f Dockerfile.client \
# 	.
```

2. Kubernetes に Istio をインストールし、各サービスを起動

```sh
$ make deploy
# 実行されるコマンド
# istioctl install -y
# kubectl apply -f manifests/namespace.yml
# kubectl apply -f manifests/

# サービスの起動を確認
$ kubectl -n circuit-breaker get all
# 出力
# NAME                            READY   STATUS    RESTARTS   AGE
# pod/client                      2/2     Running   0          74s
# pod/iris-svc-56758cc7cf-6gdhb   2/2     Running   0          74s
# pod/iris-svc-56758cc7cf-k6wq7   2/2     Running   0          74s
# pod/iris-svc-56758cc7cf-lcgqp   2/2     Running   0          74s

# NAME               TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
# service/iris-svc   ClusterIP   10.4.3.84    <none>        8000/TCP   74s

# NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
# deployment.apps/iris-svc   3/3     3            3           75s

# NAME                                  DESIRED   CURRENT   READY   AGE
# replicaset.apps/iris-svc-56758cc7cf   3         3         3       75s
```

3. 起動した API に負荷テスト

```sh
# 負荷テストクライアントに接続
$ kubectl -n circuit-breaker exec -it pod/client -- bash
# 出力
# Defaulting container name to client.
# Use 'kubectl describe pod/client -n circuit-breaker' to see all of the containers in this pod.

# 負荷テストを実行
$ vegeta attack -duration=10s -rate=1000 -targets=vegeta/post-target | vegeta report -type=text
# 出力
# Requests      [total, rate, throughput]         10000, 1000.04, 764.34
# Duration      [total, attack, wait]             10.242s, 10s, 241.972ms
# Latencies     [min, mean, 50, 90, 95, 99, max]  362.662µs, 177.282ms, 90.438ms, 427.767ms, 672.361ms, 1.419s, 2.929s
# Bytes In      [total, mean]                     747376, 74.74
# Bytes Out     [total, mean]                     350000, 35.00
# Success       [ratio]                           78.28%
# Status Codes  [code:count]                      200:7828  503:2172
# Error Set:
# 503 Service Unavailable
```

4. Kubernetes からサービスを削除

```sh
$ kubectl delete ns circuit-breaker
$ istioctl x uninstall --purge -y
$ kubectl delete ns istio-system
```

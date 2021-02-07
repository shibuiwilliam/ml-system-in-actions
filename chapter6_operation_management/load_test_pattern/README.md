# load test pattern

## 目的

推論器に負荷テストを実施します。

## 前提

- Python 3.8以上
- Docker
- Kubernetesクラスターまたはminikube

## 使い方

1. Dockerイメージをビルド

```sh
$ make build_all
docker build \
    -t shibui/ml-system-in-actions:load_test_pattern_api_0.0.1 \
    -f Dockerfile \
    .
docker build \
		-t shibui/ml-system-in-actions:load_test_pattern_loader_0.0.1 \
		-f model_loader/Dockerfile \
		.
docker build \
		-t shibui/ml-system-in-actions:load_test_pattern_client_0.0.1 \
		-f Dockerfile.client \
		.
```

2. Kubernetesでサービスを起動

```sh
$ make deploy
kubectl apply -f manifests/namespace.yml
kubectl apply -f manifests/

# 稼働確認
$ kubectl -n load-test get all
NAME                            READY   STATUS    RESTARTS   AGE
pod/client                      1/1     Running   0          45s
pod/iris-svc-598875545c-5bvpq   1/1     Running   0          44s
pod/iris-svc-598875545c-8t47v   1/1     Running   0          44s
pod/iris-svc-598875545c-mqgcd   1/1     Running   0          44s

NAME               TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
service/iris-svc   ClusterIP   10.4.7.177   <none>        8000/TCP   44s

NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/iris-svc   3/3     3            3           44s

NAME                                  DESIRED   CURRENT   READY   AGE
replicaset.apps/iris-svc-598875545c   3         3         3       44s
```

3. 起動したAPIにリクエスト

```sh
# クライアントに接続
$ kubectl -n condition-based-serving exec -it pod/client bash

# 負荷テストを実行
$ vegeta attack -duration=60s -rate=100 -targets=vegeta/post-target | vegeta report -type=text
Requests      [total, rate, throughput]         6000, 100.02, 100.01
Duration      [total, attack, wait]             59.992s, 59.99s, 1.915ms
Latencies     [min, mean, 50, 90, 95, 99, max]  1.246ms, 1.939ms, 1.928ms, 2.182ms, 2.279ms, 2.72ms, 23.222ms
Bytes In      [total, mean]                     438000, 73.00
Bytes Out     [total, mean]                     210000, 35.00
Success       [ratio]                           100.00%
Status Codes  [code:count]                      200:6000
Error Set:
```

4. Kubernetesからサービスを削除

```sh
$ kubectl delete ns load-test
```
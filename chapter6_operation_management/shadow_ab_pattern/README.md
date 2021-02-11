# shadow ab test pattern

## 目的

シャドウでA/Bテストを実施します。

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

1. Dockerイメージをビルド

```sh
$ make build_all
docker build \
	-t shibui/ml-system-in-actions:shadow_ab_pattern_api_0.0.1 \
	-f Dockerfile \
	.
docker build \
	-t shibui/ml-system-in-actions:shadow_ab_pattern_loader_0.0.1 \
	-f model_loader/Dockerfile \
	.
docker build \
	-t shibui/ml-system-in-actions:shadow_ab_pattern_client_0.0.1 \
	-f Dockerfile.client \
	.
```

2. Kubernetesでサービスを起動

```sh
$ make deploy
istioctl install -y
kubectl apply -f manifests/namespace.yml
kubectl apply -f manifests/

# 稼働確認
$ kubectl -n shadow-ab get all
NAME                            READY   STATUS    RESTARTS   AGE
pod/client                      2/2     Running   0          44s
pod/iris-rf-7cd8cb9d78-lcsq6    2/2     Running   0          43s
pod/iris-svc-74dc7654b8-xthmh   2/2     Running   0          44s

NAME           TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
service/iris   ClusterIP   10.4.0.14    <none>        8000/TCP   43s

NAME                       READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/iris-rf    3/3     3            3           44s
deployment.apps/iris-svc   3/3     3            3           44s

NAME                                  DESIRED   CURRENT   READY   AGE
replicaset.apps/iris-rf-7cd8cb9d78    3         3         3       44s
replicaset.apps/iris-svc-74dc7654b8   3         3         3       44s

NAME                                           REFERENCE             TARGETS         MINPODS   MAXPODS   REPLICAS   AGE
horizontalpodautoscaler.autoscaling/iris-rf    Deployment/iris-rf    <unknown>/70%   3         10        3          43s
horizontalpodautoscaler.autoscaling/iris-svc   Deployment/iris-svc   <unknown>/70%   3         10        3          43s
```

3. 起動したAPIにリクエスト

```sh
# クライアントに接続
$ kubectl -n shadow-ab exec -it pod/client bash

# 同じエンドポイントに複数回リクエストを送ります。
$ curl http://iris.shadow-ab.svc.cluster.local:8000/predict-test/000000
{"job_id":"000000","prediction":[0.9709315896034241,0.015583082102239132,0.013485366478562355]}
$ curl http://iris.shadow-ab.svc.cluster.local:8000/predict-test/000000
{"job_id":"000000","prediction":[0.9709315896034241,0.015583082102239132,0.013485366478562355]}
$ curl http://iris.shadow-ab.svc.cluster.local:8000/predict-test/000000
{"job_id":"000000","prediction":[0.9709315896034241,0.015583082102239132,0.013485366478562355]}
$ curl http://iris.shadow-ab.svc.cluster.local:8000/predict-test/000000
{"job_id":"000000","prediction":[0.9709315896034241,0.015583082102239132,0.013485366478562355]}
$ curl http://iris.shadow-ab.svc.cluster.local:8000/predict-test/000000
{"job_id":"000000","prediction":[0.9709315896034241,0.015583082102239132,0.013485366478562355]}

# クライアントをエクジットして、iris-rfおよびiris-svcのログを参照します。iris-rf、iris-svc両方で推論が実行されていることがわかります。
$ kubectl -n shadow-ab logs pod/iris-rf-7cd8cb9d78-lcsq6 iris-rf
[2021-02-06 09:51:35] [INFO] [14] [src.app.routers.routers] [_predict_test] [37] execute: [000000]
[2021-02-06 09:51:35] [INFO] [14] [src.ml.prediction] [predict] [50] predict proba [0.99999994 0.         0.        ]
[2021-02-06 09:51:35] [INFO] [14] [src.app.routers.routers] [wrapper] [33] [iris_rf.onnx] [/predict-test] [000000] [1.0628700256347656 ms] [None] [[0.9999999403953552, 0.0, 0.0]]
[2021-02-06 09:51:35] [INFO] [14] [uvicorn.access] [send] [458] 10.0.2.36:0 - "GET /predict-test/000000 HTTP/1.1" 200

$ kubectl -n shadow-ab logs pod/iris-svc-74dc7654b8-xthmh iris-svc
[2021-02-06 09:51:35] [INFO] [8] [src.app.routers.routers] [_predict_test] [37] execute: [000000]
[2021-02-06 09:51:35] [INFO] [8] [src.ml.prediction] [predict] [50] predict proba [0.97093159 0.01558308 0.01348537]
[2021-02-06 09:51:35] [INFO] [8] [src.app.routers.routers] [wrapper] [33] [iris_svc.onnx] [/predict-test] [000000] [0.8084774017333984 ms] [None] [[0.9709315896034241, 0.015583082102239132, 0.013485366478562355]]
[2021-02-06 09:51:35] [INFO] [8] [uvicorn.access] [send] [458] 127.0.0.1:48148 - "GET /predict-test/000000 HTTP/1.1" 200
```

4. Kubernetesからサービスを削除

```sh
$ kubectl delete ns shadow-ab
$ istioctl x uninstall --purge -y
$ kubectl delete ns istio-system
```

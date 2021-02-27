# prediction log pattern

## 目的

推論のログを記録します。

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
~/ml-system-in-actions/chapter5_operations/prediction_log_pattern
```

1. Docker イメージをビルド

```sh
$ make build_all
# 実行されるコマンド
# docker build \
#     -t shibui/ml-system-in-actions:prediction_log_pattern_api_0.0.1 \
#     -f Dockerfile.api \
#     .
# docker build \
#     -t shibui/ml-system-in-actions:prediction_log_pattern_client_0.0.1 \
#     -f Dockerfile.client \
#     .
```

2. Kubernetes で各サービスを起動

```sh
$ make deploy
# 実行されるコマンド
# kubectl apply -f manifests/namespace.yml
# kubectl apply -f manifests/

# デプロイメント確認
$ kubectl -n prediction-log get all
# 出力
# NAME                       READY   STATUS    RESTARTS   AGE
# pod/api-85d44df447-2v95h   2/2     Running   0          67s
# pod/api-85d44df447-2xhrn   2/2     Running   0          67s
# pod/api-85d44df447-xwfbn   2/2     Running   0          67s
# pod/client                 1/1     Running   0          67s

# NAME          TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
# service/api   ClusterIP   10.4.7.145   <none>        8000/TCP   67s

# NAME                  READY   UP-TO-DATE   AVAILABLE   AGE
# deployment.apps/api   3/3     3            3           67s

# NAME                             DESIRED   CURRENT   READY   AGE
# replicaset.apps/api-85d44df447   3         3         3       67s
```

3. 起動した API にリクエスト

```sh
# 起動したservice/apiにポートフォワード
$ kubectl -n prediction-log port-forward service/api 8000:8000 &

# ヘルスチェック
$ curl localhost:8000/health
# 出力
# {
#   "health":"ok"
# }

# メタデータ
$ curl localhost:8000/metadata
# 出力
# {
#   "data_type": "float32",
#   "data_structure": "(1,4)",
#   "data_sample": [
#     [
#       5.1,
#       3.5,
#       1.4,
#       0.2
#     ]
#   ],
#   "prediction_type": "float32",
#   "prediction_structure": "(1,3)",
#   "prediction_sample": [
#     0.97093159,
#     0.01558308,
#     0.01348537
#   ],
#   "outlier_type": "bool, float32",
#   "outlier_structure": "(1,2)",
#   "outlier_sample": [
#     false,
#     0.4
#   ]
# }


# ラベル一覧
$ curl localhost:8000/label
# 出力
# {
#   "0": "setosa",
#   "1": "versicolor",
#   "2": "virginica"
# }


# テストデータで推論リクエスト
$ curl localhost:8000/predict/test
# 出力
# {
#   "job_id": "ee1b0d",
#   "prediction": [
#     0.9709315896034241,
#     0.015583082102239132,
#     0.013485366478562355
#   ],
#   "is_outlier": false,
#   "outlier_score": 0.1915884017944336
# }


# 推論をリクエスト
$ curl \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"data": [[6.7, 3.0,  5.2, 2.3]]}' \
    localhost:8000/predict
# 出力
# {
#   "job_id": "1934ee",
#   "prediction": [
#     0.009793723002076149,
#     0.009877714328467846,
#     0.9803286194801331
#   ],
#   "is_outlier": false,
#   "outlier_score": 0.44043588638305664
# }

# ログを確認
$ kubectl -n prediction-log logs deployment.apps/api api
# 出力
# [2021-02-06 08:39:49] [INFO] [10] [src.app.routers.routers] [_predict] [81] execute: [d7a0a7]
# [2021-02-06 08:39:49] [INFO] [10] [src.ml.prediction] [predict] [47] predict proba [0.00979372 0.00987771 0.98032862]
# [2021-02-06 08:39:49] [INFO] [10] [src.ml.outlier_detection] [predict] [38] outlier score 0.44043588638305664
# [2021-02-06 08:39:49] [INFO] [10] [src.app.routers.routers] [wrapper] [33] [/predict] [d7a0a7] [1.0488033294677734 ms] [data=[[6.7, 3.0, 5.2, 2.3]]] [[0.009793723002076149, 0.009877714328467846, 0.9803286194801331]] [False] [0.44043588638305664]
# [2021-02-06 08:39:49] [INFO] [10] [uvicorn.access] [send] [458] 127.0.0.1:33446 - "POST /predict HTTP/1.1" 200
```

4. サービスを削除

```sh
$ kubectl delete ns prediction-log
# 出力
# namespace "prediction-log" deleted
```

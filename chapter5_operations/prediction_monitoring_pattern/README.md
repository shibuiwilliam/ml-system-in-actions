# prediction monitoring pattern

## 目的

推論のログを監視します。

## 前提

- Python 3.8 以上
- Docker
- Docker compose

## 使い方

0. カレントディレクトリ

```sh
$ pwd
~/ml-system-in-actions/chapter5_operations/prediction_monitoring_pattern
```

1. Docker イメージをビルド

```sh
$ make build_all
# 実行されるコマンド
# docker build \
#     -t shibui/ml-system-in-actions:prediction_monitoring_pattern_api_0.0.1 \
#     -f Dockerfile.api \
#     .
# docker build \
#     -t shibui/ml-system-in-actions:prediction_monitoring_pattern_job_0.0.1 \
#     -f Dockerfile.job \
#     .
```

2. Docker compose で各サービスを起動

```sh
$ make c_up
# 実行されるコマンド
# docker-compose \
#     -f ./docker-compose.yml \
#     up -d
```

3. 起動した API にリクエスト

```sh
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
#   "job_id": "3315b9",
#   "prediction": [
#     0.9709315896034241,
#     0.015583082102239132,
#     0.013485366478562355
#   ],
#   "is_outlier": false,
#   "outlier_score": 0.1915884017944336
# }


# 画像をリクエスト
$ curl \
    -X POST \
    -H "Content-Type: application/json" \
    -d '{"data": [[1.0, 2.0, 3.0, 4.0]]}' \
    localhost:8000/predict
# 出力
# {
#   "job_id": "dc138f",
#   "prediction": [
#     0.3613327741622925,
#     0.2574760615825653,
#     0.3811912536621094
#   ],
#   "prediction_elapsed": 0.5145072937011719,
#   "is_outlier": true,
#   "outlier_score": -2.941023349761963,
#   "outlier_elapsed": 0.2186298370361328
# }

# ログの確認
$ docker logs monitor
# 出力
# [2021-02-06 08:44:00,119] [1] [__main__] [INFO] start monitoring...
# [2021-02-06 08:44:00,120] [1] [__main__] [INFO] time between 2021-02-06 08:42:00 and 2021-02-06 08:44:00
# [2021-02-06 08:44:00,272] [1] [__main__] [INFO] prediction_logs between 2021-02-06 08:42:00 and 2021-02-06 08:44:00: 0
# [2021-02-06 08:44:00,273] [1] [__main__] [INFO] outlier_logs between 2021-02-06 08:42:00 and 2021-02-06 08:44:00: 0
# [2021-02-06 08:45:00,229] [1] [__main__] [INFO] time between 2021-02-06 08:43:00 and 2021-02-06 08:45:00
# [2021-02-06 08:45:00,267] [1] [__main__] [INFO] prediction_logs between 2021-02-06 08:43:00 and 2021-02-06 08:45:00: 277
# [2021-02-06 08:45:00,268] [1] [__main__] [INFO] outlier_logs between 2021-02-06 08:43:00 and 2021-02-06 08:45:00: 277
# [2021-02-06 08:45:00,268] [1] [__main__] [INFO] evaluate predictions...
# [2021-02-06 08:45:00,268] [1] [__main__] [INFO] average sepal length: 5.804332129963901
# [2021-02-06 08:45:00,269] [1] [__main__] [INFO] average sepal width: 3.0205776173285215
# [2021-02-06 08:45:00,269] [1] [__main__] [INFO] average petal length: 3.7548736462093877
# [2021-02-06 08:45:00,269] [1] [__main__] [INFO] average petal width: 1.2036101083032484
# [2021-02-06 08:45:00,269] [1] [__main__] [INFO] done evaluating predictions
# [2021-02-06 08:45:00,269] [1] [__main__] [INFO] evaluate outliers...
# [2021-02-06 08:45:00,269] [1] [__main__] [INFO] outliers: 35
# [2021-02-06 08:45:00,269] [1] [__main__] [INFO] done evaluating outliers
# [2021-02-06 08:46:00,254] [1] [__main__] [INFO] time between 2021-02-06 08:44:00 and 2021-02-06 08:46:00
# [2021-02-06 08:46:00,324] [1] [__main__] [INFO] prediction_logs between 2021-02-06 08:44:00 and 2021-02-06 08:46:00: 833
# [2021-02-06 08:46:00,324] [1] [__main__] [INFO] outlier_logs between 2021-02-06 08:44:00 and 2021-02-06 08:46:00: 833
# [2021-02-06 08:46:00,324] [1] [__main__] [INFO] evaluate predictions...
# [2021-02-06 08:46:00,326] [1] [__main__] [INFO] average sepal length: 5.7715486194477705
# [2021-02-06 08:46:00,326] [1] [__main__] [INFO] average sepal width: 3.027010804321725
# [2021-02-06 08:46:00,326] [1] [__main__] [INFO] average petal length: 3.709483793517402
# [2021-02-06 08:46:00,326] [1] [__main__] [INFO] average petal width: 1.184753901560627
# [2021-02-06 08:46:00,326] [1] [__main__] [INFO] done evaluating predictions
# [2021-02-06 08:46:00,326] [1] [__main__] [INFO] evaluate outliers...
# [2021-02-06 08:46:00,326] [1] [__main__] [INFO] outliers: 109
# [2021-02-06 08:46:00,326] [1] [__main__] [INFO] done evaluating outliers
```

4. Docker compose を停止

```sh
$ make c_down
# 実行されるコマンド
# docker-compose \
#     -f ./docker-compose.yml \
#     down
```

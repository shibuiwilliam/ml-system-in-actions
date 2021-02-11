# ml-system-in-actions
machine learning system examples

## tl;dr

- 本レポジトリは2021年XX月翔泳社出版『機械学習システムデザインパターン』のサンプルコード集です。
- 本レポジトリでは機械学習のモデル学習、リリース、推論器の稼働、運用のためのコードおよび実行環境を用例ごとに提供します。

## 実行環境

- Python 3.8以上
- Docker
- Docker-compose
- （一部）Kubernetesまたはminikube
- （一部）Android Studio

本レポジトリではプログラムの実行環境としてDocker、Docker-compose、（一部）Kubernetes/minikube、（一部）Android Studioを使用します。
また、コマンドラインとして `kubectl`、`istioctl` を使用します。
各種ミドルウェア、開発環境、コマンドラインは以下公式ドキュメントを参考にインストールしてください。

- [Docker](https://docs.docker.com/get-docker/)
- [Docker-compose](https://docs.docker.jp/compose/toc.html)
- [Kubernetesクラスター構築](https://kubernetes.io/ja/docs/setup/)
- [minikube](https://kubernetes.io/ja/docs/setup/learning-environment/minikube/)
- [kubectl](https://kubernetes.io/ja/docs/tasks/tools/install-kubectl/)
- [istioctl](https://istio.io/latest/docs/setup/getting-started/)
- [Android Studio](https://developer.android.com/studio/install)

## コード一覧

本レポジトリが提供するプログラムは以下に示す各プログラムのディレクトリで実行されることを想定して開発されています。
各プログラムを実行する際は目的のディレクトリに移動してください。
各プログラムの実行方法は各プログラムディレクトリ配下のREADMEに示してあります。

.</br>
├── [chapter2_training](./chapter2_training/)</br>
│   ├── [cifar10](./chapter2_training/cifar10)</br>
│   ├── [iris_binary](./chapter2_training/iris_binary)</br>
│   ├── [iris_sklearn_outlier](./chapter2_training/iris_sklearn_outlier)</br>
│   ├── [iris_sklearn_rf](./chapter2_training/iris_sklearn_rf)</br>
│   ├── [iris_sklearn_svc](./chapter2_training/iris_sklearn_svc)</br>
│   └── [model_db](./chapter2_training/model_db)</br>
├── [chapter3_release_patterns](./chapter3_release_patterns)</br>
│   ├── [model_in_image_pattern](./chapter3_release_patterns/model_in_image_pattern)</br>
│   └── [model_load_pattern](./chapter3_release_patterns/model_load_pattern)</br>
├── [chapter4_serving_patterns](./chapter4_serving_patterns/)</br>
│   ├── [asynchronous_pattern](./chapter4_serving_patterns/asynchronous_pattern)</br>
│   ├── [batch_pattern](./chapter4_serving_patterns/batch_pattern)</br>
│   ├── [data_cache_pattern](./chapter4_serving_patterns/data_cache_pattern)</br>
│   ├── [edge_ai_pattern](./chapter4_serving_patterns/edge_ai_pattern)</br>
│   ├── [horizontal_microservice_pattern](./chapter4_serving_patterns/horizontal_microservice_pattern)</br>
│   ├── [prediction_cache_pattern](./chapter4_serving_patterns/prediction_cache_pattern)</br>
│   ├── [prep_pred_pattern](./chapter4_serving_patterns/prep_pred_pattern)</br>
│   ├── [sync_async_pattern](./chapter4_serving_patterns/sync_async_pattern)</br>
│   ├── [synchronous_pattern](./chapter4_serving_patterns/synchronous_pattern)</br>
│   └── [web_single_pattern](./chapter4_serving_patterns/web_single_pattern)</br>
├── [chapter5_operations](./chapter5_operations/)</br>
│   ├── [prediction_log_pattern](./chapter5_operations/prediction_log_pattern)</br>
│   └── [prediction_monitoring_pattern](./chapter5_operations/prediction_monitoring_pattern)</br>
└── [chapter6_operation_management](./chapter6_operation_management/)</br>
    ├── [circuit_breaker_pattern](./chapter6_operation_management/circuit_breaker_pattern)</br>
    ├── [condition_based_pattern](./chapter6_operation_management/condition_based_pattern)</br>
    ├── [load_test_pattern](./chapter6_operation_management/load_test_pattern)</br>
    ├── [online_ab_pattern](./chapter6_operation_management/online_ab_pattern)</br>
    ├── [paramater_based_pattern](./chapter6_operation_management/paramater_based_pattern)</br>
    └── [shadow_ab_pattern](./chapter6_operation_management/shadow_ab_pattern)</br>



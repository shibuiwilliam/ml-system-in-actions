import os
from locust import HttpUser, TaskSet, task, between, constant


class APIUser(HttpUser):
    wait_time = between(1, 10)

    @task(int(os.getenv("GET_HEALTH_RATIO", 0)))
    def get_health(self):
        self.client.get(url="/health", verify=False)

    @task(int(os.getenv("GET_PREDICT_RATIO", 0)))
    def get_predict(self):
        self.client.get(url="/predict", verify=False)

    @task(int(os.getenv("GET_PREDICT_LABEL_RATIO", 0)))
    def get_predict_label(self):
        self.client.get(url="/predict/label", verify=False)

    @task(int(os.getenv("POST_PREDICT_RATIO", 0)))
    def post_predict(self):
        self.client.post(url="/predict", json={"input_data": [5.2, 3.1, 0.1, 1.0]}, headers={"content-type": "application/json"}, verify=False)

    @task(int(os.getenv("POST_PREDICT_LABEL_RATIO", 0)))
    def post_predict_label(self):
        self.client.post(url="/predict/label", json={"input_data": [5.2, 3.1, 0.1, 1.0]}, headers={"content-type": "application/json"}, verify=False)

    @task(int(os.getenv("REDIRECT_POST_PREDICT_RATIO", 0)))
    def redirect_post_predict(self):
        self.client.post(
            url="/redirect/predict", json={"data": {"input_data": [5.2, 3.1, 0.1, 1.0]}}, headers={"content-type": "application/json"}, verify=False
        )

    @task(int(os.getenv("REDIRECT_POST_PREDICT_LABEL_RATIO", 0)))
    def redirect_post_predict_label(self):
        self.client.post(
            url="/redirect/predict/label", json={"data": {"input_data": [5.2, 3.1, 0.1, 1.0]}}, headers={"content-type": "application/json"}, verify=False
        )

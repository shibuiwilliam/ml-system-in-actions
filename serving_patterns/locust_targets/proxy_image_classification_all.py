import os
from locust import HttpUser, TaskSet, task, between, constant
import image_data


class APIUser(HttpUser):
    wait_time = between(1, 10)

    @task(int(os.getenv("GET_HEALTH_RATIO", 0)))
    def get_health(self):
        self.client.get(url="/health", verify=False)

    @task(int(os.getenv("GET_HEALTH_ALL_RATIO", 0)))
    def get_health_all(self):
        self.client.get(url="/redirect/health", verify=False)

    @task(int(os.getenv("GET_PREDICT_RATIO", 0)))
    def get_redirect_predict(self):
        self.client.get(url="/redirect/predict", verify=False)

    @task(int(os.getenv("GET_PREDICT_LABEL_RATIO", 0)))
    def get_redirect_predict_label(self):
        self.client.get(url="/redirect/predict/label", verify=False)

    @task(int(os.getenv("POST_PREDICT_RATIO", 0)))
    def post_redirect_predict(self):
        self.client.post(url="/redirect/predict", json=image_data.data, headers={"content-type": "application/json"}, verify=False)

    @task(int(os.getenv("POST_PREDICT_LABEL_RATIO", 0)))
    def post_redirect_predict_label(self):
        self.client.post(url="/redirect/predict/label", json=image_data.data, headers={"content-type": "application/json"}, verify=False)

    @task(int(os.getenv("POST_PREDICT_ASYNC_RATIO", 0)))
    def post_redirect_predict_async(self):
        self.client.post(url="/redirect/predict/async", json=image_data.data, headers={"content-type": "application/json"}, verify=False)

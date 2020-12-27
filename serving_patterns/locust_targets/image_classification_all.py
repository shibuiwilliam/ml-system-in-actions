import os
from locust import HttpUser, TaskSet, task, between, constant
import image_data


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
        self.client.post(url="/predict", json=image_data.image_data, headers={"content-type": "application/json"}, verify=False)

    @task(int(os.getenv("POST_PREDICT_LABEL_RATIO", 0)))
    def post_predict_label(self):
        self.client.post(url="/predict/label", json=image_data.image_data, headers={"content-type": "application/json"}, verify=False)

    @task(int(os.getenv("POST_PREDICT_ASYNC_RATIO", 0)))
    def post_predict_async(self):
        self.client.post(url="/predict/async", json=image_data.image_data, headers={"content-type": "application/json"}, verify=False)

    @task(int(os.getenv("POST_PREDICT_FLASK_RATIO", 0)))
    def post_predict_flask(self):
        self.client.post(url="/predict/image", json=image_data.image_data, headers={"content-type": "application/json"}, verify=False)

    @task(int(os.getenv("POST_PREDICT_LABEL_FLASK_RATIO", 0)))
    def post_predict_label_flask(self):
        self.client.post(url="/predict/image/label", json=image_data.image_data, headers={"content-type": "application/json"}, verify=False)

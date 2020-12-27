import os
import random
from sklearn.datasets import load_iris
from locust import HttpUser, TaskSet, task, between, constant


class APIUser(HttpUser):
    wait_time = between(1, 10)
    iris = load_iris()
    data = iris["data"]
    num_requests_sent = 0
    request_intervals = int(os.getenv("REQUEST_INTERVALS", 500))

    def a_or_b(self):
        ab_test_group = ["group_a", "group_b"]
        return random.choice(ab_test_group)

    def get_random_data_in_time(self):
        self.num_requests_sent += 1
        if self.num_requests_sent < self.request_intervals:
            return self.data[random.randrange(0, len(self.data))]
        elif self.request_intervals <= self.num_requests_sent < self.request_intervals * 1.5:
            a = self.data[random.randrange(0, len(self.data))]
            for i in range(4):
                r = random.random()
                b = [0 for _ in range(4)]
                if r < 0.2:
                    b[i] = round(a[i] - 1.0, 1)
                elif r < 0.4:
                    b[i] = round(a[i] - 0.6, 1)
                elif r < 0.6:
                    b[i] = round(a[i] - 0.4, 1)
                elif r < 0.8:
                    b[i] = round(a[i] + 0.1, 1)
                else:
                    b[i] = round(a[i], 1)
                if b[i] <= 0:
                    b[i] = 0.1
            return b
        elif self.request_intervals * 1.5 <= self.num_requests_sent < self.request_intervals * 2.0:
            a = self.data[random.randrange(0, len(self.data))]
            for i in range(4):
                r = random.random()
                b = [0 for _ in range(4)]
                if r < 0.2:
                    b[i] = round(a[i] * 0.5, 1)
                elif r < 0.4:
                    b[i] = round(a[i] * 0.8, 1)
                elif r < 0.6:
                    b[i] = round(a[i] - 0.5, 1)
                elif r < 0.8:
                    b[i] = round(a[i] - 0.2, 1)
                else:
                    b[i] = round(a[i], 1)
                if b[i] <= 0:
                    b[i] = 0.1
            return b
        elif self.request_intervals * 2.0 <= self.num_requests_sent < self.request_intervals * 2.5:
            a = self.data[random.randrange(0, len(self.data))]
            for i in range(4):
                r = random.random()
                b = [0 for _ in range(4)]
                if r < 0.2:
                    b[i] = round(a[i] * 0.6 - 0.5, 1)
                elif r < 0.4:
                    b[i] = round(a[i] * 0.7 - 1.6, 1)
                elif r < 0.6:
                    b[i] = round(a[i] * 0.9 - 0.5, 1)
                elif r < 0.8:
                    b[i] = round(a[i] - 0.2, 1)
                else:
                    b[i] = round(a[i], 1)
                if b[i] <= 0:
                    b[i] = 0.1
            return b
        elif self.request_intervals * 2.5 <= self.num_requests_sent < self.request_intervals * 3.0:
            a = self.data[random.randrange(0, len(self.data))]
            for i in range(4):
                r = random.random()
                b = [0 for _ in range(4)]
                if r < 0.2:
                    b[i] = round(a[i] * 0.5 - 1.0, 1)
                elif r < 0.4:
                    b[i] = round(a[i] * 0.9, 1)
                elif r < 0.6:
                    b[i] = round(a[i] - 1.1, 1)
                elif r < 0.8:
                    b[i] = round(a[i] + 0.2, 1)
                else:
                    b[i] = round(a[i], 1)
                if b[i] <= 0:
                    b[i] = 0.1
            return b
        elif self.request_intervals * 3.0 <= self.num_requests_sent < self.request_intervals * 3.5:
            a = self.data[random.randrange(0, len(self.data))]
            for i in range(4):
                r = random.random()
                b = [0 for _ in range(4)]
                if r < 0.2:
                    b[i] = round(a[i] * 1.1 - 1.0, 1)
                elif r < 0.4:
                    b[i] = round(a[i] + 0.9, 1)
                elif r < 0.6:
                    b[i] = round(a[i] - 1.5, 1)
                elif r < 0.8:
                    b[i] = round(a[i] + 1.2, 1)
                else:
                    b[i] = round(a[i], 1)
                if b[i] <= 0:
                    b[i] = 0.1
            return b
        elif self.request_intervals * 4.0 <= self.num_requests_sent < self.request_intervals * 4.5:
            a = self.data[random.randrange(0, len(self.data))]
            for i in range(4):
                r = random.random()
                b = [0 for _ in range(4)]
                if r < 0.2:
                    b[i] = round(a[i] * 1.5 - 2.0, 1)
                elif r < 0.4:
                    b[i] = round(a[i] * 1.2, 1)
                elif r < 0.6:
                    b[i] = round(a[i] + 1.1, 1)
                elif r < 0.8:
                    b[i] = round(a[i] - 0.2, 1)
                else:
                    b[i] = round(a[i], 1)
                if b[i] <= 0:
                    b[i] = 0.1
            return b
        else:
            a = self.data[random.randrange(0, len(self.data))]
            for i in range(4):
                r = random.random()
                b = [0 for _ in range(4)]
                if r < 0.2:
                    b[i] = round(a[i] + 0.5, 1)
                elif r < 0.4:
                    b[i] = round(a[i] * 0.9 - 0.5, 1)
                elif r < 0.6:
                    b[i] = round(a[i] * 1.1 - 0.6, 1)
                elif r < 0.8:
                    b[i] = round(a[i] * 1.2, 1)
                else:
                    b[i] = round(a[i], 1)
                if b[i] <= 0:
                    b[i] = 0.1
            return b

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
        self.client.post(url="/predict", json={"input_data": self.get_random_data_in_time()}, headers={"content-type": "application/json"}, verify=False)

    @task(int(os.getenv("POST_PREDICT_LABEL_RATIO", 0)))
    def post_predict_label(self):
        self.client.post(url="/predict/label", json={"input_data": self.get_random_data_in_time()}, headers={"content-type": "application/json"}, verify=False)

    @task(int(os.getenv("REDIRECT_POST_PREDICT_RATIO", 0)))
    def redirect_post_predict(self):
        self.client.post(
            url="/redirect/predict",
            json={"data": {"input_data": self.get_random_data_in_time()}, "ab_test": self.a_or_b()},
            headers={"content-type": "application/json"},
            verify=False,
        )

    @task(int(os.getenv("REDIRECT_POST_PREDICT_LABEL_RATIO", 0)))
    def redirect_post_predict_label(self):
        self.client.post(
            url="/redirect/predict/label",
            json={"data": {"input_data": self.get_random_data_in_time()}, "ab_test": self.a_or_b()},
            headers={"content-type": "application/json"},
            verify=False,
        )

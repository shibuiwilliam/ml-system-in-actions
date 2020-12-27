from locust import HttpUser, TaskSet, task, between, constant


class APIUser(HttpUser):
    wait_time = between(1, 10)

    @task(1)
    def health(self):
        self.client.get("/health", verify=False)

from locust import HttpUser, TaskSet, task


class TestViews(TaskSet):
    @task
    def index(self):
        self.client.get('/')


class WebSite(HttpUser):
    host = "http://0.0.0.0:8000"
    task_set = TestViews
    min_wait = 1000
    max_wait = 2000


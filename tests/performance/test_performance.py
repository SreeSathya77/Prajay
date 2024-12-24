from locust import HttpUser, task, between

class PerformanceTest(HttpUser):
    wait_time = between(1, 3)
    
    @task
    def test_endpoint(self):
        self.client.get("/api/endpoint")
        self.client.post("/api/data", json={"key": "value"})
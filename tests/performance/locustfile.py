from locust import HttpUser, task, between
import json

class UserBehavior(HttpUser):
    wait_time = between(1, 3)
    
    def on_start(self):
        self.login()
    
    def login(self):
        self.client.post("/login", 
            json={
                "username": "testuser",
                "password": "password123"
            }
        )
    
    @task(3)
    def view_dashboard(self):
        self.client.get("/dashboard")
    
    @task(1)
    def create_item(self):
        self.client.post("/items", 
            json={
                "name": "Test Item",
                "description": "Performance test item"
            }
        )
import json
import random
from datetime import datetime, timezone

from faker import Faker
from locust import HttpUser, TaskSet, between, task

from src.core.settings import settings
from src.web.api.signing import generate_signature

faker = Faker()


def get_headers(method, body):
    timestamp = str(datetime.now(timezone.utc).timestamp() * 1000)
    signature = generate_signature(method, body, timestamp, settings.secret_key)

    headers = {
        "x-signature": signature,
        "x-timestamp": timestamp,
        "Content-Type": "application/json",
    }
    return headers


class HeroTasks(TaskSet):
    @task
    def create_hero(self):
        hero_data = {
            "name": faker.first_name(),
            "secret_name": faker.name(),
            "age": random.randint(18, 80),
        }

        headers = get_headers("POST", json.dumps(hero_data))
        response = self.client.post("/api/heroes/", json=hero_data, headers=headers)

        print(f"Status: {response.status_code}")
        try:
            print("Response:", response.json())
        except Exception as e:
            print("Error parsing response:", e)


class PythonTemplateLoadTest(HttpUser):
    tasks = [HeroTasks]
    host = "http://localhost:8000"
    wait_time = between(1, 3)

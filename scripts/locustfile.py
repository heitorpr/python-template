import json
import random
from datetime import datetime, timezone

from faker import Faker
from locust import HttpUser, between, task

from src.core.settings import settings
from src.web.api.signing import generate_signature

API_URL = "/api/heroes/"
SECRET_KEY = settings.secret_key
faker = Faker()


class PythonTemplateLoadTest(HttpUser):
    wait_time = between(1, 3)

    @task
    def create_hero(self):
        hero_data = {
            "name": faker.first_name(),
            "secret_name": faker.name(),
            "age": random.randint(18, 80),
        }

        timestamp = str(datetime.now(timezone.utc).timestamp() * 1000)
        signature = generate_signature("POST", json.dumps(hero_data), timestamp, SECRET_KEY)

        headers = {
            "x-signature": signature,
            "x-timestamp": timestamp,
            "Content-Type": "application/json",
        }

        response = self.client.post(API_URL, json=hero_data, headers=headers)
        print(f"Status: {response.status_code}")
        try:
            print("Response:", response.json())
        except Exception as e:
            print("Error parsing response:", e)

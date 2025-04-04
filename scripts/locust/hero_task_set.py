import json
import random
from datetime import datetime, timezone

from faker import Faker
from locust import TaskSet, task

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
        self.client.post("/api/heroes/", json=hero_data, headers=headers)

    @task
    def get_hero(self):
        hero_data = {
            "name": faker.first_name(),
            "secret_name": faker.name(),
            "age": random.randint(18, 80),
        }

        headers = get_headers("POST", json.dumps(hero_data))
        response = self.client.post("/api/heroes/", json=hero_data, headers=headers)

        hero_id = response.json().get("uuid")

        headers = get_headers("GET", "")
        response = self.client.get(f"/api/heroes/{hero_id}", headers=headers)

    @task
    def update_hero(self):
        hero_data = {
            "name": faker.first_name(),
            "secret_name": faker.name(),
            "age": random.randint(18, 80),
        }

        headers = get_headers("POST", json.dumps(hero_data))
        response = self.client.post("/api/heroes/", json=hero_data, headers=headers)

        hero_id = response.json().get("uuid")

        hero_update_data = {
            "age": random.randint(18, 80),
        }

        headers = get_headers("PUT", json.dumps(hero_update_data))
        response = self.client.put(
            f"/api/heroes/{hero_id}", json=hero_update_data, headers=headers
        )

    @task
    def delete_hero(self):
        hero_data = {
            "name": faker.first_name(),
            "secret_name": faker.name(),
            "age": random.randint(18, 80),
        }

        headers = get_headers("POST", json.dumps(hero_data))
        response = self.client.post("/api/heroes/", json=hero_data, headers=headers)

        hero_id = response.json().get("uuid")

        headers = get_headers("DELETE", "")
        response = self.client.delete(f"/api/heroes/{hero_id}", headers=headers)

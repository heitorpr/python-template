import json
import random
from datetime import datetime, timezone

from faker import Faker
from locust import TaskSet, task

from src.core.settings import settings
from src.web.api.signing import generate_signature

faker = Faker()


def get_headers(method: str, body: str) -> dict:
    timestamp = str(datetime.now(timezone.utc).timestamp() * 1000)
    signature = generate_signature(method, body, timestamp, settings.secret_key)

    return {
        "x-signature": signature,
        "x-timestamp": timestamp,
        "Content-Type": "application/json",
    }


def log_failure(action: str, response, extra_info=None):
    print(f"[{action}] - Status: {response.status_code}")
    print(f"Response: {response.text}")
    if extra_info:
        print(f"Info: {json.dumps(extra_info, indent=2)}")


class HeroTasks(TaskSet):
    def create_hero(self):
        hero_data = {
            "name": faker.first_name(),
            "secret_name": faker.name(),
            "age": random.randint(14, 23),
        }

        headers = get_headers("POST", json.dumps(hero_data))
        response = self.client.post("/api/heroes/", json=hero_data, headers=headers)

        if response.status_code != 201:
            log_failure("Create Hero", response, hero_data)
            return None

        return response.json().get("uuid")

    def get_hero(self, hero_id: str):
        headers = get_headers("GET", "")
        response = self.client.get(
            f"/api/heroes/{hero_id}", headers=headers, name="/api/heroes/{uuid}"
        )

        if response.status_code != 200:
            log_failure("Get Hero", response, {"hero_id": hero_id})
            return None

        return response.json().get("uuid")

    def update_hero(self, hero_id: str):
        update_data = {
            "age": random.randint(70, 120),
        }

        headers = get_headers("PUT", json.dumps(update_data))
        response = self.client.put(
            f"/api/heroes/{hero_id}", json=update_data, headers=headers, name="/api/heroes/{uuid}"
        )

        if response.status_code != 200:
            log_failure("Update Hero", response, {"hero_id": hero_id, "data": update_data})
            return None

        return response.json().get("uuid")

    def delete_hero(self, hero_id: str):
        headers = get_headers("DELETE", "")
        response = self.client.delete(
            f"/api/heroes/{hero_id}", headers=headers, name="/api/heroes/{uuid}"
        )

        if response.status_code != 204:
            log_failure("Delete Hero", response, {"hero_id": hero_id})

    @task
    def birth_and_death_of_a_hero(self):
        hero_id = self.create_hero()
        if not hero_id:
            return

        hero_id = self.get_hero(hero_id)
        if not hero_id:
            return

        hero_id = self.update_hero(hero_id)
        if not hero_id:
            return

        self.delete_hero(hero_id)

from faker import Faker
from locust import HttpUser, between

from scripts.locust.hero_task_set import HeroTasks

faker = Faker()


class PythonTemplateLoadTest(HttpUser):
    tasks = [HeroTasks]
    host = "http://localhost:8000"
    wait_time = between(1, 3)

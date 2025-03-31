import asyncio
import random
from datetime import datetime, timezone

import httpx
from faker import Faker

from src.core.settings import settings
from tests.utils.signing import generate_signature

API_URL = "http://localhost:8000/api/heroes/"
SECRET_KEY = settings.secret_key
faker = Faker()


async def create_hero():
    """Gera um herói aleatório e o envia para a API"""
    hero_data = {
        "name": faker.first_name(),
        "secret_name": faker.name(),
        "age": random.randint(18, 80),
    }

    timestamp = int(datetime.now(timezone.utc).timestamp() * 1000)
    signature = generate_signature("POST", hero_data, timestamp, SECRET_KEY)

    headers = {
        "x-signature": signature,
        "x-timestamp": str(timestamp),
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(API_URL, json=hero_data, headers=headers)
        print(f"Status: {response.status_code}")
        print("Response:", response.json())


async def main():
    tasks = [create_hero() for _ in range(5)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())

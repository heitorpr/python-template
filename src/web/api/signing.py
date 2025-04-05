import hashlib
import hmac
from datetime import datetime, timezone

from fastapi import HTTPException, Request

from src.core.settings import settings


async def _signing(request: Request):
    signature = request.headers.get("x-signature")
    timestamp = request.headers.get("x-timestamp")

    if not signature or not timestamp:
        raise HTTPException(status_code=401, detail="Missing signature or timestamp")

    current_time = datetime.now(timezone.utc).timestamp() * 1000
    if abs(current_time - float(timestamp)) > settings.timestamp_signing_threshold:
        raise HTTPException(status_code=401, detail="Timestamp expired")

    body = await request.body()

    calculated_signature = generate_signature(
        request.method, body.decode(), timestamp, settings.secret_key
    )

    if calculated_signature != signature:
        raise HTTPException(status_code=401, detail="Invalid signature")


async def signing(request: Request):
    await _signing(request)


def generate_signature(method: str, body: str, timestamp: str, secret_key):
    payload = f"{method}|{body}|{timestamp}"
    return hmac.new(secret_key.encode(), payload.encode(), hashlib.sha256).hexdigest()

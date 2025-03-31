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

    current_time = int(datetime.now(timezone.utc).timestamp() * 1000)
    if abs(current_time - int(timestamp)) > settings.timestamp_signing_threshold:
        raise HTTPException(
            status_code=401, detail=f"Timestamp expired: {abs(current_time - int(timestamp))} ms"
        )

    content_type = request.headers.get("content-type", "").lower()

    body = (
        "formData"
        if "multipart/form-data" in content_type or "application/octet-stream" in content_type
        else await request.body()
    )

    body_decoded = body.decode() if isinstance(body, bytes) else str(body)

    method = request.method
    payload = f"{method}|{'formData' if body == 'formData' else body_decoded}|{timestamp}"

    calculated_signature = hmac.new(
        settings.secret_key.encode(), payload.encode(), hashlib.sha256
    ).hexdigest()

    if calculated_signature != signature:
        raise HTTPException(status_code=401, detail="Invalid signature")


async def signing(request: Request):
    await _signing(request)

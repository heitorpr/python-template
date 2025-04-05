import time

import pytest
from fastapi import HTTPException
from starlette.requests import Request

from src.core.settings import settings
from src.web.api.signing import generate_signature, signing


async def create_request(method, body, timestamp: str, signature, content_type="application/json"):
    headers = {
        "x-signature": signature,
        "x-timestamp": timestamp,
        "content-type": content_type,
    }
    scope = {
        "method": method,
        "type": "http",
        "headers": [(k.encode(), v.encode()) for k, v in headers.items()],
    }
    request = Request(scope)
    request._body = body.encode() if isinstance(body, str) else body
    return request


async def test_valid_request():
    timestamp = str(time.time() * 1000)
    body = "test_body"
    signature = generate_signature("POST", body, timestamp, settings.secret_key)
    request = await create_request("POST", body, timestamp, signature)
    await signing(request)


async def test_missing_signature():
    timestamp = str(time.time() * 1000)
    request = await create_request("POST", "test_body", timestamp, "")
    with pytest.raises(HTTPException) as exc:
        await signing(request)
    assert exc.value.status_code == 401
    assert exc.value.detail == "Missing signature or timestamp"


async def test_missing_timestamp():
    signature = generate_signature(
        "POST", "test_body", str(time.time() * 1000), settings.secret_key
    )
    request = await create_request("POST", "test_body", "", signature)
    with pytest.raises(HTTPException) as exc:
        await signing(request)
    assert exc.value.status_code == 401
    assert exc.value.detail == "Missing signature or timestamp"


async def test_expired_timestamp():
    old_timestamp = str(float(time.time() * 1000) - (settings.timestamp_signing_threshold + 1000))
    signature = generate_signature("POST", "test_body", old_timestamp, settings.secret_key)
    request = await create_request("POST", "test_body", old_timestamp, signature)
    with pytest.raises(HTTPException) as exc:
        await signing(request)
    assert exc.value.status_code == 401
    assert exc.value.detail == "Timestamp expired"


async def test_invalid_signature():
    timestamp = str(time.time() * 1000)
    request = await create_request("POST", "test_body", timestamp, "invalid_signature")
    with pytest.raises(HTTPException) as exc:
        await signing(request)

    assert exc.value.status_code == 401
    assert exc.value.detail == "Invalid signature"


async def test_multipart_form_data():
    timestamp = str(time.time() * 1000)
    signature = generate_signature("POST", "formData", timestamp, settings.secret_key)
    request = await create_request("POST", "formData", timestamp, signature, "multipart/form-data")
    await signing(request)

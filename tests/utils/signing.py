import hashlib
import hmac
import json


def generate_signature(method, body: str | dict, timestamp, secret_key):
    if isinstance(body, dict):
        body = json.dumps(body, separators=(",", ":"))

    payload = f"{method}|{body}|{timestamp}"
    return hmac.new(secret_key.encode(), payload.encode(), hashlib.sha256).hexdigest()

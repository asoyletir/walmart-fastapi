import os
import time
import httpx

WALMART_TOKEN_URL = (os.getenv("WALMART_TOKEN_URL") or "").strip()
if not WALMART_TOKEN_URL:
    raise RuntimeError("Missing WALMART_TOKEN_URL (set it to https://sandbox.walmartapis.com/v3/token for sandbox)")

_cached = {"token": None, "exp": 0.0}

async def get_token() -> dict:
    now = time.time()
    if _cached["token"] and now < _cached["exp"]:
        return _cached["token"]

    client_id = (os.getenv("WALMART_CLIENT_ID") or "").strip()
    client_secret = (os.getenv("WALMART_CLIENT_SECRET") or "").strip()
    if not client_id or not client_secret:
        raise RuntimeError("Missing WALMART_CLIENT_ID or WALMART_CLIENT_SECRET")

    headers = {"accept": "application/json", "content-type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials"}

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            WALMART_TOKEN_URL,
            headers=headers,
            data=data,
            auth=httpx.BasicAuth(client_id, client_secret),
        )

    if r.status_code >= 400:
        raise RuntimeError(f"Token error {r.status_code}: {r.text}")

    token = r.json()
    expires_in = int(token.get("expires_in", 900))
    _cached["token"] = token
    _cached["exp"] = time.time() + max(0, expires_in - 60)
    return token

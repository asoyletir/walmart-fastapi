import os
import httpx

WALMART_TOKEN_URL = "https://marketplace.walmartapis.com/v3/token"

async def get_token():
    client_id = (os.getenv("WALMART_CLIENT_ID") or "").strip()
    client_secret = (os.getenv("WALMART_CLIENT_SECRET") or "").strip()

    if not client_id or not client_secret:
        raise RuntimeError("Missing WALMART_CLIENT_ID or WALMART_CLIENT_SECRET")

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = "grant_type=client_credentials"

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(
            WALMART_TOKEN_URL,
            headers=headers,
            content=data,
            auth=httpx.BasicAuth(client_id, client_secret),
        )

    if r.status_code >= 400:
        raise RuntimeError(f"Token error {r.status_code}: {r.text}")

    return r.json()

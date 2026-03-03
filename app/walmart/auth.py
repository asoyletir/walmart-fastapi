import os
import httpx
import base64

WALMART_TOKEN_URL = "https://sandbox.walmartapis.com"

async def get_token():
    client_id = os.getenv("WALMART_CLIENT_ID")
    client_secret = os.getenv("WALMART_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise RuntimeError("Missing WALMART_CLIENT_ID or WALMART_CLIENT_SECRET")

    credentials = f"{client_id}:{client_secret}"
    encoded = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded}",
        "Accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = "grant_type=client_credentials"

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(WALMART_TOKEN_URL, headers=headers, content=data)

    # Debug amaçlı: 400 gelirse Walmart'ın döndürdüğü mesajı görelim
    if r.status_code >= 400:
        raise RuntimeError(f"Token error {r.status_code}: {r.text}")

    return r.json()

import os
import httpx
import base64

TOKEN_URLS = {
    "prod": "https://marketplace.walmartapis.com/v3/token",
    "production": "https://marketplace.walmartapis.com/v3/token",
    "sandbox": "https://sandbox.walmartapis.com/v3/token",
}

async def get_token():
    env = (os.getenv("WALMART_ENV") or "sandbox").lower()
    token_url = TOKEN_URLS.get(env, TOKEN_URLS["sandbox"])

    client_id = os.getenv("WALMART_CLIENT_ID")
    client_secret = os.getenv("WALMART_CLIENT_SECRET")

    if not client_id or not client_secret:
        raise RuntimeError("Missing WALMART_CLIENT_ID or WALMART_CLIENT_SECRET")

    # Basic Auth header manuel oluşturuyoruz
    credentials = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }

    data = "grant_type=client_credentials"

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            token_url,
            headers=headers,
            content=data,
        )

    response.raise_for_status()
    return response.json()

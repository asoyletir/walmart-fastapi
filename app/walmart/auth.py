import os
import httpx

WALMART_TOKEN_URL = "https://marketplace.walmartapis.com/v3/token"

async def get_token():
    client_id = os.getenv("WALMART_CLIENT_ID")
    client_secret = os.getenv("WALMART_CLIENT_SECRET")

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {
        "grant_type": "client_credentials"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            WALMART_TOKEN_URL,
            headers=headers,
            data=data,
            auth=(client_id, client_secret)
        )

    response.raise_for_status()
    return response.json()

from fastapi import FastAPI, HTTPException
from app.walmart.auth import get_token
import os

app = FastAPI(title="Walmart Integration API")

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/debug")
def debug():
    return {
        "token_url": os.getenv("WALMART_TOKEN_URL"),
        "base_url": os.getenv("WALMART_BASE_URL"),
        "client_id_len": len((os.getenv("WALMART_CLIENT_ID") or "").strip()),
        "client_secret_len": len((os.getenv("WALMART_CLIENT_SECRET") or "").strip()),
    }

@app.get("/token")
async def token():
    try:
        t = await get_token()
        return {"token_type": t.get("token_type"), "expires_in": t.get("expires_in")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

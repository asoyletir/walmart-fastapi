from fastapi import FastAPI, HTTPException
from app.walmart.auth import get_token
import os
import httpx

app = FastAPI(title="Walmart Integration API")

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/token")
async def token():
    try:
        t = await get_token()
        # access_token'i göstermeyelim (güvenlik)
        return {
            "token_type": t.get("token_type"),
            "expires_in": t.get("expires_in"),
            "scope": t.get("scope"),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/sandbox/test")
async def sandbox_test():
    """
    Token al -> sandbox base url üstünden basit bir endpoint'e istek at.
    Burada hedef: Bearer token gerçekten çalışıyor mu görmek.
    """
    try:
        t = await get_token()
        access = t.get("access_token")
        if not access:
            raise RuntimeError("No access_token returned")

        base = (os.getenv("WALMART_BASE_URL") or "https://sandbox.walmartapis.com").rstrip("/")
        url = f"{base}/v3/ca/feeds"  # çalışmazsa başka endpoint deneriz

        headers = {"Authorization": f"Bearer {access}", "Accept": "application/json"}

        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(url, headers=headers)

        return {"status": r.status_code, "body": r.text[:1000]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

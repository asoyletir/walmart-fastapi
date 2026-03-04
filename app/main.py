from fastapi import FastAPI, HTTPException
from app.walmart.auth import get_token
from app.walmart.legacy_client import legacy_request

app = FastAPI(title="Walmart Integration API")

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/token")
async def token():
    try:
        return await get_token()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/legacy/ping")
async def legacy_ping():
    """
    Dokümanın önerdiği basit GET çağrısı: Get All Feed Statuses ile test. :contentReference[oaicite:14]{index=14}
    """
    try:
        return await legacy_request("GET", "/v3/ca/feeds")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI, HTTPException
from app.walmart.auth import get_token

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

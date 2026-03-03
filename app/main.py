from fastapi import FastAPI
from app.walmart.auth import get_token

app = FastAPI(title="Walmart Integration API")

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/item/{sku}")
def get_item(sku: str):
    return {"sku": sku, "source": "dummy"}

@app.get("/token")
async def token():
    return await get_token()

from fastapi import FastAPI
from app.walmart.client import walmart_request

app = FastAPI(title="Walmart Integration API")

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/wm/ping")
async def wm_ping():
    # Basit bir GET ile imza doğrulaması yapalım
    # (Feed status endpoint’i genelde erişilebilir)
    return await walmart_request("GET", "/v3/ca/feeds")

@app.get("/wm/item/{sku}")
async def wm_item(sku: str):
    return await walmart_request("GET", f"/v3/ca/items/{sku}")

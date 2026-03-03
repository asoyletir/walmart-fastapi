from fastapi import FastAPI

app = FastAPI(title="Walmart Integration API")

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/item/{sku}")
def get_item(sku: str):
    # Şimdilik dummy. Sonraki adımda Walmart API çağrısı gelecek.
    return {"sku": sku, "source": "dummy"}

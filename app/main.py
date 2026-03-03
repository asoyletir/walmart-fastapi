import os
import base64
from fastapi import FastAPI
from app.walmart.auth import get_token

app = FastAPI(title="Walmart Integration API")

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/item/{sku}")
def get_item(sku: str):
    # Şimdilik dummy. Sonraki adımda Walmart API çağrısı gelecek.
    return {"sku": sku, "source": "dummy"}

@app.get("/token")
async def token():
    return await get_token()

@app.get("/debug-creds")
def debug_creds():
    """
    Secret'ı ifşa etmeden Render env değerlerinde boşluk/newline var mı kontrol eder.
    """
    cid = os.getenv("WALMART_CLIENT_ID") or ""
    cs = os.getenv("WALMART_CLIENT_SECRET") or ""
    token_url = (os.getenv("WALMART_TOKEN_URL") or "").strip()

    info = {
        "token_url_set": bool(token_url),
        "token_url": token_url,  # URL gizli değil, göstermek OK
        "client_id_len": len(cid),
        "client_secret_len": len(cs),
        "client_id_has_newline": ("\n" in cid) or ("\r" in cid) or ("\t" in cid),
        "client_secret_has_newline": ("\n" in cs) or ("\r" in cs) or ("\t" in cs),
        "client_id_starts_ends_whitespace": (cid != cid.strip()),
        "client_secret_starts_ends_whitespace": (cs != cs.strip()),
    }

    # Basic base64’ü sadece preview olarak gösteriyoruz (secret sızdırmadan)
    pair = f"{cid.strip()}:{cs.strip()}".encode()
    b64 = base64.b64encode(pair).decode()
    info["basic_b64_len"] = len(b64)
    info["basic_b64_preview"] = f"{b64[:6]}...{b64[-6:]}" if len(b64) >= 12 else b64

    return info

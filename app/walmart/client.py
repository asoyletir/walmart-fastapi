import os
import httpx
from app.walmart.signature import build_signed_headers


def _base_url() -> str:
    # Sandbox: https://sandbox.walmartapis.com
    return (os.getenv("WALMART_BASE_URL") or "https://sandbox.walmartapis.com").rstrip("/")


async def walmart_request(method: str, path: str, params: dict | None = None):
    base = _base_url()
    full_url = f"{base}{path}"

    headers = build_signed_headers(full_url=full_url, method=method)

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.request(method, full_url, headers=headers, params=params)

    if r.status_code >= 400:
        raise RuntimeError(f"Walmart error {r.status_code}: {r.text}")

    # Bazı endpoint'ler boş dönebilir
    if not r.text:
        return {"ok": True}

    return r.json()

import os
import httpx
from app.walmart.legacy_signature import build_legacy_headers


def _base_url() -> str:
    return (os.getenv("WALMART_BASE_URL") or "https://sandbox.walmartapis.com").rstrip("/")


async def legacy_request(method: str, path: str, params: dict | None = None):
    base = _base_url()
    full_url = f"{base}{path}"  # signature needs full URL incl path+query :contentReference[oaicite:13]{index=13}

    headers = build_legacy_headers(full_url=full_url, method=method)

    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.request(method, full_url, headers=headers, params=params)

    if r.status_code >= 400:
        raise RuntimeError(f"Walmart error {r.status_code}: {r.text}")

    return r.json() if r.text else {"ok": True}

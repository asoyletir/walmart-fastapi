import os, base64, time, uuid
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def _epoch_ms() -> str:
    return str(int(time.time() * 1000))


def _load_pkcs8_private_key_from_b64(key_b64: str):
    # Walmart: Base-64 encoded, PKCS#8 stored Private Key  :contentReference[oaicite:4]{index=4}
    key_der = base64.b64decode(key_b64)
    return serialization.load_der_private_key(key_der, password=None)


def build_legacy_headers(full_url: str, method: str) -> dict:
    consumer_id = (os.getenv("WM_CONSUMER_ID") or "").strip()
    private_key_b64 = (os.getenv("WM_PRIVATE_KEY_B64") or "").strip()
    channel_type = (os.getenv("WM_CHANNEL_TYPE") or "").strip()
    tenant_id = (os.getenv("WM_TENANT_ID") or "WALMART.CA").strip()

    if not consumer_id or not private_key_b64:
        raise RuntimeError("Missing WM_CONSUMER_ID or WM_PRIVATE_KEY_B64")
    if not channel_type:
        raise RuntimeError("Missing WM_CHANNEL_TYPE (mandatory for V3)")

    timestamp = _epoch_ms()

    # String-to-sign format from CA docs:
    # consumerId + "\n" + fullUrl + "\n" + METHOD + "\n" + timestamp_ms + "\n" :contentReference[oaicite:5]{index=5}
    string_to_sign = f"{consumer_id}\n{full_url}\n{method.upper()}\n{timestamp}\n".encode("utf-8")

    private_key = _load_pkcs8_private_key_from_b64(private_key_b64)
    signature = private_key.sign(
        string_to_sign,
        padding.PKCS1v15(),
        hashes.SHA256(),
    )
    signature_b64 = base64.b64encode(signature).decode("utf-8")

    return {
        "WM_SVC.NAME": "Walmart Gateway API",                    # required :contentReference[oaicite:6]{index=6}
        "WM_QOS.CORRELATION_ID": str(uuid.uuid4()),              # required :contentReference[oaicite:7]{index=7}
        "WM_SEC.TIMESTAMP": timestamp,                           # required :contentReference[oaicite:8]{index=8}
        "WM_SEC.AUTH_SIGNATURE": signature_b64,                  # required :contentReference[oaicite:9]{index=9}
        "WM_CONSUMER.CHANNEL.TYPE": channel_type,                # required for V3 :contentReference[oaicite:10]{index=10}
        "WM_CONSUMER.ID": consumer_id,                           # required :contentReference[oaicite:11]{index=11}
        "WM_TENANT_ID": tenant_id,                               # required :contentReference[oaicite:12]{index=12}
        "Accept": "application/json",
    }

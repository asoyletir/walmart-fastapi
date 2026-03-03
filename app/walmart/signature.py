import base64
import time
import uuid
import os
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding


def _epoch_ms() -> str:
    return str(int(time.time() * 1000))


def _load_private_key_from_b64(b64_key: str):
    key_bytes = base64.b64decode(b64_key)
    return serialization.load_der_private_key(key_bytes, password=None)


def build_signed_headers(full_url: str, method: str) -> dict:
    """
    Walmart signature input (yaygın kullanılan format):
    consumerId + "\\n" + full_url + "\\n" + METHOD + "\\n" + timestamp_ms + "\\n"
    Sonra RSA-SHA256 ile imzalanıp base64 edilir.
    """
    consumer_id = (os.getenv("WM_CONSUMER_ID") or "").strip()
    key_b64 = (os.getenv("WM_PRIVATE_KEY_B64") or "").strip()
    channel_type = (os.getenv("WM_CHANNEL_TYPE") or "").strip()
    tenant_id = (os.getenv("WM_TENANT_ID") or "WALMART_CA").strip()

    if not consumer_id or not key_b64:
        raise RuntimeError("Missing WM_CONSUMER_ID or WM_PRIVATE_KEY_B64")

    timestamp = _epoch_ms()
    message = f"{consumer_id}\n{full_url}\n{method.upper()}\n{timestamp}\n".encode("utf-8")

    private_key = _load_private_key_from_b64(key_b64)
    signature = private_key.sign(
        message,
        padding.PKCS1v15(),
        hashes.SHA256(),
    )
    signature_b64 = base64.b64encode(signature).decode("utf-8")

    headers = {
        "WM_SEC.TIMESTAMP": timestamp,
        "WM_SEC.AUTH_SIGNATURE": signature_b64,
        "WM_CONSUMER.ID": consumer_id,
        "WM_QOS.CORRELATION_ID": str(uuid.uuid4()),
        "WM_TENANT_ID": tenant_id,
        "Accept": "application/json",
    }

    # Bazı CA endpoint’lerinde gerekli olabiliyor
    if channel_type:
        headers["WM_CONSUMER.CHANNEL.TYPE"] = channel_type

    return headers

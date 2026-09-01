#!/usr/bin/env python3
"""RSA 加密 + 加签调用共绩 Open API（S3 创建/重试/校验）。

用法:
  python3 scripts/call_encrypt.py POST /storage/nas/v1/encrypt/s3/check '{"supplier":"tencent",...}'
  python3 scripts/call_encrypt.py POST /storage/nas/v1/encrypt/s3/create @payload.json

环境变量:
  SUANLI_TOKEN                 必填，RSA 加验签模式 Token
  SUANLI_RSA_PRIVATE_KEY       必填，客户端私钥（PEM 或 Base64 PKCS#8）
  SUANLI_PLATFORM_PUBLIC_KEY   必填，平台公钥（创建密钥时返回，用于加密）
  SUANLI_BASE_URL              默认 https://openapi.suanli.cn
"""
from __future__ import annotations

import base64
import json
import os
import sys
import time
from pathlib import Path

try:
    import requests
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding
except ImportError:
    sys.stderr.write("请先安装依赖: pip install cryptography requests\n")
    sys.exit(1)

CHUNK_SIZE = 244
API_VERSION = "1.0.0"


def _looks_like_path(value: str) -> bool:
    return value.endswith((".pem", ".key", ".pub")) or os.path.isfile(value)


def _read_key_material(raw: str) -> bytes:
    raw = raw.strip().replace("\\n", "\n")
    if _looks_like_path(raw):
        return Path(raw).read_bytes()
    return raw.encode("utf-8")


def load_private_key(raw: str):
    data = _read_key_material(raw)
    if b"BEGIN" in data:
        return serialization.load_pem_private_key(data, password=None, backend=default_backend())
    der = base64.b64decode(raw.strip())
    try:
        return serialization.load_der_private_key(der, password=None, backend=default_backend())
    except ValueError:
        pem = (
            b"-----BEGIN PRIVATE KEY-----\n"
            + base64.encodebytes(der)
            + b"-----END PRIVATE KEY-----\n"
        )
        return serialization.load_pem_private_key(pem, password=None, backend=default_backend())


def load_public_key(raw: str):
    data = _read_key_material(raw)
    if b"BEGIN" in data:
        return serialization.load_pem_public_key(data, backend=default_backend())
    der = base64.b64decode(raw.strip())
    return serialization.load_der_public_key(der, backend=default_backend())


def encrypt_body(public_key, json_data: dict) -> str:
    payload = json.dumps(json_data, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    chunks = []
    for start in range(0, len(payload), CHUNK_SIZE):
        chunk = payload[start : start + CHUNK_SIZE]
        chunks.append(public_key.encrypt(chunk, padding.PKCS1v15()))
    return base64.b64encode(b"".join(chunks)).decode("utf-8")


def gen_sign(private_key, path: str, version: str, timestamp: str, token: str, body: str) -> str:
    content = f"{path}\n{version}\n{timestamp}\n{token}\n{body}"
    signature = private_key.sign(content.encode("utf-8"), padding.PKCS1v15(), hashes.SHA256())
    encoded = base64.b64encode(signature)
    if len(signature) != 256:
        raise SystemExit("签名解码后不是 256 字节，请换新 timestamp 重试")
    return encoded.decode("utf-8")


def read_json_payload(raw: str) -> dict:
    if raw.startswith("@"):
        text = Path(raw[1:]).read_text(encoding="utf-8")
    else:
        text = raw
    data = json.loads(text)
    if not isinstance(data, dict):
        raise SystemExit("请求体必须是 JSON object")
    return data


def main() -> int:
    if len(sys.argv) < 4:
        sys.stderr.write(
            "用法: call_encrypt.py POST /storage/nas/v1/encrypt/s3/check '<json>|@file.json'\n"
        )
        return 2

    method, path, payload = sys.argv[1], sys.argv[2], sys.argv[3]
    if method.upper() != "POST":
        sys.stderr.write("加密接口仅支持 POST\n")
        return 2
    if not path.startswith("/"):
        path = "/" + path

    token = os.environ.get("SUANLI_TOKEN")
    priv_raw = os.environ.get("SUANLI_RSA_PRIVATE_KEY")
    pub_raw = os.environ.get("SUANLI_PLATFORM_PUBLIC_KEY")
    base = os.environ.get("SUANLI_BASE_URL", "https://openapi.suanli.cn").rstrip("/")
    if not token or not priv_raw or not pub_raw:
        sys.stderr.write(
            "加密接口需要 RSA 加验签模式：请设置 SUANLI_TOKEN、"
            "SUANLI_RSA_PRIVATE_KEY、SUANLI_PLATFORM_PUBLIC_KEY\n"
        )
        return 2

    json_data = read_json_payload(payload)
    private_key = load_private_key(priv_raw)
    platform_public_key = load_public_key(pub_raw)
    encrypted_body = encrypt_body(platform_public_key, json_data)
    timestamp = str(int(time.time() * 1000))
    sign_path = f"/api{path}"
    sign_str = gen_sign(private_key, sign_path, API_VERSION, timestamp, token, encrypted_body)

    url = f"{base}{sign_path}"
    headers = {
        "token": token,
        "timestamp": timestamp,
        "version": API_VERSION,
        "sign_str": sign_str,
        "Content-Type": "text/plain",
    }
    resp = requests.post(url, headers=headers, data=encrypted_body.encode("utf-8"), timeout=60)
    sys.stdout.write(resp.text)
    if not resp.text.endswith("\n"):
        sys.stdout.write("\n")
    return 0 if resp.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

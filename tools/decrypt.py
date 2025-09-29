# -*- coding: utf-8 -*-
import argparse, base64, os, sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
PREFIX=b"V1"; NONCE_LEN=12
def _key()->bytes:
    b64=os.getenv("ENCRYPTION_KEY","").strip()
    if not b64: print("ENCRYPTION_KEY not set", file=sys.stderr); sys.exit(2)
    try: k=base64.b64decode(b64)
    except Exception: print("Bad base64 key", file=sys.stderr); sys.exit(2)
    if len(k)!=32: print(f"Key length {len(k)} != 32", file=sys.stderr); sys.exit(2)
    return k
def main():
    p=argparse.ArgumentParser()
    p.add_argument("input"); p.add_argument("output"); p.add_argument("--aad", default=None)
    a=p.parse_args(); aad=a.aad.encode() if a.aad else None
    b64=open(a.input,"r",encoding="utf-8").read().strip()
    payload=base64.b64decode(b64)
    if not payload.startswith(PREFIX): print("Missing V1 prefix", file=sys.stderr); sys.exit(2)
    body=payload[len(PREFIX):]
    nonce, ct = body[:NONCE_LEN], body[NONCE_LEN:]
    data=AESGCM(_key()).decrypt(nonce, ct, aad)
    os.makedirs(os.path.dirname(a.output) or ".", exist_ok=True)
    open(a.output,"wb").write(data)
    print(f"OK: {a.input} -> {a.output} ({len(data)} bytes)")
if __name__=="__main__": main()

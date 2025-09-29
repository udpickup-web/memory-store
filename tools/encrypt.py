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
    os.makedirs(os.path.dirname(a.output) or ".", exist_ok=True)
    data=open(a.input,"rb").read()
    nonce=os.urandom(NONCE_LEN); ct=AESGCM(_key()).encrypt(nonce, data, aad)
    out=base64.b64encode(PREFIX+nonce+ct).decode("ascii")
    open(a.output,"w",encoding="utf-8").write(out)
    print(f"OK: {a.input} -> {a.output} ({len(data)} bytes)")
if __name__=="__main__": main()

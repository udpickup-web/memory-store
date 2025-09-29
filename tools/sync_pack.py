# -*- coding: utf-8 -*-
"""
sync_pack.py — собирает все *.jsonl из out/plain/, шифрует в encrypted/*, обновляет manifest.json.
Фиксы:
- Чтение JSONL с encoding='utf-8', errors='ignore' (устойчиво к OEM/CP866 echo).
- .env подхватывается батником безопасно.
"""
import os, sys, json, base64, hashlib, datetime
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ROOT = Path(__file__).resolve().parents[1]
OUT_PLAIN = ROOT / "out" / "plain"
ENC_MEM = ROOT / "encrypted" / "memory"
ENC_INS = ROOT / "encrypted" / "instructions"
MANIFEST = ROOT / "manifest.json"
PREFIX = b"V1"; NONCE_LEN = 12

def _key()->bytes:
    b64=os.getenv("ENCRYPTION_KEY","").strip()
    if not b64: sys.exit("ENCRYPTION_KEY not set in environment (.env)")
    try:
        key=base64.b64decode(b64)
    except Exception:
        sys.exit("ENCRYPTION_KEY must be base64")
    if len(key)!=32: sys.exit("ENCRYPTION_KEY must be 32 bytes base64")
    return key

def _sha256_bytes(data: bytes)->str:
    h=hashlib.sha256(); h.update(data); return h.hexdigest()

def _encrypt_bytes(data: bytes, aad: bytes|None)->bytes:
    nonce=os.urandom(NONCE_LEN)
    ct=AESGCM(_key()).encrypt(nonce, data, aad)
    return PREFIX + nonce + ct

def load_ids_from_jsonl(path: Path)->list[str]:
    ids=[]
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line=line.strip()
            if not line: continue
            try:
                obj=json.loads(line)
            except Exception:
                continue
            if isinstance(obj, dict) and "id" in obj:
                ids.append(str(obj["id"]))
    return ids

def main():
    os.makedirs(ENC_MEM, exist_ok=True)
    os.makedirs(ENC_INS, exist_ok=True)
    now=datetime.datetime.utcnow().strftime("%Y-%m-%dT%H%M%SZ")
    aad=b"manifest:1.0"
    mem_entries=[]; ins_entries=[]
    if not OUT_PLAIN.exists():
        print("No out/plain directory; nothing to sync."); return
    files = sorted(OUT_PLAIN.glob("*.jsonl"))
    if not files:
        print("No *.jsonl in out/plain; nothing to sync."); return
    for fp in files:
        data=fp.read_bytes()
        payload=_encrypt_bytes(data, aad)
        b64=base64.b64encode(payload)
        sha=_sha256_bytes(b64)
        if fp.name.startswith("memory_"):
            out = ENC_MEM / f"{now}__{fp.name}.enc"
            out.write_text(b64.decode("ascii"), encoding="utf-8")
            ids=load_ids_from_jsonl(fp)
            mem_entries.append({"src": str(fp.relative_to(ROOT)), "enc": str(out.relative_to(ROOT)), "sha256": sha, "ids": ids})
            print(f"[mem] {fp.name} -> {out.name} ({len(ids)} ids)")
        elif fp.name.startswith("instr_") or fp.name.startswith("instructions_"):
            out = ENC_INS / f"{now}__{fp.name}.enc"
            out.write_text(b64.decode("ascii"), encoding="utf-8")
            ids=load_ids_from_jsonl(fp)
            ins_entries.append({"src": str(fp.relative_to(ROOT)), "enc": str(out.relative_to(ROOT)), "sha256": sha, "ids": ids})
            print(f"[ins] {fp.name} -> {out.name} ({len(ids)} ids)")
        else:
            print(f"[skip] {fp.name} — имя должно начинаться с memory_ или instr_")
    man=json.loads(MANIFEST.read_text(encoding="utf-8"))
    man.setdefault("snapshots", {}).setdefault("memory", []).extend(mem_entries)
    man.setdefault("snapshots", {}).setdefault("instructions", []).extend(ins_entries)
    man["updated_at"]=datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    MANIFEST.write_text(json.dumps(man, ensure_ascii=False, indent=2), encoding="utf-8")
    # Recompute checksum over encrypted/
    enc_dir = ROOT / "encrypted"
    h=hashlib.sha256()
    for r,_,files in os.walk(enc_dir):
        for n in sorted(files):
            path=os.path.join(r,n)
            h.update(n.encode("utf-8","ignore"))
            with open(path,"rb") as f:
                for ch in iter(lambda:f.read(1024*1024), b""): h.update(ch)
    checksum=h.hexdigest()
    man=json.loads(MANIFEST.read_text(encoding="utf-8"))
    man["checksum"]=checksum
    MANIFEST.write_text(json.dumps(man, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Encrypted checksum:", checksum)

if __name__=="__main__":
    main()

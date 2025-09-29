# -*- coding: utf-8 -*-
import sys, os, json, hashlib, datetime
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))
MANIFEST=os.path.join(ROOT,"manifest.json")
def sha256_path(p):
    if os.path.isfile(p):
        h=hashlib.sha256(); f=open(p,"rb")
        for chunk in iter(lambda:f.read(1024*1024), b""): h.update(chunk)
        f.close(); return h.hexdigest()
    h=hashlib.sha256()
    for r,_,files in os.walk(p):
        for n in sorted(files):
            path=os.path.join(r,n); h.update(n.encode("utf-8","ignore"))
            with open(path,"rb") as f:
                for ch in iter(lambda:f.read(1024*1024), b""): h.update(ch)
    return h.hexdigest()
def update_manifest():
    man=json.load(open(MANIFEST,"r",encoding="utf-8"))
    enc=os.path.join(ROOT,"encrypted"); man["checksum"]=sha256_path(enc)
    man["updated_at"]=datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    json.dump(man, open(MANIFEST,"w",encoding="utf-8"), ensure_ascii=False, indent=2)
    print("OK manifest checksum:", man["checksum"])
if __name__=="__main__":
    if len(sys.argv)==2 and sys.argv[1]=="update-manifest": update_manifest()
    elif len(sys.argv)==3 and sys.argv[1]=="file": print(sha256_path(sys.argv[2]))
    else: print("usage: checksum.py update-manifest | file <path>", file=sys.stderr); sys.exit(2)

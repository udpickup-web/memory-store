# -*- coding: utf-8 -*-
"""
gen_purge_request.py — формирует текст команды REQUEST: PURGE_BUFFER
на основании последних записей в manifest.json (последние добавленные ids).
Использование:
    python tools/gen_purge_request.py > out\PURGE_REQUEST.txt
"""
import json, os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifest.json"
OUTTXT = ROOT / "out" / "PURGE_REQUEST.txt"

def main():
    man = json.loads(MANIFEST.read_text(encoding="utf-8"))
    ver = man.get("updated_at") or man.get("created_at")
    checksum = man.get("checksum")
    ids=set()
    for entry in man.get("snapshots",{}).get("memory",[])[-5:]:
        for i in entry.get("ids",[]): ids.add(i)
    for entry in man.get("snapshots",{}).get("instructions",[])[-5:]:
        for i in entry.get("ids",[]): ids.add(i)
    lines = []
    lines.append("REQUEST: PURGE_BUFFER")
    lines.append(f"manifest_version: {ver}")
    lines.append(f"manifest_checksum: {checksum}")
    lines.append("confirmed_ids:")
    for i in sorted(ids):
        lines.append(f"  - {i}")
    OUTTXT.parent.mkdir(parents=True, exist_ok=True)
    OUTTXT.write_text("\n".join(lines), encoding="utf-8")
    print("Wrote", OUTTXT)

if __name__=="__main__":
    main()

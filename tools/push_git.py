# -*- coding: utf-8 -*-
import os, subprocess, sys
def run(cmd):
    print("+"," ".join(cmd)); r=subprocess.run(cmd); 
    if r.returncode!=0: sys.exit(r.returncode)
def main():
    repo=os.getenv("REPO_PATH","C:\\PROG\\BOT")
    msg=os.getenv("COMMIT_MSG","memory: update encrypted snapshots")
    os.chdir(repo)
    run(["git","add","encrypted","manifest.json"])
    run(["git","commit","-m",msg])
    remote=os.getenv("GIT_REMOTE")
    if remote: run(["git","push","origin","HEAD"])
    else: print("GIT_REMOTE not set — push skipped")
if __name__=="__main__": main()

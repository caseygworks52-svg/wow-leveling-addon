#!/usr/bin/env python3
from pathlib import Path
import re, shutil, subprocess, sys
ROOT=Path(__file__).resolve().parent.parent
ERRORS=[]
TOCS=[ROOT/"LevelGuide"/"LevelGuide.toc",ROOT/"LevelGuide_Data_Alliance"/"LevelGuide_Data_Alliance.toc",ROOT/"LevelGuide_Data_Horde"/"LevelGuide_Data_Horde.toc"]
for toc in TOCS:
    if not toc.exists(): ERRORS.append("Missing TOC: "+str(toc.relative_to(ROOT))); continue
    lines=toc.read_text(encoding="utf-8").splitlines()
    if not any(x.strip()=="## Interface: 16001" for x in lines): ERRORS.append(toc.name+": missing Interface 16001")
    for raw in lines:
        item=raw.strip()
        if not item or item.startswith("#"): continue
        target=toc.parent/item.replace("\\","/")
        if not target.is_file(): ERRORS.append(toc.name+": missing listed file "+item)
counts={}
for faction in ("Alliance","Horde"):
    path=ROOT/("LevelGuide_Data_"+faction)/"Data.lua"
    if not path.is_file(): ERRORS.append("Missing "+str(path.relative_to(ROOT))); continue
    data=path.read_text(encoding="utf-8")
    if ('LevelGuide.RegisterData("'+faction+'"') not in data[:500]: ERRORS.append(faction+": bad faction registration")
    if "quests={" not in data: ERRORS.append(faction+": missing quests table"); continue
    counts[faction]=len(re.findall(r"^\s*\[\d+\]\s*=\s*\{",data.split("quests={",1)[1],re.M))
    if counts[faction]<1000: ERRORS.append(faction+": unexpectedly few quests")
core=sorted((ROOT/"LevelGuide").glob("*.lua"))
all_lua=core+[ROOT/"LevelGuide_Data_Alliance"/"Data.lua",ROOT/"LevelGuide_Data_Horde"/"Data.lua"]
luac=shutil.which("luac5.1") or shutil.which("luac")
syntax=0
if luac:
    for path in all_lua:
        r=subprocess.run([luac,"-p",str(path)],text=True,capture_output=True)
        if r.returncode: ERRORS.append("Lua syntax error "+str(path.relative_to(ROOT))+": "+r.stderr.strip())
        else: syntax+=1
else: ERRORS.append("Lua 5.1 compiler not found; use GitHub Actions.")
engine=(ROOT/"LevelGuide"/"Engine.lua").read_text(encoding="utf-8")
compat=(ROOT/"LevelGuide"/"Compat.lua").read_text(encoding="utf-8")
if 'type(doneServer) ~= "boolean"' not in engine: ERRORS.append("Sync must preserve unknown quest states.")
if "function E.Sync(st, db, level)\n  return 0" not in engine: ERRORS.append("Level-only fallback must remain disabled.")
if "IsQuestFlaggedCompleted unavailable" not in compat: ERRORS.append("Completion API must distinguish unknown from false.")
for path in (ROOT/"LevelGuide"/"Arrow.lua",ROOT/"LevelGuide"/"MinimapTrail.lua"):
    if "mapW, mapH = 1500, 1000" in path.read_text(encoding="utf-8"): ERRORS.append(path.name+": fabricated map dimensions returned.")
print("=== LevelGuide v1.2.9 verifier ===")
print("TOCs present: "+str(sum(t.exists() for t in TOCS))+"/"+str(len(TOCS)))
print("Core Lua files: "+str(len(core)))
print("Lua files syntax-checked: "+str(syntax)+"/"+str(len(all_lua)))
print("Alliance quests: "+str(counts.get("Alliance",0)))
print("Horde quests: "+str(counts.get("Horde",0)))
print("Errors: "+str(len(ERRORS)))
for x in ERRORS: print("[ERROR] "+x)
sys.exit(1 if ERRORS else 0)

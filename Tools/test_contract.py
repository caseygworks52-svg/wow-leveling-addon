#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
def read(p): return (ROOT/p).read_text(encoding="utf-8")
compat,engine,main=read("LevelGuide/Compat.lua"),read("LevelGuide/Engine.lua"),read("LevelGuide/Main.lua")
safety,arrow,trail,pace=read("LevelGuide/Safety.lua"),read("LevelGuide/Arrow.lua"),read("LevelGuide/MinimapTrail.lua"),read("LevelGuide/PaceGuide.lua")
checks={
 "completion API has UNKNOWN state":"IsQuestFlaggedCompleted unavailable" in compat,
 "completion API validates boolean":'type(done) ~= "boolean"' in compat,
 "sync counts unknown results":"local added, reopened, unknown = 0, 0, 0" in engine,
 "sync only mutates on booleans":'type(doneServer) ~= "boolean"' in engine,
 "legacy level sync is a no-op":"function E.Sync(st, db, level)\n  return 0" in engine,
 "quest disappearance check is protected":"local okDone, result = pcall(isCompletedFn, p.id)" in engine,
 "main surfaces unverifiable syncs":"unverifiable (unchanged)" in main,
 "danger warning avoids crushing claim":"crushing risk" not in safety,
 "arrow avoids invented dimensions":"mapW, mapH = 1500, 1000" not in arrow,
 "trail avoids invented dimensions":"mapW, mapH = 1500, 1000" not in trail,
 "dungeon XP reflects 40-to-60 percent":"40% to 60% of Classic Era values" in pace,
 "party grey-mob rule is included":"zero XP to the entire party" in pace,
 "five-entry cap is included":"5 times per hour" in pace,
}
for name,ok in checks.items(): print(("PASS" if ok else "FAIL")+"  "+name)
print(str(sum(checks.values()))+"/"+str(len(checks))+" checks passed")
raise SystemExit(0 if all(checks.values()) else 1)

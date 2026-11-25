#!/usr/bin/env python3
"""Static package/data checks for LevelGuide v1.3.0 (WoW: Forever 1.60.1)."""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION = "1.3.0"
REMOVED_112_PATTERNS = [
    (r"(?<![.\w])LoadAddOn\s*\(", "bare removed LoadAddOn()"),
    (r"(?<![.\w])GetPlayerMapPosition\s*\(", "bare removed GetPlayerMapPosition()"),
    (r"(?<![.\w])SetMapToCurrentZone\s*\(", "removed SetMapToCurrentZone()"),
    (r"(?<![.\w])GetNumQuestLogEntries\s*\(", "bare removed GetNumQuestLogEntries()"),
    (r"(?<![.\w])GetQuestLogTitle\s*\(", "removed GetQuestLogTitle()"),
    (r"\btable\.unpack\b", "Lua 5.2+ table.unpack is not Lua 5.1"),
    (r"\bgoto\s+\w+", "Lua 5.2+ goto is not Lua 5.1"),
    (r"(?<!:)//", "Lua 5.3+ integer division is not Lua 5.1"),
]
def strip_comments_strings(source: str) -> str:
    pattern = re.compile(r"""--\[\[.*?\]\]|--[^\n]*|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'""", re.S)
    return pattern.sub(lambda m: '""' if m.group(0).startswith(('"', "'")) else "", source)
def main() -> int:
    errors = []
    tocs = [
        ROOT / "LevelGuide" / "LevelGuide.toc",
        ROOT / "LevelGuide_Data_Alliance" / "LevelGuide_Data_Alliance.toc",
        ROOT / "LevelGuide_Data_Horde" / "LevelGuide_Data_Horde.toc",
    ]
    for toc in tocs:
        if not toc.exists():
            errors.append(f"Missing TOC: {toc.relative_to(ROOT)}")
            continue
        lines = toc.read_text(encoding="utf-8").splitlines()
        if "## Interface: 16001" not in lines:
            errors.append(f"{toc.name}: Interface 16001 missing")
        if toc.name == "LevelGuide.toc" and f"## Version: {VERSION}" not in lines:
            errors.append(f"{toc.name}: version mismatch")
        for raw in lines:
            entry = raw.strip()
            if not entry or entry.startswith("#"):
                continue
            if not (toc.parent / entry.replace("\\", "/")).is_file():
                errors.append(f"{toc.name}: missing manifest file {entry}")
    core = sorted((ROOT / "LevelGuide").glob("*.lua"))
    for path in core:
        clean = strip_comments_strings(path.read_text(encoding="utf-8"))
        for pattern, reason in REMOVED_112_PATTERNS:
            if re.search(pattern, clean, re.M):
                errors.append(f"{path.name}: {reason}")
        for opening, closing in [("(", ")"), ("{", "}"), ("[", "]")]:
            if clean.count(opening) != clean.count(closing):
                errors.append(f"{path.name}: delimiter count mismatch {opening}{closing}")
    faction_counts = {}
    for faction in ("Alliance", "Horde"):
        path = ROOT / f"LevelGuide_Data_{faction}" / "Data.lua"
        if not path.is_file():
            errors.append(f"Missing faction data: {path.relative_to(ROOT)}")
            continue
        source = path.read_text(encoding="utf-8")
        if f'LevelGuide.RegisterData("{faction}"' not in source[:500]:
            errors.append(f"{path.name}: wrong/missing faction registration")
        if "quests={" not in source:
            errors.append(f"{path.name}: quests table missing")
            continue
        ids = re.findall(r"^\s*\[(\d+)\]\s*=\s*\{", source.split("quests={", 1)[1], re.M)
        faction_counts[faction] = len(ids)
        if len(ids) < 3000:
            errors.append(f"{faction} quest count unexpectedly low: {len(ids)}")
        if len(ids) != len(set(ids)):
            errors.append(f"{faction} quest IDs contain duplicates")
    compat = (ROOT / "LevelGuide" / "Compat.lua").read_text(encoding="utf-8")
    engine = (ROOT / "LevelGuide" / "Engine.lua").read_text(encoding="utf-8")
    main_lua = (ROOT / "LevelGuide" / "Main.lua").read_text(encoding="utf-8")
    if "function C.GetCompletedQuestSet()" not in compat:
        errors.append("Compat: bulk completion snapshot missing")
    if 'if type(done) ~= "boolean" then return nil end' not in compat:
        errors.append("Compat: tri-state completion API missing")
    if "doneServer == nil" not in engine or "unknown = unknown + 1" not in engine:
        errors.append("Engine: unknown results are not preserved")
    if "disabled: server completion data is required" not in engine:
        errors.append("Engine: level-only sync fallback not disabled")
    if main_lua.count("GL.Compat.GetCompletedQuestSet") < 3:
        errors.append("Main: init/scan/sync do not all use bulk snapshot")
    core_lua = (ROOT / "LevelGuide" / "Core.lua").read_text(encoding="utf-8")
    if f'GL.version = "{VERSION}"' not in core_lua:
        errors.append("Core version mismatch")
    if not (ROOT / "Tools" / "test_sync.lua").is_file():
        errors.append("Lua regression test missing")
    if not (ROOT / ".github" / "workflows" / "validate.yml").is_file():
        errors.append("GitHub Actions workflow missing")
    print(f"=== LevelGuide v{VERSION} Static Verifier ===")
    print(f"TOC manifests       : {len(tocs)}")
    print(f"Core Lua modules    : {len(core)} (also compiled by luac5.1 in CI)")
    print(f"Alliance quests     : {faction_counts.get('Alliance', 0)}")
    print(f"Horde quests        : {faction_counts.get('Horde', 0)}")
    print(f"Bulk sync guard     : {'present' if 'function C.GetCompletedQuestSet()' in compat else 'MISSING'}")
    print(f"Errors              : {len(errors)}")
    for error in errors:
        print(f"  [ERROR] {error}")
    return 1 if errors else 0
if __name__ == "__main__":
    sys.exit(main())

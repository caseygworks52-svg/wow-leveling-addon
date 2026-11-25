# LevelGuide v1.3.0 — WoW: Forever

## Install
Download [LevelGuide-v1.3.0.zip](LevelGuide-v1.3.0.zip), extract the three addon folders into \`World of Warcraft/_forever_/Interface/AddOns/\`, enable LevelGuide and both faction data folders at character select, then restart.

## v1.3.0 fixes
- Server sync is tri-state and fail-safe. Failed/unavailable completion queries are UNKNOWN, never "not completed"; local progress is preserved.
- Prefer Forever's documented \`C_QuestLog.GetAllCompletedQuestIDs()\` snapshot; retain guarded per-ID fallback.
- Disable the old level-only completion heuristic.
- Add Lua 5.1 regression tests, static checks, and CI compilation.

## Source and QA
The repo includes unpacked source. Run:
\`\`\`sh
python3 Tools/verify_all.py
lua5.1 Tools/test_sync.lua
find LevelGuide LevelGuide_Data_Alliance LevelGuide_Data_Horde -name '*.lua' -print0 | xargs -0 -n1 luac5.1 -p
\`\`\`
A green CI run does not replace a live in-client test.

## Data limitations
Quest data is pfQuest-derived and tagged UNVERIFIED-AUTO, not a fully verified Forever quest graph. Objective spawn coordinates are not bundled; Questie may supply optional spawn data.

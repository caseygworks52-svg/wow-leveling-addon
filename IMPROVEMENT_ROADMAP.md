# LevelGuide improvement roadmap (audit of v1.2.8)

## Implemented in v1.3.0
1. Fail-safe tri-state sync: unavailable/error/secret results never erase local progress.
2. Bulk completion snapshot through C_QuestLog.GetAllCompletedQuestIDs(), with guarded per-ID fallback.
3. Protected transition checks using pcall and strict booleans.
4. Disable level-only completion guessing.
5. Lua 5.1 regression tests for true/false/nil/error/bulk/fallback.
6. Lua 5.1 compilation of every addon/data Lua file in CI.
7. Unpacked source tree checked into Git alongside the ZIP.
8. Static manifest/version/data integrity checks.

## Next improvements (ranked)
9. Provenance manifest: source revision, extraction date, transform script, counts, and hashes per faction dataset.
10. Forever quest-data reconciliation: compare IDs, prerequisites, levels, race/class/faction masks, and objectives against a current Forever export.
11. Coordinate confidence: distinguish giver/turn-in/objective source, coordinate scale, map ID, and verified confidence.
12. Route graph tests: dangling prerequisite IDs, cycles, faction leakage, class/race exclusion, invalid hubs, cross-zone dead ends.
13. Character matrix coverage for every race/faction/class, including Skyborne and race-specific starts.
14. Performance profiling: startup, sync, refresh rate, Questie lookup, peak memory; optimize only after measurement.
15. Route benchmarks by travel distance, XP source, hub density, and revisit rate.

## Known audit boundaries
- Current quest records are pfQuest-derived and UNVERIFIED-AUTO; not every Forever quest or route is confirmed.
- Handwritten pace-guide routing and XP claims need a source ledger and in-game confirmation.
- No CI runs or Releases existed on the audited main branch. CI cannot prove live client behavior.
- Map distance/coordinate orientation still requires in-game measurement.

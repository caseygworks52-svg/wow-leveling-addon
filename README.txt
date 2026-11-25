LevelGuide v1.3.0 — WoW: Forever 1.60.1.71037 (Interface: 16001)

INSTALL
  Extract all three folders into World of Warcraft/_forever_/Interface/AddOns/:
    LevelGuide                (core engine and UI)
    LevelGuide_Data_Alliance  (LoadOnDemand Alliance quest data)
    LevelGuide_Data_Horde     (LoadOnDemand Horde quest data)
  Fully restart WoW: Forever and enable all three at Character Select -> AddOns.

v1.3.0 HOTFIXES
  - Server sync is fail-safe: unavailable, failed, or unreadable API results are UNKNOWN,
    never "not completed"; unknown results preserve local completion progress.
  - Uses C_QuestLog.GetAllCompletedQuestIDs() when available for a single completion snapshot.
  - Disables the level-only completion heuristic from deprecated Engine.Sync().
  - Adds Lua 5.1 regression tests and GitHub Actions validation to the source repository.

DATA PROVENANCE & LIMITATIONS
  - Bundled quest records are pfQuest-derived and tagged UNVERIFIED-AUTO; not a fully
    audited WoW: Forever quest graph.
  - Mob/object spawn coordinates are not bundled in Data.lua; optional Questie data may
    provide objective pins.
  - See LICENSE-pfQuest.txt, CHANGELOG.md, API_NOTES.md and IMPROVEMENT_ROADMAP.md.

# LevelGuide v1.2.9 — Audit & Improvement Roadmap

## v1.2.9 hotfixes
- Server completion checks distinguish false from unknown; unknown results do not mutate saved progress.
- Legacy level-only completion guessing is disabled.
- Failed completion checks are guarded during quest-log disappearance handling.
- Danger warnings no longer treat quest level as mob level.
- Arrow and minimap trail no longer use invented 1,500 x 1,000 yard map dimensions.
- Dungeon guidance reflects November 8, 13, and 20, 2026 rules.

## 15 future improvements
1. Forever quest-data provenance registry by quest, NPC, object, coordinate, source, and client build.
2. Quest-data validation dashboard for missing giver/finisher links, orphan prerequisites, duplicate IDs, and invalid faction/race masks.
3. Route-coverage matrix across all races, classes, factions, zones, and level brackets.
4. Objective-level location confidence for mob, object, drop-candidate, turn-in, and area pins.
5. Deterministic route scoring that separates known XP, estimated XP, and observed XP/hour.
6. Verified travel graph for flights, boats, portals, hearths, and walking transitions.
7. Dungeon planner with Forever quest bundles, level ranges, reset budget, party level spread, and grey-mob XP rules.
8. Verified class quest chains with source-backed trainer, prerequisite, level, and reward details.
9. Profession planner for recipes, trainer ranks, materials, skill-up ranges, and vendor availability.
10. Gear-upgrade evaluator with class-aware stats, weapon skill, armor proficiency, and level gates.
11. Quest-log planner with abandon-risk, chain dependencies, grey status, and turn-in travel cost.
12. Safer automation tests across gossip variants, DialogueUI, combat lockdown, and reward choices.
13. Localization-safe matching based on IDs/tokens rather than English strings.
14. CPU/OnUpdate profiling and allocation budgets while the HUD is visible or hidden.
15. Reproducible releases, migration tests, test fixtures, and CI regression protection.

## Verification limits
The quest data is pfQuest-derived and labeled UNVERIFIED-AUTO. Quest counts do not prove route accuracy. Objective spawn coordinates are not bundled; Questie support remains optional and needs testing against the exact Forever addon. CI syntax checks do not replace an in-game Human Warrior test.

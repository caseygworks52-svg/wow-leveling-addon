# WoW Forever LevelGuide

**Latest candidate:** v1.2.9 — client target 1.60.1.71037 / Interface 16001.

## Download and install
Download [LevelGuide-v1.2.9.zip](https://raw.githubusercontent.com/caseygworks52-svg/wow-leveling-addon/hotfix/v1.2.9/LevelGuide-v1.2.9.zip). Extract the three folders `LevelGuide`, `LevelGuide_Data_Alliance`, and `LevelGuide_Data_Horde` directly into `World of Warcraft/_forever_/Interface/AddOns/`. Restart WoW: Forever and enable `LevelGuide` plus the matching faction data addon.

## Review
- [v1.2.9 audit and 15-improvement roadmap](AUDIT-v1.2.9.md)
- [v1.2.9 changelog](CHANGELOG.md)
- [CI validation](.github/workflows/validate.yml)

The release candidate passes the repository's Lua 5.1 syntax/data checks and hotfix contract checks. It still needs an in-game test for quest sync, arrow/map navigation, and step transitions. Preserve your existing `WTF/.../SavedVariables/LevelGuide.lua` file when replacing the addon.

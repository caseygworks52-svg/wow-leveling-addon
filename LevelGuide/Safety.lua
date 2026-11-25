-- LevelGuide Safety: Hardcore & Solo-Survivability Dangerous-Pull Warnings (BoF-inspired).
-- Flags orange/red quests, caves/mines, elites, escorts, and underwater hazards before you pull.

local GL = LevelGuide
local S = {}
GL.Safety = S

local CAVE_KEYWORDS = { "mine", "cave", "cavern", "crypt", "barrow", "den", "hollow", "tunnel", "keep", "stronghold" }
local DANGER_KEYWORDS = { "wanted:", "bounty", "hogger", "garrick", "escort", "defend", "murloc", "gnoll", "defias" }

function S.GetWarnings(step, ctx)
  if not step or not ctx then return {} end
  local hcOn = not (GL.db and GL.db.settings and GL.db.settings.hcWarnings == false)
  if not hcOn then return {} end

  local out = {}
  local lv = ctx.level or 1
  local st = GL.state

  if st and st.data and type(st.data.quests) == "table" and step.ids then
    local hasHigh, hasCave, hasDanger = false, false, false
    for _, id in ipairs(step.ids) do
      local q = st.data.quests[id]
      if q then
        if (q.l or 1) >= lv + 3 then hasHigh = true end
        local hay = string.lower(tostring(q.n or "") .. " " .. tostring(q.o or ""))
        for _, kw in ipairs(CAVE_KEYWORDS) do
          if string.find(hay, kw, 1, true) then hasCave = true break end
        end
        for _, kw in ipairs(DANGER_KEYWORDS) do
          if string.find(hay, kw, 1, true) then hasDanger = true break end
        end
      end
    end

    if hasHigh then
      out[#out + 1] = "|cffff4444[LEVEL CAUTION]|r Quest level is 3+ above you. Quest level is not the creature's level; check the actual mobs before pulling."
    end
    if hasCave then
      out[#out + 1] = "|cffff8800[CAVE/INDOOR]|r Tight space & fast respawns — pull back to entrance, watch runners, keep potion/bandage ready."
    end
    if hasDanger and not ctx.inGroup then
      out[#out + 1] = "|cffffaa00[SOLO CAUTION]|r Quest name/text matches a caution keyword. Check nearby mob density and elite status before pulling; neither is inferred from quest text."
    end
  end
  return out
end

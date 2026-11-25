-- Run: lua5.1 Tools/test_sync.lua
LevelGuide = {}
_G.LevelGuide = LevelGuide
dofile("LevelGuide/Core.lua")
dofile("LevelGuide/Compat.lua")
dofile("LevelGuide/Engine.lua")
local C, E = LevelGuide.Compat, LevelGuide.Engine
local function expect(name, condition)
  if not condition then io.stderr:write("[FAIL] " .. name .. "\n"); os.exit(1) end
  io.stdout:write("[PASS] " .. name .. "\n")
end
C_QuestLog = {
  IsQuestFlaggedCompleted = function(id)
    if id == 101 then return true end
    if id == 102 then return false end
    error("simulated client/API failure")
  end,
  GetAllCompletedQuestIDs = function() return { 101, 103 } end,
}
expect("completed API true", C.IsQuestCompleted(101) == true)
expect("completed API false", C.IsQuestCompleted(102) == false)
expect("API error returns unknown", C.IsQuestCompleted(103) == nil)
local set = C.GetCompletedQuestSet()
expect("bulk set includes IDs", type(set) == "table" and set[101] and set[103] and not set[102])
C_QuestLog = nil
expect("missing API returns unknown", C.IsQuestCompleted(101) == nil)
expect("missing bulk API returns nil", C.GetCompletedQuestSet() == nil)
local state = { ids = { 101, 102, 103 }, _availKey = "cached" }
local db = { done = { [101] = true, [102] = true }, skipped = { [102] = true } }
local bulkCalls = 0
local added, reopened, unknown, source = E.SyncFromServer(state, db,
  function() error("per-ID fallback should not run") end,
  function() bulkCalls = bulkCalls + 1; return { [101] = true, [103] = true } end)
expect("bulk snapshot called once", bulkCalls == 1)
expect("bulk source reported", source == "bulk")
expect("bulk adds completed quest", added == 1 and db.done[103] == true)
expect("bulk reopens explicit incomplete", reopened == 1 and db.done[102] == nil)
expect("bulk unknown count", unknown == 0)
expect("changed sync invalidates cache", state._availKey == nil)
state = { ids = { 201, 202, 203 } }
db = { done = { [201] = true, [202] = true } }
added, reopened, unknown, source = E.SyncFromServer(state, db, function(id)
  if id == 201 then return nil end
  if id == 202 then return false end
  if id == 203 then return true end
  error("unexpected id")
end, function() return nil end)
expect("fallback source reported", source == "per_id")
expect("fallback preserves unknown local completion", db.done[201] == true)
expect("fallback reopens explicit false", db.done[202] == nil and reopened == 1)
expect("fallback adds explicit true", db.done[203] == true and added == 1)
expect("fallback counts unknown", unknown == 1)
state = { ids = { 301, 302 } }
db = { done = { [301] = true, [302] = true } }
added, reopened, unknown = E.SyncFromServer(state, db, function() error("offline") end, function() error("offline") end)
expect("failed APIs do not erase local progress", db.done[301] and db.done[302])
expect("failed APIs count unknown", added == 0 and reopened == 0 and unknown == 2)
state = { ids = { 401 } }; db = { done = {} }
local count, status = E.Sync(state, db, 60)
expect("level-only sync is disabled", count == 0 and status == "disabled: server completion data is required" and db.done[401] == nil)
io.stdout:write("All LevelGuide server-sync regression tests passed.\n")

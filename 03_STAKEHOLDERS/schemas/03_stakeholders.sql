-- ============================================================================
-- PMO DOMAINS — 03: Stakeholders
-- Color Code: #ffd166
-- Generated: 2026-06-16
-- ============================================================================

CREATE TABLE IF NOT EXISTS stakeholders (
    S01_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT,
    S01_stk_owner_name TEXT NOT NULL,
    S02_stk_developer TEXT,
    S03_stk_contractor TEXT,
    S04_stk_consultant TEXT,
    S05_stk_project_manager TEXT,
    S06_stk_supervising_auth TEXT,
    S07_stk_owner_rep TEXT,
    S08_stk_main_bank TEXT,
    S09_stk_funding_source TEXT,
    S10_stk_legal_rep TEXT,
    S11_stk_partners TEXT,
    S12_stk_operator TEXT
);

CREATE TABLE IF NOT EXISTS developers_registry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT,
    emirate TEXT,
    contact_info TEXT,
    portfolio_size TEXT
);

CREATE INDEX IF NOT EXISTS idx_stk_owner ON stakeholders(S01_stk_owner_name);

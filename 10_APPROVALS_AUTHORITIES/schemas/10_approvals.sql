-- ============================================================================
-- PMO DOMAINS — 10: Approvals & Authorities
-- Color Code: #3a86ff
-- Generated: 2026-06-16
-- ============================================================================

CREATE TABLE IF NOT EXISTS approvals (
    A01_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT,
    A01_primary_authority TEXT,
    A02_noc_status TEXT DEFAULT 'Pending',
    A03_noc_issue_date TEXT,
    A04_building_permit_no TEXT,
    A05_bp_issue_date TEXT,
    A06_bp_expiry_date TEXT,
    A07_completion_cert_no TEXT,
    A08_cc_issue_date TEXT,
    A09_occupation_cert_no TEXT,
    A10_oc_issue_date TEXT
);

CREATE TABLE IF NOT EXISTS authority_matrix (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emirate TEXT,
    jurisdiction TEXT,
    master_planning TEXT,
    building_permit TEXT,
    civil_defense TEXT,
    power_water TEXT,
    district_cooling TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS permit_sequence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    step_number INTEGER,
    permit_name TEXT NOT NULL,
    min_days INTEGER,
    max_days INTEGER,
    avg_days INTEGER,
    min_cost_aed REAL,
    max_cost_aed REAL,
    avg_cost_aed REAL,
    authority TEXT,
    notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_ap_project ON approvals(project_id);

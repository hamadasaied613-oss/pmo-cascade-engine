-- ============================================================================
-- PMO DOMAINS — 09: Schedule & Timeline
-- Color Code: #fb5607
-- Generated: 2026-06-16
-- ============================================================================

CREATE TABLE IF NOT EXISTS schedule_data (
    T01_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT,
    T01_start_date TEXT,
    T02_design_complete TEXT,
    T03_permit_issued TEXT,
    T04_construction_start TEXT,
    T05_construction_end TEXT,
    T06_handover_date TEXT,
    T07_duration_months INTEGER,
    T08_current_phase TEXT
);

CREATE TABLE IF NOT EXISTS wbs_activities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT,
    phase_id INTEGER,
    phase_name TEXT,
    activity_id INTEGER,
    activity_name TEXT,
    duration_days INTEGER,
    start_date TEXT,
    end_date TEXT,
    is_critical INTEGER DEFAULT 0,
    predecessor TEXT,
    resource_type TEXT,
    planned_pct REAL DEFAULT 0,
    actual_pct REAL DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_sd_project ON schedule_data(project_id);
CREATE INDEX IF NOT EXISTS idx_wa_project ON wbs_activities(project_id);

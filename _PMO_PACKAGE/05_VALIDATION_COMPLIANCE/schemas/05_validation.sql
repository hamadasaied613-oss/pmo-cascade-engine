-- ============================================================================
-- PMO DOMAINS — 05: Validation & Compliance
-- Color Code: #118ab2
-- Generated: 2026-06-16
-- ============================================================================

CREATE TABLE IF NOT EXISTS validation_results (
    V01_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT,
    V01_far_compliant INTEGER DEFAULT 0,
    V02_height_compliant INTEGER DEFAULT 0,
    V03_coverage_compliant INTEGER DEFAULT 0,
    V04_setback_compliant INTEGER DEFAULT 0,
    V05_parking_compliant INTEGER DEFAULT 0,
    V06_use_compliant INTEGER DEFAULT 0,
    V07_overall_pass INTEGER DEFAULT 0,
    V08_violation_count INTEGER DEFAULT 0,
    V09_compliance_score REAL DEFAULT 0,
    V10_last_audit_date TEXT
);

CREATE TABLE IF NOT EXISTS compliance_checks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT,
    authority TEXT,
    permit_approval TEXT,
    ref_code TEXT,
    fee_aed REAL,
    sla_days INTEGER,
    submission_date TEXT,
    target_date TEXT,
    actual_date TEXT,
    status TEXT DEFAULT 'Pending'
);

CREATE INDEX IF NOT EXISTS idx_vr_project ON validation_results(project_id);
CREATE INDEX IF NOT EXISTS idx_cc_authority ON compliance_checks(authority);

-- ============================================================================
-- PMO DOMAINS — 04: Zoning & Regulatory
-- Color Code: #ef476f
-- Generated: 2026-06-16
-- ============================================================================

CREATE TABLE IF NOT EXISTS zoning_regulatory (
    Z01_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT,
    Z01_zone_class TEXT,
    Z02_land_use_code TEXT,
    Z03_permitted_uses TEXT,
    Z04_max_far REAL,
    Z05_max_height_m REAL,
    Z06_max_floors INTEGER,
    Z07_ground_coverage_pct REAL,
    Z08_setback_front_m REAL,
    Z09_setback_rear_m REAL,
    Z10_setback_side_m REAL,
    Z11_parking_ratio REAL,
    Z12_podium_height_m REAL,
    Z13_far_bonus_eligible INTEGER DEFAULT 0,
    Z14_far_bonus_pct REAL DEFAULT 0,
    Z15_height_bonus_eligible INTEGER DEFAULT 0,
    Z16_height_bonus_m REAL DEFAULT 0,
    Z17_heritage_overlay INTEGER DEFAULT 0,
    Z18_environmental_overlay INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS planning_rules (
    rule_id INTEGER PRIMARY KEY AUTOINCREMENT,
    authority TEXT NOT NULL,
    emirate TEXT NOT NULL,
    zone_code TEXT NOT NULL,
    max_far REAL,
    max_height REAL,
    max_coverage REAL,
    setback_front_m REAL DEFAULT 3.0,
    setback_rear_m REAL DEFAULT 3.0,
    setback_side_m REAL DEFAULT 1.5,
    parking_ratio REAL DEFAULT 1.0,
    effective_date TEXT,
    expiry_date TEXT
);

CREATE TABLE IF NOT EXISTS far_limits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emirate TEXT,
    land_use TEXT,
    typology TEXT,
    far_min REAL,
    far_optimal REAL,
    far_max REAL,
    coverage_min_pct REAL,
    coverage_optimal_pct REAL,
    coverage_max_pct REAL,
    height_min_m REAL,
    height_optimal_m REAL,
    height_max_m REAL,
    notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_zr_zone ON zoning_regulatory(Z01_zone_class);
CREATE INDEX IF NOT EXISTS idx_pr_emirate ON planning_rules(emirate);

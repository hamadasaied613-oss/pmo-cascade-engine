-- ============================================================================
-- PMO DOMAINS — 07: Unit Mix & Program
-- Color Code: #8338ec
-- Generated: 2026-06-16
-- ============================================================================

CREATE TABLE IF NOT EXISTS unit_mix (
    U01_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT,
    U01_total_units INTEGER,
    U02_studio_count INTEGER DEFAULT 0,
    U03_1br_count INTEGER DEFAULT 0,
    U04_2br_count INTEGER DEFAULT 0,
    U05_3br_count INTEGER DEFAULT 0,
    U06_4br_count INTEGER DEFAULT 0,
    U07_penthouse_count INTEGER DEFAULT 0,
    U08_retail_sqm REAL DEFAULT 0,
    U09_office_sqm REAL DEFAULT 0,
    U10_hotel_rooms INTEGER DEFAULT 0,
    U11_amenity_sqm REAL DEFAULT 0,
    U12_parking_spaces INTEGER
);

CREATE TABLE IF NOT EXISTS unit_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    unit_code TEXT UNIQUE,
    unit_name TEXT,
    min_area_sqm REAL,
    max_area_sqm REAL,
    typical_area_sqm REAL,
    bedroom_count INTEGER,
    category TEXT
);

CREATE INDEX IF NOT EXISTS idx_um_project ON unit_mix(project_id);

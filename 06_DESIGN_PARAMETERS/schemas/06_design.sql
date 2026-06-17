-- ============================================================================
-- PMO DOMAINS — 06: Design Parameters
-- Color Code: #073b4c
-- Generated: 2026-06-16
-- ============================================================================

CREATE TABLE IF NOT EXISTS design_parameters (
    D01_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT,
    D01_proposed_gfa_m2 REAL,
    D02_proposed_floors INTEGER,
    D03_basement_floors INTEGER DEFAULT 0,
    D04_podium_floors INTEGER DEFAULT 0,
    D05_typical_floor_area_m2 REAL,
    D06_efficiency_ratio REAL,
    D07_structural_system TEXT,
    D08_facade_type TEXT,
    D09_core_count INTEGER,
    D10_elevator_count INTEGER,
    D11_ceiling_height_m REAL,
    D12_floor_to_floor_m REAL,
    D13_parking_levels INTEGER DEFAULT 0,
    D14_design_capacity TEXT
);

CREATE TABLE IF NOT EXISTS design_params_extended (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    parameter_name TEXT,
    parameter_value TEXT,
    unit TEXT,
    category TEXT
);

CREATE TABLE IF NOT EXISTS cost_indices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emirate TEXT,
    typology TEXT,
    structure_aed_sqm REAL,
    mep_aed_sqm REAL,
    finishes_aed_sqm REAL,
    land_price_aed_sqm REAL
);

CREATE INDEX IF NOT EXISTS idx_dp_project ON design_parameters(project_id);

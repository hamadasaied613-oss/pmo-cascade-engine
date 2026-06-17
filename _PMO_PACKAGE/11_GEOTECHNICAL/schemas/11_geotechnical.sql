-- ============================================================================
-- PMO DOMAINS — 11: Geotechnical & Foundations
-- Color Code: #80ed99
-- Generated: 2026-06-16
-- ============================================================================

CREATE TABLE IF NOT EXISTS geotechnical_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    soil_type TEXT NOT NULL,
    bc_min_kpa REAL,
    bc_max_kpa REAL,
    bc_typical_kpa REAL,
    foundation_type TEXT,
    shoring_system TEXT,
    shoring_cost_aed_m2 REAL,
    dewatering_system TEXT,
    dewatering_cost_aed_m2 REAL,
    cost_factor REAL DEFAULT 1.0,
    gw_depth_m REAL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS site_geotechnical (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emirate TEXT,
    area TEXT,
    lat REAL,
    lon REAL,
    soil_type TEXT,
    bearing_capacity_kpa REAL,
    settlement_mm REAL,
    groundwater_depth_m REAL,
    sulfate_ppm REAL,
    chloride_ppm REAL,
    pile_capacity_kn REAL,
    foundation_recommendation TEXT,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS engineering_soils (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    soil_type TEXT NOT NULL,
    uscs_group TEXT,
    unit_weight_kn_m3 REAL,
    friction_angle_deg REAL,
    cohesion_kpa REAL,
    bearing_capacity_factor_nc REAL,
    bearing_capacity_factor_nq REAL,
    bearing_capacity_factor_ng REAL,
    elastic_modulus_mpa REAL,
    poisson_ratio REAL,
    classification TEXT
);

CREATE INDEX IF NOT EXISTS idx_gd_soil ON geotechnical_data(soil_type);
CREATE INDEX IF NOT EXISTS idx_sg_emirate ON site_geotechnical(emirate);

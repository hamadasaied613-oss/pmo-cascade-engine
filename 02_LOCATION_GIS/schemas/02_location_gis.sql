-- ============================================================================
-- PMO DOMAINS — 02: Location & GIS
-- Color Code: #06d6a0
-- Generated: 2026-06-16
-- ============================================================================

CREATE TABLE IF NOT EXISTS location_data (
    L01_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT,
    L01_loc_emirate TEXT NOT NULL,
    L02_loc_jurisdiction TEXT,
    L03_loc_district TEXT,
    L04_subdistrict TEXT,
    L05_jurisdiction_region TEXT,
    L06_zoning_code TEXT,
    L07_land_use TEXT,
    L08_plot_number TEXT NOT NULL,
    L09_parcel_id TEXT,
    L10_plot_area_sqm REAL,
    L11_coord_x REAL,
    L12_coord_y REAL,
    L13_coord_z REAL,
    L14_makani_no TEXT,
    L15_location_class TEXT,
    L16_zone_code TEXT
);

CREATE TABLE IF NOT EXISTS emirates_registry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    emirate_name TEXT UNIQUE NOT NULL,
    emirate_code TEXT NOT NULL,
    authority_main TEXT,
    area_km2 REAL,
    population_k REAL,
    main_language TEXT
);

CREATE TABLE IF NOT EXISTS uae_unified_data (
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

CREATE TABLE IF NOT EXISTS polygon_coordinates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT,
    plot_id TEXT,
    vertex_index INTEGER,
    vertex_e REAL,
    vertex_n REAL
);

CREATE INDEX IF NOT EXISTS idx_loc_emirate ON location_data(L01_loc_emirate);
CREATE INDEX IF NOT EXISTS idx_loc_jurisdiction ON location_data(L02_loc_jurisdiction);

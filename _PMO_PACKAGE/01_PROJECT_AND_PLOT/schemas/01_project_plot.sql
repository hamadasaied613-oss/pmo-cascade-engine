-- ============================================================================
-- PMO DOMAINS — 01: Project & Plot Data
-- Color Code: #00b4d8
-- Generated: 2026-06-16
-- ============================================================================

-- Core project identification and plot geometry
CREATE TABLE IF NOT EXISTS project_identity (
    P01_id INTEGER PRIMARY KEY AUTOINCREMENT,
    P02_project_name TEXT NOT NULL,
    P03_project_code TEXT,
    P04_project_desc TEXT,
    P05_proj_status TEXT DEFAULT 'Planning',
    P06_phase_code TEXT,
    P07_proj_type_code TEXT,
    P08_category TEXT,
    P09_program_code TEXT
);

CREATE TABLE IF NOT EXISTS plot_data (
    plot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER NOT NULL,
    P03_plot_no TEXT NOT NULL,
    P04_plot_area_ft2 REAL,
    P05_plot_area_m2 REAL,
    P06_plot_width_m REAL,
    P07_plot_depth_m REAL,
    P08_plot_status TEXT DEFAULT 'Planning',
    P09_existing_structure INTEGER DEFAULT 0,
    FOREIGN KEY (project_id) REFERENCES project_identity(P01_id)
);

CREATE TABLE IF NOT EXISTS project_master (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT UNIQUE NOT NULL,
    name TEXT,
    emirate TEXT,
    district TEXT,
    zone TEXT,
    plot_area_m2 REAL,
    coverage_pct REAL,
    far REAL,
    height_limit_m REAL,
    gfa_m2 REAL,
    floors INTEGER,
    building_height_m REAL,
    structural_system TEXT,
    soil_type TEXT,
    total_cost_aed REAL,
    cost_per_sqm_aed REAL,
    duration_days INTEGER,
    quality_score REAL,
    status TEXT,
    risk_level TEXT,
    created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS plot_geometry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id INTEGER,
    plot_no TEXT,
    centroid_x REAL,
    centroid_y REAL,
    area_sqm REAL,
    perimeter_m REAL,
    vertex_count INTEGER,
    FOREIGN KEY (project_id) REFERENCES project_identity(P01_id)
);

CREATE INDEX IF NOT EXISTS idx_pi_status ON project_identity(P05_proj_status);
CREATE INDEX IF NOT EXISTS idx_pm_emirate ON project_master(emirate);
CREATE INDEX IF NOT EXISTS idx_pm_project ON project_master(project_id);

-- ============================================================================
-- PMO DOMAINS — 08: Cost & Economics
-- Color Code: #ff006e
-- Generated: 2026-06-16
-- ============================================================================

CREATE TABLE IF NOT EXISTS cost_analysis (
    C01_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT,
    C01_construction_cost_aed REAL,
    C02_cost_per_sqm_aed REAL,
    C03_contingency_pct REAL DEFAULT 10,
    C04_land_cost_aed REAL,
    C05_soft_cost_aed REAL,
    C06_finance_cost_aed REAL DEFAULT 0,
    C07_total_cost_aed REAL,
    C08_projected_revenue_aed REAL,
    C09_net_profit_aed REAL,
    C10_roi_pct REAL,
    C11_npv_aed REAL,
    C12_irr_pct REAL
);

CREATE TABLE IF NOT EXISTS csi_cost_codes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    csi_code INTEGER,
    category TEXT,
    basic_aed_sqm REAL,
    standard_aed_sqm REAL,
    premium_aed_sqm REAL,
    luxury_aed_sqm REAL
);

CREATE TABLE IF NOT EXISTS cost_benchmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_key TEXT,
    uom TEXT,
    value REAL,
    source TEXT
);

CREATE TABLE IF NOT EXISTS financial_projections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT,
    year INTEGER,
    capex_aed REAL,
    opex_aed REAL,
    revenue_aed REAL,
    net_cash_flow_aed REAL
);

CREATE INDEX IF NOT EXISTS idx_ca_project ON cost_analysis(project_id);

-- ============================================================================
-- PMO DOMAINS — 12: Sustainability, Quality & BIM
-- Color Code: #c77dff
-- Generated: 2026-06-16
-- ============================================================================

CREATE TABLE IF NOT EXISTS sustainability (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT,
    sustainability_id TEXT,
    leed_certification_goal TEXT,
    estidama_pearl_target TEXT,
    dubai_green_score REAL,
    energy_consumption_target REAL,
    water_consumption_target REAL,
    recycled_material_target REAL,
    renewable_energy_pct REAL,
    carbon_footprint_target REAL,
    waste_diversion_target REAL,
    green_roof_area_pct REAL,
    ev_charging_stations INTEGER,
    green_materials_pct REAL,
    operational_carbon_reduction REAL,
    embodied_carbon_reduction REAL
);

CREATE TABLE IF NOT EXISTS quality_master (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT,
    quality_id TEXT,
    quality_plan_id TEXT,
    inspection_test_plan_id TEXT,
    material_approval_status TEXT,
    shop_drawing_status TEXT,
    testing_requirement TEXT,
    inspection_hold_point TEXT,
    quality_control_checklist TEXT,
    non_conformance_report_id TEXT,
    corrective_action_id TEXT,
    quality_kpi_measurement TEXT,
    customer_satisfaction_index REAL,
    defect_density REAL,
    rework_cost_aed REAL,
    first_pass_yield REAL,
    quality_management_system TEXT,
    accreditation_certification TEXT,
    regulatory_compliance_status TEXT
);

CREATE TABLE IF NOT EXISTS risk_register (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT,
    risk_id TEXT,
    risk_category TEXT,
    risk_description TEXT,
    probability_pct REAL,
    impact_level REAL,
    risk_score REAL,
    risk_owner TEXT,
    risk_response_strategy TEXT,
    mitigation_action TEXT,
    contingency_plan TEXT,
    trigger_indicator TEXT,
    risk_status TEXT,
    risk_budget_aed REAL
);

CREATE TABLE IF NOT EXISTS bim_master (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT,
    bim_id TEXT,
    bim_uses TEXT,
    lod_requirement TEXT,
    model_responsibility_matrix TEXT,
    cde_platform TEXT,
    clash_detection_protocol TEXT,
    quantity_takeoff_method TEXT,
    simulation_4d_required INTEGER DEFAULT 0,
    costing_5d_required INTEGER DEFAULT 0,
    asset_information_requirement TEXT,
    co_bie_deliverable TEXT,
    digital_twin_requirement TEXT,
    software_platforms TEXT,
    bim_standards_compliance TEXT
);

CREATE TABLE IF NOT EXISTS omm_master (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT,
    omm_id TEXT,
    preventive_maintenance_schedule TEXT,
    spare_parts_inventory TEXT,
    warranty_management TEXT,
    service_provider_contracts TEXT,
    facility_management_system TEXT,
    energy_management_system TEXT,
    life_cycle_cost_analysis TEXT,
    replacement_schedule TEXT,
    operational_budget_aed_year REAL,
    maintenance_staffing TEXT,
    handover_requirements TEXT,
    as_built_documentation TEXT
);

CREATE INDEX IF NOT EXISTS idx_sus_project ON sustainability(project_id);
CREATE INDEX IF NOT EXISTS idx_rr_project ON risk_register(project_id);

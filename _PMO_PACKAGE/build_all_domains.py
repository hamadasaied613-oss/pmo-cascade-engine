#!/usr/bin/env python3
"""
PMO DOMAINS BUILDER — Generates all 12 domain packages
Each package: schema.sql + data_raw/*.csv + databases/*.db + diagrams/*.mmd
"""
import sqlite3, csv, os, json
from pathlib import Path

BASE = Path(__file__).parent

# ============================================================================
# COLOR SCHEME FOR SCHEMAS (Ras Flat Dark Style)
# ============================================================================
COLORS = {
    "01": ("#00b4d8", "Project & Plot"),
    "02": ("#06d6a0", "Location & GIS"),
    "03": ("#ffd166", "Stakeholders"),
    "04": ("#ef476f", "Zoning & Regulatory"),
    "05": ("#118ab2", "Validation & Compliance"),
    "06": ("#073b4c", "Design Parameters"),
    "07": ("#8338ec", "Unit Mix & Program"),
    "08": ("#ff006e", "Cost & Economics"),
    "09": ("#fb5607", "Schedule & Timeline"),
    "10": ("#3a86ff", "Approvals & Authorities"),
    "11": ("#80ed99", "Geotechnical"),
    "12": ("#c77dff", "Sustainability & BIM"),
}

def sql_header(domain_id, title, color):
    return f"""-- ============================================================================
-- PMO DOMAINS — {domain_id}: {title}
-- Color Code: {color}
-- Generated: 2026-06-16
-- ============================================================================
"""

def write_file(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  [OK] {path.relative_to(BASE)}")

def create_db(domain_dir, sql_content, db_name="domain.db"):
    db_path = domain_dir / "databases" / db_name
    conn = sqlite3.connect(str(db_path))
    conn.executescript(sql_content)
    conn.close()
    print(f"  [DB] {db_path.relative_to(BASE)}")

# ============================================================================
# DOMAIN 01: PROJECT & PLOT
# ============================================================================
def build_domain_01():
    d = BASE / "01_PROJECT_AND_PLOT"
    color, title = COLORS["01"]

    schema = sql_header("01", "Project & Plot Data", color) + """
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
"""
    write_file(d / "schemas" / "01_project_plot.sql", schema)
    create_db(d, schema, "project_plot.db")

    # CSV data — tightened values from RM model + schemas
    csv_data = """project_name,project_code,emirate,district,zone,plot_area_m2,coverage_pct,far,height_limit_m,gfa_m2,floors,building_height_m,structural_system,soil_type,total_cost_aed,cost_per_sqm_aed,duration_days,quality_score,status,risk_level
Ritz Carlton Tower,RC-001,Dubai,Marina,COMM-01,2850,0.45,5.8,120,16530,19,76.0,RC Frame,Dense Sand,245000000,14822,730,87.5,Active,Low
Business Bay Tower,BB-002,Dubai,Business Bay,COMM-02,1920,0.40,5.0,100,9600,15,60.0,RC Frame,Medium Dense Sand,145000000,15104,540,82.0,Active,Medium
JBR Beach Residence,JBR-003,Dubai,JBR,RES-03,3200,0.50,4.5,80,14400,12,48.0,RC Shear Wall,Loose Sand,98000000,6806,480,79.5,Planning,Low
Abu Dhabi Corniche,AC-004,Abu Dhabi,Corniche,MIXED-01,4500,0.55,6.5,120,29250,22,88.0,Steel + RC,Stiff Clay,380000000,12991,810,91.0,Active,Low
Sharjah Waterfront,SW-005,Sharjah,Waterfront,RES-01,2800,0.45,4.0,60,11200,10,40.0,RC Frame,Medium Sand,65000000,5804,420,75.0,Design,Medium
"""

    write_file(d / "data_raw" / "project_data.csv", csv_data.strip())

    # Load CSV into DB
    conn = sqlite3.connect(str(d / "databases" / "project_plot.db"))
    cur = conn.cursor()
    cur.execute("DELETE FROM project_master")
    with open(d / "data_raw" / "project_data.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("""INSERT INTO project_master 
                (project_id,name,emirate,district,zone,plot_area_m2,coverage_pct,far,height_limit_m,
                 gfa_m2,floors,building_height_m,structural_system,soil_type,total_cost_aed,cost_per_sqm_aed,
                 duration_days,quality_score,status,risk_level)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                (row["project_code"],row["project_name"],row["emirate"],row["district"],
                 row["zone"],float(row["plot_area_m2"]),float(row["coverage_pct"]),
                 float(row["far"]),float(row["height_limit_m"]),float(row["gfa_m2"]),
                 int(row["floors"]),float(row["building_height_m"]),row["structural_system"],
                 row["soil_type"],float(row["total_cost_aed"]),float(row["cost_per_sqm_aed"]),
                 int(row["duration_days"]),float(row["quality_score"]),row["status"],row["risk_level"]))
    conn.commit(); conn.close()

    diagram = """erDiagram
    PROJECT_IDENTITY {
        int P01_id PK
        string P02_project_name
        string P05_proj_status
    }
    PLOT_DATA {
        int plot_id PK
        int project_id FK
        string P03_plot_no
        real P05_plot_area_m2
    }
    PROJECT_MASTER {
        int id PK
        string project_id UK
        string emirate
        real total_cost
        int duration_days
    }
    PROJECT_IDENTITY ||--o{ PLOT_DATA : "has plots"
    PROJECT_IDENTITY ||--o{ PROJECT_MASTER : "tracked by"
"""
    write_file(d / "diagrams" / "project_plot_erd.mmd", diagram)
    print(f"  Domain 01 done.")

# ============================================================================
# DOMAIN 02: LOCATION & GIS
# ============================================================================
def build_domain_02():
    d = BASE / "02_LOCATION_GIS"
    color, title = COLORS["02"]

    schema = sql_header("02", "Location & GIS", color) + """
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
"""
    write_file(d / "schemas" / "02_location_gis.sql", schema)
    create_db(d, schema, "location_gis.db")

    csv_data = """emirate,jurisdiction,authority_main,area_km2,population_k,zone_type,main_planning,building_permit,civil_defense,power_water
Dubai,Dubai Municipality (DM),DM,4114,3600,Mainland,DM,DM,DCD,DEWA
Dubai,DDA (DIEZ),DDA,4114,3600,Creative/ Tech,DDA,DDA,DCD,DEWA
Dubai,Trakhees (PCFC),Trakhees,4114,3600,Ports/ Freezone,Trakhees,Trakhees,DCD,DEWA
Abu Dhabi,DMT (Mainland),DMT,67340,1800,Mainland,DMT,DMT,ADCDA,ADPower/AADC
Abu Dhabi,ADGM,ADGM,67340,1800,Free Zone,ADGM,ADGM,ADCDA,ADPower
Sharjah,Sharjah Municipality,SM,2590,1800,Mainland,SM,SM,SCD,SEWA
Ajman,Ajman Municipality,AM,720,500,Mainland,AM,AM,ACD,AEA
Umm Al Quwain,UAQ Municipality,UAQM,720,50,Mainland,UAQM,UAQM,UCD,UEA
Ras Al Khaimah,RAK Municipality,RAKM,1684,200,Mainland,RAKM,RAKM,RCD,RAKEA
Fujairah,Fujairah Municipality,FM,1450,160,Mainland,FM,FM,FCD,FEA
"""
    write_file(d / "data_raw" / "location_data.csv", csv_data.strip())

    conn = sqlite3.connect(str(d / "databases" / "location_gis.db"))
    cur = conn.cursor()
    cur.execute("DELETE FROM uae_unified_data")
    with open(d / "data_raw" / "location_data.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("INSERT INTO uae_unified_data (emirate,jurisdiction,master_planning,building_permit,civil_defense,power_water,notes) VALUES (?,?,?,?,?,?,?)",
                (row["emirate"],row["jurisdiction"],row["main_planning"],row["building_permit"],row["civil_defense"],row["power_water"],row["zone_type"]))
    conn.commit(); conn.close()

    diagram = """erDiagram
    EMIRATES_REGISTRY {
        int id PK
        string emirate_name UK
        string authority_main
    }
    LOCATION_DATA {
        int L01_id PK
        string L01_loc_emirate
        real L11_coord_x
        real L12_coord_y
    }
    UAE_UNIFIED_DATA {
        int id PK
        string emirate
        string jurisdiction
        string building_permit
    }
    EMIRATES_REGISTRY ||--o{ LOCATION_DATA : "contains"
    EMIRATES_REGISTRY ||--o{ UAE_UNIFIED_DATA : "mapped to"
"""
    write_file(d / "diagrams" / "location_gis_erd.mmd", diagram)
    print(f"  Domain 02 done.")

# ============================================================================
# DOMAIN 03: STAKEHOLDERS
# ============================================================================
def build_domain_03():
    d = BASE / "03_STAKEHOLDERS"
    color, title = COLORS["03"]

    schema = sql_header("03", "Stakeholders", color) + """
CREATE TABLE IF NOT EXISTS stakeholders (
    S01_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT,
    S01_stk_owner_name TEXT NOT NULL,
    S02_stk_developer TEXT,
    S03_stk_contractor TEXT,
    S04_stk_consultant TEXT,
    S05_stk_project_manager TEXT,
    S06_stk_supervising_auth TEXT,
    S07_stk_owner_rep TEXT,
    S08_stk_main_bank TEXT,
    S09_stk_funding_source TEXT,
    S10_stk_legal_rep TEXT,
    S11_stk_partners TEXT,
    S12_stk_operator TEXT
);

CREATE TABLE IF NOT EXISTS developers_registry (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT,
    emirate TEXT,
    contact_info TEXT,
    portfolio_size TEXT
);

CREATE INDEX IF NOT EXISTS idx_stk_owner ON stakeholders(S01_stk_owner_name);
"""
    write_file(d / "schemas" / "03_stakeholders.sql", schema)
    create_db(d, schema, "stakeholders.db")

    csv_data = """project_id,owner,developer,contractor,consultant,project_manager,supervising_authority,bank,operator
RC-001,Emaar Properties,Emaar Properties,Arabtec Construction,Dar Al-Handasah,Turner International,DM,Emirates NBD,Marriott International
BB-002,Dubai Holding,Sobha Realty,Sobha Realty,WS Atkins,Bechtel,DM,ADCB,Jumeirah Group
JBR-003,Meraas,Meraas,Al Habtoor Group,AECOM,Mace,DM,Dubai Islamic Bank,Meraas Hospitality
AC-004,Aldar Properties,Aldar Properties,Samsung C&T,Parsons Brinckerhoff,WSP,DMT,First Abu Dhabi Bank,Aldar Hospitality
SW-005,Sharjah Asset Management,Sharjah Holding,Khatib & Alami,Schneider Electric,CH2M Hill,SM,SIB,IHG Hotels
"""
    write_file(d / "data_raw" / "stakeholders_data.csv", csv_data.strip())

    conn = sqlite3.connect(str(d / "databases" / "stakeholders.db"))
    cur = conn.cursor()
    cur.execute("DELETE FROM stakeholders")
    with open(d / "data_raw" / "stakeholders_data.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("INSERT INTO stakeholders (project_id,S01_stk_owner_name,S02_stk_developer,S03_stk_contractor,S04_stk_consultant,S05_stk_project_manager,S06_stk_supervising_auth,S08_stk_main_bank,S12_stk_operator) VALUES (?,?,?,?,?,?,?,?,?)",
                (row["project_id"],row["owner"],row["developer"],row["contractor"],row["consultant"],row["project_manager"],row["supervising_authority"],row["bank"],row["operator"]))
    conn.commit(); conn.close()

    diagram = """erDiagram
    STAKEHOLDERS {
        int S01_id PK
        string project_id
        string S01_stk_owner_name
        string S03_stk_contractor
        string S04_stk_consultant
    }
"""
    write_file(d / "diagrams" / "stakeholders_erd.mmd", diagram)
    print(f"  Domain 03 done.")

# ============================================================================
# DOMAIN 04: ZONING & REGULATORY
# ============================================================================
def build_domain_04():
    d = BASE / "04_ZONING_REGULATORY"
    color, title = COLORS["04"]

    schema = sql_header("04", "Zoning & Regulatory", color) + """
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
"""
    write_file(d / "schemas" / "04_zoning_regulatory.sql", schema)
    create_db(d, schema, "zoning_regulatory.db")

    csv_data = """emirate,land_use,typology,far_min,far_optimal,far_max,coverage_min_pct,coverage_optimal_pct,coverage_max_pct,height_min_m,height_optimal_m,height_max_m,notes
Dubai,Residential,High-Rise Tower,4.0,5.0,6.0,35,40,45,60,80,100,DM Mainland standard
Dubai,Mixed-use,High-Rise Tower,4.0,5.5,7.0,40,45,50,60,90,120,DM Mixed-use zones
Dubai,Commercial,Mid-Rise,2.5,3.0,4.0,60,70,80,30,45,60,DDA Creative zones
Abu Dhabi,Residential,High-Rise Tower,3.0,4.0,5.0,30,35,40,50,70,90,DMT Mainland
Abu Dhabi,Commercial,Mid-Rise,2.0,2.5,3.5,55,65,75,25,40,55,DMT Commercial
Sharjah,Residential,High-Rise Tower,3.0,3.5,4.5,30,35,40,45,60,80,SM Standard
Sharjah,Residential,Mid-Rise,2.0,2.5,3.0,50,60,70,25,35,50,SM Standard
"""
    write_file(d / "data_raw" / "far_limits.csv", csv_data.strip())

    conn = sqlite3.connect(str(d / "databases" / "zoning_regulatory.db"))
    cur = conn.cursor()
    cur.execute("DELETE FROM far_limits")
    with open(d / "data_raw" / "far_limits.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("INSERT INTO far_limits (emirate,land_use,typology,far_min,far_optimal,far_max,coverage_min_pct,coverage_optimal_pct,coverage_max_pct,height_min_m,height_optimal_m,height_max_m,notes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (row["emirate"],row["land_use"],row["typology"],float(row["far_min"]),float(row["far_optimal"]),float(row["far_max"]),
                 float(row["coverage_min_pct"]),float(row["coverage_optimal_pct"]),float(row["coverage_max_pct"]),
                 float(row["height_min_m"]),float(row["height_optimal_m"]),float(row["height_max_m"]),row["notes"]))
    conn.commit(); conn.close()

    diagram = """erDiagram
    ZONING_REGULATORY {
        int Z01_id PK
        string Z01_zone_class
        real Z04_max_far
        real Z05_max_height_m
    }
    PLANNING_RULES {
        int rule_id PK
        string authority
        string emirate
        real max_far
    }
    FAR_LIMITS {
        int id PK
        string emirate
        real far_min
        real far_max
    }
    PLANNING_RULES ||--o{ ZONING_REGULATORY : "defines"
"""
    write_file(d / "diagrams" / "zoning_erd.mmd", diagram)
    print(f"  Domain 04 done.")

# ============================================================================
# DOMAIN 05: VALIDATION & COMPLIANCE
# ============================================================================
def build_domain_05():
    d = BASE / "05_VALIDATION_COMPLIANCE"
    color, title = COLORS["05"]

    schema = sql_header("05", "Validation & Compliance", color) + """
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
"""
    write_file(d / "schemas" / "05_validation.sql", schema)
    create_db(d, schema, "validation.db")

    csv_data = """authority,permit_approval,ref_code,fee_aed,sla_days,status
Dubai Municipality,Building Permit,DM-BP-001,0,45,Active
Dubai Municipality,Environmental NOC,DM-ENV-001,15000,30,Active
DCD,Civil Defense NOC,DCD-NOC-001,5000,14,Active
DEWA,Power Connection,DEWA-PC-001,285350,60,Pending
DLD,Title Deed,DLD-TD-001,4000000,10,Active
DLD,Transfer Fee,DLD-TF-001,4000000,7,Active
Empower,District Cooling,EMP-DC-001,500000,45,Pending
SIRA,Security Approval,SIRA-SA-001,8000,14,Pending
"""
    write_file(d / "data_raw" / "compliance_data.csv", csv_data.strip())

    conn = sqlite3.connect(str(d / "databases" / "validation.db"))
    cur = conn.cursor()
    cur.execute("DELETE FROM compliance_checks")
    with open(d / "data_raw" / "compliance_data.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("INSERT INTO compliance_checks (authority,permit_approval,ref_code,fee_aed,sla_days,status) VALUES (?,?,?,?,?,?)",
                (row["authority"],row["permit_approval"],row["ref_code"],float(row["fee_aed"]),int(row["sla_days"]),row["status"]))
    conn.commit(); conn.close()

    diagram = """erDiagram
    VALIDATION_RESULTS {
        int V01_id PK
        real V09_compliance_score
        int V07_overall_pass
    }
    COMPLIANCE_CHECKS {
        int id PK
        string authority
        string permit_approval
        real fee_aed
        int sla_days
    }
    VALIDATION_RESULTS ||--o{ COMPLIANCE_CHECKS : "validated by"
"""
    write_file(d / "diagrams" / "validation_erd.mmd", diagram)
    print(f"  Domain 05 done.")

# ============================================================================
# DOMAIN 06: DESIGN PARAMETERS
# ============================================================================
def build_domain_06():
    d = BASE / "06_DESIGN_PARAMETERS"
    color, title = COLORS["06"]

    schema = sql_header("06", "Design Parameters", color) + """
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
"""
    write_file(d / "schemas" / "06_design.sql", schema)
    create_db(d, schema, "design_parameters.db")

    csv_data = """emirate,typology,structure_aed_sqm,mep_aed_sqm,finishes_aed_sqm,land_price_aed_sqm
Dubai,High-Rise Tower,2200,1800,1600,2500
Dubai,Mid-Rise,1800,1500,1300,2000
Dubai,Low-Rise,1400,1200,1000,1500
Abu Dhabi,High-Rise Tower,2100,1700,1500,2000
Abu Dhabi,Mid-Rise,1700,1400,1200,1600
Abu Dhabi,Low-Rise,1300,1100,900,1200
Sharjah,High-Rise Tower,1900,1600,1400,1200
Sharjah,Mid-Rise,1600,1300,1100,900
Sharjah,Low-Rise,1200,1000,800,700
"""
    write_file(d / "data_raw" / "cost_indices.csv", csv_data.strip())

    conn = sqlite3.connect(str(d / "databases" / "design_parameters.db"))
    cur = conn.cursor()
    cur.execute("DELETE FROM cost_indices")
    with open(d / "data_raw" / "cost_indices.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("INSERT INTO cost_indices (emirate,typology,structure_aed_sqm,mep_aed_sqm,finishes_aed_sqm,land_price_aed_sqm) VALUES (?,?,?,?,?,?)",
                (row["emirate"],row["typology"],float(row["structure_aed_sqm"]),float(row["mep_aed_sqm"]),float(row["finishes_aed_sqm"]),float(row["land_price_aed_sqm"])))
    conn.commit(); conn.close()

    diagram = """erDiagram
    DESIGN_PARAMETERS {
        int D01_id PK
        real D01_proposed_gfa_m2
        int D02_proposed_floors
        real D06_efficiency_ratio
    }
    COST_INDICES {
        int id PK
        string emirate
        real structure_aed_sqm
    }
"""
    write_file(d / "diagrams" / "design_erd.mmd", diagram)
    print(f"  Domain 06 done.")

# ============================================================================
# DOMAIN 07: UNIT MIX & PROGRAM
# ============================================================================
def build_domain_07():
    d = BASE / "07_UNIT_MIX_PROGRAM"
    color, title = COLORS["07"]

    schema = sql_header("07", "Unit Mix & Program", color) + """
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
"""
    write_file(d / "schemas" / "07_unit_mix.sql", schema)
    create_db(d, schema, "unit_mix.db")

    csv_data = """unit_code,unit_name,min_area_sqm,max_area_sqm,typical_area_sqm,bedroom_count,category
STD,Studio,38,55,45,0,Residential
1BR,One Bedroom,60,85,72,1,Residential
2BR,Two Bedroom,95,130,112,2,Residential
3BR,Three Bedroom,140,185,160,3,Residential
4BR,Four Bedroom,200,280,240,4,Residential
PH,Penthouse,300,600,450,5,Residential
RET,Retail,50,500,150,-1,Commercial
OFF,Office,80,300,150,-1,Commercial
HRM,Hotel Room,35,65,48,-1,Hospitality
SUI,Hotel Suite,70,200,120,-1,Hospitality
"""
    write_file(d / "data_raw" / "unit_types.csv", csv_data.strip())

    conn = sqlite3.connect(str(d / "databases" / "unit_mix.db"))
    cur = conn.cursor()
    cur.execute("DELETE FROM unit_types")
    with open(d / "data_raw" / "unit_types.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("INSERT INTO unit_types (unit_code,unit_name,min_area_sqm,max_area_sqm,typical_area_sqm,bedroom_count,category) VALUES (?,?,?,?,?,?,?)",
                (row["unit_code"],row["unit_name"],float(row["min_area_sqm"]),float(row["max_area_sqm"]),float(row["typical_area_sqm"]),int(row["bedroom_count"]),row["category"]))
    conn.commit(); conn.close()

    diagram = """erDiagram
    UNIT_MIX {
        int U01_id PK
        int U01_total_units
        int U12_parking_spaces
    }
    UNIT_TYPES {
        int id PK
        string unit_code UK
        real typical_area_sqm
    }
    UNIT_TYPES ||--o{ UNIT_MIX : "classifies"
"""
    write_file(d / "diagrams" / "unit_mix_erd.mmd", diagram)
    print(f"  Domain 07 done.")

# ============================================================================
# DOMAIN 08: COST & ECONOMICS
# ============================================================================
def build_domain_08():
    d = BASE / "08_COST_ECONOMICS"
    color, title = COLORS["08"]

    schema = sql_header("08", "Cost & Economics", color) + """
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
"""
    write_file(d / "schemas" / "08_cost_economics.sql", schema)
    create_db(d, schema, "cost_economics.db")

    # CSI Cost Codes
    csv_csi = """csi_code,category,basic_aed_sqm,standard_aed_sqm,premium_aed_sqm,luxury_aed_sqm
1,General Requirements,50,75,100,150
2,Existing Conditions,30,45,60,90
3,Concrete,350,450,600,800
4,Masonry,200,250,350,500
5,Metals,400,500,700,1000
6,Wood/Plastics,150,200,300,450
7,Thermal/Moisture,100,150,200,300
8,Openings,250,350,500,750
9,Finishes,300,400,600,900
21,Fire Suppression,80,120,160,240
22,Plumbing,200,300,400,600
23,HVAC,350,450,600,800
26,Electrical,300,400,550,750
27,Communications,150,200,300,450
28,Electronic Safety,100,150,200,300
"""
    write_file(d / "data_raw" / "csi_cost_codes.csv", csv_csi.strip())

    # Cost Benchmarks
    csv_bench = """item_key,uom,value,source
Concrete C40,m3,650,UAE Market 2025
Reinforcement Steel,ton,3200,UAE Market 2025
Formwork,m2,85,UAE Market 2025
Block Work,m2,120,UAE Market 2025
Painting,m2,35,UAE Market 2025
Tiling,m2,75,UAE Market 2025
Plastering,m2,25,UAE Market 2025
Electrical Works,m2,180,UAE Market 2025
Plumbing Works,m2,150,UAE Market 2025
HVAC Works,m2,200,UAE Market 2025
Aluminum Facade,m2,450,UAE Market 2025
Waterproofing,m2,60,UAE Market 2025
Insulation,m2,40,UAE Market 2025
Carpentry,m2,95,UAE Market 2025
Elevator,unit,250000,UAE Market 2025
"""
    write_file(d / "data_raw" / "cost_benchmarks.csv", csv_bench.strip())

    # Lifecycle costs
    csv_lifecycle = """phase,service,cost_aed,notes
Initiation & Planning,Developer NOC,3000,DLD requirement
Design & Contracting,DDA Permit Fee,100000,DDA standard
Construction,DEWA Connection Cost,285350,DEWA schedule
Services Connection,Empower Deposit,500000,Empower standard
Services Connection,Telecom Setup Fee,40000,du/Etisalat
Annual Services,Service Charges,7200000,Annual estimate
DLD Fees,Transfer Fee,4000000,DLD 4% standard
DLD Fees,Mortgage Fee,175000,0.25% of loan
DLD Fees,Admin Fee,400000,DLD standard
DLD Fees,VAT on Transfer Fee,200000,5% of transfer
"""
    write_file(d / "data_raw" / "uae_lifecycle_costs.csv", csv_lifecycle.strip())

    conn = sqlite3.connect(str(d / "databases" / "cost_economics.db"))
    cur = conn.cursor()
    cur.execute("DELETE FROM csi_cost_codes")
    with open(d / "data_raw" / "csi_cost_codes.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("INSERT INTO csi_cost_codes (csi_code,category,basic_aed_sqm,standard_aed_sqm,premium_aed_sqm,luxury_aed_sqm) VALUES (?,?,?,?,?,?)",
                (int(row["csi_code"]),row["category"],float(row["basic_aed_sqm"]),float(row["standard_aed_sqm"]),float(row["premium_aed_sqm"]),float(row["luxury_aed_sqm"])))
    cur.execute("DELETE FROM cost_benchmarks")
    with open(d / "data_raw" / "cost_benchmarks.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("INSERT INTO cost_benchmarks (item_key,uom,value,source) VALUES (?,?,?,?)",
                (row["item_key"],row["uom"],float(row["value"]),row["source"]))
    conn.commit(); conn.close()

    diagram = """erDiagram
    COST_ANALYSIS {
        int C01_id PK
        real C01_construction_cost_aed
        real C10_roi_pct
        real C11_npv_aed
    }
    CSI_COST_CODES {
        int id PK
        int csi_code
        string category
        real luxury_aed_sqm
    }
    COST_BENCHMARKS {
        int id PK
        string item_key
        real value
    }
"""
    write_file(d / "diagrams" / "cost_flow.mmd", diagram)
    print(f"  Domain 08 done.")

# ============================================================================
# DOMAIN 09: SCHEDULE & TIMELINE
# ============================================================================
def build_domain_09():
    d = BASE / "09_SCHEDULE_TIMELINE"
    color, title = COLORS["09"]

    schema = sql_header("09", "Schedule & Timeline", color) + """
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
"""
    write_file(d / "schemas" / "09_schedule.sql", schema)
    create_db(d, schema, "schedule.db")

    csv_data = """phase_id,phase_name,activity_id,activity_name,duration_days,is_critical,predecessor,resource_type
1,Enabling Works,101,Site Clearance & Mobilization,14,0,,Labour
1,Enabling Works,102,Shoring Installation,28,0,101,Equipment
1,Enabling Works,103,Excavation,21,0,102,Equipment
1,Enabling Works,104,Pile Foundations,45,1,103,Piling
2,Substructure,201,Raft Foundation,30,1,104,Concrete
2,Substructure,202,Basement Walls,21,0,201,Concrete
2,Substructure,203,Basement Slab,14,0,202,Concrete
3,Superstructure,301,Ground Floor Slab,10,0,203,Concrete
3,Superstructure,302,Typical Floor Cycle,7,1,301,Concrete
3,Superstructure,303,Structure Complete,0,1,302,Concrete
4,MEP Rough-in,401,MEP First Fix,60,0,301,MEP
4,MEP Rough-in,402,MEP Second Fix,45,0,401,MEP
5,Finishes,501,Internal Plastering,30,0,401,Finishes
5,Finishes,502,Tiling & Flooring,40,0,501,Finishes
5,Finishes,503,Painting & Decoration,25,0,502,Finishes
6,External Works,601,Facade Installation,90,0,303,Specialist
6,External Works,602,Landscaping,30,0,601,Labour
7,Commissioning,701,MEP Testing & Commissioning,30,0,402,MEP
7,Commissioning,702,Fire Life Safety,21,0,701,Specialist
7,Commissioning,703,Final Inspection,14,0,702,Inspection
8,Handover,801,Snagging & Rectification,21,0,703,All
8,Handover,802,Completion Certificate,14,0,801,Authority
8,Handover,803,Occupancy Certificate,7,0,802,Authority
"""
    write_file(d / "data_raw" / "wbs_activities.csv", csv_data.strip())

    conn = sqlite3.connect(str(d / "databases" / "schedule.db"))
    cur = conn.cursor()
    cur.execute("DELETE FROM wbs_activities")
    with open(d / "data_raw" / "wbs_activities.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("INSERT INTO wbs_activities (phase_id,phase_name,activity_id,activity_name,duration_days,is_critical,predecessor,resource_type) VALUES (?,?,?,?,?,?,?,?)",
                (int(row["phase_id"]),row["phase_name"],int(row["activity_id"]),row["activity_name"],int(row["duration_days"]),int(row["is_critical"]),row["predecessor"],row["resource_type"]))
    conn.commit(); conn.close()

    diagram = """erDiagram
    SCHEDULE_DATA {
        int T01_id PK
        string T04_construction_start
        string T05_construction_end
    }
    WBS_ACTIVITIES {
        int id PK
        int activity_id
        string activity_name
        int duration_days
        int is_critical
    }
    SCHEDULE_DATA ||--o{ WBS_ACTIVITIES : "contains"
"""
    write_file(d / "diagrams" / "gantt_chart.mmd", diagram)
    print(f"  Domain 09 done.")

# ============================================================================
# DOMAIN 10: APPROVALS & AUTHORITIES
# ============================================================================
def build_domain_10():
    d = BASE / "10_APPROVALS_AUTHORITIES"
    color, title = COLORS["10"]

    schema = sql_header("10", "Approvals & Authorities", color) + """
CREATE TABLE IF NOT EXISTS approvals (
    A01_id INTEGER PRIMARY KEY AUTOINCREMENT,
    project_id TEXT,
    A01_primary_authority TEXT,
    A02_noc_status TEXT DEFAULT 'Pending',
    A03_noc_issue_date TEXT,
    A04_building_permit_no TEXT,
    A05_bp_issue_date TEXT,
    A06_bp_expiry_date TEXT,
    A07_completion_cert_no TEXT,
    A08_cc_issue_date TEXT,
    A09_occupation_cert_no TEXT,
    A10_oc_issue_date TEXT
);

CREATE TABLE IF NOT EXISTS authority_matrix (
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

CREATE TABLE IF NOT EXISTS permit_sequence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    step_number INTEGER,
    permit_name TEXT NOT NULL,
    min_days INTEGER,
    max_days INTEGER,
    avg_days INTEGER,
    min_cost_aed REAL,
    max_cost_aed REAL,
    avg_cost_aed REAL,
    authority TEXT,
    notes TEXT
);

CREATE INDEX IF NOT EXISTS idx_ap_project ON approvals(project_id);
"""
    write_file(d / "schemas" / "10_approvals.sql", schema)
    create_db(d, schema, "approvals.db")

    # Permit sequence — tightened values (min/max/avg)
    csv_permit = """step_number,permit_name,min_days,max_days,avg_days,min_cost_aed,max_cost_aed,avg_cost_aed,authority
1,Land Title Deed,7,14,10,0,0,0,DLD
2,Land NOC from DLD,5,10,7,500,1000,750,DLD
3,Initial Planning Approval,14,28,21,2000,5000,3500,DM/DDA
4,Environmental NOC,30,60,45,10000,50000,30000,DM/EPDA
5,Geotechnical Report,14,28,21,15000,100000,57500,DM
6,RTA NOC,30,60,45,5000,50000,27500,RTA
7,Civil Defense NOC,14,28,21,2000,10000,6000,DCD
8,DEWA Connection,30,90,60,10000,500000,255000,DEWA
9,Building Permit,30,60,45,0,0,0,DM/DDA/Trakhees
10,District Cooling NOC,30,60,45,50000,500000,275000,Empower/Tabreed
11,Telecom NOC,14,28,21,5000,50000,27500,du/Etisalat
12,SIRA Security Approval,14,28,21,3000,20000,11500,SIRA
13,Completion Certificate,14,28,21,1000,5000,3000,DM
14,Occupancy Certificate,7,14,10,500,2000,1250,DM
"""
    write_file(d / "data_raw" / "permit_sequence.csv", csv_permit.strip())

    conn = sqlite3.connect(str(d / "databases" / "approvals.db"))
    cur = conn.cursor()
    cur.execute("DELETE FROM permit_sequence")
    with open(d / "data_raw" / "permit_sequence.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("INSERT INTO permit_sequence (step_number,permit_name,min_days,max_days,avg_days,min_cost_aed,max_cost_aed,avg_cost_aed,authority) VALUES (?,?,?,?,?,?,?,?,?)",
                (int(row["step_number"]),row["permit_name"],int(row["min_days"]),int(row["max_days"]),int(row["avg_days"]),
                 float(row["min_cost_aed"]),float(row["max_cost_aed"]),float(row["avg_cost_aed"]),row["authority"]))
    conn.commit(); conn.close()

    diagram = """erDiagram
    PERMIT_SEQUENCE {
        int id PK
        int step_number
        string permit_name
        int min_days
        int max_days
        real avg_cost_aed
    }
    APPROVALS {
        int A01_id PK
        string A02_noc_status
        string A04_building_permit_no
    }
    PERMIT_SEQUENCE ||--o{ APPROVALS : "tracked by"
"""
    write_file(d / "diagrams" / "permit_flow.mmd", diagram)
    print(f"  Domain 10 done.")

# ============================================================================
# DOMAIN 11: GEOTECHNICAL
# ============================================================================
def build_domain_11():
    d = BASE / "11_GEOTECHNICAL"
    color, title = COLORS["11"]

    schema = sql_header("11", "Geotechnical & Foundations", color) + """
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
"""
    write_file(d / "schemas" / "11_geotechnical.sql", schema)
    create_db(d, schema, "geotechnical.db")

    # Soil types — tightened values
    csv_soil = """soil_type,bc_min_kpa,bc_max_kpa,bc_typical_kpa,found_type,shoring,shoring_aed_m2,dewatering,dewatering_aed_m2,cost_factor,gw_depth_m,notes
Dense Sand,200,400,300,Shallow/Piles,Sheet Piling,350,Medium,45,1.0,5.0,Common in coastal areas
Medium Sand,150,250,200,Shallow/Piles,Sheet Piling,380,Medium,55,1.1,4.0,Widely distributed
Loose Sand,75,150,112,Piles,Secant Piles,520,High,75,1.3,3.0,Requires pile foundation
Stiff Clay,100,200,150,Shallow/Piles,Diaphragm Wall,650,Low,35,1.2,6.0,Good bearing capacity
Medium Clay,75,150,112,Piles,Secant Piles,580,Medium,65,1.4,5.0,Settlement concerns
Soft Clay,50,100,75,Piles,Diaphragm Wall,890,High,85,1.6,2.0,Poor foundation conditions
Coastal Sabkha,50,100,75,Deep Piles,Diaphragm Wall,1200,Critical,95,1.8,0.5,Very challenging - high sulfate
Fill Material,50,100,75,Piles,Secant Piles,500,High,70,1.5,3.0,Variable quality
Rock,500,5000,2750,Shallow,None,250,Low,15,0.9,10.0,Excellent - minimal shoring
"""
    write_file(d / "data_raw" / "soil_types.csv", csv_soil.strip())

    # Site-specific data
    csv_site = """emirate,area,lat,lon,soil_type,bearing_capacity_kpa,settlement_mm,groundwater_depth_m,sulfate_ppm,chloride_ppm,pile_capacity_kn,foundation_recommendation
Dubai,Downtown,25.1972,55.2744,Dense Sand,350,15,2.5,1200,800,1500,Raft Foundation
Dubai,Marina,25.0781,55.1398,Medium Dense Sand,280,25,1.8,2100,1500,1200,Piled Foundation
Dubai,JVC,25.0456,55.2234,Medium Sand,220,30,3.0,1800,1200,1000,Piled Foundation
Dubai,Dubai Hills,25.1105,55.2567,Stiff Clay,180,20,4.0,900,600,1100,Raft/Piled
Abu Dhabi,Al Reem,24.5014,54.4088,Sabkha,120,50,0.5,3500,2800,800,Deep Piled Foundation
Abu Dhabi,Yas Island,24.4567,54.6012,Medium Clay,150,35,1.5,2200,1800,900,Piled Foundation
Sharjah,Al Mamzar,25.3123,55.3456,Loose Sand,100,40,2.0,1500,1000,700,Deep Piled
Rak,Al Marjan,25.6789,55.9012,Coastal Sabkha,80,55,0.8,4000,3200,600,Deep Piled + Ground Improvement
"""
    write_file(d / "data_raw" / "site_geotechnical.csv", csv_site.strip())

    # Engineering soil properties
    csv_eng_soil = """soil_type,uscs_group,unit_weight_kn_m3,friction_angle_deg,cohesion_kpa,nc,nq,ng,elastic_modulus_mpa,poisson_ratio,classification
Dense Sand,SW,21,38,0,61.35,48.93,78.61,100,0.3,High
Medium Sand,SM,19,33,0,46.12,35.19,48.03,60,0.3,Medium
Loose Sand,SP,17,28,0,31.61,22.46,22.02,25,0.3,Low
Stiff Clay,CH,20,0,100,30.17,18.4,0,80,0.45,Medium
Medium Clay,CL,18,0,50,17.69,11.2,0,40,0.45,Low-Medium
Soft Clay,ML,16,0,25,11.73,7.4,0,15,0.5,Low
Coastal Sabkha,SM-SC,17,25,15,25.21,13.1,7.7,20,0.35,Low
Fill Material,Mixed,16,20,5,11.85,6.4,3.9,10,0.4,Very Low
Rock,Rock,25,45,500,200,150,120,5000,0.2,Very High
"""
    write_file(d / "data_raw" / "engineering_soils.csv", csv_eng_soil.strip())

    conn = sqlite3.connect(str(d / "databases" / "geotechnical.db"))
    cur = conn.cursor()
    cur.execute("DELETE FROM geotechnical_data")
    with open(d / "data_raw" / "soil_types.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("INSERT INTO geotechnical_data (soil_type,bc_min_kpa,bc_max_kpa,bc_typical_kpa,foundation_type,shoring_system,shoring_cost_aed_m2,dewatering_system,dewatering_cost_aed_m2,cost_factor,gw_depth_m,notes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (row["soil_type"],float(row["bc_min_kpa"]),float(row["bc_max_kpa"]),float(row["bc_typical_kpa"]),
                 row["found_type"],row["shoring"],float(row["shoring_aed_m2"]),row["dewatering"],
                 float(row["dewatering_aed_m2"]),float(row["cost_factor"]),float(row["gw_depth_m"]),row["notes"]))
    cur.execute("DELETE FROM site_geotechnical")
    with open(d / "data_raw" / "site_geotechnical.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("INSERT INTO site_geotechnical (emirate,area,lat,lon,soil_type,bearing_capacity_kpa,settlement_mm,groundwater_depth_m,sulfate_ppm,chloride_ppm,pile_capacity_kn,foundation_recommendation) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                (row["emirate"],row["area"],float(row["lat"]),float(row["lon"]),row["soil_type"],
                 float(row["bearing_capacity_kpa"]),float(row["settlement_mm"]),float(row["groundwater_depth_m"]),
                 float(row["sulfate_ppm"]),float(row["chloride_ppm"]),float(row["pile_capacity_kn"]),row["foundation_recommendation"]))
    cur.execute("DELETE FROM engineering_soils")
    with open(d / "data_raw" / "engineering_soils.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("INSERT INTO engineering_soils (soil_type,uscs_group,unit_weight_kn_m3,friction_angle_deg,cohesion_kpa,bearing_capacity_factor_nc,bearing_capacity_factor_nq,bearing_capacity_factor_ng,elastic_modulus_mpa,poisson_ratio,classification) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                (row["soil_type"],row["uscs_group"],float(row["unit_weight_kn_m3"]),float(row["friction_angle_deg"]),
                 float(row["cohesion_kpa"]),float(row["nc"]),float(row["nq"]),float(row["ng"]),
                 float(row["elastic_modulus_mpa"]),float(row["poisson_ratio"]),row["classification"]))
    conn.commit(); conn.close()

    diagram = """erDiagram
    GEOTECHNICAL_DATA {
        int id PK
        string soil_type
        real bc_min_kpa
        real bc_max_kpa
        real shoring_aed_m2
    }
    SITE_GEOTECHNICAL {
        int id PK
        string emirate
        string area
        real bearing_capacity_kpa
        real settlement_mm
    }
    ENGINEERING_SOILS {
        int id PK
        string soil_type
        string uscs_group
        real friction_angle_deg
    }
    GEOTECHNICAL_DATA ||--o{ SITE_GEOTECHNICAL : "applied to"
    GEOTECHNICAL_DATA ||--o{ ENGINEERING_SOILS : "properties of"
"""
    write_file(d / "diagrams" / "soil_profile.mmd", diagram)
    print(f"  Domain 11 done.")

# ============================================================================
# DOMAIN 12: SUSTAINABILITY & QUALITY & BIM
# ============================================================================
def build_domain_12():
    d = BASE / "12_SUSTAINABILITY_QUALITY_BIM"
    color, title = COLORS["12"]

    schema = sql_header("12", "Sustainability, Quality & BIM", color) + """
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
"""
    write_file(d / "schemas" / "12_sustainability.sql", schema)
    create_db(d, schema, "sustainability.db")

    # Risk catalog
    csv_risk = """risk_id,risk_name,category,description,probability_pct,impact_level,risk_score,standard_mitigation
R101,False Float in Schedule,Schedule/Claims,Artificially inflated schedule buffer masks delays,60,80,48,Maintain transparent schedules; conduct independent reviews
R102,Weather Delays (Summer Heat),Environmental,Productivity loss due to extreme summer temperatures,80,60,48,Schedule outdoor work Oct-Apr; provide cooling stations
R103,Material Import Delays,Supply Chain,Delays at port or customs for imported materials,60,70,42,Maintain buffer stock; pre-approve suppliers; source locally
R104,Municipality Approval Delays,Regulatory,Longer than expected time for NOCs and permits,50,60,30,Ensure complete submissions; engage dedicated permits manager
R105,Unexpected Geotechnical Conditions,Technical,Soil conditions differ from initial report,40,90,36,Comprehensive soil investigation; contingency in foundation budget
R106,Material Price Escalation,Financial,Steel/concrete price increases during construction,55,65,36,Lock prices in contracts; include escalation clause
R107,Labor Shortage,Resource,Difficulty in securing skilled labor,45,70,32,Pre-qualify multiple subcontractors; early mobilization
R108,Design Changes Late in Project,Design,Client-initiated changes after construction starts,35,85,30,Firm scope freeze; change order procedures
R109,Currency Fluctuation,Financial,Exchange rate changes affecting imported materials,40,55,22,Hedge currency risk; local sourcing strategy
R110,COVID/Pandemic Disruption,Force Majeure,Work restrictions due to health emergencies,20,90,18,Business continuity plan; remote work protocols
"""
    write_file(d / "data_raw" / "risk_catalog.csv", csv_risk.strip())

    conn = sqlite3.connect(str(d / "databases" / "sustainability.db"))
    cur = conn.cursor()
    cur.execute("DELETE FROM risk_register")
    with open(d / "data_raw" / "risk_catalog.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("INSERT INTO risk_register (risk_id,risk_category,risk_description,probability_pct,impact_level,risk_score,mitigation_action) VALUES (?,?,?,?,?,?,?)",
                (row["risk_id"],row["category"],row["description"],float(row["probability_pct"]),
                 float(row["impact_level"]),float(row["risk_score"]),row["standard_mitigation"]))
    conn.commit(); conn.close()

    diagram = """erDiagram
    SUSTAINABILITY {
        int id PK
        string leed_certification_goal
        real carbon_footprint_target
    }
    QUALITY_MASTER {
        int id PK
        string quality_id
        real first_pass_yield
    }
    RISK_REGISTER {
        int id PK
        string risk_id
        real risk_score
    }
    BIM_MASTER {
        int id PK
        string bim_id
        string lod_requirement
    }
    OMM_MASTER {
        int id PK
        string omm_id
        real operational_budget_aed_year
    }
"""
    write_file(d / "diagrams" / "sustainability_erd.mmd", diagram)
    print(f"  Domain 12 done.")

# ============================================================================
# MASTER INDEX
# ============================================================================
def build_master_index():
    d = BASE
    csv_index = """domain_id,domain_name,domain_name_ar,schema_file,data_files,database_file,color_hex,description
01,Project & Plot,المشروع والأراضي,01_project_plot.sql,project_data.csv,project_plot.db,00b4d8,Project identity plot geometry and master data
02,Location & GIS,الموقع والخرائط,02_location_gis.sql,location_data.csv,location_gis.db,06d6a0,Emirates jurisdictions coordinates and GIS data
03,Stakeholders,أصحاب المصلحة,03_stakeholders.sql,stakeholders_data.csv,stakeholders.db,ffd166,Owner developer contractor consultant registry
04,Zoning & Regulatory,التخطيط والتنظيم,04_zoning_regulatory.sql,far_limits.csv,zoning_regulatory.db,ef476f,FAR height coverage setback limits per emirate
05,Validation & Compliance,المطابقة والتوثيق,05_validation.sql,compliance_data.csv,validation.db,118ab2,Permit compliance checks and SLA tracking
06,Design Parameters,التصميم والمعايير,06_design.sql,cost_indices.csv,design_parameters.db,073b4c,Structural systems facade MEP design parameters
07,Unit Mix & Program,الوحدات والبرامج,07_unit_mix.sql,unit_types.csv,unit_mix.db,8338ec,Unit types areas and program mix
08,Cost & Economics,التكاليف والتحليل المالي,08_cost_economics.sql,csi_cost_codes.csv,cost_economics.db,ff006e,CSI cost codes benchmarks lifecycle costs
09,Schedule & Timeline,الخطة الزمنية,09_schedule.sql,wbs_activities.csv,schedule.db,fb5607,WBS activities durations critical path
10,Approvals & Authorities,الموافقات والسلطات,10_approvals.sql,permit_sequence.csv,approvals.db,3a86ff,14-step permit sequence with timelines and costs
11,Geotechnical,الجيوتقنية والأساسيات,11_geotechnical.sql,soil_types.csv,geotechnical.db,80ed99,Soil types bearing capacity shoring foundations
12,Sustainability & BIM,الاستدامة والجودة,12_sustainability.sql,risk_catalog.csv,sustainability.db,c77dff,LEED Estidama quality risk BIM OMM
"""
    write_file(d / "domain_index.csv", csv_index.strip())

    # Build the Python DB with all domains
    conn = sqlite3.connect(str(d / "DOMAINS.db"))
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS domain_index (domain_id TEXT, domain_name TEXT, domain_name_ar TEXT, schema_file TEXT, data_files TEXT, database_file TEXT, color_hex TEXT, description TEXT)")
    cur.execute("DELETE FROM domain_index")
    with open(d / "domain_index.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cur.execute("INSERT INTO domain_index VALUES (?,?,?,?,?,?,?,?)",
                (row["domain_id"],row["domain_name"],row["domain_name_ar"],row["schema_file"],row["data_files"],row["database_file"],row["color_hex"],row["description"]))
    conn.commit(); conn.close()
    print(f"  Master index done.")

# ============================================================================
# MAIN
# ============================================================================
if __name__ == "__main__":
    print("=" * 60)
    print("PMO DOMAINS BUILDER — 12 Domain Packages")
    print("=" * 60)
    build_domain_01()
    build_domain_02()
    build_domain_03()
    build_domain_04()
    build_domain_05()
    build_domain_06()
    build_domain_07()
    build_domain_08()
    build_domain_09()
    build_domain_10()
    build_domain_11()
    build_domain_12()
    build_master_index()
    print("=" * 60)
    print("ALL 12 DOMAINS BUILT SUCCESSFULLY")
    print("=" * 60)

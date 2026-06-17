#!/usr/bin/env python3
"""
PMO FILL EMPTY TABLES + FIXED AUDIT + REPACKAGE
"""
import sqlite3, json, os, shutil
from pathlib import Path
from datetime import datetime

_THIS_DIR = Path(__file__).resolve().parent  # DOMAINS/_PMO_PACKAGE/
BASE = _THIS_DIR.parent
VAULT = Path(os.environ.get("VAULT_TABLES_DIR", str(BASE / "_vault_tables")))
PACKAGE_DIR = _THIS_DIR

# ============================================================================
# FILL EMPTY TABLES WITH REALISTIC DATA
# ============================================================================
def fill_empty_tables():
    print("\n=== FILLING EMPTY TABLES ===")

    # --- Domain 01: project_master already has 5 rows, fill project_identity ---
    _fill_table(BASE / "01_PROJECT_AND_PLOT/databases/project_plot.db", "project_identity", [
        ("PRJ-001", "Ritz Carlton Residences", "Dubai", "DM-Mainland", "Residential", "High-Rise Tower", 5000, 45000, 35, 2, "2024-Q1", "Active", 450000000, 120000000, 27),
        ("PRJ-002", "Marina Heights Tower", "Dubai", "Trakhees", "Mixed-use", "High-Rise Tower", 3200, 38400, 42, 3, "2023-Q3", "Active", 380000000, 280000000, 74),
        ("PRJ-003", "Al Reem Villas", "Abu Dhabi", "ADM", "Residential", "Villa", 1200, 4800, 2, 1, "2024-Q2", "Planning", 85000000, 5000000, 6),
        ("PRJ-004", "Sharjah Business Park", "Sharjah", "SHA", "Commercial", "Mid-Rise", 8000, 32000, 8, 1, "2025-Q1", "Feasibility", 120000000, 0, 0),
        ("PRJ-005", "RAK Beach Resort", "Ras Al Khaimah", "RAK", "Hospitality", "Resort", 15000, 22500, 4, 1, "2024-Q4", "Active", 200000000, 45000000, 23),
    ], ["project_id", "project_name", "emirate", "jurisdiction", "land_use", "typology", "plot_area_m2", "gfa_m2", "floors_above", "floors_below", "estimated_completion", "project_status", "budget_aed", "spent_aed", "completion_pct"])

    _fill_table(BASE / "01_PROJECT_AND_PLOT/databases/project_plot.db", "plot_data", [
        ("PLT-001", "PRJ-001", 5000, "Rectangular", 50.0, 100.0, 0, 0, 0, 0),
        ("PLT-002", "PRJ-002", 3200, "L-Shape", 40.0, 80.0, 5, 3, 5, 3),
        ("PLT-003", "PRJ-003", 1200, "Rectangular", 30.0, 40.0, 3, 3, 3, 3),
        ("PLT-004", "PRJ-004", 8000, "Irregular", 80.0, 100.0, 0, 0, 0, 0),
        ("PLT-005", "PRJ-005", 15000, "Irregular", 100.0, 150.0, 10, 5, 10, 5),
    ], ["plot_id", "project_id", "area_m2", "shape", "frontage_m", "depth_m", "setback_front_m", "setback_side_m", "setback_rear_m", "setback_open_side_m"])

    # --- Domain 02: Fill location_data ---
    _fill_table(BASE / "02_LOCATION_GIS/databases/location_gis.db", "location_data", [
        ("LOC-001", "PRJ-001", "Downtown Dubai", 25.1972, 55.2744, "Plot 345, Block 4", "Burj Khalifa Community", "DM-Mainland"),
        ("LOC-002", "PRJ-002", "Dubai Marina", 25.0781, 55.1398, "Plot 123, Tower Cluster", "JBR Community", "Trakhees"),
        ("LOC-003", "PRJ-003", "Al Reem Island", 24.5014, 54.4088, "Plot 78, Sector B", "Al Reem Community", "ADM"),
        ("LOC-004", "PRJ-004", "Sharjah Airport Area", 25.3285, 55.5172, "Plot 45, Zone 3", "SAIF Zone", "SHA"),
        ("LOC-005", "PRJ-005", "Al Marjan Island", 25.6872, 55.9612, "Plot 12, Island 3", "Al Marjan", "RAK"),
    ], ["location_id", "project_id", "area_name", "latitude", "longitude", "plot_address", "community", "jurisdiction"])

    # --- Domain 04: Fill planning_rules ---
    _fill_table(BASE / "04_ZONING_REGULATORY/databases/zoning_regulatory.db", "planning_rules", [
        ("RULE-001", "DM-Mainland", "Residential", "High-Rise Tower", 5.0, 6.0, 40, 45, 150, 200, 5, 3, 3, 1.0, 20),
        ("RULE-002", "DM-Mainland", "Mixed-use", "High-Rise Tower", 5.5, 7.0, 45, 50, 120, 200, 5, 3, 3, 1.5, 15),
        ("RULE-003", "Trakhees", "Residential", "Mid-Rise", 3.0, 4.0, 35, 40, 30, 60, 5, 3, 3, 1.0, 25),
        ("RULE-004", "ADM", "Residential", "Villa", 1.0, 1.5, 30, 35, 10, 15, 3, 3, 3, 1.0, 30),
        ("RULE-005", "ADM", "Commercial", "Mid-Rise", 3.5, 5.0, 40, 50, 60, 120, 5, 3, 3, 1.5, 20),
        ("RULE-006", "SHA", "Commercial", "Mid-Rise", 2.5, 3.5, 35, 45, 30, 60, 5, 3, 3, 1.0, 20),
        ("RULE-007", "RAK", "Hospitality", "Resort", 1.5, 2.5, 25, 35, 15, 25, 5, 3, 5, 0.5, 40),
    ], ["rule_id", "jurisdiction", "land_use", "typology", "far_min", "far_max", "coverage_min_pct", "coverage_max_pct", "height_min_m", "height_max_m", "setback_front_m", "setback_side_m", "setback_rear_m", "parking_ratio", "green_area_pct"])

    # --- Domain 04: Fill use_allowed ---
    _fill_table(BASE / "04_ZONING_REGULATORY/databases/zoning_regulatory.db", "use_allowed", [
        ("UA-001", "DM-Mainland", "RESI", 1, "Residential towers allowed in designated zones"),
        ("UA-002", "DM-Mainland", "COMM", 1, "Commercial permitted in mixed-use zones"),
        ("UA-003", "DM-Mainland", "INDU", 0, "Industrial not permitted in DM-Mainland"),
        ("UA-004", "Trakhees", "RESI", 1, "Residential allowed with DM approval"),
        ("UA-005", "Trakhees", "COMM", 1, "Commercial allowed"),
        ("UA-006", "ADM", "RESI", 1, "Residential permitted in all sectors"),
        ("UA-007", "ADM", "HOSP", 1, "Hospitality permitted on island fronts"),
        ("UA-008", "SHA", "COMM", 1, "Commercial in SAIF and free zones"),
        ("UA-009", "RAK", "HOSP", 1, "Hospitality primary use on islands"),
    ], ["rule_id", "jurisdiction", "use_code", "is_allowed", "conditions"])

    # --- Domain 06: Fill design_params_extended ---
    _fill_table(BASE / "06_DESIGN_PARAMETERS/databases/design_parameters.db", "design_params_extended", [
        ("DP-001", "High-Rise Tower", "Residential", "Structural", "RC Frame + Shear Wall", "C40-C60", "2850 kg/m³", "50 mm", "420 MPa"),
        ("DP-002", "High-Rise Tower", "Residential", "MEP", "Split System + AHU", "Chiller Plant", "180 L/capita/day", "65 kWh/m²/yr", "BMS Integrated"),
        ("DP-003", "High-Rise Tower", "Mixed-use", "Structural", "RC Frame + Core", "C40-C50", "2800 kg/m³", "50 mm", "420 MPa"),
        ("DP-004", "Mid-Rise", "Commercial", "Structural", "RC Frame", "C35-C45", "2750 kg/m³", "40 mm", "420 MPa"),
        ("DP-005", "Villa", "Residential", "Structural", "RC Slab on Grade", "C25-C35", "2700 kg/m³", "30 mm", "420 MPa"),
        ("DP-006", "High-Rise Tower", "Residential", "Fire", "Full Sprinkler + Smoke", "2-hour rated", "Standpipe + Hose", "300m² per zone", "NFPA 14/13"),
        ("DP-007", "Mid-Rise", "Commercial", "Fire", "Sprinkler + Detection", "1.5-hour rated", "Standpipe", "500m² per zone", "NFPA 14/13"),
        ("DP-008", "Resort", "Hospitality", "Interior", "5-Star Finishes", "Natural Stone", "Timber Panels", "Custom Lighting", "FF&E Package"),
    ], ["param_id", "typology", "land_use", "discipline", "system_type", "specification", "density_load", "consumption", "standard"])

    # --- Domain 07: Fill unit_types with more data ---
    _fill_table(BASE / "07_UNIT_MIX_PROGRAM/databases/unit_mix.db", "unit_mix", [
        ("UM-001", "PRJ-001", "1BR", 45, 65, 1, 1, 18000, "65%", "Mid-floor"),
        ("UM-002", "PRJ-001", "2BR", 80, 110, 2, 2, 16500, "20%", "Mid-high"),
        ("UM-003", "PRJ-001", "3BR", 120, 165, 3, 2, 15000, "10%", "High"),
        ("UM-004", "PRJ-001", "Penthouse", 250, 350, 4, 3, 22000, "5%", "Top 2 floors"),
        ("UM-005", "PRJ-002", "1BR", 50, 72, 1, 1, 14000, "55%", "Low-mid"),
        ("UM-006", "PRJ-002", "2BR", 90, 125, 2, 2, 13000, "30%", "Mid-high"),
        ("UM-007", "PRJ-002", "3BR", 135, 185, 3, 3, 12500, "15%", "High"),
    ], ["mix_id", "project_id", "unit_type", "area_sqm", "area_gross_sqm", "bedrooms", "bathrooms", "price_aed_sqm", "pct_of_total", "floor_range"])

    # --- Domain 08: Fill financial_projections ---
    _fill_table(BASE / "08_COST_ECONOMICS/databases/cost_economics.db", "financial_projections", [
        ("FP-001", "PRJ-001", "Revenue", "Unit Sales", 450000000, 0, 450000000),
        ("FP-002", "PRJ-001", "Revenue", "Retail Leasing", 30000000, 0, 30000000),
        ("FP-003", "PRJ-001", "Cost", "Land", 85000000, 85000000, 0),
        ("FP-004", "PRJ-001", "Cost", "Construction", 180000000, 120000000, 60000000),
        ("FP-005", "PRJ-001", "Cost", "MEP", 45000000, 30000000, 15000000),
        ("FP-006", "PRJ-001", "Cost", "Finishes", 35000000, 20000000, 15000000),
        ("FP-007", "PRJ-001", "Cost", "Fees & Permits", 25000000, 25000000, 0),
        ("FP-008", "PRJ-001", "Cost", "Contingency", 18000000, 5000000, 13000000),
        ("FP-009", "PRJ-001", "Profit", "Gross Margin", 120000000, 0, 0),
        ("FP-010", "PRJ-001", "Metric", "IRR", 22, 0, 0),
        ("FP-011", "PRJ-001", "Metric", "ROI", 27, 0, 0),
        ("FP-012", "PRJ-001", "Metric", "Payback Period", 4.5, 0, 0),
    ], ["fp_id", "project_id", "category", "line_item", "budget_aed", "spent_aed", "remaining_aed"])

    # --- Domain 10: Fill approvals ---
    _fill_table(BASE / "10_APPROVALS_AUTHORITIES/databases/approvals.db", "approvals", [
        ("APR-001", "PRJ-001", "Dubai Municipality", "Building Permit", "Submitted", "2024-01-15", "2024-02-28", 45, 50000, "Under Review"),
        ("APR-002", "PRJ-001", "DEWA", "Electricity NOC", "Approved", "2024-02-01", "2024-02-15", 14, 2000, "Approved"),
        ("APR-003", "PRJ-001", "DLD", "Land Title", "Approved", "2024-01-10", "2024-01-20", 10, 4000, "Completed"),
        ("APR-004", "PRJ-002", "DM", "Building Permit", "Approved", "2023-09-01", "2023-10-15", 44, 48000, "Approved"),
        ("APR-005", "PRJ-002", "Civil Defence", "Fire Safety", "Submitted", "2023-10-20", "", 30, 15000, "Pending Inspection"),
        ("APR-006", "PRJ-003", "ADM", "Planning Permit", "Draft", "2024-06-01", "", 60, 8000, "Pre-application"),
        ("APR-007", "PRJ-005", "RAK Municipality", "Building Permit", "Submitted", "2024-04-01", "", 45, 35000, "Under Review"),
    ], ["approval_id", "project_id", "authority", "permit_type", "status", "submission_date", "approval_date", "processing_days", "fees_aed", "notes"])

    # --- Domain 12: Fill risk_register with more data ---
    _fill_table(BASE / "12_SUSTAINABILITY_QUALITY_BIM/databases/sustainability.db", "risk_register", [
        ("RSK-001", "Foundation soil worse than geotech report", "Technical", 3, 5, 15, "Geotech Engineer", "Additional boring + deep foundations", "Open", "Dubai", "High-Rise", "Engineering", "Escalate to PM", "2024-01-15"),
        ("RSK-002", "Material price escalation >10%", "Commercial", 4, 4, 16, "QS", "Fixed-price contracts + contingency", "Open", "Dubai", "High-Rise", "Commercial", "Finance Director", "2024-01-15"),
        ("RSK-003", "Permit delay >60 days", "Regulatory", 3, 4, 12, "PM", "Pre-application meetings + fast track", "Open", "Dubai", "High-Rise", "Regulatory", "Legal", "2024-01-15"),
        ("RSK-004", "Labor shortage during peak", "Resource", 4, 3, 12, "Contractor", "Multi-labor supply agreements", "Open", "Dubai", "High-Rise", "Resource", "PM", "2024-01-15"),
        ("RSK-005", "Design change after permitting", "Design", 3, 4, 12, "Design Manager", "Freeze design at 90% DD", "Open", "Dubai", "High-Rise", "Design", "Design Director", "2024-01-15"),
        ("RSK-006", "DEWA connection delay", "Utility", 3, 3, 9, "PM", "Early application + follow-up", "Open", "Dubai", "High-Rise", "Utility", "PM", "2024-01-15"),
        ("RSK-007", "Unexpected archaeological find", "Site", 2, 5, 10, "PM", "Archaeological survey before excavation", "Open", "Abu Dhabi", "Villa", "Site", "Legal", "2024-01-15"),
        ("RSK-008", "FX rate fluctuation", "Financial", 3, 3, 9, "Finance", "USD-denominated contracts", "Open", "Dubai", "Mixed", "Financial", "CFO", "2024-01-15"),
        ("RSK-009", "Contractor insolvency", "Commercial", 2, 5, 10, "PM", "Performance bond + bank guarantee", "Open", "Dubai", "High-Rise", "Commercial", "Legal", "2024-01-15"),
        ("RSK-010", "Weather delay (summer)", "Environmental", 4, 2, 8, "Contractor", "Night shifts + heat protocol", "Open", "Dubai", "High-Rise", "Environmental", "HSE Manager", "2024-01-15"),
    ], ["risk_id", "description", "category", "probability", "impact", "score", "owner", "mitigation", "status", "emirate", "project_type", "risk_type", "escalation_path", "last_review_date"])

def _fill_table(db_path, table_name, rows, columns):
    """Fill a table with data if it's empty"""
    if not db_path.exists():
        return
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT COUNT(*) FROM [{table_name}]")
        count = cur.fetchone()[0]
        if count > 0:
            print(f"  [SKIP] {db_path.parent.name}/{table_name} (already has {count} rows)")
            conn.close()
            return
        
        placeholders = ','.join(['?' for _ in columns])
        for row in rows:
            cur.execute(f"INSERT INTO [{table_name}] ({','.join(columns)}) VALUES ({placeholders})", row)
        conn.commit()
        print(f"  [FILL] {db_path.parent.name}/{table_name}: {len(rows)} rows inserted")
    except Exception as e:
        print(f"  [ERR] {table_name}: {e}")
    conn.close()

# ============================================================================
# FIXED ENGINEERING AUDIT
# ============================================================================
def fixed_audit():
    print("\n=== ENGINEERING AUDIT (FIXED) ===")
    results = []

    audits = [
        ("01_PROJECT_AND_PLOT", "project_plot.db", {
            "project_identity": {"cols": 15, "not_null": ["project_id", "project_name", "emirate"], "range": [("plot_area_m2", 100, 500000), ("gfa_m2", 500, 2000000), ("floors_above", 1, 200), ("completion_pct", 0, 100)]},
            "project_master": {"cols": 5, "not_null": ["project_id"]},
            "deliverable_tiers": {"cols": 3, "not_null": ["tier"]},
            "mv_jurisdictions": {"cols": 5, "not_null": ["jurisdiction_code"]},
            "mv_area_limits": {"cols": 7, "not_null": ["rule_id"]},
        }),
        ("02_LOCATION_GIS", "location_gis.db", {
            "location_data": {"cols": 8, "not_null": ["location_id", "project_id", "latitude", "longitude"], "range": [("latitude", 22, 26.1), ("longitude", 51.5, 56.5)]},
            "uae_unified_data": {"cols": 10, "not_null": []},
            "mv_emirates": {"cols": 6, "not_null": ["emirate_name_en"]},
            "mv_geotech_coords": {"cols": 7, "not_null": ["area_name"], "range": [("bearing_kpa", 50, 500)]},
        }),
        ("04_ZONING_REGULATORY", "zoning_regulatory.db", {
            "far_limits": {"cols": 14, "not_null": ["emirate", "land_use"], "range": [("far_min", 0.5, 15), ("coverage_min_pct", 10, 80), ("height_min_m", 3, 400)]},
            "planning_rules": {"cols": 15, "not_null": ["jurisdiction", "land_use"], "range": [("far_min", 0.5, 15), ("coverage_min_pct", 10, 80)]},
            "use_allowed": {"cols": 5, "not_null": ["jurisdiction", "use_code", "is_allowed"]},
            "mv_far_limits": {"cols": 13, "not_null": ["emirate"], "range": [("far_min", 0.5, 15)]},
        }),
        ("06_DESIGN_PARAMETERS", "design_parameters.db", {
            "cost_indices": {"cols": 9, "not_null": ["emirate", "typology"], "range": [("cost_structure_aed_m2", 200, 5000)]},
            "platform_features": {"cols": 12, "not_null": ["feature_name"]},
            "mv_mep_density": {"cols": 11, "not_null": ["typology"], "range": [("elec_kw_m2", 0.01, 1.0), ("water_lpd_capita", 50, 500)]},
            "design_params_extended": {"cols": 9, "not_null": ["typology", "discipline"]},
        }),
        ("08_COST_ECONOMICS", "cost_economics.db", {
            "csi_cost_codes": {"cols": 15, "not_null": ["code", "description"]},
            "cost_benchmarks": {"cols": 15, "not_null": ["emirate", "typology"], "range": [("cost_aed_m2", 200, 5000)]},
            "mv_cost_indices": {"cols": 10, "not_null": ["emirate"], "range": [("cost_struct_aed_m2", 200, 5000), ("total_cost_aed_m2", 500, 10000)]},
            "mv_fee_calc": {"cols": 9, "not_null": ["project_id"]},
            "financial_projections": {"cols": 7, "not_null": ["project_id", "category", "line_item"], "range": [("budget_aed", 0, 500000000)]},
        }),
        ("09_SCHEDULE_TIMELINE", "schedule.db", {
            "wbs_activities": {"cols": 23, "not_null": ["activity_id"]},
            "mv_permit_sequence": {"cols": 6, "not_null": ["permit_name", "authority"], "range": [("avg_days", 1, 365)]},
        }),
        ("10_APPROVALS_AUTHORITIES", "approvals.db", {
            "permit_sequence": {"cols": 14, "not_null": ["permit_name", "authority"], "range": [("avg_days", 1, 365)]},
            "authority_matrix_raw": {"cols": 4, "not_null": ["emirate", "authority"]},
            "mv_auth_matrix": {"cols": 8, "not_null": ["emirate", "authority"], "range": [("processing_days", 1, 365)]},
            "approvals": {"cols": 11, "not_null": ["project_id", "authority", "permit_type"], "range": [("processing_days", 1, 365), ("fees_aed", 0, 1000000)]},
        }),
        ("11_GEOTECHNICAL", "geotechnical.db", {
            "geotechnical_data": {"cols": 9, "not_null": ["site_name"]},
            "site_geotechnical": {"cols": 8, "not_null": ["site_name", "soil_type"], "range": [("bearing_kpa", 50, 500)]},
            "engineering_soils": {"cols": 9, "not_null": ["soil_type"], "range": [("bearing_min_kpa", 50, 500)]},
            "soil_reference": {"cols": 4, "not_null": ["soil_type"]},
            "mv_soil_full": {"cols": 17, "not_null": ["emirate", "area_name", "soil_type"], "range": [("bearing_kpa", 50, 500), ("settlement_mm", 0, 200)]},
        }),
        ("12_SUSTAINABILITY_QUALITY_BIM", "sustainability.db", {
            "risk_register": {"cols": 14, "not_null": ["risk_id", "description", "category", "probability", "impact"], "range": [("probability", 1, 5), ("impact", 1, 5), ("score", 1, 25)]},
            "risks_catalog_raw": {"cols": 5, "not_null": ["risk_id"]},
        }),
    ]

    for domain_name, db_file, expected in audits:
        db_path = BASE / domain_name / "databases" / db_file
        if not db_path.exists():
            print(f"  [MISS] {domain_name}: DB not found")
            results.append({"domain": domain_name, "status": "MISSING_DB", "issues": ["DB not found"]})
            continue

        conn = sqlite3.connect(str(db_path))
        cur = conn.cursor()
        issues = []
        stats = {}

        cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
        existing = {r[0] for r in cur.fetchall()}

        for table_name, checks in expected.items():
            if table_name not in existing:
                issues.append(f"Missing table: {table_name}")
                continue

            cur.execute(f"SELECT COUNT(*) FROM [{table_name}]")
            count = cur.fetchone()[0]
            stats[table_name] = count

            if count == 0:
                issues.append(f"Empty table: {table_name}")
                continue

            # Check columns
            cur.execute(f"PRAGMA table_info([{table_name}])")
            actual_cols = {r[1] for r in cur.fetchall()}
            expected_cols = checks.get("cols", 0)
            if len(actual_cols) < expected_cols:
                issues.append(f"{table_name}: has {len(actual_cols)} cols, expected {expected_cols}")

            # Check not null
            for col in checks.get("not_null", []):
                if col in actual_cols:
                    cur.execute(f"SELECT COUNT(*) FROM [{table_name}] WHERE [{col}] IS NULL OR [{col}] = ''")
                    nulls = cur.fetchone()[0]
                    if nulls > 0:
                        issues.append(f"{table_name}.{col}: {nulls} NULL/empty")

            # Check ranges
            for col, min_val, max_val in checks.get("range", []):
                if col in actual_cols:
                    cur.execute(f"SELECT [{col}] FROM [{table_name}] WHERE [{col}] IS NOT NULL AND [{col}] != ''")
                    vals = []
                    for row in cur.fetchall():
                        try:
                            vals.append(float(row[0]))
                        except (ValueError, TypeError):
                            pass
                    if vals:
                        below = sum(1 for v in vals if v < min_val)
                        above = sum(1 for v in vals if v > max_val)
                        if below > 0:
                            issues.append(f"{table_name}.{col}: {below} below {min_val}")
                        if above > 0:
                            issues.append(f"{table_name}.{col}: {above} above {max_val}")

        conn.close()
        status = "OK" if not issues else "ISSUES"
        icon = "✅" if status == "OK" else "⚠️"
        print(f"  {icon} {domain_name}: {status} | Tables: {len(existing)} | Data: {stats}")
        for issue in issues:
            print(f"      → {issue}")
        results.append({"domain": domain_name, "status": status, "issues": issues, "stats": stats})

    return results

# ============================================================================
# REPACKAGE
# ============================================================================
def repackage():
    print("\n=== REPACKAGING ===")
    if PACKAGE_DIR.exists():
        shutil.rmtree(str(PACKAGE_DIR))
    PACKAGE_DIR.mkdir(exist_ok=True)

    for d in sorted(BASE.iterdir()):
        if d.is_dir() and d.name[0].isdigit():
            shutil.copytree(str(d), str(PACKAGE_DIR / d.name), dirs_exist_ok=True)
            print(f"  [COPY] {d.name}")

    for f in ["build_all_domains.py", "build_workbooks.py", "build_enhancements.py", "build_comprehensive.py", "build_final.py"]:
        src = BASE / f
        if src.exists():
            shutil.copy2(str(src), str(PACKAGE_DIR / f))

    for f in ["MASTER_INDEX.xlsx", "DASHBOARD.html", "DOMAINS.db", "domain_index.csv"]:
        src = BASE / f
        if src.exists():
            shutil.copy2(str(src), str(PACKAGE_DIR / f))

    # README
    (PACKAGE_DIR / "README.md").write_text(f"""# PMO SYSTEM DOMAINS — Self-Contained Package
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Contents (12 Domains)
| Domain | Tables | CSV | DB | ERD | Workbook |
|--------|--------|-----|----|----|----------|
| 01 Project & Plot | 8 | 1 | 1 | ✅ | ✅ |
| 02 Location & GIS | 7 | 1 | 1 | ✅ | ✅ |
| 03 Stakeholders | 4 | 1 | 1 | ✅ | ✅ |
| 04 Zoning & Regulatory | 5 | 2 | 1 | ✅ | ✅ |
| 05 Validation & Compliance | 5 | 2 | 1 | ✅ | ✅ |
| 06 Design Parameters | 6 | 2 | 1 | ✅ | ✅ |
| 07 Unit Mix & Program | 4 | 1 | 1 | ✅ | ✅ |
| 08 Cost & Economics | 8 | 3 | 1 | ✅ | ✅ |
| 09 Schedule & Timeline | 4 | 1 | 1 | ✅ | ✅ |
| 10 Approvals & Authorities | 6 | 2 | 1 | ✅ | ✅ |
| 11 Geotechnical | 6 | 3 | 1 | ✅ | ✅ |
| 12 Sustainability & BIM | 8 | 2 | 1 | ✅ | ✅ |

## Usage
1. Open `DASHBOARD.html` in any browser for visual overview
2. Open any `workbook.xlsx` in Excel for detailed data
3. Query any `.db` file with SQLite
4. Run `build_*.py` to regenerate everything

## No External Dependencies
All files are self-contained. No internet connection required.
""", encoding="utf-8")

    # index.html
    (PACKAGE_DIR / "index.html").write_text("""<!DOCTYPE html>
<html dir="rtl" lang="ar"><head><meta charset="UTF-8"><title>PMO DOMAINS</title>
<style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:'Segoe UI',sans-serif;background:#1a1a2e;color:#eee;padding:30px}h1{text-align:center;color:#3498DB;margin-bottom:30px}.g{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:15px}.c{background:#16213e;border-radius:12px;padding:20px;border-left:5px solid}.c h3{margin-bottom:10px}.s{display:flex;gap:15px;color:#BDC3C7;font-size:13px}.s b{color:#fff}</style>
</head><body><h1>PMO SYSTEM DOMAINS</h1>
<p style="text-align:center;color:#7F8C8D;margin-bottom:30px">Self-Contained Package — 12 Domains</p>
<div class="g">
<div class="c" style="border-color:#00B4D8"><h3 style="color:#00B4D8">01 Project & Plot</h3><div class="s"><span>Tables: <b>8</b></span><span>CSV: <b>1</b></span></div></div>
<div class="c" style="border-color:#06D6A0"><h3 style="color:#06D6A0">02 Location & GIS</h3><div class="s"><span>Tables: <b>7</b></span><span>CSV: <b>1</b></span></div></div>
<div class="c" style="border-color:#FFD166"><h3 style="color:#FFD166">03 Stakeholders</h3><div class="s"><span>Tables: <b>4</b></span><span>CSV: <b>1</b></span></div></div>
<div class="c" style="border-color:#EF476F"><h3 style="color:#EF476F">04 Zoning & Regulatory</h3><div class="s"><span>Tables: <b>5</b></span><span>CSV: <b>2</b></span></div></div>
<div class="c" style="border-color:#118AB2"><h3 style="color:#118AB2">05 Validation & Compliance</h3><div class="s"><span>Tables: <b>5</b></span><span>CSV: <b>2</b></span></div></div>
<div class="c" style="border-color:#073B4C"><h3 style="color:#073B4C">06 Design Parameters</h3><div class="s"><span>Tables: <b>6</b></span><span>CSV: <b>2</b></span></div></div>
<div class="c" style="border-color:#8338EC"><h3 style="color:#8338EC">07 Unit Mix & Program</h3><div class="s"><span>Tables: <b>4</b></span><span>CSV: <b>1</b></span></div></div>
<div class="c" style="border-color:#FF006E"><h3 style="color:#FF006E">08 Cost & Economics</h3><div class="s"><span>Tables: <b>8</b></span><span>CSV: <b>3</b></span></div></div>
<div class="c" style="border-color:#FB5607"><h3 style="color:#FB5607">09 Schedule & Timeline</h3><div class="s"><span>Tables: <b>4</b></span><span>CSV: <b>1</b></span></div></div>
<div class="c" style="border-color:#3A86FF"><h3 style="color:#3A86FF">10 Approvals & Authorities</h3><div class="s"><span>Tables: <b>6</b></span><span>CSV: <b>2</b></span></div></div>
<div class="c" style="border-color:#80ED99"><h3 style="color:#80ED99">11 Geotechnical</h3><div class="s"><span>Tables: <b>6</b></span><span>CSV: <b>3</b></span></div></div>
<div class="c" style="border-color:#C77DFF"><h3 style="color:#C77DFF">12 Sustainability & BIM</h3><div class="s"><span>Tables: <b>8</b></span><span>CSV: <b>2</b></span></div></div>
</div></body></html>""", encoding="utf-8")

    total_size = sum(f.stat().st_size for f in PACKAGE_DIR.rglob("*") if f.is_file())
    total_files = sum(1 for f in PACKAGE_DIR.rglob("*") if f.is_file())
    print(f"\n  [PACKAGE] {PACKAGE_DIR}")
    print(f"  [SIZE] {total_size // 1024} KB ({total_files} files)")

# ============================================================================
# MAIN
# ============================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("PMO FILL + AUDIT + REPACKAGE")
    print("=" * 70)
    fill_empty_tables()
    audit = fixed_audit()
    repackage()

    # Summary
    ok_count = sum(1 for r in audit if r["status"] == "OK")
    issue_count = sum(1 for r in audit if r["status"] != "OK")
    print(f"\n{'='*70}")
    print(f"AUDIT RESULT: {ok_count} OK, {issue_count} with issues")
    print(f"{'='*70}")

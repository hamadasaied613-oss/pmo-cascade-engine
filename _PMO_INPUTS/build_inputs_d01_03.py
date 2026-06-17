#!/usr/bin/env python3
"""Input Templates: Domain 01-03. Each field shows its source."""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))

def nb(cells):
    return {"nbformat": 4, "nbformat_minor": 0,
            "metadata": {"colab": {"provenance": []},
                         "kernelspec": {"name": "python3", "display_name": "Python 3"},
                         "language_info": {"name": "python"}},
            "cells": cells}

def md(s):
    return {"cell_type": "markdown", "metadata": {}, "source": s.split("\n")}

def code(s):
    return {"cell_type": "code", "metadata": {}, "source": s.split("\n"),
            "outputs": [], "execution_count": None}

def save(path, cells):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(nb(cells), f, indent=2)

D01 = os.path.join(BASE, "DOMAIN_01_PROJECT")

# ══════════════════════════════════════════════════════════════════════════════
# INPUT 01: Client Brief Input
# ══════════════════════════════════════════════════════════════════════════════
save(os.path.join(D01, "INPUT_01_Client_Brief.ipynb"), [
    md("# INPUT: Client Brief\n---\n**Output Destination:** Client Brief Template (Domain 01)\n**Methodology:** RIBA Stage 0, PMBOK Requirements\n**ISO:** ISO 21500:2012\n\n## Purpose\nCollect all client requirements and project vision before any design or planning activity.\n\n## Source Legend\n| Symbol | Meaning |\n|--------|---------|\n| **[ABS]** | Absolute input - Client provides directly |\n| **[REF]** | Reference from previous document |\n| **[DER]** | Derived/calculated from other inputs |\n| **[STD]** | Standard/default value (no input needed) |\n| **[ACT]** | Output from a previous activity |\n\n## Flow: INPUT → ACTIVITY → OUTPUT\n**INPUT:** This template → **ACTIVITY:** Design Brief Matrix processing → **OUTPUT:** Client Brief template"),
    code("""# CLIENT BRIEF INPUT TEMPLATE
print("=" * 70)
print("INPUT TEMPLATE: CLIENT BRIEF")
print("Output Destination: Domain 01 - Client Brief")
print("=" * 70)
print("")

inputs = [
    ("Project Name", "[ABS] Client provides", "Client", "Project Charter"),
    ("Project Vision", "[ABS] Client provides", "Client", "Project Charter"),
    ("Client Name", "[ABS] Client provides", "Client", "Project Charter"),
    ("Client Contact", "[ABS] Client provides", "Client", "Project Charter"),
    ("Client Organization", "[ABS] Client provides", "Client", "Project Charter"),
    ("Project Type", "[ABS] Client provides", "Client", "Project Charter"),
    ("Project Location", "[ABS] Client provides", "Client", "Site Analysis"),
    ("Plot Number", "[ABS] Client provides", "Client", "Site Analysis"),
    ("Plot Area (m2)", "[ABS] Client provides", "Client/DLD", "Plot Analysis"),
    ("GFA (m2)", "[ABS] Client provides", "Client", "Feasibility Report"),
    ("Budget Range (AED)", "[ABS] Client provides", "Client", "Feasibility Report"),
    ("Target Completion", "[ABS] Client provides", "Client", "Master Program"),
    ("Quality Tier", "[ABS] Client provides", "Client", "Design Parameters"),
    ("Target Market", "[ABS] Client provides", "Client", "Market Analysis"),
    ("Number of Units", "[ABS] Client provides", "Client", "Unit Mix"),
    ("Special Requirements", "[ABS] Client provides", "Client", "Design Brief"),
    ("Sustainability Target", "[ABS] Client provides", "Client", "Estidama/LEED"),
    ("Branding Requirements", "[ABS] Client provides", "Client", "Design Parameters"),
    ("Handover Date", "[ABS] Client provides", "Client", "Master Program"),
    ("Phasing Requirements", "[ABS] Client provides", "Client", "Master Program"),
]

print("INPUT FIELD                    SOURCE                      WHERE FROM         FEEDS TO")
print("-" * 90)
for inp in inputs:
    print(f"  {inp[0]:<32} {inp[1]:<27} {inp[2]:<17} {inp[3]}")

print("")
print("=" * 70)
print("DATA ENTRY CELLS:")
print("  Fill each field above. The SOURCE column tells you:")
print("  - [ABS]: Enter directly from client discussion/contract")
print("  - [REF]: Look up from referenced document")
print("  - [DER]: Will be calculated automatically")
print("  - [STD]: Use standard default value")
print("  - [ACT]: Will be filled by another process first")
print("=" * 70)
print("")
print("VALIDATION RULES:")
print("  - Plot Area > 0")
print("  - Budget Range: min < max")
print("  - Target Completion > today")
print("  - Project Type must be from approved list")
print("  - Location must be valid Qatar/UAE address")
print("")
print("OUTPUT FIELDS (auto-populated from inputs):")
print("  - Brief Reference Number: AUTO-GENERATED")
print("  - Date Prepared: TODAY")
print("  - Prepared By: CURRENT USER")
print("  - Version: 1.0")
print("  - Status: DRAFT")
"""),
])

# ══════════════════════════════════════════════════════════════════════════════
# INPUT 02: Project Charter Input
# ══════════════════════════════════════════════════════════════════════════════
save(os.path.join(D01, "INPUT_02_Project_Charter.ipynb"), [
    md("# INPUT: Project Charter\n---\n**Output Destination:** Project Charter Template (Domain 01)\n**Methodology:** PMI-PMBOK Section 4.1\n**ISO:** ISO 21500:2012\n\n## Purpose\nDefine project authorization, high-level scope, and constraints.\n\n## Source Legend\n| Symbol | Meaning |\n|--------|---------|\n| **[ABS]** | Absolute input - Client provides directly |\n| **[REF]** | Reference from previous document |\n| **[DER]** | Derived/calculated from other inputs |\n| **[STD]** | Standard/default value |\n| **[ACT]** | Output from a previous activity |\n\n## Flow\n**INPUT:** Client Brief → **THIS INPUT** → **ACTIVITY:** Charter Processing → **OUTPUT:** Project Charter"),
    code("""# PROJECT CHARTER INPUT TEMPLATE
print("=" * 70)
print("INPUT TEMPLATE: PROJECT CHARTER")
print("Output Destination: Domain 01 - Project Charter")
print("=" * 70)
print("")

inputs = [
    ("Project Name", "[REF] From Client Brief", "INPUT_01", "Client Brief"),
    ("Project Manager", "[ABS] Client/PMO assigns", "Client/PMO", "Stakeholder Register"),
    ("Sponsor", "[ABS] Client provides", "Client", "Stakeholder Register"),
    ("Business Case", "[REF] From Feasibility Report", "INPUT_03", "Feasibility Report"),
    ("High-Level Scope", "[ABS] Client + PM defines", "Client/PM", "Design Brief"),
    ("Deliverables", "[ABS] PM defines", "PM", "Master Program"),
    ("Milestones", "[DER] From Master Program", "ACT-MasterProgram", "Master Program"),
    ("Budget (High-Level)", "[REF] From Client Brief", "INPUT_01", "Client Brief"),
    ("Timeline (High-Level)", "[ABS] Client provides", "Client", "Master Program"),
    ("Constraints", "[ABS] PM + Client define", "Client/PM", "Risk Register"),
    ("Assumptions", "[ABS] PM + Client define", "Client/PM", "Risk Register"),
    ("Success Criteria", "[ABS] Client defines", "Client", "Feasibility Report"),
    ("Authority Level", "[ABS] Client defines", "Client", "RACI Matrix"),
    ("Risk Tolerance", "[ABS] Client defines", "Client", "Risk Register"),
    ("Change Control", "[STD] PMI-PMBOK process", "STD", "Change Management"),
    ("Approvals Required", "[ABS] Client defines", "Client", "Authority Matrix"),
]

print("INPUT FIELD                    SOURCE                      WHERE FROM         FEEDS TO")
print("-" * 90)
for inp in inputs:
    print(f"  {inp[0]:<32} {inp[1]:<27} {inp[2]:<17} {inp[3]}")

print("")
print("=" * 70)
print("DATA ENTRY CELLS:")
print("  Fill each field. SOURCE column explains data origin:")
print("  - [ABS]: Enter from client discussions")
print("  - [REF]: Reference from named document (see WHERE FROM)")
print("  - [DER]: Auto-calculated from activity output")
print("  - [STD]: Standard value applied automatically")
print("  - [ACT]: Filled by another process first")
print("=" * 70)
print("")
print("VALIDATION RULES:")
print("  - Project Manager must be registered user")
print("  - Sponsor must be senior management")
print("  - Budget must match Client Brief range")
print("  - Timeline must be realistic (min 6 months)")
print("")
print("OUTPUT FIELDS (auto-populated):")
print("  - Charter Reference: AUTO-GENERATED")
print("  - Approval Date: SIGN-OFF DATE")
print("  - Version: 1.0")
print("  - Status: PENDING APPROVAL")
"""),
])

# ══════════════════════════════════════════════════════════════════════════════
# INPUT 03: Feasibility Report Input
# ══════════════════════════════════════════════════════════════════════════════
save(os.path.join(D01, "INPUT_03_Feasibility_Report.ipynb"), [
    md("# INPUT: Feasibility Report\n---\n**Output Destination:** Feasibility Report Template (Domain 01)\n**Methodology:** PMI-PMBOK Business Case\n**ISO:** ISO 21500:2012\n\n## Purpose\nAssess project viability across technical, financial, and regulatory dimensions.\n\n## Source Legend\n| Symbol | Meaning |\n|--------|---------|\n| **[ABS]** | Absolute input |\n| **[REF]** | Reference from previous document |\n| **[DER]** | Derived/calculated |\n| **[STD]** | Standard/default value |\n| **[ACT]** | Output from a previous activity |\n\n## Flow\n**INPUT:** Client Brief + Project Charter → **THIS INPUT** → **ACTIVITY:** Feasibility Analysis → **OUTPUT:** Feasibility Report"),
    code("""# FEASIBILITY REPORT INPUT TEMPLATE
print("=" * 70)
print("INPUT TEMPLATE: FEASIBILITY REPORT")
print("Output Destination: Domain 01 - Feasibility Report")
print("=" * 70)
print("")

inputs = [
    ("Project Name", "[REF] From Client Brief", "INPUT_01", "Client Brief"),
    ("Plot Location", "[REF] From Client Brief", "INPUT_01", "Client Brief"),
    ("Plot Area (m2)", "[REF] From Client Brief", "INPUT_01", "Client Brief"),
    ("GFA Target (m2)", "[REF] From Client Brief", "INPUT_01", "Client Brief"),
    ("Budget (AED)", "[REF] From Client Brief", "INPUT_01", "Client Brief"),
    ("Project Type", "[REF] From Client Brief", "INPUT_01", "Client Brief"),
    ("Market Demand Data", "[ABS] Market research", "Consultant", "Market Analysis"),
    ("Comparable Projects", "[ABS] Market research", "Consultant", "Benchmarking"),
    ("Land Cost (AED/m2)", "[ABS] Client/DLD provides", "Client/DLD", "Financial Feasibility"),
    ("Construction Cost (AED/m2)", "[ABS] QS provides", "QS", "Cost Estimate"),
    ("FAR Allowable", "[ABS] From zoning", "ACT-Zoning", "FAR Analysis"),
    ("Parking Ratio Required", "[ABS] From zoning", "ACT-Zoning", "Parking Analysis"),
    ("Infrastructure Capacity", "[ABS] Utility survey", "ACT-Utilities", "Infrastructure Assessment"),
    ("Environmental Constraints", "[ABS] Environmental study", "ACT-Environmental", "Environmental Assessment"),
    ("Geotechnical Conditions", "[ABS] Geotech report", "ACT-Geotech", "Geotechnical Report"),
    ("Regulatory Requirements", "[ABS] Legal review", "Consultant", "Zoning Compliance"),
    ("Financing Terms", "[ABS] Client provides", "Client", "Financial Feasibility"),
    ("Revenue Projections", "[DER] From market data", "DERIVED", "Revenue Projection"),
    ("ROI Target (%)", "[ABS] Client defines", "Client", "Financial Feasibility"),
    ("Payback Period (years)", "[ABS] Client defines", "Client", "Financial Feasibility"),
]

print("INPUT FIELD                    SOURCE                      WHERE FROM         FEEDS TO")
print("-" * 90)
for inp in inputs:
    print(f"  {inp[0]:<32} {inp[1]:<27} {inp[2]:<17} {inp[3]}")

print("")
print("=" * 70)
print("VALIDATION RULES:")
print("  - All financial figures in AED")
print("  - FAR must not exceed zoning allowance")
print("  - Construction cost per QCS/DM benchmarks")
print("  - Revenue projections must be conservative")
print("")
print("OUTPUT FIELDS (auto-populated):")
print("  - Feasibility Verdict: FEASIBLE/NOT FEASIBLE/CONDITIONAL")
print("  - Risk Score: CALCULATED")
print("  - Recommendation: CALCULATED")
print("  - Reference Number: AUTO-GENERATED")
print("  - Date: TODAY")
"""),
])

# ══════════════════════════════════════════════════════════════════════════════
# INPUT 04: Risk Register Input
# ══════════════════════════════════════════════════════════════════════════════
save(os.path.join(D01, "INPUT_04_Risk_Register.ipynb"), [
    md("# INPUT: Risk Register\n---\n**Output Destination:** Risk Register Template (Domain 01)\n**Methodology:** PMI-PMBOK Section 11, ISO 31000\n**ISO:** ISO 31000:2018\n\n## Purpose\nIdentify, assess, and plan responses for project risks.\n\n## Source Legend\n| Symbol | Meaning |\n|--------|---------|\n| **[ABS]** | Absolute input |\n| **[REF]** | Reference from previous document |\n| **[DER]** | Derived/calculated |\n| **[STD]** | Standard/default value |\n| **[ACT]** | Output from a previous activity |\n\n## Flow\n**INPUT:** Client Brief + Feasibility + Project Charter → **THIS INPUT** → **ACTIVITY:** Risk Analysis → **OUTPUT:** Risk Register"),
    code("""# RISK REGISTER INPUT TEMPLATE
print("=" * 70)
print("INPUT TEMPLATE: RISK REGISTER")
print("Output Destination: Domain 01 - Risk Register")
print("=" * 70)
print("")

inputs = [
    ("Risk ID", "[DER] Auto-generated", "SYSTEM", "Risk Register"),
    ("Risk Description", "[ABS] Team identifies", "Team", "Risk Register"),
    ("Risk Category", "[ABS] Team classifies", "Team", "Risk Register"),
    ("Probability (1-5)", "[ABS] Team assesses", "Team", "Risk Register"),
    ("Impact (1-5)", "[ABS] Team assesses", "Team", "Risk Register"),
    ("Risk Score", "[DER] Prob x Impact", "CALCULATED", "Risk Register"),
    ("Risk Owner", "[ABS] PM assigns", "PM", "Risk Register"),
    ("Response Strategy", "[ABS] Team decides", "Team", "Risk Register"),
    ("Mitigation Actions", "[ABS] Team defines", "Team", "Risk Register"),
    ("Contingency Budget", "[DER] From risk score", "CALCULATED", "Contingency Budget"),
    ("Trigger Events", "[ABS] Team identifies", "Team", "Risk Register"),
    ("Status", "[STD] Open", "STD", "Risk Register"),
    ("Lessons Learned", "[ACT] From previous projects", "ACT-Historical", "Risk Register"),
]

print("INPUT FIELD                    SOURCE                      WHERE FROM         FEEDS TO")
print("-" * 90)
for inp in inputs:
    print(f"  {inp[0]:<32} {inp[1]:<27} {inp[2]:<17} {inp[3]}")

print("")
print("=" * 70)
print("VALIDATION RULES:")
print("  - Probability: 1 (Rare) to 5 (Almost Certain)")
print("  - Impact: 1 (Negligible) to 5 (Catastrophic)")
print("  - Risk Score = Probability x Impact")
print("  - High risks (>=15) require immediate response")
print("")
print("OUTPUT FIELDS (auto-populated):")
print("  - Risk Score: CALCULATED")
print("  - Risk Level: LOW/MEDIUM/HIGH/CRITICAL")
print("  - Response Required: YES/NO")
print("  - Next Review Date: CALCULATED")
"""),
])

# ══════════════════════════════════════════════════════════════════════════════
# INPUT 05: Matrix Book Input
# ══════════════════════════════════════════════════════════════════════════════
save(os.path.join(D01, "INPUT_05_Matrix_Book.ipynb"), [
    md("# INPUT: Matrix Book\n---\n**Output Destination:** Matrix Book Template (Domain 01)\n**Methodology:** PMI-PMBOK Integration\n**ISO:** ISO 21500:2012\n\n## Purpose\nConsolidate all project parameters into a single reference matrix.\n\n## Source Legend\n| Symbol | Meaning |\n|--------|---------|\n| **[ABS]** | Absolute input |\n| **[REF]** | Reference from previous document |\n| **[DER]** | Derived/calculated |\n| **[STD]** | Standard/default value |\n| **[ACT]** | Output from a previous activity |\n\n## Flow\n**INPUT:** All Domain 01 inputs → **THIS INPUT** → **ACTIVITY:** Matrix Consolidation → **OUTPUT:** Matrix Book"),
    code("""# MATRIX BOOK INPUT TEMPLATE
print("=" * 70)
print("INPUT TEMPLATE: MATRIX BOOK")
print("Output Destination: Domain 01 - Matrix Book")
print("=" * 70)
print("")

inputs = [
    ("Project Parameters", "[REF] From Client Brief", "INPUT_01", "Matrix Book"),
    ("Design Parameters", "[REF] From Design Brief", "ACT-Design", "Design Parameters"),
    ("Cost Parameters", "[REF] From Feasibility", "INPUT_03", "Cost Estimate"),
    ("Schedule Parameters", "[REF] From Master Program", "ACT-Schedule", "Master Program"),
    ("Quality Parameters", "[ABS] Client defines", "Client", "Quality Management"),
    ("Safety Parameters", "[ABS] Standards define", "STD", "Safety Management"),
    ("Environmental Parameters", "[ABS] Standards define", "STD", "Environmental Assessment"),
    ("Regulatory Parameters", "[REF] From Zoning", "ACT-Zoning", "Zoning Compliance"),
    ("Stakeholder Parameters", "[REF] From Stakeholder Reg", "ACT-Stakeholders", "Stakeholder Register"),
    ("Risk Parameters", "[REF] From Risk Register", "INPUT_04", "Risk Register"),
    ("Communication Parameters", "[ABS] PM defines", "PM", "Communication Plan"),
    ("Procurement Parameters", "[ABS] PM defines", "PM", "Procurement Strategy"),
]

print("INPUT FIELD                    SOURCE                      WHERE FROM         FEEDS TO")
print("-" * 90)
for inp in inputs:
    print(f"  {inp[0]:<32} {inp[1]:<27} {inp[2]:<17} {inp[3]}")

print("")
print("=" * 70)
print("NOTE: Matrix Book consolidates inputs from ALL other templates.")
print("  Fill all other input templates first, then run this consolidation.")
print("=" * 70)
print("")
print("OUTPUT FIELDS (auto-populated):")
print("  - Matrix Reference: AUTO-GENERATED")
print("  - Consolidation Date: TODAY")
print("  - Version: 1.0")
print("  - Status: DRAFT")
"""),
])

# ══════════════════════════════════════════════════════════════════════════════
# INPUT 06: Benchmarking Report Input
# ══════════════════════════════════════════════════════════════════════════════
save(os.path.join(D01, "INPUT_06_Benchmarking.ipynb"), [
    md("# INPUT: Benchmarking Report\n---\n**Output Destination:** Benchmarking Report (Domain 01)\n**Methodology:** PMI-PMBOK Benchmarking\n**ISO:** ISO 21500:2012\n\n## Purpose\nCompare project parameters against industry standards and comparable projects.\n\n## Flow\n**INPUT:** Market Data + Comparable Projects → **THIS INPUT** → **ACTIVITY:** Benchmark Analysis → **OUTPUT:** Benchmarking Report"),
    code("""# BENCHMARKING REPORT INPUT TEMPLATE
print("=" * 70)
print("INPUT TEMPLATE: BENCHMARKING REPORT")
print("Output Destination: Domain 01 - Benchmarking Report")
print("=" * 70)
print("")

inputs = [
    ("Comparable Project 1 Name", "[ABS] Research", "Consultant", "Benchmarking"),
    ("Comparable Project 1 Cost/m2", "[ABS] Research", "Consultant", "Benchmarking"),
    ("Comparable Project 1 Duration", "[ABS] Research", "Consultant", "Benchmarking"),
    ("Comparable Project 1 Quality", "[ABS] Research", "Consultant", "Benchmarking"),
    ("Comparable Project 2 Name", "[ABS] Research", "Consultant", "Benchmarking"),
    ("Comparable Project 2 Cost/m2", "[ABS] Research", "Consultant", "Benchmarking"),
    ("Comparable Project 2 Duration", "[ABS] Research", "Consultant", "Benchmarking"),
    ("Comparable Project 2 Quality", "[ABS] Research", "Consultant", "Benchmarking"),
    ("Industry Average Cost/m2", "[ABS] Market data", "Market", "Benchmarking"),
    ("Industry Average Duration", "[ABS] Market data", "Market", "Benchmarking"),
    ("Industry Safety Record", "[ABS] Market data", "Market", "Benchmarking"),
    ("Industry Quality Score", "[ABS] Market data", "Market", "Benchmarking"),
]

print("INPUT FIELD                    SOURCE                      WHERE FROM         FEEDS TO")
print("-" * 90)
for inp in inputs:
    print(f"  {inp[0]:<32} {inp[1]:<27} {inp[2]:<17} {inp[3]}")

print("")
print("OUTPUT FIELDS (auto-populated):")
print("  - Variance from Average: CALCULATED")
print("  - Percentile Rank: CALCULATED")
print("  - Benchmark Verdict: ABOVE/AT/BELOW AVERAGE")
print("  - Recommendations: CALCULATED")
"""),
])

print("Domain 01 Input Templates: 6 generated")

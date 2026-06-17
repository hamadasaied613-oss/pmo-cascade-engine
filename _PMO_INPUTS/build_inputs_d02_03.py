#!/usr/bin/env python3
"""Input Templates: Domain 02-03."""
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

D02 = os.path.join(BASE, "DOMAIN_02_LOCATION")
D03 = os.path.join(BASE, "DOMAIN_03_STAKEHOLDERS")

# ══════════════════════════════════════════════════════════════════════════════
# DOMAIN 02 INPUTS
# ══════════════════════════════════════════════════════════════════════════════

# INPUT 01: Site Analysis
save(os.path.join(D02, "INPUT_01_Site_Analysis.ipynb"), [
    md("# INPUT: Site Analysis Report\n---\n**Output Destination:** Site Analysis Report (Domain 02)\n**Methodology:** RIBA Stage 1, Site Analysis\n**ISO:** ISO 21500:2012\n\n## Purpose\nCollect all site-specific data for analysis.\n\n## Source Legend\n| Symbol | Meaning |\n|--------|---------|\n| **[ABS]** | Absolute input |\n| **[REF]** | Reference from previous document |\n| **[DER]** | Derived/calculated |\n| **[STD]** | Standard/default value |\n| **[ACT]** | Output from a previous activity |\n\n## Flow\n**INPUT:** Client Brief + Site Visit → **THIS INPUT** → **ACTIVITY:** Site Analysis → **OUTPUT:** Site Analysis Report"),
    code("""# SITE ANALYSIS INPUT TEMPLATE
print("=" * 70)
print("INPUT TEMPLATE: SITE ANALYSIS REPORT")
print("Output Destination: Domain 02 - Site Analysis Report")
print("=" * 70)
print("")

inputs = [
    ("Plot Number", "[REF] From Client Brief", "INPUT_01-D01", "Client Brief"),
    ("Plot Address", "[ABS] Site visit confirms", "Site Visit", "Site Analysis"),
    ("Plot Area (m2)", "[REF] From Client Brief", "INPUT_01-D01", "Client Brief"),
    ("Plot Dimensions", "[ABS] Survey measurement", "Surveyor", "Site Analysis"),
    ("Plot Shape", "[ABS] Visual observation", "Site Visit", "Site Analysis"),
    ("Topography", "[ABS] Survey data", "Surveyor", "Site Analysis"),
    ("Existing Structures", "[ABS] Site visit", "Site Visit", "Site Analysis"),
    ("Access Points", "[ABS] Site visit", "Site Visit", "Site Analysis"),
    ("Road Width (m)", "[ABS] Survey measurement", "Surveyor", "Site Analysis"),
    ("Road Classification", "[ABS] Municipality data", "ACT-Municipality", "Site Analysis"),
    ("Nearest Highway", "[ABS] Map measurement", "GIS", "Site Analysis"),
    ("Public Transport", "[ABS] Map research", "GIS", "Site Analysis"),
    ("Surrounding Land Use", "[ABS] Zoning map", "ACT-Zoning", "Site Analysis"),
    ("Nearby Facilities", "[ABS] Map research", "GIS", "Site Analysis"),
    ("Utilities Available", "[ABS] Utility survey", "ACT-Utilities", "Infrastructure"),
    ("Soil Type", "[REF] From Geotech Report", "ACT-Geotech", "Geotechnical Report"),
    ("Water Table Level", "[REF] From Geotech Report", "ACT-Geotech", "Geotechnical Report"),
    ("Flood Risk Level", "[ABS] Environmental data", "ACT-Environmental", "Environmental"),
    ("Noise Level (dB)", "[ABS] Environmental data", "ACT-Environmental", "Environmental"),
    ("Air Quality", "[ABS] Environmental data", "ACT-Environmental", "Environmental"),
    ("Wind Direction", "[ABS] Meteorological data", "STD-Met", "Design Parameters"),
    ("Sun Path", "[ABS] Solar analysis", "CALCULATED", "Daylighting Analysis"),
    ("Seismic Zone", "[ABS] Building code", "STD-Code", "Structural Concept"),
    ("Historical Significance", "[ABS] Heritage survey", "ACT-Heritage", "Zoning Compliance"),
    ("Protected Views", "[ABS] Planning data", "ACT-Planning", "Zoning Compliance"),
]

print("INPUT FIELD                    SOURCE                      WHERE FROM         FEEDS TO")
print("-" * 90)
for inp in inputs:
    print(f"  {inp[0]:<32} {inp[1]:<27} {inp[2]:<17} {inp[3]}")

print("")
print("VALIDATION RULES:")
print("  - Plot Area > 0")
print("  - Road Width: 6m min for residential")
print("  - Noise Level: dB(A) measurement")
print("  - Water Table: depth in meters")
print("")
print("OUTPUT FIELDS (auto-populated):")
print("  - Site Score: CALCULATED")
print("  - Constraints List: CALCULATED")
print("  - Opportunities List: CALCULATED")
print("  - Reference Number: AUTO-GENERATED")
"""),
])

# INPUT 02: GIS Data
save(os.path.join(D02, "INPUT_02_GIS_Data.ipynb"), [
    md("# INPUT: GIS Data Report\n---\n**Output Destination:** GIS Data Report (Domain 02)\n**Methodology:** GIS Spatial Analysis\n**ISO:** ISO 19100 Series\n\n## Purpose\nCollect GIS data for spatial analysis.\n\n## Flow\n**INPUT:** Site Address + GIS Software → **THIS INPUT** → **ACTIVITY:** GIS Analysis → **OUTPUT:** GIS Data Report"),
    code("""# GIS DATA INPUT TEMPLATE
print("=" * 70)
print("INPUT TEMPLATE: GIS DATA REPORT")
print("Output Destination: Domain 02 - GIS Data Report")
print("=" * 70)
print("")

inputs = [
    ("Coordinates (Lat)", "[ABS] GPS measurement", "GPS", "GIS Report"),
    ("Coordinates (Long)", "[ABS] GPS measurement", "GPS", "GIS Report"),
    ("Coordinates (UTM)", "[ABS] GPS measurement", "GPS", "GIS Report"),
    ("Elevation (m)", "[ABS] Survey data", "Surveyor", "Site Analysis"),
    ("Slope (%)", "[ABS] Topography survey", "Surveyor", "Site Analysis"),
    ("Aspect (direction)", "[ABS] Topography survey", "Surveyor", "Site Analysis"),
    ("Catchment Area (km2)", "[ABS] GIS calculation", "GIS", "Site Analysis"),
    ("Population Density", "[ABS] Census data", "STD-Census", "Market Analysis"),
    ("Distance to CBD (km)", "[ABS] Map measurement", "GIS", "Site Analysis"),
    ("Distance to Airport (km)", "[ABS] Map measurement", "GIS", "Site Analysis"),
    ("Distance to Port (km)", "[ABS] Map measurement", "GIS", "Site Analysis"),
    ("Distance to Metro (km)", "[ABS] Map measurement", "GIS", "Site Analysis"),
    ("Flood Zone Classification", "[ABS] Flood map", "ACT-Environmental", "Environmental"),
    ("Seismic Zone", "[ABS] Seismic map", "STD-Code", "Structural Concept"),
    ("Land Use Zone", "[ABS] Zoning map", "ACT-Zoning", "Zoning Compliance"),
    ("Building Height Limit (m)", "[ABS] Zoning map", "ACT-Zoning", "FAR Analysis"),
    ("FAR Maximum", "[ABS] Zoning map", "ACT-Zoning", "FAR Analysis"),
    ("Setback Requirements (m)", "[ABS] Zoning map", "ACT-Zoning", "Zoning Compliance"),
]

print("INPUT FIELD                    SOURCE                      WHERE FROM         FEEDS TO")
print("-" * 90)
for inp in inputs:
    print(f"  {inp[0]:<32} {inp[1]:<27} {inp[2]:<17} {inp[3]}")

print("")
print("OUTPUT FIELDS (auto-populated):")
print("  - Site Suitability Score: CALCULATED")
print("  - Spatial Analysis Maps: AUTO-GENERATED")
print("  - Constraint Overlay: CALCULATED")
print("  - Reference Number: AUTO-GENERATED")
"""),
])

# INPUT 03: Transportation Study
save(os.path.join(D02, "INPUT_03_Transportation.ipynb"), [
    md("# INPUT: Transportation Study\n---\n**Output Destination:** Transportation Study (Domain 02)\n**Methodology:** Traffic Impact Assessment\n**ISO:** ISO 14001:2015\n\n## Purpose\nAssess transportation accessibility and traffic impact.\n\n## Flow\n**INPUT:** Site Location + Traffic Data → **THIS INPUT** → **ACTIVITY:** Traffic Analysis → **OUTPUT:** Transportation Study"),
    code("""# TRANSPORTATION STUDY INPUT TEMPLATE
print("=" * 70)
print("INPUT TEMPLATE: TRANSPORTATION STUDY")
print("Output Destination: Domain 02 - Transportation Study")
print("=" * 70)
print("")

inputs = [
    ("Nearest Intersection", "[ABS] Site visit", "Site Visit", "Traffic Study"),
    ("Road Classification", "[ABS] Municipality data", "ACT-Municipality", "Site Analysis"),
    ("Lane Count", "[ABS] Site observation", "Site Visit", "Traffic Study"),
    ("Speed Limit (km/h)", "[ABS] Traffic authority", "ACT-Traffic", "Traffic Study"),
    ("AADT (vehicles/day)", "[ABS] Traffic count", "Traffic Survey", "Traffic Study"),
    ("Peak Hour Factor", "[ABS] Traffic count", "Traffic Survey", "Traffic Study"),
    ("Public Transit Routes", "[ABS] Transit map", "ACT-Transit", "Site Analysis"),
    ("Metro Station Distance (km)", "[ABS] Map measurement", "GIS", "Site Analysis"),
    ("Bus Stop Distance (m)", "[ABS] Map measurement", "GIS", "Site Analysis"),
    ("Parking Availability", "[ABS] Site survey", "Site Visit", "Parking Analysis"),
    ("Pedestrian Infrastructure", "[ABS] Site survey", "Site Visit", "Walkability Study"),
    ("Cycling Infrastructure", "[ABS] Site survey", "Site Visit", "Walkability Study"),
    ("Truck Route Access", "[ABS] Logistics survey", "ACT-Logistics", "Site Analysis"),
    ("Fire Access Requirements", "[ABS] Civil Defence", "ACT-CivilDefence", "Fire Safety"),
    ("Proposed Trip Generation", "[DER] From project size", "CALCULATED", "Traffic Study"),
    ("Level of Service Target", "[ABS] Client/standard", "STD", "Traffic Study"),
]

print("INPUT FIELD                    SOURCE                      WHERE FROM         FEEDS TO")
print("-" * 90)
for inp in inputs:
    print(f"  {inp[0]:<32} {inp[1]:<27} {inp[2]:<17} {inp[3]}")

print("")
print("OUTPUT FIELDS (auto-populated):")
print("  - Traffic Impact Score: CALCULATED")
print("  - Level of Service: CALCULATED")
print("  - Parking Requirement: CALCULATED")
print("  - Reference Number: AUTO-GENERATED")
"""),
])

# INPUT 04: Environmental Assessment
save(os.path.join(D02, "INPUT_04_Environmental.ipynb"), [
    md("# INPUT: Environmental Assessment\n---\n**Output Destination:** Environmental Assessment (Domain 02)\n**Methodology:** Environmental Impact Assessment\n**ISO:** ISO 14001:2015\n\n## Purpose\nCollect environmental data for impact assessment.\n\n## Flow\n**INPUT:** Site Data + Environmental Surveys → **THIS INPUT** → **ACTIVITY:** Environmental Analysis → **OUTPUT:** Environmental Assessment"),
    code("""# ENVIRONMENTAL ASSESSMENT INPUT TEMPLATE
print("=" * 70)
print("INPUT TEMPLATE: ENVIRONMENTAL ASSESSMENT")
print("Output Destination: Domain 02 - Environmental Assessment")
print("=" * 70)
print("")

inputs = [
    ("Air Quality - PM10", "[ABS] Environmental survey", "ENV Consultant", "Environmental"),
    ("Air Quality - PM2.5", "[ABS] Environmental survey", "ENV Consultant", "Environmental"),
    ("Air Quality - NOx", "[ABS] Environmental survey", "ENV Consultant", "Environmental"),
    ("Air Quality - SO2", "[ABS] Environmental survey", "ENV Consultant", "Environmental"),
    ("Noise Level - Day dB(A)", "[ABS] Noise survey", "ENV Consultant", "Noise Zoning"),
    ("Noise Level - Night dB(A)", "[ABS] Noise survey", "ENV Consultant", "Noise Zoning"),
    ("Water Quality - BOD", "[ABS] Water survey", "ENV Consultant", "Environmental"),
    ("Water Quality - COD", "[ABS] Water survey", "ENV Consultant", "Environmental"),
    ("Water Quality - TSS", "[ABS] Water survey", "ENV Consultant", "Environmental"),
    ("Soil Contamination", "[ABS] Soil survey", "ENV Consultant", "Geotechnical"),
    ("Flora Assessment", "[ABS] Ecological survey", "ENV Consultant", "Environmental"),
    ("Fauna Assessment", "[ABS] Ecological survey", "ENV Consultant", "Environmental"),
    ("Marine Assessment", "[ABS] Marine survey", "ENV Consultant", "Environmental"),
    ("Flood Risk Level", "[ABS] Flood study", "ACT-Flood", "Environmental"),
    ("Climate Data - Temperature", "[ABS] Meteorological", "STD-Met", "Energy Analysis"),
    ("Climate Data - Humidity", "[ABS] Meteorological", "STD-Met", "Energy Analysis"),
    ("Climate Data - Solar", "[ABS] Solar data", "STD-Met", "Energy Analysis"),
    ("Climate Data - Wind", "[ABS] Wind data", "STD-Met", "Structural Concept"),
    ("Heritage Assets", "[ABS] Heritage survey", "ACT-Heritage", "Zoning Compliance"),
    ("Protected Habitats", "[ABS] Ecological survey", "ENV Consultant", "Environmental"),
]

print("INPUT FIELD                    SOURCE                      WHERE FROM         FEEDS TO")
print("-" * 90)
for inp in inputs:
    print(f"  {inp[0]:<32} {inp[1]:<27} {inp[2]:<17} {inp[3]}")

print("")
print("OUTPUT FIELDS (auto-populated):")
print("  - Environmental Score: CALCULATED")
print("  - Impact Level: LOW/MEDIUM/HIGH/CRITICAL")
print("  - Mitigation Requirements: CALCULATED")
print("  - Reference Number: AUTO-GENERATED")
"""),
])

# ══════════════════════════════════════════════════════════════════════════════
# DOMAIN 03 INPUTS
# ══════════════════════════════════════════════════════════════════════════════

# INPUT 01: Stakeholder Register
save(os.path.join(D03, "INPUT_01_Stakeholder_Register.ipynb"), [
    md("# INPUT: Stakeholder Register\n---\n**Output Destination:** Stakeholder Register (Domain 03)\n**Methodology:** PMI-PMBOK Section 13.1\n**ISO:** ISO 21500:2012\n\n## Purpose\nIdentify and classify all project stakeholders.\n\n## Flow\n**INPUT:** Client Brief + Project Charter → **THIS INPUT** → **ACTIVITY:** Stakeholder Analysis → **OUTPUT:** Stakeholder Register"),
    code("""# STAKEHOLDER REGISTER INPUT TEMPLATE
print("=" * 70)
print("INPUT TEMPLATE: STAKEHOLDER REGISTER")
print("Output Destination: Domain 03 - Stakeholder Register")
print("=" * 70)
print("")

inputs = [
    ("Stakeholder Name", "[ABS] Team identifies", "Team", "Stakeholder Register"),
    ("Organization", "[ABS] Team identifies", "Team", "Stakeholder Register"),
    ("Role/Position", "[ABS] Team identifies", "Team", "Stakeholder Register"),
    ("Contact Information", "[ABS] Team collects", "Team", "Stakeholder Register"),
    ("Interest Level (1-5)", "[ABS] Team assesses", "Team", "Stakeholder Register"),
    ("Influence Level (1-5)", "[ABS] Team assesses", "Team", "Stakeholder Register"),
    ("Attitude (Supportive/Neutral/Resistant)", "[ABS] Team assesses", "Team", "Stakeholder Register"),
    ("Communication Needs", "[ABS] Team identifies", "Team", "Communication Plan"),
    ("Information Requirements", "[ABS] Team identifies", "Team", "Communication Plan"),
    ("Engagement Strategy", "[ABS] PM decides", "PM", "Stakeholder Register"),
    ("Power/Interest Grid Position", "[DER] From Power/Interest", "CALCULATED", "Stakeholder Register"),
    ("Risk Level", "[DER] From Influence/Attitude", "CALCULATED", "Risk Register"),
]

print("INPUT FIELD                    SOURCE                      WHERE FROM         FEEDS TO")
print("-" * 90)
for inp in inputs:
    print(f"  {inp[0]:<32} {inp[1]:<27} {inp[2]:<17} {inp[3]}")

print("")
print("OUTPUT FIELDS (auto-populated):")
print("  - Power/Interest Grid: CALCULATED")
print("  - Engagement Priority: CALCULATED")
print("  - Communication Frequency: CALCULATED")
print("  - Reference Number: AUTO-GENERATED")
"""),
])

# INPUT 02: RACI Matrix
save(os.path.join(D03, "INPUT_02_RACI_Matrix.ipynb"), [
    md("# INPUT: RACI Matrix\n---\n**Output Destination:** RACI Matrix (Domain 03)\n**Methodology:** PMI-PMBOK Responsibility Assignment\n**ISO:** ISO 21500:2012\n\n## Purpose\nDefine Responsible, Accountable, Consulted, Informed roles.\n\n## Flow\n**INPUT:** Stakeholder Register + Project Charter → **THIS INPUT** → **ACTIVITY:** RACI Assignment → **OUTPUT:** RACI Matrix"),
    code("""# RACI MATRIX INPUT TEMPLATE
print("=" * 70)
print("INPUT TEMPLATE: RACI MATRIX")
print("Output Destination: Domain 03 - RACI Matrix")
print("=" * 70)
print("")

inputs = [
    ("Activity/Deliverable", "[ABS] PM defines", "PM", "Master Program"),
    ("Responsible (R)", "[ABS] PM assigns", "PM", "RACI Matrix"),
    ("Accountable (A)", "[ABS] PM assigns", "PM", "RACI Matrix"),
    ("Consulted (C)", "[ABS] PM assigns", "PM", "RACI Matrix"),
    ("Informed (I)", "[ABS] PM assigns", "PM", "RACI Matrix"),
    ("Stakeholder Name", "[REF] From Stakeholder Reg", "INPUT_01-D03", "Stakeholder Register"),
    ("Role", "[REF] From Stakeholder Reg", "INPUT_01-D03", "Stakeholder Register"),
    ("Authority Level", "[ABS] Client defines", "Client", "Project Charter"),
    ("Escalation Path", "[ABS] PM defines", "PM", "Escalation Procedure"),
]

print("INPUT FIELD                    SOURCE                      WHERE FROM         FEEDS TO")
print("-" * 90)
for inp in inputs:
    print(f"  {inp[0]:<32} {inp[1]:<27} {inp[2]:<17} {inp[3]}")

print("")
print("OUTPUT FIELDS (auto-populated):")
print("  - RACI Conflict Check: CALCULATED")
print("  - Responsibility Coverage: CALCULATED")
print("  - Reference Number: AUTO-GENERATED")
"""),
])

# INPUT 03: Communication Plan
save(os.path.join(D03, "INPUT_03_Communication_Plan.ipynb"), [
    md("# INPUT: Communication Plan\n---\n**Output Destination:** Communication Plan (Domain 03)\n**Methodology:** PMI-PMBOK Section 10.2\n**ISO:** ISO 21500:2012\n\n## Purpose\nDefine communication channels, frequency, and content.\n\n## Flow\n**INPUT:** Stakeholder Register + RACI Matrix → **THIS INPUT** → **ACTIVITY:** Communication Design → **OUTPUT:** Communication Plan"),
    code("""# COMMUNICATION PLAN INPUT TEMPLATE
print("=" * 70)
print("INPUT TEMPLATE: COMMUNICATION PLAN")
print("Output Destination: Domain 03 - Communication Plan")
print("=" * 70)
print("")

inputs = [
    ("Communication Type", "[ABS] PM defines", "PM", "Communication Plan"),
    ("Audience", "[ABS] PM defines", "PM", "Communication Plan"),
    ("Frequency", "[ABS] PM defines", "PM", "Communication Plan"),
    ("Format", "[ABS] PM defines", "PM", "Communication Plan"),
    ("Channel", "[ABS] PM defines", "PM", "Communication Plan"),
    ("Content Summary", "[ABS] PM defines", "PM", "Communication Plan"),
    ("Responsible Person", "[ABS] PM assigns", "PM", "RACI Matrix"),
    ("Escalation Trigger", "[ABS] PM defines", "PM", "Escalation Procedure"),
    ("Stakeholder Needs", "[REF] From Stakeholder Reg", "INPUT_01-D03", "Stakeholder Register"),
    ("Reporting Requirements", "[ABS] Client defines", "Client", "Project Charter"),
]

print("INPUT FIELD                    SOURCE                      WHERE FROM         FEEDS TO")
print("-" * 90)
for inp in inputs:
    print(f"  {inp[0]:<32} {inp[1]:<27} {inp[2]:<17} {inp[3]}")

print("")
print("OUTPUT FIELDS (auto-populated):")
print("  - Communication Calendar: AUTO-GENERATED")
print("  - Distribution List: CALCULATED")
print("  - Reference Number: AUTO-GENERATED")
"""),
])

print("Domain 02-03 Input Templates: 7 generated")

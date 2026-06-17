#!/usr/bin/env python3
"""
Gateway Reference Tables for Domino Cascade System
7 tables that power the entire input→output chain
"""
import sqlite3, os

BASE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE, "gateway.db")

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# ══════════════════════════════════════════════════════════════════════════════
# TABLE 1: zoning_matrix - FAR, Height, Setbacks, Parking by Zone
# ══════════════════════════════════════════════════════════════════════════════
c.execute("DROP TABLE IF EXISTS zoning_matrix")
c.execute("""CREATE TABLE zoning_matrix (
    id INTEGER PRIMARY KEY,
    emirate TEXT NOT NULL,
    zone_code TEXT NOT NULL,
    zone_name TEXT,
    land_use TEXT NOT NULL,
    building_type TEXT NOT NULL,
    far_min REAL,
    far_optimal REAL,
    far_max REAL,
    height_min_m REAL,
    height_optimal_m REAL,
    height_max_m REAL,
    max_floors INTEGER,
    coverage_min_pct REAL,
    coverage_optimal_pct REAL,
    coverage_max_pct REAL,
    setback_front_m REAL,
    setback_rear_m REAL,
    setback_side_m REAL,
    parking_ratio_residential REAL,
    parking_ratio_commercial REAL,
    parking_ratio_hotel REAL,
    parking_ratio_mixed REAL,
    podium_max_m REAL,
    heritage_overlay INTEGER DEFAULT 0,
    environmental_overlay INTEGER DEFAULT 0,
    notes TEXT
)""")

zoning_data = [
    # Dubai Downtown
    ("Dubai", "DTC-01", "Downtown Core", "Mixed-Use", "High-Rise", 3.5, 4.0, 5.0, 30, 50, 75, 20, 40, 50, 60, 3, 3, 2, 1.0, 1.5, 0.5, 1.0, 15, 0, 0, "Prime downtown"),
    ("Dubai", "DTC-01", "Downtown Core", "Residential", "High-Rise", 3.0, 3.5, 4.5, 30, 50, 75, 20, 35, 45, 55, 3, 3, 2, 1.0, 0, 0, 0, 15, 0, 0, "Residential towers"),
    ("Dubai", "DTC-01", "Downtown Core", "Commercial", "High-Rise", 4.0, 5.0, 6.0, 30, 60, 100, 25, 45, 55, 65, 3, 3, 2, 0, 1.5, 0, 0, 15, 0, 0, "Office towers"),
    ("Dubai", "DTC-01", "Downtown Core", "Hotel", "High-Rise", 3.5, 4.0, 5.0, 30, 50, 75, 20, 40, 50, 60, 3, 3, 2, 0, 0, 0.5, 0, 15, 0, 0, "Hotel towers"),
    
    # Dubai Marina
    ("Dubai", "MAR-01", "Dubai Marina", "Mixed-Use", "High-Rise", 3.5, 4.0, 5.0, 30, 50, 75, 20, 40, 50, 60, 3, 3, 2, 1.0, 1.5, 0.5, 1.0, 15, 0, 0, "Marina district"),
    ("Dubai", "MAR-01", "Dubai Marina", "Residential", "High-Rise", 3.0, 3.5, 4.5, 30, 50, 75, 20, 35, 45, 55, 3, 3, 2, 1.0, 0, 0, 0, 15, 0, 0, "Marina residential"),
    
    # Dubai JVC
    ("Dubai", "JVC-01", "Jumeirah Village", "Residential", "Mid-Rise", 2.0, 2.5, 3.0, 15, 25, 35, 10, 40, 50, 60, 5, 5, 3, 1.0, 0, 0, 0, 10, 0, 0, "Suburban residential"),
    ("Dubai", "JVC-01", "Jumeirah Village", "Residential", "Low-Rise", 1.5, 2.0, 2.5, 8, 12, 15, 4, 50, 60, 70, 5, 5, 3, 1.0, 0, 0, 0, 0, 0, 0, "Villas"),
    
    # Dubai Sports City
    ("Dubai", "DSC-01", "Sports City", "Mixed-Use", "Mid-Rise", 2.5, 3.0, 3.5, 15, 25, 40, 12, 40, 50, 60, 5, 5, 3, 1.0, 1.0, 0.5, 1.0, 10, 0, 0, "Sports community"),
    
    # Dubai Business Bay
    ("Dubai", "BB-01", "Business Bay", "Commercial", "High-Rise", 4.0, 5.0, 7.0, 30, 60, 100, 25, 45, 55, 65, 3, 3, 2, 0, 1.5, 0, 0, 15, 0, 0, "Business district"),
    ("Dubai", "BB-01", "Business Bay", "Mixed-Use", "High-Rise", 3.5, 4.5, 6.0, 30, 50, 80, 22, 40, 50, 60, 3, 3, 2, 1.0, 1.5, 0.5, 1.0, 15, 0, 0, "Mixed business"),
    
    # Dubai JBR
    ("Dubai", "JBR-01", "JBR Beach", "Mixed-Use", "High-Rise", 3.5, 4.0, 5.0, 30, 50, 75, 20, 40, 50, 60, 3, 3, 2, 1.0, 1.5, 0.5, 1.0, 15, 0, 0, "Beachfront"),
    
    # Abu Dhabi Al Reem
    ("Abu Dhabi", "AR-01", "Al Reem Island", "Mixed-Use", "High-Rise", 3.5, 4.0, 5.0, 30, 50, 75, 20, 40, 50, 60, 3, 3, 2, 1.0, 1.5, 0.5, 1.0, 15, 0, 0, "Island development"),
    ("Abu Dhabi", "AR-01", "Al Reem Island", "Residential", "High-Rise", 3.0, 3.5, 4.5, 30, 50, 75, 20, 35, 45, 55, 3, 3, 2, 1.0, 0, 0, 0, 15, 0, 0, "Residential towers"),
    
    # Abu Dhabi Corniche
    ("Abu Dhabi", "CORN-01", "Corniche", "Hotel", "High-Rise", 3.0, 3.5, 4.0, 30, 45, 60, 18, 40, 50, 60, 5, 5, 3, 0, 0, 0.5, 0, 12, 0, 1, "Waterfront hotel"),
    ("Abu Dhabi", "CORN-01", "Corniche", "Mixed-Use", "High-Rise", 3.5, 4.0, 5.0, 30, 50, 75, 20, 40, 50, 60, 5, 5, 3, 1.0, 1.5, 0.5, 1.0, 15, 0, 1, "Corniche mixed"),
    
    # Abu Dhabi Yas Island
    ("Abu Dhabi", "YAS-01", "Yas Island", "Mixed-Use", "Mid-Rise", 2.5, 3.0, 3.5, 15, 25, 40, 12, 40, 50, 60, 5, 5, 3, 1.0, 1.0, 0.5, 1.0, 10, 0, 0, "Entertainment district"),
    
    # Sharjah Al Mamzar
    ("Sharjah", "MAM-01", "Al Mamzar", "Residential", "Mid-Rise", 2.0, 2.5, 3.0, 15, 25, 35, 10, 40, 50, 60, 5, 5, 3, 1.0, 0, 0, 0, 10, 0, 0, "Beach residential"),
    
    # Sharjah Al Khan
    ("Sharjah", "KHAN-01", "Al Khan", "Residential", "Mid-Rise", 2.0, 2.5, 3.5, 15, 25, 40, 12, 40, 50, 60, 5, 5, 3, 1.0, 0, 0, 0, 10, 0, 0, "Waterfront residential"),
    
    # RAK Al Marjan
    ("RAK", "MARJ-01", "Al Marjan Island", "Hotel", "Mid-Rise", 2.0, 2.5, 3.0, 15, 25, 40, 12, 35, 45, 55, 5, 5, 3, 0, 0, 0.5, 0, 10, 0, 1, "Island hotel"),
    
    # Sharjah SAIF Zone
    ("Sharjah", "SAIF-01", "SAIF Zone", "Industrial", "Low-Rise", 1.0, 1.5, 2.0, 8, 12, 15, 4, 50, 60, 70, 8, 8, 5, 0.5, 0.5, 0, 0, 0, 0, 0, "Industrial free zone"),
    
    # Qatar Lusail
    ("Qatar", "LUS-01", "Lusail City", "Mixed-Use", "High-Rise", 3.5, 4.0, 5.0, 30, 50, 80, 22, 40, 50, 60, 3, 3, 2, 1.0, 1.5, 0.5, 1.0, 15, 0, 0, "Lusail mega project"),
    ("Qatar", "LUS-01", "Lusail City", "Residential", "High-Rise", 3.0, 3.5, 4.5, 30, 50, 75, 20, 35, 45, 55, 3, 3, 2, 1.0, 0, 0, 0, 15, 0, 0, "Lusail residential"),
    
    # Qatar West Bay
    ("Qatar", "WB-01", "West Bay", "Commercial", "High-Rise", 4.0, 5.0, 7.0, 30, 60, 100, 25, 45, 55, 65, 3, 3, 2, 0, 1.5, 0, 0, 15, 0, 0, "CBD towers"),
    ("Qatar", "WB-01", "West Bay", "Mixed-Use", "High-Rise", 3.5, 4.5, 6.0, 30, 50, 80, 22, 40, 50, 60, 3, 3, 2, 1.0, 1.5, 0.5, 1.0, 15, 0, 0, "CBD mixed"),
    
    # Qatar Al Wakrah
    ("Qatar", "WAK-01", "Al Wakrah", "Residential", "Mid-Rise", 2.0, 2.5, 3.0, 15, 25, 35, 10, 40, 50, 60, 5, 5, 3, 1.0, 0, 0, 0, 10, 0, 0, "Suburban residential"),
    
    # Qatar Al Rayyan
    ("Qatar", "RAY-01", "Al Rayyan", "Sports", "Stadium", 1.0, 1.5, 2.0, 0, 0, 30, 3, 30, 40, 50, 10, 10, 8, 3.0, 0, 0, 0, 0, 0, 0, "Stadium precinct"),
]

c.executemany("""INSERT INTO zoning_matrix 
    (emirate, zone_code, zone_name, land_use, building_type,
     far_min, far_optimal, far_max,
     height_min_m, height_optimal_m, height_max_m, max_floors,
     coverage_min_pct, coverage_optimal_pct, coverage_max_pct,
     setback_front_m, setback_rear_m, setback_side_m,
     parking_ratio_residential, parking_ratio_commercial, parking_ratio_hotel, parking_ratio_mixed,
     podium_max_m, heritage_overlay, environmental_overlay, notes)
    VALUES (?,?,?,?,?, ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", zoning_data)

print(f"zoning_matrix: {len(zoning_data)} rows inserted")

# ══════════════════════════════════════════════════════════════════════════════
# TABLE 2: cost_matrix - Construction Cost by Region/Type/Quality
# ══════════════════════════════════════════════════════════════════════════════
c.execute("DROP TABLE IF EXISTS cost_matrix")
c.execute("""CREATE TABLE cost_matrix (
    id INTEGER PRIMARY KEY,
    emirate TEXT NOT NULL,
    building_type TEXT NOT NULL,
    quality_level TEXT NOT NULL,
    structure_aed_sqm REAL,
    mep_aed_sqm REAL,
    finishes_aed_sqm REAL,
    facade_aed_sqm REAL,
    total_construction_aed_sqm REAL,
    land_price_aed_sqm REAL,
    soft_cost_pct REAL,
    contingency_pct REAL,
    developer_profit_pct REAL,
    notes TEXT
)""")

cost_data = [
    # Dubai High-Rise
    ("Dubai", "Residential", "Basic", 1200, 600, 400, 300, 2500, 8000, 12, 10, 20, "Economy residential"),
    ("Dubai", "Residential", "Standard", 1500, 750, 600, 500, 3350, 12000, 12, 10, 20, "Standard residential"),
    ("Dubai", "Residential", "Premium", 2000, 1000, 900, 800, 4700, 18000, 12, 10, 20, "Premium residential"),
    ("Dubai", "Residential", "Luxury", 2800, 1400, 1400, 1200, 6800, 25000, 12, 10, 20, "Ultra luxury"),
    
    ("Dubai", "Commercial", "Basic", 1400, 700, 500, 400, 3000, 10000, 12, 10, 18, "Basic office"),
    ("Dubai", "Commercial", "Standard", 1800, 900, 700, 600, 4000, 15000, 12, 10, 18, "Standard office"),
    ("Dubai", "Commercial", "Premium", 2400, 1200, 1000, 900, 5500, 22000, 12, 10, 18, "Grade A office"),
    ("Dubai", "Commercial", "Luxury", 3200, 1600, 1500, 1400, 7700, 30000, 12, 10, 18, "Iconic office"),
    
    ("Dubai", "Hotel", "Basic", 1600, 800, 600, 500, 3500, 12000, 15, 10, 22, "3-star hotel"),
    ("Dubai", "Hotel", "Standard", 2000, 1000, 800, 700, 4500, 18000, 15, 10, 22, "4-star hotel"),
    ("Dubai", "Hotel", "Premium", 2800, 1400, 1200, 1000, 6400, 25000, 15, 10, 22, "5-star hotel"),
    ("Dubai", "Hotel", "Luxury", 3500, 1800, 1800, 1500, 8600, 35000, 15, 10, 22, "7-star hotel"),
    
    ("Dubai", "Mixed-Use", "Basic", 1300, 650, 450, 350, 2750, 9000, 12, 10, 20, "Basic mixed"),
    ("Dubai", "Mixed-Use", "Standard", 1650, 825, 650, 550, 3675, 14000, 12, 10, 20, "Standard mixed"),
    ("Dubai", "Mixed-Use", "Premium", 2200, 1100, 950, 850, 5100, 20000, 12, 10, 20, "Premium mixed"),
    ("Dubai", "Mixed-Use", "Luxury", 3000, 1500, 1400, 1300, 7200, 28000, 12, 10, 20, "Luxury mixed"),
    
    # Dubai Low/Mid-Rise
    ("Dubai", "Residential-Villa", "Basic", 1000, 500, 350, 250, 2100, 5000, 10, 8, 22, "Basic villa"),
    ("Dubai", "Residential-Villa", "Standard", 1300, 650, 500, 400, 2850, 8000, 10, 8, 22, "Standard villa"),
    ("Dubai", "Residential-Villa", "Premium", 1800, 900, 800, 700, 4200, 12000, 10, 8, 22, "Premium villa"),
    ("Dubai", "Residential-Villa", "Luxury", 2500, 1250, 1200, 1000, 5950, 18000, 10, 8, 22, "Luxury villa"),
    
    # Abu Dhabi
    ("Abu Dhabi", "Residential", "Basic", 1100, 550, 380, 280, 2310, 6000, 12, 10, 18, "Basic residential"),
    ("Abu Dhabi", "Residential", "Standard", 1400, 700, 550, 450, 3100, 10000, 12, 10, 18, "Standard residential"),
    ("Abu Dhabi", "Residential", "Premium", 1850, 925, 850, 750, 4375, 15000, 12, 10, 18, "Premium residential"),
    ("Abu Dhabi", "Residential", "Luxury", 2600, 1300, 1300, 1100, 6300, 22000, 12, 10, 18, "Luxury residential"),
    
    ("Abu Dhabi", "Commercial", "Basic", 1300, 650, 450, 350, 2750, 8000, 12, 10, 16, "Basic office"),
    ("Abu Dhabi", "Commercial", "Standard", 1700, 850, 650, 550, 3750, 12000, 12, 10, 16, "Standard office"),
    ("Abu Dhabi", "Commercial", "Premium", 2200, 1100, 900, 800, 5000, 18000, 12, 10, 16, "Premium office"),
    ("Abu Dhabi", "Commercial", "Luxury", 3000, 1500, 1400, 1200, 7100, 25000, 12, 10, 16, "Luxury office"),
    
    ("Abu Dhabi", "Hotel", "Standard", 1800, 900, 700, 600, 4000, 14000, 15, 10, 20, "4-star hotel"),
    ("Abu Dhabi", "Hotel", "Premium", 2500, 1250, 1100, 900, 5750, 22000, 15, 10, 20, "5-star hotel"),
    
    ("Abu Dhabi", "Mixed-Use", "Standard", 1550, 775, 600, 500, 3425, 11000, 12, 10, 18, "Standard mixed"),
    ("Abu Dhabi", "Mixed-Use", "Premium", 2000, 1000, 875, 775, 4650, 17000, 12, 10, 18, "Premium mixed"),
    
    # Sharjah
    ("Sharjah", "Residential", "Basic", 900, 450, 320, 220, 1890, 4000, 10, 8, 20, "Basic residential"),
    ("Sharjah", "Residential", "Standard", 1200, 600, 480, 380, 2660, 6000, 10, 8, 20, "Standard residential"),
    ("Sharjah", "Residential", "Premium", 1600, 800, 700, 600, 3700, 9000, 10, 8, 20, "Premium residential"),
    ("Sharjah", "Residential", "Luxury", 2200, 1100, 1000, 850, 5150, 14000, 10, 8, 20, "Luxury residential"),
    
    ("Sharjah", "Commercial", "Standard", 1400, 700, 550, 450, 3100, 7000, 10, 8, 16, "Standard office"),
    ("Sharjah", "Commercial", "Premium", 1800, 900, 750, 650, 4100, 10000, 10, 8, 16, "Premium office"),
    
    # RAK
    ("RAK", "Residential", "Standard", 1000, 500, 400, 300, 2200, 3000, 10, 8, 20, "Standard residential"),
    ("RAK", "Hotel", "Standard", 1500, 750, 600, 500, 3350, 5000, 15, 10, 22, "Resort hotel"),
    ("RAK", "Hotel", "Premium", 2000, 1000, 850, 750, 4600, 8000, 15, 10, 22, "Premium resort"),
    
    # Qatar
    ("Qatar", "Residential", "Basic", 1000, 500, 350, 280, 2130, 5000, 12, 10, 18, "Basic residential"),
    ("Qatar", "Residential", "Standard", 1350, 675, 530, 430, 2985, 8000, 12, 10, 18, "Standard residential"),
    ("Qatar", "Residential", "Premium", 1800, 900, 800, 700, 4200, 14000, 12, 10, 18, "Premium residential"),
    ("Qatar", "Residential", "Luxury", 2500, 1250, 1200, 1000, 5950, 20000, 12, 10, 18, "Luxury residential"),
    
    ("Qatar", "Commercial", "Standard", 1600, 800, 600, 500, 3500, 10000, 12, 10, 16, "Standard office"),
    ("Qatar", "Commercial", "Premium", 2200, 1100, 900, 800, 5000, 16000, 12, 10, 16, "Premium office"),
    
    ("Qatar", "Hotel", "Standard", 1700, 850, 650, 550, 3750, 12000, 15, 10, 22, "4-star hotel"),
    ("Qatar", "Hotel", "Premium", 2400, 1200, 1050, 900, 5550, 20000, 15, 10, 22, "5-star hotel"),
    
    ("Qatar", "Mixed-Use", "Standard", 1500, 750, 580, 480, 3310, 9000, 12, 10, 18, "Standard mixed"),
    ("Qatar", "Mixed-Use", "Premium", 2000, 1000, 850, 750, 4600, 15000, 12, 10, 18, "Premium mixed"),
    
    # Qatar Industrial
    ("Qatar", "Industrial", "Basic", 600, 300, 200, 150, 1250, 2000, 8, 8, 15, "Basic warehouse"),
    ("Qatar", "Industrial", "Standard", 800, 400, 300, 200, 1700, 3000, 8, 8, 15, "Standard industrial"),
]

c.executemany("""INSERT INTO cost_matrix 
    (emirate, building_type, quality_level,
     structure_aed_sqm, mep_aed_sqm, finishes_aed_sqm, facade_aed_sqm,
     total_construction_aed_sqm, land_price_aed_sqm,
     soft_cost_pct, contingency_pct, developer_profit_pct, notes)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", cost_data)

print(f"cost_matrix: {len(cost_data)} rows inserted")

# ══════════════════════════════════════════════════════════════════════════════
# TABLE 3: structural_matrix - Structural Systems by Type/Height/Soil
# ══════════════════════════════════════════════════════════════════════════════
c.execute("DROP TABLE IF EXISTS structural_matrix")
c.execute("""CREATE TABLE structural_matrix (
    id INTEGER PRIMARY KEY,
    building_type TEXT NOT NULL,
    height_min_m REAL,
    height_max_m REAL,
    floors_min INTEGER,
    floors_max INTEGER,
    soil_types TEXT,
    structural_system TEXT NOT NULL,
    max_span_m REAL,
    concrete_grade TEXT,
    steel_grade TEXT,
    foundation_type TEXT,
    cost_factor REAL,
    notes TEXT
)""")

structural_data = [
    # Low-Rise (1-4 floors, up to 15m)
    ("Residential", 0, 15, 1, 4, "All", "Load Bearing Masonry", 6.0, "C25", "B500", "Strip Footing", 1.0, "Villas and small residential"),
    ("Commercial", 0, 15, 1, 4, "All", "RC Frame", 8.0, "C30", "B500", "Pad Footing", 1.1, "Small commercial"),
    ("Industrial", 0, 15, 1, 4, "All", "Steel Frame", 15.0, "N/A", "S355", "Pad Footing", 1.0, "Warehouses"),
    
    # Mid-Rise (5-10 floors, 15-35m)
    ("Residential", 15, 35, 5, 10, "Sand,Stiff Clay", "RC Frame", 8.0, "C35", "B500", "Raft Foundation", 1.0, "Mid-rise residential"),
    ("Residential", 15, 35, 5, 10, "Rock,Dense Sand", "RC Frame", 9.0, "C35", "B500", "Pad Footing", 0.95, "Rocky soil advantage"),
    ("Commercial", 15, 35, 5, 10, "Sand,Stiff Clay", "RC Frame", 10.0, "C40", "B500", "Raft Foundation", 1.05, "Mid-rise office"),
    ("Mixed-Use", 15, 35, 5, 10, "Sand,Stiff Clay", "RC Frame with Shear Wall", 8.0, "C40", "B500", "Raft Foundation", 1.1, "Mixed podium+tower"),
    
    # High-Rise (11-20 floors, 35-75m)
    ("Residential", 35, 75, 11, 20, "Dense Sand,Stiff Clay", "RC Core + Shear Wall", 7.0, "C45", "B500", "Pile Foundation", 1.2, "Typical residential tower"),
    ("Residential", 35, 75, 11, 20, "Rock", "RC Core + Shear Wall", 8.0, "C40", "B500", "Pad/Raft", 1.1, "Rock advantage"),
    ("Residential", 35, 75, 11, 20, "Loose Sand,Soft Clay", "RC Core + Shear Wall", 6.5, "C50", "B500", "Pile + Pile Cap", 1.35, "Weak soil premium"),
    ("Commercial", 35, 75, 11, 20, "Dense Sand,Stiff Clay", "RC Core + Shear Wall", 9.0, "C50", "B500", "Pile Foundation", 1.25, "Office tower"),
    ("Hotel", 35, 75, 11, 20, "Dense Sand,Stiff Clay", "RC Core + Shear Wall", 7.0, "C45", "B500", "Pile Foundation", 1.2, "Hotel tower"),
    ("Mixed-Use", 35, 75, 11, 20, "Dense Sand,Stiff Clay", "RC Core + Shear Wall + Outrigger", 8.0, "C50", "B500", "Pile Foundation", 1.3, "Mixed tower"),
    
    # Ultra High-Rise (21+ floors, 75m+)
    ("Residential", 75, 200, 21, 60, "Dense Sand,Rock", "RC Core + Steel Composite", 7.0, "C60", "S355-S460", "Deep Pile", 1.5, "Ultra high-rise residential"),
    ("Commercial", 75, 200, 21, 60, "Dense Sand,Rock", "Steel Composite + Outrigger", 10.0, "C60", "S355-S460", "Deep Pile", 1.6, "Ultra high-rise office"),
    ("Mixed-Use", 75, 200, 21, 60, "Dense Sand,Rock", "RC Core + Steel Composite + Belt", 8.0, "C60", "S355-S460", "Deep Pile", 1.7, "Mega tower"),
    ("Hotel", 75, 150, 21, 45, "Dense Sand,Rock", "RC Core + Steel Composite", 7.0, "C55", "S355", "Deep Pile", 1.5, "Ultra high-rise hotel"),
    
    # Coastal/Sabkha
    ("Residential", 15, 50, 5, 15, "Coastal Sabkha", "RC Core + Shear Wall", 6.5, "C50", "B500", "Deep Pile + Corrosion Protection", 1.4, "Coastal premium"),
    ("Hotel", 15, 50, 5, 15, "Coastal Sabkha", "RC Core + Shear Wall", 6.5, "C50", "B500", "Deep Pile + Corrosion Protection", 1.4, "Beachfront hotel"),
]

c.executemany("""INSERT INTO structural_matrix 
    (building_type, height_min_m, height_max_m, floors_min, floors_max,
     soil_types, structural_system, max_span_m, concrete_grade, steel_grade,
     foundation_type, cost_factor, notes)
    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)""", structural_data)

print(f"structural_matrix: {len(structural_data)} rows inserted")

conn.commit()
conn.close()

print(f"\nGateway DB created: {DB_PATH}")
print(f"File size: {os.path.getsize(DB_PATH)/1024:.1f} KB")

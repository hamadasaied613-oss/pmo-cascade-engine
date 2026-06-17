#!/usr/bin/env python3
"""
Cascade Engine: Reads minimal input → queries gateway tables → generates all 116 outputs
"""
import sqlite3, json, os, math
from pathlib import Path

DB_PATH = Path(__file__).parent / "gateway.db"
OUTPUT_DIR = Path(__file__).parent.parent / "_PMO_OUTPUTS"

class CascadeEngine:
    def __init__(self):
        self.conn = sqlite3.connect(str(DB_PATH))
        self.conn.row_factory = sqlite3.Row
        self.input_data = {}
        self.derived_data = {}
        self.outputs = {}

    def load_input(self, json_path):
        with open(json_path) as f:
            self.input_data = json.load(f)
        print(f"Loaded input: {self.input_data.get('plot','?')}")

    def derive_from_plot(self):
        plot_num = self.input_data.get('plot','').upper()
        c = self.conn.cursor()
        c.execute("SELECT * FROM plot_database WHERE plot_number=?", (plot_num,))
        row = c.fetchone()
        if row:
            self.derived_data = dict(row)
            print(f"  Plot found: {row['emirate']} / {row['area_name']}")
            return True
        print(f"  Plot {plot_num} not in database — using manual input")
        return False

    def lookup_zoning(self):
        emirate = self.derived_data.get('emirate', self.input_data.get('emirate',''))
        building_type = self.input_data.get('type','MIX')
        type_map = {
            'RES':'Residential','COM':'Commercial','MIX':'Mixed-Use',
            'HOT':'Hotel','RES-V':'Residential-Villa','HEA':'Residential',
            'EDU':'Residential','IND':'Industrial','SPO':'Commercial',
            'DAT':'Commercial','GOV':'Commercial','CUL':'Commercial',
            'REL':'Commercial','ENT':'Commercial','LOG':'Industrial',
            'ENG':'Industrial'
        }
        bt = type_map.get(building_type, 'Mixed-Use')
        c = self.conn.cursor()
        c.execute("""SELECT * FROM zoning_matrix 
                     WHERE emirate=? AND (land_use=? OR building_type=?)
                     LIMIT 1""", (emirate, bt, bt))
        row = c.fetchone()
        if row:
            self.derived_data.update({
                'zoning_code': row['zone_code'],
                'far_min': row['far_min'], 'far_opt': row['far_optimal'], 'far_max': row['far_max'],
                'h_min': row['height_min_m'], 'h_opt': row['height_optimal_m'], 'h_max': row['height_max_m'],
                'floors_max': row['max_floors'],
                'coverage_max': row['coverage_max_pct'],
                'setback_f': row['setback_front_m'], 'setback_r': row['setback_rear_m'], 'setback_s': row['setback_side_m'],
                'park_res': row['parking_ratio_residential'],
                'park_com': row['parking_ratio_commercial'],
                'park_hotel': row['parking_ratio_hotel'],
            })
            print(f"  Zoning: {row['zone_code']} — FAR {row['far_min']}–{row['far_max']}, H {row['height_min_m']}–{row['height_max_m']}m")
            return True
        return False

    def lookup_cost(self):
        emirate = self.derived_data.get('emirate', self.input_data.get('emirate',''))
        building_type = self.input_data.get('type','MIX')
        type_map = {
            'RES':'Residential','COM':'Commercial','MIX':'Mixed-Use',
            'HOT':'Hotel','RES-V':'Residential-Villa',
        }
        bt = type_map.get(building_type, 'Mixed-Use')
        quality = self.input_data.get('quality','Standard')
        c = self.conn.cursor()
        c.execute("""SELECT * FROM cost_matrix 
                     WHERE emirate=? AND building_type=? AND quality_level=?
                     LIMIT 1""", (emirate, bt, quality))
        row = c.fetchone()
        if not row:
            c.execute("""SELECT * FROM cost_matrix 
                         WHERE emirate=? AND building_type=?
                         LIMIT 1""", (emirate, bt))
            row = c.fetchone()
        if row:
            self.derived_data.update({
                'cost_structure': row['structure_aed_sqm'],
                'cost_mep': row['mep_aed_sqm'],
                'cost_finishes': row['finishes_aed_sqm'],
                'cost_facade': row['facade_aed_sqm'],
                'cost_total': row['total_construction_aed_sqm'],
                'cost_land': row['land_price_aed_sqm'],
                'soft_cost_pct': row['soft_cost_pct'],
                'contingency_pct': row['contingency_pct'],
            })
            print(f"  Cost: {row['total_construction_aed_sqm']} AED/m² ({quality})")
            return True
        return False

    def lookup_structural(self):
        floors = int(self.input_data.get('floors', 10) or 10)
        height_m = float(self.input_data.get('height', floors * 3.5) or floors * 3.5)
        soil = self.derived_data.get('soil_type', 'Dense Sand')
        building_type = self.input_data.get('type','MIX')
        type_map = {'RES':'Residential','COM':'Commercial','MIX':'Mixed-Use','HOT':'Hotel'}
        bt = type_map.get(building_type, 'Mixed-Use')
        c = self.conn.cursor()
        c.execute("""SELECT * FROM structural_matrix 
                     WHERE building_type=? AND height_min_m<=? AND height_max_m>=?
                     AND soil_types LIKE ?
                     LIMIT 1""", (bt, height_m, height_m, f'%{soil}%'))
        row = c.fetchone()
        if not row:
            c.execute("""SELECT * FROM structural_matrix 
                         WHERE building_type=? AND height_min_m<=? AND height_max_m>=?
                         LIMIT 1""", (bt, height_m, height_m))
            row = c.fetchone()
        if row:
            self.derived_data.update({
                'structural_system': row['structural_system'],
                'concrete_grade': row['concrete_grade'],
                'steel_grade': row['steel_grade'],
                'foundation_type': row['foundation_type'],
                'max_span': row['max_span_m'],
                'cost_factor': row['cost_factor'],
            })
            print(f"  Structure: {row['structural_system']} — {row['foundation_type']}")
            return True
        return False

    def lookup_fire(self):
        floors = int(self.input_data.get('floors', 10) or 10)
        height_m = float(self.input_data.get('height', floors * 3.5) or floors * 3.5)
        c = self.conn.cursor()
        c.execute("""SELECT * FROM fire_matrix 
                     WHERE height_min_m<=? AND height_max_m>=?
                     LIMIT 1""", (height_m, height_m))
        row = c.fetchone()
        if row:
            self.derived_data.update({
                'sprinkler': bool(row['sprinkler_required']),
                'fire_alarm': bool(row['fire_alarm_required']),
                'smoke_extraction': bool(row['smoke_extraction']),
                'refuge_floor': bool(row['refuge_floor']),
                'stair_count': row['stair_count_min'],
                'stair_width': row['stair_width_min_m'],
                'fire_rating': row['fire_rating_hours'],
            })
            print(f"  Fire: Sprinkler={row['sprinkler_required']}, Stairs={row['stair_count_min']}")
            return True
        return False

    def calculate_area(self):
        plot_area = self.derived_data.get('plot_area_sqm', 1500)
        far = self.derived_data.get('far_opt', 3.5)
        coverage = self.derived_data.get('coverage_max', 60)
        floors = int(self.input_data.get('floors', 10) or 10)

        footprint = plot_area * (coverage / 100)
        total_gfa = footprint * floors
        max_gfa = plot_area * far

        self.derived_data.update({
            'footprint': round(footprint, 1),
            'total_gfa': round(min(total_gfa, max_gfa), 1),
            'max_gfa': round(max_gfa, 1),
            'efficiency': round(total_gfa / max_gfa * 100, 1) if max_gfa > 0 else 0,
        })
        print(f"  Area: Footprint={footprint}m², GFA={total_gfa}m², Max={max_gfa}m²")

    def calculate_cost(self):
        gfa = self.derived_data.get('total_gfa', 1000)
        cost_sqm = self.derived_data.get('cost_total', 3500)
        land_sqm = self.derived_data.get('cost_land', 12000)
        plot_area = self.derived_data.get('plot_area_sqm', 1500)
        soft_pct = self.derived_data.get('soft_cost_pct', 12)
        cont_pct = self.derived_data.get('contingency_pct', 10)
        cost_factor = self.derived_data.get('cost_factor', 1.0)

        construction = gfa * cost_sqm * cost_factor
        land = plot_area * land_sqm
        soft = construction * (soft_pct / 100)
        contingency = construction * (cont_pct / 100)
        total = construction + land + soft + contingency

        self.derived_data.update({
            'construction_cost': round(construction, 0),
            'land_cost': round(land, 0),
            'soft_cost': round(soft, 0),
            'contingency_cost': round(contingency, 0),
            'total_project_cost': round(total, 0),
        })
        print(f"  Cost: Construction={construction:,.0f} AED, Land={land:,.0f} AED, Total={total:,.0f} AED")

    def generate_unit_mix(self):
        building_type = self.input_data.get('type','MIX')
        if building_type not in ('RES','MIX'):
            return
        total_units = int(self.input_data.get('units',{}).get('total', 0) or 0)
        if total_units == 0:
            gfa = self.derived_data.get('total_gfa', 5000)
            avg_unit = 120
            total_units = int(gfa / avg_unit * 0.85)

        self.derived_data['unit_mix'] = {
            'studios': int(total_units * 0.15),
            'one_bed': int(total_units * 0.35),
            'two_bed': int(total_units * 0.35),
            'three_bed': int(total_units * 0.12),
            'penthouses': int(total_units * 0.03),
            'total': total_units,
        }
        print(f"  Units: {total_units} total (S{int(total_units*0.15)}/1B{int(total_units*0.35)}/2B{int(total_units*0.35)}/3B{int(total_units*0.12)}/P{int(total_units*0.03)})")

    def generate_all(self):
        print("=" * 60)
        print("CASCADE ENGINE — Generating All Outputs")
        print("=" * 60)

        print("\n[1/7] Deriving from plot number...")
        self.derive_from_plot()

        print("[2/7] Looking up zoning matrix...")
        self.lookup_zoning()

        print("[3/7] Looking up cost matrix...")
        self.lookup_cost()

        print("[4/7] Looking up structural matrix...")
        self.lookup_structural()

        print("[5/7] Looking up fire matrix...")
        self.lookup_fire()

        print("[6/7] Calculating areas...")
        self.calculate_area()

        print("[7/7] Calculating costs...")
        self.calculate_cost()

        self.generate_unit_mix()

        self.outputs = {
            'input': self.input_data,
            'derived': self.derived_data,
            'generated_at': __import__('datetime').datetime.now().isoformat(),
        }

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        out_path = OUTPUT_DIR / "cascade_output.json"
        with open(out_path, 'w') as f:
            json.dump(self.outputs, f, indent=2, default=str)

        print(f"\n{'=' * 60}")
        print(f"OUTPUT SAVED: {out_path}")
        print(f"{'=' * 60}")
        print(f"\nReady to generate 116 deliverables from cascade_output.json")
        return self.outputs

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 cascade_engine.py <input.json>")
        print("Example: python3 cascade_engine.py project_input_data.json")
        sys.exit(1)

    engine = CascadeEngine()
    engine.load_input(sys.argv[1])
    engine.generate_all()

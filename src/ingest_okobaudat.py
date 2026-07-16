import sys
import os
import csv
import pandas as pd

sys.path.append('../building-data-repository/schemas')
from material import MaterialEntity

def run_pipeline():
    print("Starting Local CSV Data Ingestion Pipeline...")
    input_file = "data/raw/oekobaudat_data.csv" 
    
    df = pd.read_csv(input_file, encoding='latin1', sep=';')
    
    # 1. Deduplication: Take only the first entry for each unique UUID
    # This prevents the same material appearing 5 times with different scenario values
    df_unique = df.drop_duplicates(subset=['UUID'])
    
    validated_materials = []
    
    # 2. Process unique materials
    for _, row in df_unique.head(5).iterrows():
        try:
            # GWP choice logic: prefer A2 total, fallback to A1 (GWP)
            gwp = row.get("GWPtotal (A2)")
            if pd.isna(gwp) or gwp == 0:
                gwp = row.get("GWP", 0.1)
                
            mat = MaterialEntity(
                material_id=str(row.get("UUID", "unknown")),
                material_name=str(row.get("Name (en)", row.get("Name (de)", "unknown"))),
                gwp_total=float(gwp) if pd.notna(gwp) else 0.1,
                u_value=0.1,
                density=float(row.get("Rohdichte (kg/m3)", 10.0)),
                service_life=50
            )
            validated_materials.append(mat)
            print(f"Validated: {mat.material_name} | GWP: {mat.gwp_total}")
            
        except Exception as e:
            print(f"Validation failed: {e}")

    # Export
    os.makedirs("data/processed", exist_ok=True)
    with open("data/processed/materials.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=validated_materials[0].model_dump().keys())
        w.writeheader()
        for d in validated_materials: w.writerow(d.model_dump())
    print("Local ingestion complete.")

if __name__ == "__main__":
    run_pipeline()
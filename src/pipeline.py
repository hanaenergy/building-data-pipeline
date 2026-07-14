import os
import datetime
import pandas as pd
from load_data import load_data
from clean_data import clean_data
from geocode import geocode_buildings
from weather import fetch_climate_data
from benchmark import enrich_benchmark_data
from materials import calculate_embodied_carbon

def run_pipeline():
    """
    Master function to orchestrate the ETL pipeline.
    """
    print("="*60)
    print(" STARTING HANA ENERGY ETL PIPELINE v1.5")
    print("="*60)

    # 1. Define Paths
    input_file = os.path.join("data", "raw", "building_data.xlsx")
    output_dir = os.path.join("data", "processed")
    output_file = os.path.join(output_dir, "enriched_building_data.xlsx")

    os.makedirs(output_dir, exist_ok=True)

    # 2. Execute Pipeline Steps
    print("\n[STEP 1] Data Ingestion & Initial Validation")
    df_raw = load_data(input_file)
    if df_raw is None:
        print("[ERROR] Pipeline terminated due to missing input file.")
        return

    print("\n[STEP 2] Data Cleaning & Normalization")
    df_clean = clean_data(df_raw)

    print("\n[STEP 3] Geocoding (Address to Coordinates)")
    df_geo = geocode_buildings(df_clean)

    print("\n[STEP 4] Climate Data Enrichment (API)")
    df_weather = fetch_climate_data(df_geo, year=2023)

    print("\n[STEP 5] Reference Benchmark Enrichment")
    df_bench = enrich_benchmark_data(df_weather)
    
    print("\n[STEP 6] Material LCA Calculation (baubook)")
    df_lca = calculate_embodied_carbon(df_bench)

    # 3. Final Validation & Export
    print("\n[STEP 7] Final Data Quality Validation & Export")
    df_final = df_lca.copy()

    # Add Pipeline Metadata
    df_final['Processing_Timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_final['Pipeline_Version'] = "v1.5"

    print(f"[INFO] Exporting final dataset to: {output_file}")
    df_final.to_excel(output_file, index=False)

    print("\n" + "="*60)
    print(" PIPELINE EXECUTION COMPLETED SUCCESSFULLY")
    print("="*60)

if __name__ == "__main__":
    run_pipeline()
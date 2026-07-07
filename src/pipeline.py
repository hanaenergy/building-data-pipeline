import os
import datetime
import pandas as pd
from load_data import load_and_validate_data
from clean_data import clean_building_data
from geocode import geocode_buildings
from weather import fetch_climate_data
from benchmark import enrich_benchmark_data

def evaluate_data_quality(row):
    """
    Evaluate the final record to assign a Data_Quality_Flag.
    """
    if pd.isnull(row.get('Latitude')) or pd.isnull(row.get('Heating_Degree_Days')):
        return 'Warning: Missing API Data'
    elif pd.isnull(row.get('Annual_Energy_kWh')):
        return 'Warning: Missing Raw Energy Data'
    else:
        return 'Valid'

def run_pipeline():
    """
    Master function to orchestrate the ETL pipeline.
    """
    print("="*60)
    print(" STARTING HANA ENERGY ETL PIPELINE v1.0")
    print("="*60)

    # 1. Define Paths
    input_file = os.path.join("data", "raw", "building_data.xlsx")
    output_dir = os.path.join("data", "processed")
    output_file = os.path.join(output_dir, "enriched_building_data.xlsx")

    os.makedirs(output_dir, exist_ok=True)

    # 2. Execute Pipeline Steps
    print("\n[STEP 1] Data Ingestion & Initial Validation")
    df_raw = load_and_validate_data(input_file)
    if df_raw is None:
        print("[ERROR] Pipeline terminated due to missing input file.")
        return

    print("\n[STEP 2] Data Cleaning & Normalization")
    df_clean = clean_building_data(df_raw)

    print("\n[STEP 3] Geocoding (Address to Coordinates)")
    df_geo = geocode_buildings(df_clean)

    print("\n[STEP 4] Climate Data Enrichment (API)")
    df_weather = fetch_climate_data(df_geo, year=2023)

    print("\n[STEP 5] Reference Benchmark Enrichment")
    df_bench = enrich_benchmark_data(df_weather)

    # 3. Final Validation & Export
    print("\n[STEP 6] Final Data Quality Validation & Export")
    df_final = df_bench.copy()

    # Add Pipeline Metadata
    df_final['Data_Quality_Flag'] = df_final.apply(evaluate_data_quality, axis=1)
    df_final['Processing_Timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    df_final['Pipeline_Version'] = "v1.0"

    print(f"[INFO] Exporting final dataset to: {output_file}")
    df_final.to_excel(output_file, index=False)

    print("\n" + "="*60)
    print(" PIPELINE EXECUTION COMPLETED SUCCESSFULLY")
    print("="*60)

if __name__ == "__main__":
    run_pipeline()
import pandas as pd
import os

def enrich_benchmark_data(df):
    """
    Enrich building data with energy benchmarks (kWh/m2) based on 
    Building_Type and Construction_Year, simulating the EU TABULA database.
    
    Args:
        df (pd.DataFrame): Dataframe containing 'Building_Type' and 'Construction_Year'.
        
    Returns:
        pd.DataFrame: Enriched dataframe with 'Energy_Benchmark_kWh_m2' and 'Benchmark_Matched'.
    """
    print("[INFO] Starting benchmark data enrichment...")
    
    df_bench = df.copy()
    
    # Initialize new columns
    df_bench['Energy_Benchmark_kWh_m2'] = None
    df_bench['Benchmark_Matched'] = 'No'
    
    # 1. Define Mock TABULA Benchmark Reference (Austria)
    # Format: { 'Building_Type': { 'Year_Threshold': Benchmark_Value } }
    benchmark_ref = {
        'Office': {
            'old': 250,      # Before 1980
            'medium': 180,   # 1980 - 2000
            'new': 120       # After 2000
        },
        'Residential': {
            'old': 200,
            'medium': 150,
            'new': 90
        },
        'Retail': {
            'old': 300,
            'medium': 220,
            'new': 150
        }
    }
    
    success_count = 0
    
    # 2. Apply Mapping Logic
    for index, row in df_bench.iterrows():
        b_type = row.get('Building_Type')
        year = row.get('Construction_Year')
        
        # Skip if essential matching data is missing
        if pd.isnull(b_type) or pd.isnull(year):
            continue
            
        b_type = str(b_type).strip().title()
        
        # Determine age category
        if year < 1980:
            age_category = 'old'
        elif 1980 <= year <= 2000:
            age_category = 'medium'
        else:
            age_category = 'new'
            
        # Assign benchmark if building type exists in reference
        if b_type in benchmark_ref:
            benchmark_val = benchmark_ref[b_type][age_category]
            df_bench.at[index, 'Energy_Benchmark_kWh_m2'] = benchmark_val
            df_bench.at[index, 'Benchmark_Matched'] = 'Yes'
            success_count += 1
            
    # --- Data Quality Report (Benchmark Enrichment) ---
    missing_bench = len(df_bench) - success_count
    success_rate = (success_count / len(df_bench)) * 100 if len(df_bench) > 0 else 0
    
    print("\n" + "="*50)
    print(" DATA QUALITY REPORT: BENCHMARK ENRICHMENT")
    print("="*50)
    print(f"Total Buildings Processed : {len(df_bench)}")
    print(f"Benchmarks Matched        : {success_count} ({success_rate:.1f}%)")
    print(f"Benchmarks Missing        : {missing_bench}")
    print("="*50 + "\n")
    
    return df_bench

if __name__ == "__main__":
    # Test the benchmark module independently
    from load_data import load_and_validate_data
    from clean_data import clean_building_data
    
    target_file = os.path.join("data", "raw", "building_data.xlsx")
    raw_df = load_and_validate_data(target_file)
    
    if raw_df is not None:
        cleaned_df = clean_building_data(raw_df)
        bench_df = enrich_benchmark_data(cleaned_df)
        
        print("\n[INFO] Data Preview with Benchmarks (First 5 rows):")
        preview_cols = ['Building_ID', 'Building_Type', 'Construction_Year', 'Energy_Benchmark_kWh_m2', 'Benchmark_Matched']
        print(bench_df[preview_cols].head(5))
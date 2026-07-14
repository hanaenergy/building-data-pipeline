import pandas as pd
import os

def enrich_benchmark_data(df, tabula_csv_path=None):
    """
    Enrich building data with advanced TABULA reference data including U-values, 
    energy, primary energy, and CO2 reduction scenarios.
    """
    print("[INFO] Starting Advanced Reference Benchmark Mapping...")
    
    if tabula_csv_path is None:
        tabula_csv_path = os.path.join("data", "raw", "tabula_reference.csv")
        
    if not os.path.exists(tabula_csv_path):
        print(f"[ERROR] Benchmark reference file not found at {tabula_csv_path}")
        return df

    # Load offline master data
    ref_df = pd.read_csv(tabula_csv_path)
    
    # 1. Define the exact columns we want to extract from the CSV
    target_metrics = [
        'U_Wall_Cur', 'U_Roof_Cur', 'U_Window_Cur',
        'Energy_Cur_kWh', 'Energy_Std_kWh', 'Energy_Adv_kWh',
        'Primary_Cur_kWh', 'Primary_Std_kWh', 'Primary_Adv_kWh',
        'CO2_Cur_kg', 'CO2_Std_kg', 'CO2_Adv_kg', 'Source'
    ]
    
    # 2. Initialize these columns in our main dataframe to prevent KeyError
    for metric in target_metrics:
        df[metric] = None
        
    success_count = 0

    # 3. Iterate and map
    for index, row in df.iterrows():
        country = row.get('Country')
        b_type = row.get('Building_Type')
        year = row.get('Construction_Year')
        
        # Ensure all three matching keys exist
        if pd.notnull(country) and pd.notnull(b_type) and pd.notnull(year):
            # Filter the reference dataframe for Country, Type, and Year bracket
            match = ref_df[
                (ref_df['Country'] == country) &
                (ref_df['Building_Type'] == b_type) & 
                (ref_df['Year_Start'] <= year) & 
                (ref_df['Year_End'] >= year)
            ]
            
            if not match.empty:
                # Loop through all target metrics and assign them dynamically
                for metric in target_metrics:
                    df.at[index, metric] = match.iloc[0][metric]
                success_count += 1

    print(f"[INFO] Advanced Benchmark mapping completed. Successful matches: {success_count}/{len(df)}")
    return df
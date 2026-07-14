import pandas as pd
import os

def calculate_embodied_carbon(df, master_csv_path=None):
    """
    Merge building data with the baubook materials master data
    and calculate total embodied carbon (LCA).
    """
    print("[INFO] Starting Material Data (baubook) Enrichment & LCA Calculation...")

    # Set default path for master material file
    if master_csv_path is None:
        master_csv_path = os.path.join("data", "raw", "baubook_master.csv")

    # Check if master data exists to prevent pipeline crashes
    if not os.path.exists(master_csv_path):
        print(f"[ERROR] Master material file not found at {master_csv_path}")
        df['Total_Embodied_Carbon_kgCO2e'] = None
        df['Material_Match_Status'] = 'Failed: No Master File'
        return df

    # 1. Load the baubook master data
    master_df = pd.read_csv(master_csv_path)
    
    # 2. Merge (Join) the building dataset with the master dataset
    # We use 'left' join to ensure we don't lose any building records even if material is missing
    df_merged = pd.merge(
        df, 
        master_df, 
        how='left', 
        left_on='Primary_Material_ID', 
        right_on='Material_ID'
    )

    # 3. Initialize the target calculation columns
    df_merged['Total_Embodied_Carbon_kgCO2e'] = None
    df_merged['Material_Match_Status'] = 'No Material Data'

    success_count = 0
    
    # 4. Transform: Apply the LCA mathematical logic
    for index, row in df_merged.iterrows():
        qty = row.get('Material_Quantity_kg')
        factor = row.get('Embodied_Carbon_kgCO2e_per_kg')
        mat_id = row.get('Primary_Material_ID')
        
        # If both quantity and factor exist, calculate the footprint
        if pd.notnull(qty) and pd.notnull(factor):
            total_carbon = qty * factor
            df_merged.at[index, 'Total_Embodied_Carbon_kgCO2e'] = round(total_carbon, 2)
            df_merged.at[index, 'Material_Match_Status'] = 'Success'
            success_count += 1
        # If material ID exists but factor wasn't found in master data
        elif pd.notnull(mat_id) and pd.isnull(factor):
            df_merged.at[index, 'Material_Match_Status'] = 'Warning: Unknown Material ID'

    # Clean up duplicate 'Material_ID' column from the merge
    if 'Material_ID' in df_merged.columns:
        df_merged = df_merged.drop(columns=['Material_ID'])

    # --- Data Quality Report ---
    total_rows = len(df_merged)
    success_rate = (success_count / total_rows) * 100 if total_rows > 0 else 0
    
    print("\n" + "="*50)
    print(" DATA QUALITY REPORT: MATERIALS & LCA")
    print("="*50)
    print(f"Total Buildings Processed   : {total_rows}")
    print(f"Successful LCA Calculations : {success_count} ({success_rate:.1f}%)")
    print("="*50 + "\n")

    return df_merged

if __name__ == "__main__":
    # Independent module test
    from load_data import load_and_validate_data
    
    target_file = os.path.join("data", "raw", "building_data.xlsx")
    raw_df = load_and_validate_data(target_file)
    
    if raw_df is not None:
        lca_df = calculate_embodied_carbon(raw_df)
        
        print("\n[INFO] Data Preview with Embodied Carbon (First 5 records with materials):")
        # Filter preview to only show rows where we inputted test material data
        preview_cols = ['Building_ID', 'Primary_Material_ID', 'Material_Name', 'Total_Embodied_Carbon_kgCO2e', 'Material_Match_Status']
        print(lca_df[lca_df['Primary_Material_ID'].notnull()][preview_cols].head(5))
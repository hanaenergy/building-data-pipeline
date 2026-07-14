import os
import pandas as pd
import numpy as np

def _append_flag(existing_flag, new_message):
    """Helper function to append multiple flags with a separator."""
    if pd.isna(existing_flag) or existing_flag == "":
        return new_message
    return str(existing_flag) + " | " + new_message

def clean_data(df):
    print("[INFO] Starting data cleaning and validation process...")
    
    # 1. Rule: Duplicate Record (Warning)
    # Identify duplicates, drop the rest, and flag the kept record
    duplicates = df.duplicated(subset=['Building_ID'], keep=False)
    if duplicates.any():
        duplicate_ids = df[duplicates]['Building_ID'].unique()
        print(f"[WARNING] Found duplicate Building_IDs: {duplicate_ids}. Keeping first occurrence.")
        
        df = df.drop_duplicates(subset=['Building_ID'], keep='first')
        
        # Flag the surviving record
        mask_dup = df['Building_ID'].isin(duplicate_ids)
        df.loc[mask_dup, 'Data_Quality_Flag'] = df.loc[mask_dup, 'Data_Quality_Flag'].apply(
            lambda x: _append_flag(x, "WARNING: Duplicate Building_ID")
        )

    # 2. Rule: Invalid Postal Code (Warning)
    # Ensure it is treated as a string, check length and alphanumeric format
    def is_invalid_postal(pc):
        pc_str = str(pc).strip()
        if pd.isna(pc) or len(pc_str) < 4 or not pc_str.isalnum():
            return True
        return False
        
    mask_postal = df['Postal_Code'].apply(is_invalid_postal)
    df.loc[mask_postal, 'Data_Quality_Flag'] = df.loc[mask_postal, 'Data_Quality_Flag'].apply(
        lambda x: _append_flag(x, "WARNING: Invalid Postal Code")
    )
    
    # 3. Rule: Missing Energy Data (Warning)
    mask_energy_missing = df['Annual_Energy_kWh'].isna()
    df.loc[mask_energy_missing, 'Data_Quality_Flag'] = df.loc[mask_energy_missing, 'Data_Quality_Flag'].apply(
        lambda x: _append_flag(x, "WARNING: Missing Annual_Energy_kWh")
    )
    
    # 4. Rule: Energy Outlier (Outlier)
    # Calculate kWh/m2 to check for physical boundaries (10 ~ 1500)
    if 'Annual_Energy_kWh' in df.columns and 'Floor_Area_m2' in df.columns:
        energy_m2 = df['Annual_Energy_kWh'] / df['Floor_Area_m2']
        mask_outlier = (energy_m2 < 10) | (energy_m2 > 1500)
        
        df.loc[mask_outlier, 'Data_Quality_Flag'] = df.loc[mask_outlier, 'Data_Quality_Flag'].apply(
            lambda x: _append_flag(x, "OUTLIER: Energy/m2 out of expected bounds")
        )

    return df

if __name__ == "__main__":
    # Test the cleaning module independently
    from load_data import load_data # Fixed import name
    
    target_file = os.path.join("data", "raw", "building_data.xlsx")
    raw_df = load_data(target_file) # Fixed function name
    
    if raw_df is not None:
        cleaned_df = clean_data(raw_df) # Fixed function name
        
        print("[INFO] City distribution after cleaning:")
        print(cleaned_df['City'].value_counts())
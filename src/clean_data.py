import pandas as pd
import os

def clean_building_data(df):
    """
    Clean the raw building dataframe:
    1. Remove logical duplicates based on Address and Postal_Code.
    2. Normalize City names (e.g., 'wien', 'WIEN' -> 'Vienna').
    
    Args:
        df (pd.DataFrame): The raw dataframe.
        
    Returns:
        pd.DataFrame: The cleaned dataframe.
    """
    print("[INFO] Starting data cleaning process...")
    
    df_clean = df.copy()
    initial_rows = len(df_clean)
    
    # 1. Handle Logical Duplicates
    # Ignore 'Building_ID' and check for duplicates based on physical attributes
    subset_cols = ['Address', 'Postal_Code', 'Floor_Area_m2']
    df_clean = df_clean.drop_duplicates(subset=subset_cols, keep='first')
    dropped_dupes = initial_rows - len(df_clean)
    
    # 2. Normalize City Names
    if 'City' in df_clean.columns:
        df_clean['City'] = df_clean['City'].fillna('Unknown')
        df_clean['City'] = df_clean['City'].astype(str).str.strip().str.title()
        
        city_mapping = {
            'Wien': 'Vienna',
            'Vien': 'Vienna'
        }
        df_clean['City'] = df_clean['City'].replace(city_mapping)
        
    # --- Data Quality Report (Post-Cleaning) ---
    print("\n" + "="*50)
    print(" DATA QUALITY REPORT: POST-CLEANING")
    print("="*50)
    print(f"Rows Removed (Duplicates) : {dropped_dupes}")
    print(f"Final Cleaned Rows        : {len(df_clean)}")
    print("="*50 + "\n")
    
    return df_clean

if __name__ == "__main__":
    # Test the cleaning module independently
    from load_data import load_and_validate_data
    
    target_file = os.path.join("data", "raw", "building_data.xlsx")
    raw_df = load_and_validate_data(target_file)
    
    if raw_df is not None:
        cleaned_df = clean_building_data(raw_df)
        
        print("[INFO] City distribution after cleaning:")
        print(cleaned_df['City'].value_counts())
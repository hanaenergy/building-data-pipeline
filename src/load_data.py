import pandas as pd
import os

def load_and_validate_data(file_path):
    """
    Load raw building data from an Excel file and perform initial data quality validation.
    
    Args:
        file_path (str): Path to the raw Excel file.
        
    Returns:
        pd.DataFrame or None: Loaded dataframe if successful, None otherwise.
    """
    print(f"[INFO] Loading data from: {file_path}")
    
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        print(f"[ERROR] File not found: {file_path}")
        return None
        
    # --- Data Quality Report (Initial Load) ---
    print("\n" + "="*50)
    print(" DATA QUALITY REPORT: INITIAL LOAD")
    print("="*50)
    
    # 1. Row/Column count
    print(f"Total Rows Processed : {len(df)}")
    print(f"Total Columns        : {len(df.columns)}")
    
    # 2. Duplicate check
    duplicate_count = df.duplicated().sum()
    print(f"Duplicate Rows       : {duplicate_count}")
    
    # 3. Missing values check
    missing_values = df.isnull().sum()
    missing_cols = missing_values[missing_values > 0]
    
    if not missing_cols.empty:
        print("\n[WARNING] Missing Values Detected:")
        for col, count in missing_cols.items():
            print(f" - {col}: {count} missing")
    else:
        print("\n[INFO] No missing values detected.")
        
    print("="*50 + "\n")
    
    return df

if __name__ == "__main__":
    # Set file path relative to the project root
    target_file = os.path.join("data", "raw", "building_data.xlsx")
    
    # Execute function
    raw_df = load_and_validate_data(target_file)
    
    # Display preview
    if raw_df is not None:
        print("[INFO] Data Preview (First 3 rows):")
        print(raw_df.head(3))
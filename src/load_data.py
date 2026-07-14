import pandas as pd
import os

def load_data(file_path):
    print(f"[INFO] Loading data from: {file_path}")
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"[ERROR] File not found: {file_path}")
        
    df = pd.read_excel(file_path)
    
    # 1. Initialize Data Quality Flag column
    df['Data_Quality_Flag'] = ""
    
    # 2. Rule: Missing Core Identifier (Error)
    # Drop rows where Building_ID or Address is missing
    initial_row_count = len(df)
    df = df.dropna(subset=['Building_ID', 'Address'])
    dropped_rows = initial_row_count - len(df)
    
    if dropped_rows > 0:
        print(f"[ERROR] Dropped {dropped_rows} rows due to missing Building_ID or Address.")
        
    return df

if __name__ == "__main__":
    # Set file path relative to the project root
    target_file = os.path.join("data", "raw", "building_data.xlsx")
    
    # Execute function (Fixed function name)
    raw_df = load_data(target_file)
    
    # Display preview
    if raw_df is not None:
        print("[INFO] Data Preview (First 3 rows):")
        print(raw_df.head(3))
import pandas as pd
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import os

def geocode_buildings(df):
    """
    Convert building addresses into Latitude and Longitude using Nominatim API.
    Implements rate limiting to respect API usage policies.
    
    Args:
        df (pd.DataFrame): The cleaned dataframe containing address components.
        
    Returns:
        pd.DataFrame: The dataframe enriched with Latitude and Longitude.
    """
    print("[INFO] Starting geocoding process...")
    print("[INFO] Applying a 1-second delay between requests to respect Nominatim API limits.")
    
    # Initialize geocoder with a custom user_agent (required by Nominatim)
    geolocator = Nominatim(user_agent="hana_energy_etl_pipeline")
    
    # Apply RateLimiter (Nominatim requires max 1 request per second)
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1.1)
    
    df_geo = df.copy()
    
    # Create a full address string for maximum accuracy
    df_geo['Full_Address'] = (
        df_geo['Address'].astype(str) + ", " + 
        df_geo['Postal_Code'].astype(str) + ", " + 
        df_geo['City'].astype(str) + ", " + 
        df_geo['Country'].astype(str)
    )
    
    print(f"[INFO] Geocoding {len(df_geo)} addresses. This will take approximately {len(df_geo)} seconds...")
    
    # Apply geocoding logic
    df_geo['Location'] = df_geo['Full_Address'].apply(lambda x: geocode(x) if pd.notnull(x) else None)
    
    # Extract coordinates
    df_geo['Latitude'] = df_geo['Location'].apply(lambda loc: loc.latitude if loc else None)
    df_geo['Longitude'] = df_geo['Location'].apply(lambda loc: loc.longitude if loc else None)
    
    # Drop temporary columns
    df_geo = df_geo.drop(columns=['Full_Address', 'Location'])
    
    # --- Data Quality Report (Geocoding) ---
    success_count = df_geo['Latitude'].notnull().sum()
    failed_count = len(df_geo) - success_count
    success_rate = (success_count / len(df_geo)) * 100
    
    print("\n" + "="*50)
    print(" DATA QUALITY REPORT: GEOCODING")
    print("="*50)
    print(f"Total Addresses Processed : {len(df_geo)}")
    print(f"Successful Geocodes       : {success_count} ({success_rate:.1f}%)")
    print(f"Failed Geocodes           : {failed_count}")
    print("="*50 + "\n")
    
    # Log the IDs of failed geocodes for further inspection
    if failed_count > 0:
        print("[WARNING] The following Building_IDs failed to geocode (likely invalid addresses):")
        failed_ids = df_geo[df_geo['Latitude'].isnull()]['Building_ID'].tolist()
        print(f" - {failed_ids}")
        
    return df_geo

if __name__ == "__main__":
    # Test the geocoding module independently
    from load_data import load_and_validate_data
    from clean_data import clean_building_data
    
    target_file = os.path.join("data", "raw", "building_data.xlsx")
    raw_df = load_and_validate_data(target_file)
    
    if raw_df is not None:
        cleaned_df = clean_building_data(raw_df)
        geo_df = geocode_buildings(cleaned_df)
        
        print("\n[INFO] Data Preview with Coordinates (First 3 rows):")
        print(geo_df[['Building_ID', 'Address', 'Latitude', 'Longitude']].head(3))
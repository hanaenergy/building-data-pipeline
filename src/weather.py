import pandas as pd
import requests
import time
import os

def fetch_climate_data(df, year=2023):
    """
    Fetch daily mean temperature from Open-Meteo Historical API 
    and calculate annual Heating Degree Days (HDD) base 18°C.
    
    Args:
        df (pd.DataFrame): Dataframe containing 'Latitude' and 'Longitude'.
        year (int): The reference year for historical climate data.
        
    Returns:
        pd.DataFrame: Enriched dataframe with 'Heating_Degree_Days'.
    """
    print(f"[INFO] Starting climate data enrichment for reference year {year}...")
    
    df_weather = df.copy()
    df_weather['Heating_Degree_Days'] = None
    
    total_rows = len(df_weather)
    success_count = 0
    
    print(f"[INFO] Fetching climate data and calculating HDD for {total_rows} locations...")
    
    for index, row in df_weather.iterrows():
        lat = row.get('Latitude')
        lon = row.get('Longitude')
        
        # Skip if coordinates are missing
        if pd.isnull(lat) or pd.isnull(lon):
            continue
            
        # 1. Fetch raw daily mean temperature (temperature_2m_mean)
        url = (
            f"https://archive-api.open-meteo.com/v1/archive?"
            f"latitude={lat}&longitude={lon}&"
            f"start_date={year}-01-01&end_date={year}-12-31&"
            f"daily=temperature_2m_mean&timezone=auto"
        )
        
        try:
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                daily_temps = data.get('daily', {}).get('temperature_2m_mean', [])
                
                # Filter out missing daily records
                valid_temps = [t for t in daily_temps if t is not None]
                
                if valid_temps:
                    # 2. Transform: Apply Business Logic (Calculate HDD Base 18)
                    # Formula: max(0, 18.0 - daily_mean_temperature)
                    annual_hdd = sum(max(0, 18.0 - t) for t in valid_temps)
                    
                    df_weather.at[index, 'Heating_Degree_Days'] = round(annual_hdd, 1)
                    success_count += 1
            else:
                print(f"[WARNING] API Error for Building_ID {row['Building_ID']}: Status {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Request failed for Building_ID {row['Building_ID']}: {e}")
            
        # Rate limiting: wait 0.5 seconds between requests
        time.sleep(0.5)
        
    # --- Data Quality Report (Climate Enrichment) ---
    missing_hdd = len(df_weather) - success_count
    success_rate = (success_count / len(df_weather)) * 100 if len(df_weather) > 0 else 0
    
    print("\n" + "="*50)
    print(" DATA QUALITY REPORT: CLIMATE ENRICHMENT")
    print("="*50)
    print(f"Total Locations Processed : {len(df_weather)}")
    print(f"Successful API Matches    : {success_count} ({success_rate:.1f}%)")
    print(f"Missing Climate Data      : {missing_hdd}")
    print("="*50 + "\n")
    
    return df_weather

if __name__ == "__main__":
    # Test the weather module independently
    from load_data import load_and_validate_data
    from clean_data import clean_building_data
    from geocode import geocode_buildings
    
    target_file = os.path.join("data", "raw", "building_data.xlsx")
    raw_df = load_and_validate_data(target_file)
    
    if raw_df is not None:
        cleaned_df = clean_building_data(raw_df)
        geo_df = geocode_buildings(cleaned_df)
        weather_df = fetch_climate_data(geo_df)
        
        print("\n[INFO] Data Preview with Climate Data (First 3 rows):")
        print(weather_df[['Building_ID', 'City', 'Latitude', 'Heating_Degree_Days']].head(3))
import requests
import sys
import json
import csv
import os

# Import schema from the repository
sys.path.append('../building-data-repository/schemas')
from material import MaterialEntity

def fetch_okobaudat_metadata(limit=5):
    url = f"https://www.oekobaudat.de/OEKOBAU.DAT/resource/processes?format=json&search=true&startIndex=0&pageSize={limit}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])
        
    except requests.exceptions.RequestException as e:
        print(f"API Connection Error: {e}")
        return []

def export_to_csv(materials, filename="data/processed/materials.csv"):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    if not materials:
        print("No materials to export.")
        return

    # Extract field names automatically from the Pydantic schema
    fieldnames = list(materials[0].model_dump().keys())
    
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for mat in materials:
            writer.writerow(mat.model_dump())
            
    print(f"Successfully exported {len(materials)} records to {filename}")

def run_pipeline():
    print("Starting OKOBAUDAT Data Ingestion Pipeline...")
    raw_data = fetch_okobaudat_metadata(limit=5)
    
    validated_materials = []
    
    for item in raw_data:
        try:
            material = MaterialEntity(
                material_id=item.get("uuid", "Unknown"),
                material_name=item.get("name", "Unknown Material"),
                u_value=0.1, 
                gwp_total=0.0,
                density=10.0,
                service_life=50
            )
            validated_materials.append(material)
        except Exception as e:
            print(f"Validation Error for {item.get('name')}: {e}")
            
    if validated_materials:
        export_to_csv(validated_materials)

if __name__ == "__main__":
    run_pipeline()
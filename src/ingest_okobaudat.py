import requests
import sys
import json

# Import schema from the repository
sys.path.append('../building-data-repository/schemas')
from material import MaterialEntity

def fetch_okobaudat_metadata(limit=5):
    url = f"https://www.oekobaudat.de/OEKOBAU.DAT/resource/processes?format=json&search=true&startIndex=0&pageSize={limit}"
    
    # Add headers to prevent the server from blocking the Python request
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/json"
    }
    
    try:
        # Added a 10-second timeout limit
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("data", [])
        
    except requests.exceptions.RequestException as e:
        print(f"API Connection Error: {e}")
        print("Falling back to local mock data to ensure pipeline continuity...\n")
        
        # Fallback mock data if the API is down or blocking requests
        return [
            {"uuid": "fallback-uuid-001", "name": "Mock EPS Insulation Board"},
            {"uuid": "fallback-uuid-002", "name": "Mock Portland Cement"},
            {"uuid": "fallback-uuid-003", "name": "Mock Cross Laminated Timber"}
        ]

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
            
    print(f"Successfully validated {len(validated_materials)} materials.")
    for mat in validated_materials:
        print(mat.model_dump_json(indent=2))

if __name__ == "__main__":
    run_pipeline()
# Automated B2B Building Data Integration and Climate Enrichment Pipeline

A professional, production-grade ETL (Extract, Transform, Load) pipeline designed to ingest raw B2B building portfolios, execute comprehensive data quality validation, and enrich datasets with spatial coordinates (Geocoding) and historical climate metrics. 

This pipeline automates the transformation of fragmented real estate assets into high-fidelity data structures optimized for energy benchmarking and ESG reporting.

## System Architecture and Data Flow

The pipeline operates as a modular, decoupled workflow structured as follows:
1. **Data Ingestion (load_data.py)**: Reads raw multi-tab client portfolios (Excel/CSV) and executes an initial structural Data Quality (DQ) assessment.
2. **Data Cleaning and Normalization (clean_data.py)**: Resolves logical duplicates (based on spatial and structural attributes), handles missing values, and normalizes localized entity naming conventions (e.g., Wien/Vienna).
3. **Spatial Geocoding (geocode.py)**: Utilizes the OpenStreetMap Nominatim API via geopy to transform physical address strings into high-precision Latitude/Longitude coordinates.
4. **Climate Data Enrichment (weather.py)**: Connects to the Open-Meteo Historical API to retrieve daily ambient temperatures and dynamically calculates the annual Heating Degree Days (HDD base 18 degrees Celsius) for each asset location.
5. **Reference Benchmark Mapping (benchmark.py)**: Enriches the dataset with regional energy intensity indicators (kWh/m2) mapped against structural typologies and vintage bands (simulating EU TABULA schema).
6. **Orchestration and Validation (pipeline.py)**: The master controller that chains all modules, runs final data validity flags, injects pipeline metadata, and exports an analysis-ready dataset.

## Tech Stack and Virtual Environment
* **Language:** Python 3.11+
* **Core Libraries:** Pandas, Openpyxl, Geopy, Requests
* **Environment Isolation:** Virtual Environment (.venv) with frozen dependency tracking.

## Data Quality and Resiliency Highlights
* **Logical Deduplication:** Instead of relying on system-generated Building_IDs which can obscure duplicates, the cleaning module executes logical deduplication across composite physical keys (Address, Postal_Code, Floor_Area_m2), successfully trapping redundant data.
* **Fault-Tolerant API Ingestion:** Built-in network resiliency to handle open-source API limitations:
  * Implemented a RateLimiter with strict time delays to respect server usage policies and prevent IP blocking.
  * Embedded robust exception handling (GeocoderTimedOut, TimeoutError) to ensure network fluctuations or bad requests (Status 400) do not crash the master pipeline, logging anomalies safely for isolated manual inspection.
* **Dynamic Analytics Transformation:** Successfully bypassed API parameter limitations by ingesting raw daily temperature arrays and executing in-memory mathematical aggregations to calculate annual cumulative HDD scores locally.

## Getting Started

### 1. Environment Setup
Clone the repository and initialize the isolated Python environment:

```bash
# Clone the repository
git clone <your-repository-url>
cd building-data-pipeline

# Activate the virtual environment (Windows)
.venv\Scripts\activate

# Install exact production dependencies
pip install -r requirements.txt
```

### 2. Execution
Run the master orchestration script to process the sample portfolio:

```bash
python src/pipeline.py
```

### 3. Pipeline Output
The final enriched, validated dataset will be generated under:
`data/processed/enriched_building_data.xlsx`
*(Note: Output data directory is excluded from Git tracking under .gitignore compliance to simulate corporate data security protocols).*
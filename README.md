# Automated Building Data ETL Pipeline

A professional, production-grade ETL (Extract, Transform, Load) pipeline designed to ingest building portfolios, environmental datasets, and material databases. It executes comprehensive data quality validation against centralized schemas and enriches datasets for ESG reporting, energy benchmarking, and retrofit analysis.

This pipeline serves as the execution engine for the Hana Energy ecosystem, consuming validation rules from the adjacent `building-data-repository`.

## System Architecture and Data Flow

The pipeline operates as a modular workflow relying on strict Pydantic schemas:
1. **Schema Integration**: Dynamically imports core entities (Building, Material, Climate) from the adjacent `building-data-repository` to enforce strict data validation.
2. **Material Data Ingestion (ingest_okobaudat.py)**: Connects to the OKOBAUDAT API to extract standardized construction material properties, validating them against the MaterialEntity schema and exporting analysis-ready data to CSV.
3. **Portfolio Ingestion and Initial Validation (load_data.py)**: Reads raw multi-tab client portfolios (Excel/CSV) and executes structural Data Quality (DQ) assessment, immediately isolating critical errors.
4. **Data Cleaning and Normalization (clean_data.py)**: Resolves logical duplicates, handles missing values, and flags warnings/outliers without halting the pipeline, ensuring maximum data retention for analytical auditing.
5. **Spatial Geocoding (geocode.py)**: Utilizes the OpenStreetMap Nominatim API via geopy to transform physical address strings into high-precision Latitude/Longitude coordinates.
6. **Climate Data Enrichment (weather.py)**: Connects to the Open-Meteo Historical API to retrieve daily ambient temperatures and dynamically calculates the annual Heating Degree Days (HDD base 18 degrees Celsius) for each asset location.
7. **Advanced Reference Benchmark Mapping (benchmark.py)**: Enriches the dataset with comprehensive Austrian TABULA typologies, including U-values, current energy intensity, and advanced retrofitting scenarios covering primary energy and CO2 emissions.
8. **Orchestration and Quality Reporting (pipeline.py)**: The master controller that chains all modules, injects pipeline metadata, outputs an automated Data Quality Summary Report to the terminal, and exports an analysis-ready dataset.

## Tech Stack and Virtual Environment
* **Language:** Python 3.10+
* **Core Libraries:** Pydantic, Pandas, Openpyxl, Geopy, Requests
* **Architecture:** Decoupled ETL engine with external schema dependencies.

## Data Quality and Resiliency Highlights
* **Strict Schema Enforcement:** All incoming data is validated against central Pydantic models before processing, ensuring zero schema drift and maintaining absolute data integrity.
* **Fault-Tolerant API Ingestion:** Built-in network resiliency to handle open-source API limitations and unstable endpoints:
  * Custom User-Agent headers, timeout limits, and local mock data fallbacks to ensure pipeline continuity.
  * Implemented a RateLimiter with strict time delays to respect server usage policies and prevent IP blocking.
* **Automated Quality Gateway:** Every record passes through a strict rules engine assigning Error, Warning, or Outlier flags. The pipeline generates a summarized terminal report outlining issue breakdowns for immediate auditing.
* **Dynamic Analytics Transformation:** Successfully bypassed API parameter limitations by ingesting raw daily temperature arrays and executing in-memory mathematical aggregations to calculate annual cumulative HDD scores locally.

## Getting Started

### 1. Repository Structure Prerequisite
Because this pipeline relies on centralized schemas, ensure both repositories are cloned in the same parent directory to allow local imports:

```text
Projects/
├── building-data-repository/    # Core schemas and data dictionary
└── building-data-pipeline/      # This ETL engine
```

### 2. Environment Setup
Navigate to the pipeline repository and initialize the isolated Python environment:

```bash
cd building-data-pipeline

# Activate the virtual environment (Windows)
.\.venv\Scripts\activate

# Install exact production dependencies
pip install -r requirements.txt
```

### 3. Execution
Run the OKOBAUDAT material ingestion module:

```bash
python src/ingest_okobaudat.py
```

Run the master portfolio orchestration script:
```bash
python src/pipeline.py
```

### 4. Pipeline Output
Processed and enriched datasets will be generated under the `data/processed/` directory.

(Note: Output data directories are excluded from Git tracking under .gitignore compliance to simulate corporate data security protocols).
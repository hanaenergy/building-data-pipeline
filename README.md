# Automated B2B Building Data Integration and Climate Enrichment Pipeline

A professional, production-grade ETL (Extract, Transform, Load) pipeline designed to ingest raw B2B building portfolios, execute comprehensive data quality validation, and enrich datasets with spatial coordinates (Geocoding) and historical climate metrics. 

This pipeline automates the transformation of fragmented real estate assets into high-fidelity data structures optimized for energy benchmarking, ESG reporting, and future financial impact analysis.

## System Architecture and Data Flow

The pipeline operates as a modular, decoupled workflow structured as follows:
1. **Data Ingestion & Initial Validation (load_data.py)**: Reads raw multi-tab client portfolios (Excel/CSV) and executes structural Data Quality (DQ) assessment, immediately isolating critical errors.
2. **Data Cleaning and Normalization (clean_data.py)**: Resolves logical duplicates, handles missing values, and flags warnings/outliers without halting the pipeline, ensuring maximum data retention for analytical auditing.
3. **Spatial Geocoding (geocode.py)**: Utilizes the OpenStreetMap Nominatim API via geopy to transform physical address strings into high-precision Latitude/Longitude coordinates.
4. **Climate Data Enrichment (weather.py)**: Connects to the Open-Meteo Historical API to retrieve daily ambient temperatures and dynamically calculates the annual Heating Degree Days (HDD base 18 degrees Celsius) for each asset location.
5. **Advanced Reference Benchmark Mapping (benchmark.py)**: Enriches the dataset with comprehensive Austrian TABULA typologies, including U-values, current energy intensity, and advanced retrofitting scenarios (Standard/NZEB) covering primary energy and CO2 emissions.
6. **Orchestration and Quality Reporting (pipeline.py)**: The master controller that chains all modules, injects pipeline metadata, outputs an automated Data Quality Summary Report to the terminal, and exports an analysis-ready dataset.

## Tech Stack and Virtual Environment
* **Language:** Python 3.11+
* **Core Libraries:** Pandas, Openpyxl, Geopy, Requests
* **Environment Isolation:** Virtual Environment (.venv) with frozen dependency tracking.

## Data Quality and Resiliency Highlights
* **Automated Quality Gateway:** Every record passes through a strict rules engine assigning Error, Warning, or Outlier flags. The pipeline generates a summarized terminal report outlining issue breakdowns for immediate auditing.
* **Fault-Tolerant API Ingestion:** Built-in network resiliency to handle open-source API limitations:
  * Implemented a RateLimiter with strict time delays to respect server usage policies and prevent IP blocking.
  * Embedded robust exception handling to ensure network fluctuations or bad requests do not crash the master pipeline.
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

(Note: Output data directory is excluded from Git tracking under .gitignore compliance to simulate corporate data security protocols).
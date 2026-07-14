# Project Specification

## 1. Project Overview

### Objective
Transform messy building data into a trusted analysis-ready dataset by enforcing rigorous quality validation and enriching it with public climate metrics and advanced building reference data.

### Target Users
- Energy consulting firms
- Property management companies
- Sustainability teams
- Data analysts

---

## 2. Business Problem

Building data is often stored in Excel files with inconsistent addresses, missing values, and duplicated records. Manually cleaning and enriching this data is time-consuming and error-prone. This project automates the ETL process, establishing a reliable ground truth for downstream ESG reporting and financial decision-making.

---

## 3. Input Dataset

| Column | Description |
|---------|-------------|
| Building_ID | Unique identifier |
| Address | Building address |
| Postal_Code | Postal code |
| City | City |
| Country | Country |
| Construction_Year | Construction year |
| Building_Type | SFH, TH, MFH, AB, Office, Retail |
| Floor_Area_m2 | Gross floor area |
| Heating_System | Gas, Oil, Heat Pump, District |
| Annual_Energy_kWh | Annual energy consumption |

---

## 4. Data Quality Rules

To ensure high reliability and build a trusted dataset, all incoming data must pass through a strict validation gateway. The pipeline evaluates records based on the following rules and assigns a `Data_Quality_Flag`. 

| Validation Stage | Rule Name | Target Field(s) | Condition / Threshold | Severity | System Action |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Ingestion** | Missing Core Identifier | `Building_ID`, `Address` | is NULL or Empty | **Error** | Drop row, log to error file |
| **Ingestion** | Duplicate Record | `Building_ID` | Count > 1 | **Warning** | Keep first occurrence, drop duplicates, flag record |
| **Ingestion** | Invalid Postal Code | `Postal_Code` | Length < 4 or non-alphanumeric | **Warning** | Flag record, proceed to geocoding |
| **Geocoding** | Geocoding Failure | `Latitude`, `Longitude` | API returns NULL | **Error** | Drop row, log to error file (Cannot fetch climate data) |
| **Climate** | Missing Weather Data | `Heating_Degree_Days` | API returns NULL | **Warning** | Flag record, proceed without climate context |
| **Benchmark** | Missing Mapping Keys | `Country`, `Building_Type`, `Construction_Year` | is NULL or Unrecognized | **Warning** | Flag record, leave Benchmark fields NULL |
| **Business Logic** | Missing Energy Data | `Annual_Energy_kWh` | is NULL | **Warning** | Flag record, skip efficiency difference calculation |
| **Business Logic** | Energy Outlier | `Annual_Energy_kWh_m2` | < 10 or > 1500 kWh/m²a | **Outlier** | Flag record for manual review |

### Severity Definitions
* **Error:** A critical flaw that prevents the pipeline from processing the record further. The record is dropped from the main dataset and isolated for review.
* **Warning:** The record can proceed through the pipeline, but the missing or invalid data may degrade analytical quality. A flag is appended to the final output.
* **Outlier:** The data format is valid, but the physical or business value is highly unrealistic (e.g., residential energy consumption matching industrial levels). The record is processed but flagged for auditor review.

---

## 5. External Data Sources

### Geocoding
- geopy (Nominatim)

### Climate Data
- Open-Meteo Historical Weather API

### Reference Data
- Austrian TABULA Typology Matrix (Scientific Report D 6.9)

---

## 6. ETL Pipeline

1. **Load:** Ingest raw dirty Excel files.
2. **Validate:** Drop critical errors based on Data Quality Rules.
3. **Clean:** Normalize strings, handle duplicates, and flag warnings/outliers.
4. **Geocode:** Translate physical addresses to coordinates.
5. **Climate API:** Fetch and calculate Heating Degree Days.
6. **Benchmark Merge:** Map advanced structural and energy retrofitting scenarios.
7. **Quality Report:** Generate automated terminal summary of data integrity.
8. **Export:** Save final enriched dataset with pipeline metadata.

---

## 7. Output Dataset

In addition to the cleaned input columns, the output dataset includes the following enriched fields:

**Spatial & Climate Metrics**
- `Latitude`, `Longitude`
- `Heating_Degree_Days`

**Benchmark & Retrofitting Scenarios (TABULA)**
- `U_Wall_Cur`, `U_Roof_Cur`, `U_Window_Cur`
- `Energy_Cur_kWh`, `Energy_Std_kWh`, `Energy_Adv_kWh`
- `Primary_Cur_kWh`, `Primary_Std_kWh`, `Primary_Adv_kWh`
- `CO2_Cur_kg`, `CO2_Std_kg`, `CO2_Adv_kg`
- `Source`

**Pipeline Metadata**
- `Data_Quality_Flag`
- `Processing_Timestamp`
- `Pipeline_Version`

---

## 8. Development Roadmap

The project is structured into a phased growth model, prioritizing data integrity before feature expansion.

### MVP v1: Trusted Data Foundation (Completed)
- Robust ETL pipeline architecture.
- Strict data quality validation and terminal reporting.
- Advanced TABULA benchmark integration.

### MVP v2: Financial Engine (Next)
- Translate energy gaps into business intelligence.
- Estimate potential OPEX savings (EUR) for retrofitting scenarios.
- Implement a `Confidence_Score` based on data quality flags and mapping accuracy to guide decision-making.

### MVP v3: Interactive Dashboard
- Build a Streamlit application to visualize the trusted dataset.
- Map-based portfolio overview and scenario comparison tools for investor demonstrations.

### MVP v4: Operational Cloud Integration
- Migrate from flat files to a relational database (PostgreSQL).
- Containerize the application (Docker) for cloud deployment.
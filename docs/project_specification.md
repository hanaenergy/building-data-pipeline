# Project Specification

## 1. Project Overview

### Objective
Transform messy building data into a trusted analysis-ready dataset by enriching it with public climate and building reference data.

### Target Users
- Energy consulting firms
- Property management companies
- Sustainability teams
- Data analysts

---

## 2. Business Problem

Building data is often stored in Excel files with inconsistent addresses, missing values, and duplicated records.

Manually cleaning and enriching this data is time-consuming and error-prone.

This project automates the process.

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
| Building_Type | Office, Residential, Retail |
| Floor_Area_m2 | Gross floor area |
| Heating_System | Gas, Oil, Heat Pump |
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

## 5. External Data Sources

### Geocoding
- geopy (Nominatim)

### Climate Data
- Open-Meteo API

### Reference Data
- TABULA
- EU Building Stock Observatory

---

## 6. ETL Pipeline

1. Load raw Excel
2. Validate raw data
3. Clean building information
4. Normalize addresses
5. Geocode addresses
6. Enrich climate data
7. Enrich benchmark data
8. Validate enriched dataset
9. Export final dataset

---

## 7. Output Dataset

Additional columns

- Latitude
- Longitude
- Heating_Degree_Days
- Energy_Benchmark_kWh_m2
- Data_Quality_Flag
- Processing_Timestamp

---

## 8. Future Enhancements

- Carbon emission estimation
- Dashboard
- Streamlit interface
- PostgreSQL integration
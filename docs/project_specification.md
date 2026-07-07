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

## 4. External Data Sources

### Geocoding
- geopy (Nominatim)

### Climate Data
- Open-Meteo API

### Reference Data
- TABULA
- EU Building Stock Observatory

---

## 5. ETL Pipeline

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

## 6. Output Dataset

Additional columns

- Latitude
- Longitude
- Heating_Degree_Days
- Energy_Benchmark_kWh_m2
- Data_Quality_Flag
- Processing_Timestamp

---

## 7. Future Enhancements

- Carbon emission estimation
- Dashboard
- Streamlit interface
- PostgreSQL integration
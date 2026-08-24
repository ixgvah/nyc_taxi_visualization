# 🚖 NYC Taxi Data Visualization (Power BI)

Interactive Power BI dashboard analyzing **105M NYC Taxi trips** (Yellow & Green Taxi) across **2019–2023**. The report focuses on fleet comparison, geographical trip distribution, and temporal demand patterns.

---

## Project Overview & Key Questions

The goal of this project was to design a high-performance Power BI business intelligence solution to help **fleet managers, city planners, and data analysts** understand urban mobility patterns, pricing dynamics, and fleet utilization in New York City.

The dashboard answers the following business questions:

1. **Volume & Rush Hours:** What is the total volume of rides and passengers, and at what times of day is demand highest?
2. **Fleet Comparison:** How does market share split between Yellow Taxi and Green Taxi?
3. **Economics & Tips:** What are the average fare, total payment, and tip amounts?
4. **Trip Duration:** What is the average duration of a taxi ride?
5. **Geospatial Hotspots:** What are the top high-demand pickup zones across NYC?
6. **Payment Preferences:** What is the breakdown between credit card and cash transactions?
7. **Trip Corridors:** Which pickup-to-dropoff corridors generate the heaviest traffic?
8. **Peak Patterns:** Which day of the week and specific hour represent peak demand?
9. **Year-over-Year Dynamics:** How did ride volume and pricing change year-over-year?
10. **Workday vs. Weekend:** How do fares and tipping behaviors differ between weekdays and weekends?
11. **Seasonality:** Which months experience the highest demand?
12. **Pandemic Impact:** How severely did COVID-19 impact taxi demand, and what did the recovery trajectory look like?

---

## Datasets & Sources

Data was sourced directly from the **NYC Taxi & Limousine Commission (TLC)**:
* **Official Data Page:** [NYC TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
* **Data Dictionaries:**
  * [Yellow Taxi Dictionary (PDF)](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf)
  * [Green Taxi Dictionary (PDF)](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_green.pdf)

The dataset covers **2019–2023** to capture long-term structural market shifts and track recovery following the COVID-19 pandemic.

---

## Data Engineering with PySpark

Raw monthly Parquet files contain millions of unaggregated trip-level records. To eliminate memory bottlenecks in Power BI while retaining full analytical precision, a custom ETL pipeline was implemented in **PySpark**.

### Data Processing & Cleaning Logic:
* **Schema Standardization:** Unified differing column schemas between Yellow (`tpep_*`) and Green (`lpep_*`) taxi datasets.
* **Data Cleansing:** Filtered out invalid records (e.g., negative `fare_amount`, negative `trip_distance`, out-of-scope trip timestamps).

### Aggregation Grain:
Data was aggregated by the following dimensions: `taxi_type` | `pickup_date` | `pickup_hour` | `pickup_location_key` | `dropoff_location_key` | `rate_code_key` | `payment_type`.  
The purpose was to optimize query performance and reduce overall dataset volume.

### Extracted Aggregations:
* `trip_count`: Total number of rides (provides the weight for accurate ratio calculations in DAX).
* `total_passengers`: Sum of passengers across trips.
* `total_distance`: Sum of miles driven.
* `total_duration_minutes`: Sum of all trip durations in minutes (enabling true weighted average trip duration in Power BI).
* `total_fare`: Base metered fare amounts.
* `tips_amount`: Recorded credit card tips.
* `tolls_amount`: Highway and bridge toll fees.
* `congestion_surcharge`: NYC congestion pricing charges.
* `extra`: Rush-hour and overnight extras.
* `total_amount`: Grand total charged to passengers.

---

## 📊 Dashboard Views & Key Insights
### 1. Executive Summary & Fleet Dynamics
<img width="1268" height="1078" alt="image" src="https://github.com/user-attachments/assets/4ac075af-924e-42ba-9f66-2903096860d8" />

### 2. Geospatial & Route Analysis
<img width="1244" height="1074" alt="image" src="https://github.com/user-attachments/assets/62804881-92f5-4044-ad64-44db7a9505ca" />

### 3. Temporal Demand & Rush-Hour Trends
<img width="1296" height="1096" alt="image" src="https://github.com/user-attachments/assets/a6ef580b-ab54-4237-8e18-2a9923e2ca09" />

### 4. Pricing, Tipping & Economic Indicators
<img width="1280" height="1032" alt="image" src="https://github.com/user-attachments/assets/68a8e354-daad-4ee5-acd8-14b717033437" />

---

## 🚀 How to View the Dashboard

1. Download the `.pbix` file from the **[Releases](https://github.com/ixgvah/nyc_taxi_report/releases/tag/v1.1)** tab.
2. Open locally using **Microsoft Power BI Desktop**.

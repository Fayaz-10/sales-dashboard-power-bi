# Data Quality Audit & Cleaning Report
**Source File:** `data/raw_sales_data.csv`  **Initial Row Count:** 2,535  **Initial Column Count:** 18  
## 1. Initial Data Quality Diagnostics
- **Duplicate Order IDs Detected:** 35 rows- **Missing Values per Column:**  - `State`: 12 missing values  - `Payment_Method`: 8 missing values
---
## 2. Transformation & Cleaning Execution Steps
### Step 1: Deduplication
- **Rule:** Identify redundant order records by primary key (`Order_ID`) and retain only the first valid instance.
- **Impact:** Removed 35 duplicate records. Current rows: 2,500.
### Step 2: Text Standardization & Whitespace Sanitization
- **Rule:** Trim leading/trailing whitespace across all text columns.
- **Impact:** Sanitized string values. Row count unchanged.
### Step 3: Product Catalog Canonicalization
- **Rule:** Map `Product_ID` to canonical `Category`, `Subcategory`, and `Unit_Price` to eliminate catalog corruption.
- **Impact:** Exactly 20 unique product SKUs with 100% primary key uniqueness for `Dim_Product`.
### Step 4: Geographic State-to-Region Standardization
- **Rule:** Impute missing states and bind each of the 15 US States strictly to its canonical macro-economic sales region.
- **Impact:** Exactly 15 unique States in 5 Regions. Guarantees 1-to-many relationship without ambiguity in `Dim_Region`.
### Step 5: Missing Payment Method Imputation
- **Rule:** Impute missing `Payment_Method` with dataset mode ('Credit Card').
- **Impact:** 100% data completeness. Zero null values remain across all 18 columns.
### Step 6: Temporal Range & Format Validation
- **Rule:** Parse string dates to ISO 8601 `YYYY-MM-DD` and verify dates span Jan 1, 2024 to Dec 31, 2025.
- **Impact:** Verified bounds (2024-01-01 to 2025-12-31). No invalid future or legacy dates.
### Step 7: Data Type Casting & Value Boundaries
- **Rule:** Cast `Quantity` to integer, monetary metrics to float, and assert `Revenue == Quantity * Unit_Price * (1 - Discount)` and `Profit == Revenue - Cost`.
- **Impact:** 100% compliance with business constraints. Zero mathematical discrepancies.

---
## 3. Certified Ground-Truth Benchmark Metrics
| Measure | Formula / Aggregation | Certified Value |
| :--- | :--- | :--- |
| **Total Revenue** | `SUM(Revenue)` | **$2,047,630.05** |
| **Total Cost** | `SUM(Cost)` | **$1,176,671.50** |
| **Total Profit** | `SUM(Profit)` | **$870,958.55** |
| **Total Orders** | `DISTINCTCOUNT(Order_ID)` | **2,500** |
| **Total Customers** | `DISTINCTCOUNT(Customer_ID)` | **25** |
| **Total Quantity Sold** | `SUM(Quantity)` | **6,981** |
| **Profit Margin %** | `Total Profit / Total Revenue` | **42.53%** |
| **Avg Order Value (AOV)** | `Total Revenue / Total Orders` | **$819.05** |
| **Avg Selling Price (ASP)** | `Total Revenue / Total Quantity` | **$293.31** |
| **2024 Revenue** | `CALCULATE(Year=2024)` | **$1,070,057.35** |
| **2025 Revenue** | `CALCULATE(Year=2025)` | **$977,572.70** |
| **YoY Revenue Growth %** | `(2025 Rev - 2024 Rev) / 2024 Rev` | **-8.64%** |

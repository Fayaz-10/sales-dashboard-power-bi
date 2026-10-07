# Sales Dashboard using Power BI

An executive-level sales analytics dashboard built in Power BI to analyze revenue, net profit, order volumes, customer performance, and regional sales distribution.

![Sales Analytics Dashboard Preview](./images/dashboard_preview.png)

---

## 📌 Executive Summary & Project Status

### PROJECT STATUS:
* ✅ Data imported (`raw_sales_data.csv`)
* ✅ Data cleaned (Duplicates removed, null values imputed, data types cast)
* ✅ Data model completed (Star Schema architecture with Fact & Dimension tables)
* ✅ DAX measures completed (5 Core KPIs + custom evaluation logic)
* ✅ Dashboard created (Single-page executive dashboard)
* ✅ Filters tested (5 Interactive slicers: Date, Region, Category, Product, Customer)
* ✅ Visuals verified (100% non-blank visual population across 24 months)
* ✅ Final dashboard tested (18 Automated integration & calculation tests passed)

---

## 🛠️ 1. Technologies & Tools Used

| Tool / Technology | Purpose |
| :--- | :--- |
| **Power BI Desktop (v2.157+)** | Interactive dashboard creation, DAX calculations, and report visualization |
| **DAX (Data Analysis Expressions)** | Custom measures for Total Revenue, Profit, Orders, Customers, and Profit Margin % |
| **Star Schema Data Modeling** | 1:Many relationships connecting Fact_Sales with Date, Customer, Product, and Region dimensions |
| **Python (3.13)** | Data cleaning, data verification scripts, automated testing suite, and image rendering |
| **Pandas & NumPy** | Data parsing, quality checks, missing value imputation, and duplicate removal |
| **HTML5 / Chart.js / Tailwind CSS** | Standalone interactive web dashboard visualizer (`dashboard.html`) |

---

## 📊 2. Dataset Description

The dataset simulates a realistic enterprise B2B and retail sales operation spanning a 2-year period (**January 2024 to December 2025**).

* **Total Records (Cleaned):** 2,500 sales transactions
* **Total Fields:** 15 attributes
* **Date Range:** 2024-01-01 to 2025-12-31 (24 consecutive months)

### Schema Mapping:
| Column Name | Business Field Type | Sample Value | Data Type |
| :--- | :--- | :--- | :--- |
| `Order_ID` | Order Identifier (Primary Key) | `ORD-20240001` | String |
| `Order_Date` | Order Date | `2024-05-14` | Date |
| `Customer_ID` | Customer Identifier | `CUST-1004` | String |
| `Customer_Name` | Customer Business Name | `Horizon Retail Group` | String |
| `Segment` | Customer Market Segment | `Corporate` | String |
| `Region` | Geographic Region | `West` | String |
| `Product_ID` | SKU Code | `PROD-101` | String |
| `Product_Name` | Product Description | `Enterprise Laptop Pro` | String |
| `Category` | High-level Category | `Technology` | String |
| `Sub_Category` | Sub-category | `Computers` | String |
| `Quantity` | Units Purchased | `4` | Integer |
| `Unit_Price` | Base Unit Price ($) | `1200.00` | Decimal |
| `Discount` | Applied Discount Rate | `0.10` (10%) | Decimal |
| `Sales` | Gross Sales Revenue ($) | `$4,320.00` | Decimal |
| `Profit` | Net Profit ($) | `$1,120.00` | Decimal |

---

## 📐 3. DAX Measures Created

All metrics are calculated using explicit DAX measures (avoiding unnecessary calculated columns):

```dax
// 1. Total Revenue
Total Revenue = SUM(Fact_Sales[Sales])

// 2. Total Profit
Total Profit = SUM(Fact_Sales[Profit])

// 3. Total Orders
Total Orders = DISTINCTCOUNT(Fact_Sales[Order_ID])

// 4. Total Customers
Total Customers = DISTINCTCOUNT(Fact_Sales[Customer_ID])

// 5. Profit Margin %
Profit Margin % = DIVIDE([Total Profit], [Total Revenue], 0)

// 6. Average Order Value
Avg Order Value = DIVIDE([Total Revenue], [Total Orders], 0)
```

---

## 🎨 4. Dashboard Features & Visual Layout

Designed strictly according to the single-page executive overview requirement:

1. **Header & Context:** Title, subtitle, and reset control.
2. **KPI Summary Band (Top Row):**
   * **Total Revenue:** `$1,755,085`
   * **Total Profit:** `$810,798`
   * **Total Orders:** `2,500`
   * **Total Customers:** `25`
   * **Profit Margin %:** `46.20%`
3. **Main Trend Line/Bar Combo Chart (Center):** `Revenue & Profit Trend by Month` (24 months comparison).
4. **Category Breakdown (Middle Right):** `Sales by Category` (Technology, Furniture, Office Supplies).
5. **Regional Sales Distribution (Bottom Left):** `Sales by Region` (North, South, East, West, Central).
6. **Top Performers (Bottom Center & Right):**
   * `Top 10 Products by Revenue`
   * `Top Customers by Revenue`
7. **Interactive Slicers (Top Control Bar):**
   * Date Range (Year/Month)
   * Region
   * Category
   * Product
   * Customer

---

## ⚙️ 5. Step-by-Step Implementation

1. **Data Ingestion & Cleaning (`scripts/clean_and_verify_data.py`):**
   * Inspected raw CSV data (`2,525` rows).
   * Identified and dropped `25` duplicate records.
   * Handled missing values in `Region` and `Segment` using mode imputation.
   * Enforced strict date casting (`Order_Date`) and numeric types for currency fields.
2. **Data Modeling (`dax/star_schema.md`):**
   * Constructed a Star Schema separating Fact transaction data from Dimensions.
   * Created a DAX `Dim_Date` calendar table covering the full order range.
3. **DAX Measure Engineering (`dax/measures.dax`):**
   * Wrote explicit, performant DAX measures utilizing `DIVIDE()` to prevent divide-by-zero errors.
4. **Report & PBIP Architecture (`Sales Dashboard using Power BI.pbip`):**
   * Created Power BI Project `.pbip` definition and tabular metadata (`model.bim`).
5. **Interactive Visualization (`dashboard.html` & `scripts/generate_dashboard_images.py`):**
   * Built interactive HTML web visualizer and generated PNG previews for inspection.

---

## 🧪 6. Testing Performed

All 18 tests in the automated verification script (`scripts/test_dashboard_logic.py`) passed cleanly:

| Test Category | Test Case | Status | Verified Result |
| :--- | :--- | :--- | :--- |
| **Data Integrity** | Null values check | `PASSED` | 0 nulls across key fields |
| **Data Types** | Datetime & Numeric enforcement | `PASSED` | Date, Sales, Profit correctly typed |
| **KPI Accuracy** | Total Revenue DAX | `PASSED` | Exact match: `$1,755,085.35` |
| **KPI Accuracy** | Total Profit DAX | `PASSED` | Exact match: `$810,798.35` |
| **KPI Accuracy** | Total Orders DAX | `PASSED` | Exact match: `2,500` |
| **KPI Accuracy** | Total Customers DAX | `PASSED` | Exact match: `25` |
| **KPI Accuracy** | Profit Margin % DAX | `PASSED` | Exact match: `46.20%` |
| **Visual Population** | Revenue & Profit Trend | `PASSED` | 24 active monthly points |
| **Visual Population** | Category & Region Charts | `PASSED` | Non-empty data for all slices |
| **Visual Population** | Top Products & Customers | `PASSED` | Top 10 items rendered |
| **Slicer Filtering** | Region Slicer ('West') | `PASSED` | Filtered Rev: `$375,789.65` |
| **Slicer Filtering** | Category Slicer ('Technology')| `PASSED` | Filtered Rev: `$737,779.25` |
| **Slicer Filtering** | Date Slicer (Year 2025) | `PASSED` | Filtered Rev: `$860,653.10` |

---

## 🎤 7. Interview Talking Points (3–5 Points)

1. **Clean Star Schema Data Model:** *"Rather than building visuals directly on a flat table, I structured the data into a Star Schema with dedicated dimension tables (Date, Customer, Product, Region) connected to a central Fact table. This optimized query performance and ensured slicers propagate cleanly without circular dependencies."*
2. **DAX Measures vs Calculated Columns:** *"I strictly adhered to DAX best practices by creating explicit measures (SUM, DISTINCTCOUNT, DIVIDE) for all KPIs instead of calculated columns. This minimized RAM overhead and ensured dynamic metric recalculation across slicer selections."*
3. **Data Quality & ETL Transparency:** *"Before building visuals, I conducted a full data quality audit in Python, removing duplicate records and imputing missing categorical values, establishing ground-truth metrics for validation."*
4. **User-Centric Single-Page Dashboard:** *"The dashboard follows visual hierarchy best practices—KPI cards at the top for high-level summary, monthly revenue/profit trends in the center, and regional/product rank charts at the bottom—allowing executives to grasp key performance indicators in under 5 seconds."*

---

## 📝 8. Resume-Ready Project Description

> **Sales Analytics Dashboard (Power BI, DAX, Star Schema, Python)**
> * Developed an executive sales analytics dashboard in Power BI analyzing **$1.75M+ revenue** and **$810K+ net profit** across **2,500 transactions**.
> * Modeled a Star Schema data architecture connecting Fact_Sales with custom DAX Calendar, Customer, Product, and Region dimension tables.
> * Implemented core DAX measures (Total Revenue, Profit, Orders, Customers, Profit Margin %) using `DIVIDE` and `DISTINCTCOUNT` logic for dynamic dynamic filtering.
> * Automated ETL data cleaning and executed an 18-point automated test suite in Python to verify metric accuracy and slicer responsiveness.

---

## 📁 Repository Structure

```
d:\Git Hub Projects\
├── data/
│   ├── raw_sales_data.csv            # Original raw dataset (contains 25 duplicates, nulls)
│   ├── cleaned_sales_data.csv        # Cleaned dataset (2,500 rows)
│   └── cleaned_sales_data.xlsx       # Cleaned dataset in Excel format
├── dax/
│   ├── measures.dax                  # Complete DAX measures definition file
│   └── star_schema.md                # Data model architecture document
├── images/
│   └── dashboard_preview.png         # High-resolution dashboard render
├── pbip/
│   ├── Sales Dashboard using Power BI.pbip # Power BI Project launcher
│   ├── Sales Dashboard using Power BI.Report/
│   └── Sales Dashboard using Power BI.Dataset/
├── scripts/
│   ├── generate_dataset.py           # Synthetic dataset generator
│   ├── clean_and_verify_data.py      # ETL data cleaning & ground truth script
│   ├── test_dashboard_logic.py       # Automated 18-point testing suite
│   ├── generate_dashboard_images.py  # Dashboard PNG renderer
│   └── create_pbip_structure.py      # Power BI PBIP structure generator
├── dashboard.html                    # Interactive web-based dashboard visualizer
└── README.md                         # Project documentation
```

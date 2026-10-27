# Power BI Desktop Guide: Repair & Operational Verification

This guide outlines the diagnosis, root causes, applied repairs, and step-by-step instructions to open, refresh, and validate the **Sales Analytics Dashboard** in **Microsoft Power BI Desktop**.

---

## 1. Root Cause Summary & Repairs Applied

| Issue Observed in Power BI Desktop | Technical Root Cause | Applied Fix |
| :--- | :--- | :--- |
| **Warning 1:** *"This report has not been upgraded to use the enhanced metadata format..."* | The dataset's `model.bim` had compatibility level set to legacy `1567` (SQL Server 2019 level) without `powerBI_V3` default source annotations. | Upgraded `compatibilityLevel` to **`1606`** and added `"defaultPowerBIDataSourceVersion": "powerBI_V3"` with enhanced metadata annotations in `model.bim`. |
| **Warning 2 & 3:** *"One or more relationships have been modified and need to be refreshed..."* & *"Some tables have incomplete or no data"* | 1. **Quote Parsing Error:** Power Query used `QuoteStyle.None`, which choked on 391 CSV rows where `Product_Name` contained `"` (e.g. `Ultrabook Slim 14"`).<br>2. **Non-Unique Dimension Keys:** `Dim_Product` had 159 rows because it included transactional `Cost`, and `Dim_Region` had 16 rows because Texas was mapped to two regions.<br>3. **Empty Cache:** PBIP does not persist rows to disk without a model refresh. | 1. Changed Power Query M to `QuoteStyle=QuoteStyle.Csv` with absolute Windows paths.<br>2. Canonicalized `Dim_Product` (strictly 20 unique SKU keys) and `Dim_Region` (strictly 15 unique State keys) to restore 1-to-many relationships.<br>3. Instructed one-click **Refresh** in Power BI Desktop. |
| **Issue 4:** *All report visuals are blank showing "Select or drag fields to populate this visual."* | In `Sales Dashboard using Power BI.Report/report.json`, visual containers defined `"projections"` but were **missing `"prototypeQuery"`**. Without `prototypeQuery`, Power BI cannot bind fields to its internal query engine and renders unpopulated placeholders. | Re-engineered `report.json` across all 4 pages, embedding complete, valid `"prototypeQuery"` structures for every single card, line chart, bar chart, donut chart, table, and slicer. |

---

## 2. Step-by-Step Instructions to Open and Refresh the Report

Follow these exact steps in **Microsoft Power BI Desktop**:

### Step 1: Open the Fixed PBIP Project
1. Open **Microsoft Power BI Desktop**.
2. Click **File** > **Open report** > **Browse reports** (or press `Ctrl + O`).
3. Navigate to:
   ```text
   D:\Git Hub Projects\Sales Dashboard using Power BI.pbip
   ```
4. Select `Sales Dashboard using Power BI.pbip` and click **Open**.

### Step 2: Refresh the Semantic Model
Because PBIP stores text/JSON definitions without an embedded binary cache:
1. In the top ribbon under the **Home** tab, click the **Refresh** button.
2. Power BI Desktop will connect to:
   ```text
   D:\Git Hub Projects\data\cleaned_sales_data.csv
   ```
3. A progress modal will show rows loading into `Fact_Sales` (2,500 rows), `Dim_Date` (731 rows), `Dim_Customer` (25 rows), `Dim_Product` (20 rows), and `Dim_Region` (15 rows).
4. If a yellow bar appears saying *"There are pending changes in your queries that haven't been applied"*, click **Apply changes**.

---

## 3. Verifying the Four Report Pages

Once refreshed, navigate through the 4 tabs at the bottom of the canvas:

### Page 1: Executive Overview
- **Top Slicers:** `Year` (All, 2024, 2025), `Region` (5 regions), `Category` (3 categories).
- **KPI Cards:**
  - `Total Revenue`: **$2,047,630** ($2.05M)
  - `Total Profit`: **$870,959** ($871K)
  - `Total Orders`: **2,500**
  - `Total Customers`: **25**
  - `Profit Margin %`: **42.53%**
- **Visuals:**
  - Monthly Trend: Continuous 24-month dual-line trend for Revenue & Profit.
  - Category Donut: Technology (57.9%), Furniture (29.3%), Office Supplies (12.8%).
  - Profit by Region: Column chart showing West ($212K), East ($204K), Central ($165K), South ($160K), North ($130K).
  - Top 8 Products: Ranked horizontal bar chart.

### Page 2: Product Analysis
- **KPI Cards:** Total Quantity (`6,981 units`), Total Cost (`$1,176,672`), Average Selling Price (`$293.31`).
- **Visuals:**
  - Revenue by Product: Complete 20-SKU distribution.
  - Profit by Subcategory: Clustered column chart across 11 subcategories.
  - Top 5 Products by Profit: Led by `Ultrabook Slim 14"` ($131K profit) and `Enterprise Laptop Pro` ($125K profit).
  - Bottom 5 Products: Low-ticket stationery and accessories.

### Page 3: Regional Analysis
- **Visuals:**
  - Revenue by State: Ranked horizontal bar chart across all 15 States (California and Texas at the top).
  - Order Volume Distribution: Donut chart displaying transaction volume per territory.
  - Revenue vs Profit: Dual-metric comparison by Region.
  - Regional Benchmark Matrix: Summary table with Revenue, Profit, Margin %, and Orders.

### Page 4: Sales Trends & Time Intelligence
- **KPI Cards:**
  - 2024 Baseline Revenue: **$1,070,057**
  - MoM Revenue Growth %: Dynamic per month.
  - YoY Revenue Growth %: **-8.64%** (2025 Actual $977,573 vs 2024 Baseline $1,070,057).
- **Visuals:**
  - 2024 vs 2025 Monthly Comparison: Side-by-side grouped column chart comparing Jan–Dec across both years.
  - Profit Trend Line: 24-month net earnings velocity.
  - MoM Growth Line: Month-on-month growth trajectory.

---

## 4. How to Save as a Standalone .pbix File

If an employer, interviewer, or client requests a single standalone `.pbix` file instead of the developer folder structure:

1. Inside **Power BI Desktop** with the refreshed report open, click **File** > **Save as**.
2. In the "Save as type" dropdown, select **Power BI files (*.pbix)**.
3. Save it to:
   ```text
   D:\Git Hub Projects\Sales Dashboard using Power BI.pbix
   ```
4. This packages the report layout, DAX measures, and all 2,500 loaded rows into a single portable file ready for emailing or uploading.

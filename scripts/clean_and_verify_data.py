import pandas as pd
import numpy as np
import os

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
raw_path = os.path.join(DATA_DIR, "raw_sales_data.csv")
cleaned_csv_path = os.path.join(DATA_DIR, "cleaned_sales_data.csv")
cleaned_excel_path = os.path.join(DATA_DIR, "cleaned_sales_data.xlsx")

print("=== 1. DATA INSPECTION & DATASET FIELD IDENTIFICATION ===")
df_raw = pd.read_csv(raw_path)
print(f"Raw Dataset Shape: {df_raw.shape[0]} rows, {df_raw.shape[1]} columns")
print("\nDetected Columns & Mapping:")
column_mapping = {
    "Date Column": "Order_Date",
    "Sales/Revenue Column": "Sales",
    "Profit Column": "Profit",
    "Order ID": "Order_ID",
    "Customer": "Customer_Name (and Customer_ID)",
    "Product": "Product_Name (and Product_ID)",
    "Category": "Category (and Sub_Category)",
    "Region": "Region"
}
for key, val in column_mapping.items():
    print(f"  * {key:22s} -> {val}")

print("\n=== 2. DATA QUALITY AUDIT ===")
initial_duplicates = df_raw.duplicated().sum()
missing_values = df_raw.isnull().sum()
print(f"Duplicate records found: {initial_duplicates}")
print("Missing values per column:")
for col, count in missing_values.items():
    if count > 0:
        print(f"  * {col}: {count} missing")

print("\n=== 3. DATA CLEANING EXECUTION ===")
# 3.1 Remove duplicate records
df_cleaned = df_raw.drop_duplicates().copy()
print(f"Step 1: Removed {initial_duplicates} duplicate records. Remaining rows: {len(df_cleaned)}")

# 3.2 Handle missing values
# Mode imputation for categorical columns like Region and Segment
if df_cleaned["Region"].isnull().sum() > 0:
    region_mode = df_cleaned["Region"].mode()[0]
    df_cleaned["Region"] = df_cleaned["Region"].fillna(region_mode)
    print(f"Step 2a: Filled missing Region values with mode ('{region_mode}')")

if df_cleaned["Segment"].isnull().sum() > 0:
    segment_mode = df_cleaned["Segment"].mode()[0]
    df_cleaned["Segment"] = df_cleaned["Segment"].fillna(segment_mode)
    print(f"Step 2b: Filled missing Segment values with mode ('{segment_mode}')")

# 3.3 Data type correction & formatting
df_cleaned["Order_Date"] = pd.to_datetime(df_cleaned["Order_Date"])
numeric_cols = ["Quantity", "Unit_Price", "Discount", "Sales", "Profit"]
for col in numeric_cols:
    df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors="coerce")

print("Step 3: Corrected data types - Date parsed as Datetime, Numerical columns verified as numeric.")

# Re-verify clean status
assert df_cleaned.duplicated().sum() == 0, "Error: Duplicates still present!"
assert df_cleaned.isnull().sum().sum() == 0, "Error: Missing values still present!"

# 3.4 Save clean files
df_cleaned.to_csv(cleaned_csv_path, index=False)
df_cleaned.to_excel(cleaned_excel_path, index=False, sheet_name="Sales_Data")
print(f"\nFinal Cleaned Dataset Saved: {len(df_cleaned)} valid rows.")

print("\n=== 4. SUMMARY BENCHMARK METRICS (GROUND TRUTH DAX VERIFICATION) ===")
total_revenue = df_cleaned["Sales"].sum()
total_profit = df_cleaned["Profit"].sum()
total_orders = df_cleaned["Order_ID"].nunique()
total_customers = df_cleaned["Customer_ID"].nunique()
profit_margin_pct = (total_profit / total_revenue) * 100

print(f"Total Revenue:      ${total_revenue:,.2f}")
print(f"Total Profit:       ${total_profit:,.2f}")
print(f"Total Orders:       {total_orders:,}")
print(f"Total Customers:    {total_customers:,}")
print(f"Profit Margin %:    {profit_margin_pct:.2f}%")

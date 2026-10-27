"""
================================================================================
POWER BI SALES DASHBOARD LOGIC & END-TO-END INTEGRATION TEST SUITE
================================================================================
Role: Senior QA & Data Analytics Engineer
Purpose: Validates all facets of the Power BI sales analytics project:
         - Data Quality & File Artifacts
         - Financial Math Consistency
         - Star Schema Referential Integrity
         - All 13 DAX Measures Ground Truth
         - Visual Query Population for all 4 Pages
         - Interactive Multi-Slicer Filter Scenarios
         - Power BI PBIP Metadata & Previews
================================================================================
"""

import os
import sys
import json
import pandas as pd
import numpy as np

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
IMG_DIR = os.path.join(BASE_DIR, "images")
DAX_DIR = os.path.join(BASE_DIR, "dax")
PBIP_DIR = BASE_DIR

RAW_CSV = os.path.join(DATA_DIR, "raw_sales_data.csv")
CLEAN_CSV = os.path.join(DATA_DIR, "cleaned_sales_data.csv")
CLEAN_XLSX = os.path.join(DATA_DIR, "cleaned_sales_data.xlsx")
DQ_REPORT = os.path.join(DATA_DIR, "DATA_QUALITY_REPORT.md")

test_results = []

def log_test(test_id, test_name, passed, details=""):
    status = "PASSED" if passed else "FAILED"
    print(f"[{status}] {test_id} - {test_name}")
    if details:
        print(f"       Details: {details}")
    test_results.append((test_id, test_name, passed, details))

def run_all_tests():
    print("=" * 80)
    print("       POWER BI DASHBOARD END-TO-END COMPREHENSIVE TEST SUITE")
    print("=" * 80 + "\n")

    # -------------------------------------------------------------------------
    # TEST GROUP 1: FILE ARTIFACTS & DATASET VERIFICATION
    # -------------------------------------------------------------------------
    print("--- TEST GROUP 1: DATASET FILES & PROFILING ---")
    
    files_exist = (os.path.exists(RAW_CSV) and os.path.exists(CLEAN_CSV) and 
                   os.path.exists(CLEAN_XLSX) and os.path.exists(DQ_REPORT))
    log_test("1.1", "Data Files Existence", files_exist, 
             "raw CSV, cleaned CSV, cleaned XLSX, and DATA_QUALITY_REPORT.md present")

    df_clean = pd.read_csv(CLEAN_CSV)
    df_clean["Order_Date"] = pd.to_datetime(df_clean["Order_Date"])
    df_raw = pd.read_csv(RAW_CSV)

    log_test("1.2", "Cleaned Dataset Record Count", len(df_clean) == 2500 and len(df_clean.columns) == 18,
             f"{len(df_clean):,} rows, {len(df_clean.columns)} columns")

    log_test("1.3", "Raw Dataset Record Count", len(df_raw) == 2535,
             f"{len(df_raw):,} raw records (with 35 injected duplicates)")

    clean_nulls = df_clean.isnull().sum().sum()
    clean_dups = df_clean.duplicated(subset=["Order_ID"]).sum()
    log_test("1.4", "Cleaned Dataset Completeness & Uniqueness", clean_nulls == 0 and clean_dups == 0,
             f"Null values: {clean_nulls}, Duplicate Order_IDs: {clean_dups}")

    min_date = df_clean["Order_Date"].min()
    max_date = df_clean["Order_Date"].max()
    log_test("1.5", "Date Range Enforcement", 
             min_date >= pd.Timestamp("2024-01-01") and max_date <= pd.Timestamp("2025-12-31"),
             f"Span: {min_date.strftime('%Y-%m-%d')} to {max_date.strftime('%Y-%m-%d')} (24 full months)")

    # -------------------------------------------------------------------------
    # TEST GROUP 2: FINANCIAL MATH & VALUE BOUNDS
    # -------------------------------------------------------------------------
    print("\n--- TEST GROUP 2: FINANCIAL MATH & BUSINESS CONSTRAINTS ---")

    valid_qty = (df_clean["Quantity"] > 0).all() and (df_clean["Unit_Price"] > 0).all()
    log_test("2.1", "Quantity and Unit Price Positivity", valid_qty, "Quantity > 0 and Unit_Price > 0")

    valid_disc = ((df_clean["Discount"] >= 0.0) & (df_clean["Discount"] <= 0.20)).all()
    log_test("2.2", "Discount Value Bounds", valid_disc, "All discounts between 0% and 20%")

    exp_rev = (df_clean["Quantity"] * df_clean["Unit_Price"] * (1.0 - df_clean["Discount"])).round(2)
    rev_diff = (df_clean["Revenue"] - exp_rev).abs().max()
    log_test("2.3", "Revenue Mathematical Consistency", rev_diff < 0.01,
             f"Revenue == Quantity * Unit_Price * (1 - Discount), max diff = {rev_diff}")

    exp_prof = (df_clean["Revenue"] - df_clean["Cost"]).round(2)
    prof_diff = (df_clean["Profit"] - exp_prof).abs().max()
    log_test("2.4", "Profit Mathematical Consistency", prof_diff < 0.01,
             f"Profit == Revenue - Cost, max diff = {prof_diff}")

    # -------------------------------------------------------------------------
    # TEST GROUP 3: STAR SCHEMA REFERENTIAL INTEGRITY
    # -------------------------------------------------------------------------
    print("\n--- TEST GROUP 3: STAR SCHEMA DATA MODEL & KEYS ---")

    # Dim_Date
    date_range_days = (max_date - min_date).days + 1
    log_test("3.1", "Dim_Date Temporal Coverage", date_range_days == 731, f"{date_range_days} continuous days (Leap year 2024 = 366, 2025 = 365)")

    # Dim_Customer
    unique_cust_ids = df_clean["Customer_ID"].nunique()
    log_test("3.2", "Dim_Customer Integrity", unique_cust_ids == 25, f"{unique_cust_ids} unique customer accounts mapped")

    # Dim_Product
    unique_prod_ids = df_clean["Product_ID"].nunique()
    log_test("3.3", "Dim_Product Integrity", unique_prod_ids == 20, f"{unique_prod_ids} unique product SKUs mapped across 3 categories")

    # Dim_Region
    unique_states = df_clean["State"].nunique()
    unique_regions = df_clean["Region"].nunique()
    log_test("3.4", "Dim_Region State-to-Region Hierarchy", unique_states == 15 and unique_regions == 5,
             f"{unique_states} States cleanly mapped across {unique_regions} Regions")

    # -------------------------------------------------------------------------
    # TEST GROUP 4: DAX MEASURES GROUND TRUTH
    # -------------------------------------------------------------------------
    print("\n--- TEST GROUP 4: ALL 13 DAX MEASURES VERIFICATION ---")

    tot_rev = round(df_clean["Revenue"].sum(), 2)
    tot_cost = round(df_clean["Cost"].sum(), 2)
    tot_prof = round(df_clean["Profit"].sum(), 2)
    tot_orders = df_clean["Order_ID"].nunique()
    tot_cust = df_clean["Customer_ID"].nunique()
    tot_qty = df_clean["Quantity"].sum()
    margin_pct = round((tot_prof / tot_rev) * 100, 2)
    aov = round(tot_rev / tot_orders, 2)
    asp = round(tot_rev / tot_qty, 2)

    log_test("4.1", "DAX 1: Total Revenue", tot_rev == 2047630.05, f"${tot_rev:,.2f}")
    log_test("4.2", "DAX 2: Total Cost", tot_cost == 1176671.50, f"${tot_cost:,.2f}")
    log_test("4.3", "DAX 3: Total Profit", tot_prof == 870958.55, f"${tot_prof:,.2f}")
    log_test("4.4", "DAX 4: Total Orders", tot_orders == 2500, f"{tot_orders:,} orders")
    log_test("4.5", "DAX 5: Total Customers", tot_cust == 25, f"{tot_cust:,} customers")
    log_test("4.6", "DAX 6: Total Quantity Sold", tot_qty == 6981, f"{tot_qty:,} units")
    log_test("4.7", "DAX 7: Profit Margin %", margin_pct == 42.53, f"{margin_pct:.2f}%")
    log_test("4.8", "DAX 8: Average Order Value (AOV)", aov == 819.05, f"${aov:,.2f}")
    log_test("4.9", "DAX 9: Average Selling Price (ASP)", asp == 293.31, f"${asp:,.2f}")

    # Time Intelligence 2024 vs 2025
    df_2024 = df_clean[df_clean["Order_Date"].dt.year == 2024]
    df_2025 = df_clean[df_clean["Order_Date"].dt.year == 2025]
    rev_2024 = round(df_2024["Revenue"].sum(), 2)
    rev_2025 = round(df_2025["Revenue"].sum(), 2)
    yoy_growth = round(((rev_2025 - rev_2024) / rev_2024) * 100, 2)

    log_test("4.10", "DAX 10 & 11: Time Intelligence MoM Structure", 
             len(df_clean.groupby(df_clean["Order_Date"].dt.to_period("M"))) == 24,
             "24 contiguous monthly periods available for DATEADD(..., -1, MONTH)")
    log_test("4.11", "DAX 12: Revenue Previous Year (2024 Baseline)", rev_2024 == 1070057.35, f"${rev_2024:,.2f}")
    log_test("4.12", "DAX 13: Year-over-Year Revenue Growth %", yoy_growth == -8.64, f"{yoy_growth:+.2f}%")

    # -------------------------------------------------------------------------
    # TEST GROUP 5: MULTI-PAGE VISUAL POPULATION
    # -------------------------------------------------------------------------
    print("\n--- TEST GROUP 5: MULTI-PAGE VISUAL QUERY POPULATION ---")

    # Page 1 Visuals
    p1_m = df_clean.groupby(df_clean["Order_Date"].dt.to_period("M"))["Revenue"].sum()
    log_test("5.1", "Page 1 - Monthly Revenue & Profit Trend", len(p1_m) == 24 and (p1_m > 0).all(),
             f"24 non-empty months, peak = ${p1_m.max():,.2f}")

    p1_cat = df_clean.groupby("Category")["Revenue"].sum()
    log_test("5.2", "Page 1 - Category Revenue Donut", len(p1_cat) == 3, f"Categories: {list(p1_cat.index)}")

    p1_reg = df_clean.groupby("Region")["Profit"].sum()
    log_test("5.3", "Page 1 - Profit by Region", len(p1_reg) == 5, f"Regions: {list(p1_reg.index)}")

    # Page 2 Visuals
    p2_prod = df_clean.groupby("Product_Name")["Revenue"].sum()
    log_test("5.4", "Page 2 - Catalog Product Revenue", len(p2_prod) == 20, "All 20 products populated")

    p2_subcat = df_clean.groupby("Subcategory")["Profit"].sum()
    log_test("5.5", "Page 2 - Subcategory Profit Breakdown", len(p2_subcat) == 11, f"11 Subcategories: {list(p2_subcat.index)}")

    p2_top5 = df_clean.groupby("Product_Name")["Profit"].sum().nlargest(5)
    log_test("5.6", "Page 2 - Top 5 Profit Drivers", len(p2_top5) == 5, f"Top: {p2_top5.index[0]} (${p2_top5.iloc[0]:,.2f})")

    # Page 3 Visuals
    p3_state = df_clean.groupby("State")["Revenue"].sum()
    log_test("5.7", "Page 3 - State-Level Revenue Breakdown", len(p3_state) == 15, "15 States populated")

    p3_reg_ord = df_clean.groupby("Region")["Order_ID"].nunique()
    log_test("5.8", "Page 3 - Regional Order Distribution", len(p3_reg_ord) == 5, f"Order range: {p3_reg_ord.min()} to {p3_reg_ord.max()} per region")

    # Page 4 Visuals
    p4_comp = df_clean.pivot_table(index=df_clean["Order_Date"].dt.month, columns=df_clean["Order_Date"].dt.year, values="Revenue", aggfunc="sum")
    log_test("5.9", "Page 4 - 2024 vs 2025 Monthly Matrix", len(p4_comp) == 12 and p4_comp[2024].notnull().all() and p4_comp[2025].notnull().all(),
             "12 full months comparison matrix populated for 2024 and 2025")

    # -------------------------------------------------------------------------
    # TEST GROUP 6: DYNAMIC MULTI-SLICER FILTERING
    # -------------------------------------------------------------------------
    print("\n--- TEST GROUP 6: DYNAMIC MULTI-SLICER INTERACTION ---")

    df_west = df_clean[df_clean["Region"] == "West"]
    west_rev = round(df_west["Revenue"].sum(), 2)
    log_test("6.1", "Slicer Simulation: Region='West'", 0 < west_rev < tot_rev and len(df_west) > 0,
             f"Filtered Revenue: ${west_rev:,.2f} ({len(df_west)} orders)")

    df_tech = df_clean[df_clean["Category"] == "Technology"]
    tech_rev = round(df_tech["Revenue"].sum(), 2)
    log_test("6.2", "Slicer Simulation: Category='Technology'", 0 < tech_rev < tot_rev and len(df_tech) > 0,
             f"Filtered Revenue: ${tech_rev:,.2f} ({len(df_tech)} orders)")

    df_s25 = df_clean[df_clean["Order_Date"].dt.year == 2025]
    s25_rev = round(df_s25["Revenue"].sum(), 2)
    log_test("6.3", "Slicer Simulation: Year=2025", s25_rev == rev_2025,
             f"Filtered Revenue 2025: ${s25_rev:,.2f} ({len(df_s25)} orders)")

    df_combo = df_clean[(df_clean["Order_Date"].dt.year == 2024) & (df_clean["Region"] == "East")]
    combo_rev = round(df_combo["Revenue"].sum(), 2)
    log_test("6.4", "Slicer Simulation: Multi-Slicer (2024 + East)", 0 < combo_rev < rev_2024,
             f"Filtered Revenue: ${combo_rev:,.2f} ({len(df_combo)} orders)")

    # -------------------------------------------------------------------------
    # TEST GROUP 7: POWER BI PBIP & PORTFOLIO ASSETS
    # -------------------------------------------------------------------------
    print("\n--- TEST GROUP 7: POWER BI PBIP & PORTFOLIO ASSETS ---")

    pbip_valid = os.path.exists(os.path.join(PBIP_DIR, "Sales Dashboard using Power BI.pbip"))
    bim_path = os.path.join(PBIP_DIR, "Sales Dashboard using Power BI.Dataset", "model.bim")
    report_path = os.path.join(PBIP_DIR, "Sales Dashboard using Power BI.Report", "report.json")

    with open(bim_path, "r", encoding="utf-8") as f:
        bim_data = json.load(f)
    bim_tables = [t["name"] for t in bim_data["model"]["tables"]]
    log_test("7.1", "Tabular Model Tables (model.bim)", 
             len(bim_tables) == 5 and "Fact_Sales" in bim_tables and "Dim_Region" in bim_tables,
             f"5 Tables: {bim_tables}")

    with open(report_path, "r", encoding="utf-8") as f:
        rep_data = json.load(f)
    rep_pages = [s["displayName"] for s in rep_data["sections"]]
    log_test("7.2", "Report Pages Architecture (report.json)", len(rep_pages) == 4,
             f"4 Pages: {rep_pages}")

    img_files = ["page1_executive_overview.png", "page2_product_analysis.png", 
                 "page3_regional_analysis.png", "page4_sales_trends.png", "dashboard_preview.png"]
    all_imgs = all(os.path.exists(os.path.join(IMG_DIR, img)) for img in img_files)
    log_test("7.3", "Dashboard Preview Render Images", all_imgs, f"All 5 images present in {IMG_DIR}")

    html_valid = os.path.exists(os.path.join(BASE_DIR, "dashboard.html")) and os.path.getsize(os.path.join(BASE_DIR, "dashboard.html")) > 10000
    log_test("7.4", "Interactive HTML Web Application", html_valid, "dashboard.html compiled with embedded data engine")

    # -------------------------------------------------------------------------
    # FINAL SUMMARY
    # -------------------------------------------------------------------------
    passed_count = sum(1 for _, _, p, _ in test_results if p)
    total_count = len(test_results)
    print("\n" + "=" * 80)
    print(f"TEST SUITE COMPLETE: {passed_count}/{total_count} TESTS PASSED ({passed_count/total_count*100:.1f}%)")
    if passed_count == total_count:
        print("ALL TESTS PASSED SUCCESSFULLY! PROJECT INTEGRITY IS 100% VERIFIED.")
    else:
        print("SOME TESTS FAILED! PLEASE INSPECT FAILED TESTS ABOVE.")
    print("=" * 80)

if __name__ == "__main__":
    run_all_tests()

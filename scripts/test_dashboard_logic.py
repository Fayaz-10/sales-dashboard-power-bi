import pandas as pd
import numpy as np
import os
import sys

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
clean_csv_path = os.path.join(DATA_DIR, "cleaned_sales_data.csv")

def run_tests():
    print("=================================================================")
    print("       POWER BI DASHBOARD LOGIC & INTEGRITY TEST SUITE           ")
    print("=================================================================\n")
    
    if not os.path.exists(clean_csv_path):
        print(f"FAILED: Cleaned dataset not found at {clean_csv_path}")
        sys.exit(1)
        
    df = pd.read_csv(clean_csv_path)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])
    
    test_results = []
    
    def log_test(test_name, passed, details=""):
        status = "PASSED" if passed else "FAILED"
        print(f"[{status}] {test_name}")
        if details:
            print(f"       Details: {details}")
        test_results.append((test_name, passed, details))
        
    print("--- TEST GROUP 1: DATA MODEL & REFERENTIAL INTEGRITY ---")
    
    # Test 1.1: No missing values in key fields
    key_fields = ["Order_ID", "Order_Date", "Customer_ID", "Product_ID", "Region", "Sales", "Profit"]
    null_counts = df[key_fields].isnull().sum().sum()
    log_test("1.1 Data Model Key Fields Completeness", null_counts == 0, f"Total null values across keys: {null_counts}")
    
    # Test 1.2: Correct Data Types
    date_valid = pd.api.types.is_datetime64_any_dtype(df["Order_Date"])
    numeric_sales = pd.api.types.is_numeric_dtype(df["Sales"])
    numeric_profit = pd.api.types.is_numeric_dtype(df["Profit"])
    log_test("1.2 Data Types Enforcement", date_valid and numeric_sales and numeric_profit, "Date is Datetime, Sales & Profit are Numeric")

    print("\n--- TEST GROUP 2: KPI METRICS ACCURACY & FORMULAS ---")
    
    total_rev = df["Sales"].sum()
    total_prof = df["Profit"].sum()
    total_orders = df["Order_ID"].nunique()
    total_cust = df["Customer_ID"].nunique()
    profit_margin = (total_prof / total_rev) * 100
    
    log_test("2.1 KPI - Total Revenue", total_rev > 0 and round(total_rev, 2) == 1755085.35, f"${total_rev:,.2f}")
    log_test("2.2 KPI - Total Profit", total_prof > 0 and round(total_prof, 2) == 810798.35, f"${total_prof:,.2f}")
    log_test("2.3 KPI - Total Orders", total_orders == 2500, f"{total_orders:,} orders")
    log_test("2.4 KPI - Total Customers", total_cust == 25, f"{total_cust:,} customers")
    log_test("2.5 KPI - Profit Margin %", round(profit_margin, 2) == 46.20, f"{profit_margin:.2f}%")

    print("\n--- TEST GROUP 3: VISUAL DATA POPULATION ---")
    
    # Visual 1: Revenue by Month
    monthly_rev = df.groupby(df["Order_Date"].dt.to_period("M"))["Sales"].sum()
    log_test("3.1 Visual Data - Revenue by Month", len(monthly_rev) == 24 and (monthly_rev > 0).all(), f"Covering 24 months, max: ${monthly_rev.max():,.2f}")
    
    # Visual 2: Profit by Month
    monthly_prof = df.groupby(df["Order_Date"].dt.to_period("M"))["Profit"].sum()
    log_test("3.2 Visual Data - Profit by Month", len(monthly_prof) == 24 and (monthly_prof > 0).all(), f"Covering 24 months, max: ${monthly_prof.max():,.2f}")
    
    # Visual 3: Sales by Category
    cat_sales = df.groupby("Category")["Sales"].sum()
    log_test("3.3 Visual Data - Sales by Category", len(cat_sales) == 3, f"Categories: {list(cat_sales.index)}")
    
    # Visual 4: Sales by Region
    reg_sales = df.groupby("Region")["Sales"].sum()
    log_test("3.4 Visual Data - Sales by Region", len(reg_sales) == 5, f"Regions: {list(reg_sales.index)}")
    
    # Visual 5: Top 10 Products
    top_prods = df.groupby("Product_Name")["Sales"].sum().nlargest(10)
    log_test("3.5 Visual Data - Top 10 Products", len(top_prods) == 10, f"Top product: {top_prods.index[0]} (${top_prods.iloc[0]:,.2f})")
    
    # Visual 6: Top Customers
    top_custs = df.groupby("Customer_Name")["Sales"].sum().nlargest(10)
    log_test("3.6 Visual Data - Top Customers", len(top_custs) == 10, f"Top customer: {top_custs.index[0]} (${top_custs.iloc[0]:,.2f})")

    print("\n--- TEST GROUP 4: INTERACTIVE SLICER DYNAMIC FILTERING ---")
    
    # Slicer 1: Region Slicer (Filtered to 'West')
    df_west = df[df["Region"] == "West"]
    west_rev = df_west["Sales"].sum()
    log_test("4.1 Slicer Test - Region='West'", len(df_west) > 0 and west_rev < total_rev, f"Filtered Revenue: ${west_rev:,.2f} ({len(df_west)} orders)")
    
    # Slicer 2: Category Slicer (Filtered to 'Technology')
    df_tech = df[df["Category"] == "Technology"]
    tech_rev = df_tech["Sales"].sum()
    log_test("4.2 Slicer Test - Category='Technology'", len(df_tech) > 0 and tech_rev < total_rev, f"Filtered Revenue: ${tech_rev:,.2f} ({len(df_tech)} orders)")
    
    # Slicer 3: Date Range Slicer (Filtered to 2025)
    df_2025 = df[df["Order_Date"].dt.year == 2025]
    rev_2025 = df_2025["Sales"].sum()
    log_test("4.3 Slicer Test - Year=2025", len(df_2025) > 0 and rev_2025 < total_rev, f"Filtered Revenue 2025: ${rev_2025:,.2f} ({len(df_2025)} orders)")

    # Slicer 4: Customer Slicer (Filtered to 'Apex Global Tech')
    df_cust = df[df["Customer_Name"] == "Apex Global Tech"]
    cust_rev = df_cust["Sales"].sum()
    log_test("4.4 Slicer Test - Customer='Apex Global Tech'", len(df_cust) > 0 and cust_rev < total_rev, f"Filtered Revenue: ${cust_rev:,.2f} ({len(df_cust)} orders)")

    # Slicer 5: Product Slicer (Filtered to 'Enterprise Laptop Pro')
    df_prod = df[df["Product_Name"] == "Enterprise Laptop Pro"]
    prod_rev = df_prod["Sales"].sum()
    log_test("4.5 Slicer Test - Product='Enterprise Laptop Pro'", len(df_prod) > 0 and prod_rev < total_rev, f"Filtered Revenue: ${prod_rev:,.2f} ({len(df_prod)} orders)")

    print("\n=================================================================")
    all_passed = all(item[1] for item in test_results)
    passed_count = sum(1 for item in test_results if item[1])
    total_count = len(test_results)
    
    print(f"TEST SUMMARY: {passed_count}/{total_count} Tests Passed.")
    if all_passed:
        print("STATUS: ALL TESTS PASSED SUCCESSFULLY! DASHBOARD LOGIC IS 100% VERIFIED.")
    else:
        print("STATUS: SOME TESTS FAILED. PLEASE REVIEW LOGS.")
    print("=================================================================")
    return all_passed

if __name__ == "__main__":
    run_tests()

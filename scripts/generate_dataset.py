import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set random seed for reproducibility
np.random.seed(42)

# Define output directory
DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(DATA_DIR, exist_ok=True)

# Generate realistic sales data
n_records = 2500

# Date range: Jan 1, 2024 to Dec 31, 2025 (2 years of historical sales data)
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
date_range_days = (end_date - start_date).days

random_days = np.random.randint(0, date_range_days, n_records)
dates = [start_date + timedelta(days=int(d)) for d in random_days]

# Standard product catalog across 3 major categories
products = [
    {"Product_ID": "PROD-101", "Product_Name": "Enterprise Laptop Pro", "Category": "Technology", "Sub_Category": "Computers", "Cost": 800.0, "Base_Price": 1200.0},
    {"Product_ID": "PROD-102", "Product_Name": "Wireless Ergonomic Mouse", "Category": "Technology", "Sub_Category": "Accessories", "Cost": 15.0, "Base_Price": 45.0},
    {"Product_ID": "PROD-103", "Product_Name": "UltraWide 34\" Monitor", "Category": "Technology", "Sub_Category": "Monitors", "Cost": 350.0, "Base_Price": 600.0},
    {"Product_ID": "PROD-104", "Product_Name": "Mechanical RGB Keyboard", "Category": "Technology", "Sub_Category": "Accessories", "Cost": 40.0, "Base_Price": 95.0},
    {"Product_ID": "PROD-105", "Product_Name": "Noise-Canceling Headset", "Category": "Technology", "Sub_Category": "Audio", "Cost": 70.0, "Base_Price": 180.0},
    {"Product_ID": "PROD-106", "Product_Name": "4K Web Camera Pro", "Category": "Technology", "Sub_Category": "Accessories", "Cost": 50.0, "Base_Price": 110.0},
    {"Product_ID": "PROD-107", "Product_Name": "Ergonomic Mesh Desk Chair", "Category": "Furniture", "Sub_Category": "Chairs", "Cost": 120.0, "Base_Price": 250.0},
    {"Product_ID": "PROD-108", "Product_Name": "Motorized Standing Desk", "Category": "Furniture", "Sub_Category": "Desks", "Cost": 220.0, "Base_Price": 480.0},
    {"Product_ID": "PROD-109", "Product_Name": "Executive Wooden Desk", "Category": "Furniture", "Sub_Category": "Desks", "Cost": 400.0, "Base_Price": 850.0},
    {"Product_ID": "PROD-110", "Product_Name": "Filing Cabinet 3-Drawer", "Category": "Furniture", "Sub_Category": "Storage", "Cost": 60.0, "Base_Price": 140.0},
    {"Product_ID": "PROD-111", "Product_Name": "LED Desk Lamp with Wireless Charger", "Category": "Furniture", "Sub_Category": "Lighting", "Cost": 20.0, "Base_Price": 55.0},
    {"Product_ID": "PROD-112", "Product_Name": "Premium Leather Office Chair", "Category": "Furniture", "Sub_Category": "Chairs", "Cost": 180.0, "Base_Price": 380.0},
    {"Product_ID": "PROD-113", "Product_Name": "Heavy-Duty Shredder", "Category": "Office Supplies", "Sub_Category": "Equipment", "Cost": 80.0, "Base_Price": 175.0},
    {"Product_ID": "PROD-114", "Product_Name": "Recycled Printer Paper (Case)", "Category": "Office Supplies", "Sub_Category": "Paper", "Cost": 18.0, "Base_Price": 42.0},
    {"Product_ID": "PROD-115", "Product_Name": "Gel Ink Pens (Pack of 24)", "Category": "Office Supplies", "Sub_Category": "Stationery", "Cost": 5.0, "Base_Price": 16.0},
    {"Product_ID": "PROD-116", "Product_Name": "Thermal Label Printer", "Category": "Office Supplies", "Sub_Category": "Equipment", "Cost": 90.0, "Base_Price": 210.0},
    {"Product_ID": "PROD-117", "Product_Name": "Heavy Duty Binder Clips (Box)", "Category": "Office Supplies", "Sub_Category": "Stationery", "Cost": 3.0, "Base_Price": 12.0},
    {"Product_ID": "PROD-118", "Product_Name": "Desk Storage Organizer Tray", "Category": "Office Supplies", "Sub_Category": "Storage", "Cost": 8.0, "Base_Price": 24.0}
]

regions = ["North", "South", "East", "West", "Central"]

# Customer database
customers = [
    {"Customer_ID": f"CUST-{1000+i}", "Customer_Name": name, "Segment": seg}
    for i, (name, seg) in enumerate([
        ("Apex Global Tech", "Corporate"), ("Summit Solutions", "Corporate"),
        ("BlueSky Dynamics", "Consumer"), ("Horizon Retail Group", "Home Office"),
        ("Vanguard Industries", "Corporate"), ("Nexus Systems Inc", "Corporate"),
        ("Pinnacle Enterprises", "Corporate"), ("Starlight Digital", "Consumer"),
        ("Cascade Logistics", "Corporate"), ("Quantum Innovations", "Corporate"),
        ("Beacon Financial", "Corporate"), ("Silverline Healthcare", "Corporate"),
        ("Crestview Media", "Consumer"), ("Titan Supply Co", "Home Office"),
        ("Omega Software", "Corporate"), ("Alpha Retailers", "Consumer"),
        ("Eclipse Networks", "Corporate"), ("Zenith Consulting", "Home Office"),
        ("Prism Interactive", "Consumer"), ("Atlas Ventures", "Corporate"),
        ("Nova Analytics", "Corporate"), ("Veritas Partners", "Corporate"),
        ("Orion Tech Labs", "Corporate"), ("Meridian Energy", "Corporate"),
        ("Sterling Commerce", "Consumer")
    ])
]

# Generate records
data = []
for i in range(n_records):
    order_id = f"ORD-{20240001 + i}"
    order_date = dates[i]
    prod = np.random.choice(products)
    cust = np.random.choice(customers)
    region = np.random.choice(regions)
    
    # Quantity between 1 and 10
    quantity = int(np.random.choice([1, 2, 3, 4, 5, 6, 8, 10], p=[0.3, 0.25, 0.15, 0.1, 0.1, 0.05, 0.03, 0.02]))
    
    # Discount between 0% and 20%
    discount = float(np.random.choice([0.0, 0.05, 0.10, 0.15, 0.20], p=[0.5, 0.2, 0.15, 0.1, 0.05]))
    
    unit_price = prod["Base_Price"]
    unit_cost = prod["Cost"]
    
    revenue = round(quantity * unit_price * (1 - discount), 2)
    total_cost = round(quantity * unit_cost, 2)
    profit = round(revenue - total_cost, 2)
    
    data.append({
        "Order_ID": order_id,
        "Order_Date": order_date.strftime("%Y-%m-%d"),
        "Customer_ID": cust["Customer_ID"],
        "Customer_Name": cust["Customer_Name"],
        "Segment": cust["Segment"],
        "Region": region,
        "Product_ID": prod["Product_ID"],
        "Product_Name": prod["Product_Name"],
        "Category": prod["Category"],
        "Sub_Category": prod["Sub_Category"],
        "Quantity": quantity,
        "Unit_Price": unit_price,
        "Discount": discount,
        "Sales": revenue,
        "Profit": profit
    })

df_clean = pd.DataFrame(data)

# Create raw dataset with minor dirty records (for cleaning step demonstration)
df_raw = df_clean.copy()

# Add 25 duplicate rows
duplicates = df_raw.sample(n=25, random_state=42)
df_raw = pd.concat([df_raw, duplicates], ignore_index=True)

# Introduce a few missing values in Region and Segment (to be cleaned)
df_raw.loc[10:14, "Region"] = np.nan
df_raw.loc[50:53, "Segment"] = None

# Save raw dataset
raw_csv_path = os.path.join(DATA_DIR, "raw_sales_data.csv")
df_raw.to_csv(raw_csv_path, index=False)
print(f"Raw dataset created: {raw_csv_path} ({len(df_raw)} rows)")

# Save clean CSV and XLSX datasets
clean_csv_path = os.path.join(DATA_DIR, "cleaned_sales_data.csv")
clean_xlsx_path = os.path.join(DATA_DIR, "cleaned_sales_data.xlsx")

df_clean.to_csv(clean_csv_path, index=False)
df_clean.to_excel(clean_xlsx_path, index=False, sheet_name="Sales_Data")

print(f"Cleaned CSV dataset created: {clean_csv_path} ({len(df_clean)} rows)")
print(f"Cleaned Excel dataset created: {clean_xlsx_path} ({len(df_clean)} rows)")

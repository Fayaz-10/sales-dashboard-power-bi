"""
================================================================================
SYNTHETIC SALES DATA GENERATOR (JANUARY 2024 - DECEMBER 2025)
================================================================================
Role: Data Analyst & Data Engineer
Purpose: Generates a realistic, internally consistent synthetic B2B/Retail
         sales dataset for Power BI portfolio demonstration.
DISCLAIMER: This dataset is entirely synthetic and generated for educational
            and portfolio purposes. It does not represent any real commercial entity.
================================================================================
"""

import os
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# Set fixed random seed for 100% reproducibility
np.random.seed(42)
random.seed(42)

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
os.makedirs(DATA_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. Product Catalog (3 Categories, 11 Subcategories, 20 SKUs)
# -----------------------------------------------------------------------------
PRODUCTS = [
    # Technology (Computers, Monitors, Accessories, Audio)
    {"Product_ID": "PROD-101", "Product_Name": "Enterprise Laptop Pro", "Category": "Technology", "Subcategory": "Computers", "Unit_Cost": 750.0, "Unit_Price": 1200.0},
    {"Product_ID": "PROD-102", "Product_Name": "Ultrabook Slim 14\"", "Category": "Technology", "Subcategory": "Computers", "Unit_Cost": 600.0, "Unit_Price": 950.0},
    {"Product_ID": "PROD-103", "Product_Name": "UltraWide 34\" Monitor", "Category": "Technology", "Subcategory": "Monitors", "Unit_Cost": 360.0, "Unit_Price": 600.0},
    {"Product_ID": "PROD-104", "Product_Name": "27\" 4K UHD Monitor", "Category": "Technology", "Subcategory": "Monitors", "Unit_Cost": 250.0, "Unit_Price": 420.0},
    {"Product_ID": "PROD-105", "Product_Name": "Wireless Ergonomic Mouse", "Category": "Technology", "Subcategory": "Accessories", "Unit_Cost": 18.0, "Unit_Price": 45.0},
    {"Product_ID": "PROD-106", "Product_Name": "Mechanical RGB Keyboard", "Category": "Technology", "Subcategory": "Accessories", "Unit_Cost": 42.0, "Unit_Price": 95.0},
    {"Product_ID": "PROD-107", "Product_Name": "4K Web Camera Pro", "Category": "Technology", "Subcategory": "Accessories", "Unit_Cost": 52.0, "Unit_Price": 110.0},
    {"Product_ID": "PROD-108", "Product_Name": "Noise-Canceling Headset", "Category": "Technology", "Subcategory": "Audio", "Unit_Cost": 75.0, "Unit_Price": 180.0},

    # Furniture (Chairs, Desks, Storage, Lighting)
    {"Product_ID": "PROD-109", "Product_Name": "Ergonomic Mesh Desk Chair", "Category": "Furniture", "Subcategory": "Chairs", "Unit_Cost": 120.0, "Unit_Price": 250.0},
    {"Product_ID": "PROD-110", "Product_Name": "Premium Leather Office Chair", "Category": "Furniture", "Subcategory": "Chairs", "Unit_Cost": 185.0, "Unit_Price": 380.0},
    {"Product_ID": "PROD-111", "Product_Name": "Motorized Standing Desk", "Category": "Furniture", "Subcategory": "Desks", "Unit_Cost": 230.0, "Unit_Price": 480.0},
    {"Product_ID": "PROD-112", "Product_Name": "Executive Wooden Desk", "Category": "Furniture", "Subcategory": "Desks", "Unit_Cost": 410.0, "Unit_Price": 850.0},
    {"Product_ID": "PROD-113", "Product_Name": "Filing Cabinet 3-Drawer", "Category": "Furniture", "Subcategory": "Storage", "Unit_Cost": 65.0, "Unit_Price": 140.0},
    {"Product_ID": "PROD-114", "Product_Name": "LED Desk Lamp with Charger", "Category": "Furniture", "Subcategory": "Lighting", "Unit_Cost": 22.0, "Unit_Price": 55.0},

    # Office Supplies (Equipment, Paper, Stationery, Storage)
    {"Product_ID": "PROD-115", "Product_Name": "Heavy-Duty Paper Shredder", "Category": "Office Supplies", "Subcategory": "Equipment", "Unit_Cost": 80.0, "Unit_Price": 175.0},
    {"Product_ID": "PROD-116", "Product_Name": "Thermal Label Printer", "Category": "Office Supplies", "Subcategory": "Equipment", "Unit_Cost": 92.0, "Unit_Price": 210.0},
    {"Product_ID": "PROD-117", "Product_Name": "Recycled Printer Paper Case", "Category": "Office Supplies", "Subcategory": "Paper", "Unit_Cost": 18.0, "Unit_Price": 42.0},
    {"Product_ID": "PROD-118", "Product_Name": "Glossy Heavy Photo Paper", "Category": "Office Supplies", "Subcategory": "Paper", "Unit_Cost": 12.0, "Unit_Price": 28.0},
    {"Product_ID": "PROD-119", "Product_Name": "Gel Ink Pens (Pack of 24)", "Category": "Office Supplies", "Subcategory": "Stationery", "Unit_Cost": 5.5, "Unit_Price": 16.0},
    {"Product_ID": "PROD-120", "Product_Name": "Heavy Duty Binder Clips Box", "Category": "Office Supplies", "Subcategory": "Stationery", "Unit_Cost": 3.5, "Unit_Price": 12.0}
]

# -----------------------------------------------------------------------------
# 2. Geographic Regions & States Mapping
# -----------------------------------------------------------------------------
REGION_STATE_MAP = {
    "West": ["California", "Washington", "Oregon"],
    "East": ["New York", "Massachusetts", "Pennsylvania"],
    "Central": ["Illinois", "Ohio", "Michigan"],
    "South": ["Texas", "Florida", "Georgia"],
    "North": ["Minnesota", "Wisconsin", "Iowa"]
}

# -----------------------------------------------------------------------------
# 3. Customer Directory (25 Realistic B2B & Retail Clients)
# -----------------------------------------------------------------------------
CUSTOMERS = [
    {"Customer_ID": "CUST-1001", "Customer_Name": "Apex Global Tech", "Segment": "Corporate", "Region": "West", "State": "California"},
    {"Customer_ID": "CUST-1002", "Customer_Name": "Summit Solutions", "Segment": "Corporate", "Region": "Central", "State": "Illinois"},
    {"Customer_ID": "CUST-1003", "Customer_Name": "BlueSky Dynamics", "Segment": "Consumer", "Region": "East", "State": "New York"},
    {"Customer_ID": "CUST-1004", "Customer_Name": "Horizon Retail Group", "Segment": "Home Office", "Region": "South", "State": "Texas"},
    {"Customer_ID": "CUST-1005", "Customer_Name": "Vanguard Industries", "Segment": "Corporate", "Region": "North", "State": "Minnesota"},
    {"Customer_ID": "CUST-1006", "Customer_Name": "Nexus Systems Inc", "Segment": "Corporate", "Region": "West", "State": "Washington"},
    {"Customer_ID": "CUST-1007", "Customer_Name": "Pinnacle Enterprises", "Segment": "Corporate", "Region": "East", "State": "Massachusetts"},
    {"Customer_ID": "CUST-1008", "Customer_Name": "Starlight Digital", "Segment": "Consumer", "Region": "Central", "State": "Ohio"},
    {"Customer_ID": "CUST-1009", "Customer_Name": "Cascade Logistics", "Segment": "Corporate", "Region": "West", "State": "Oregon"},
    {"Customer_ID": "CUST-1010", "Customer_Name": "Quantum Innovations", "Segment": "Corporate", "Region": "South", "State": "Florida"},
    {"Customer_ID": "CUST-1011", "Customer_Name": "Beacon Financial", "Segment": "Corporate", "Region": "East", "State": "New York"},
    {"Customer_ID": "CUST-1012", "Customer_Name": "Silverline Healthcare", "Segment": "Corporate", "Region": "Central", "State": "Michigan"},
    {"Customer_ID": "CUST-1013", "Customer_Name": "Crestview Media", "Segment": "Consumer", "Region": "West", "State": "California"},
    {"Customer_ID": "CUST-1014", "Customer_Name": "Titan Supply Co", "Segment": "Home Office", "Region": "South", "State": "Georgia"},
    {"Customer_ID": "CUST-1015", "Customer_Name": "Omega Software", "Segment": "Corporate", "Region": "North", "State": "Wisconsin"},
    {"Customer_ID": "CUST-1016", "Customer_Name": "Alpha Retailers", "Segment": "Consumer", "Region": "East", "State": "Pennsylvania"},
    {"Customer_ID": "CUST-1017", "Customer_Name": "Eclipse Networks", "Segment": "Corporate", "Region": "West", "State": "California"},
    {"Customer_ID": "CUST-1018", "Customer_Name": "Zenith Consulting", "Segment": "Home Office", "Region": "Central", "State": "Illinois"},
    {"Customer_ID": "CUST-1019", "Customer_Name": "Prism Interactive", "Segment": "Consumer", "Region": "South", "State": "Texas"},
    {"Customer_ID": "CUST-1020", "Customer_Name": "Atlas Ventures", "Segment": "Corporate", "Region": "East", "State": "New York"},
    {"Customer_ID": "CUST-1021", "Customer_Name": "Nova Analytics", "Segment": "Corporate", "Region": "West", "State": "Washington"},
    {"Customer_ID": "CUST-1022", "Customer_Name": "Veritas Partners", "Segment": "Corporate", "Region": "Central", "State": "Ohio"},
    {"Customer_ID": "CUST-1023", "Customer_Name": "Orion Tech Labs", "Segment": "Corporate", "Region": "South", "State": "Florida"},
    {"Customer_ID": "CUST-1024", "Customer_Name": "Meridian Energy", "Segment": "Corporate", "Region": "North", "State": "Iowa"},
    {"Customer_ID": "CUST-1025", "Customer_Name": "Sterling Commerce", "Segment": "Consumer", "Region": "West", "State": "California"}
]

PAYMENT_METHODS = ["Credit Card", "Bank Transfer", "PayPal", "Purchase Order"]
PAYMENT_WEIGHTS = [0.45, 0.30, 0.15, 0.10]

# -----------------------------------------------------------------------------
# 4. Generate Clean Target Dataset (Exactly 2,500 Valid Records)
# -----------------------------------------------------------------------------
N_CLEAN_RECORDS = 2500
START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2025, 12, 31)
TOTAL_DAYS = (END_DATE - START_DATE).days + 1

# Generate evenly distributed dates across 2024 and 2025 with slight seasonality
random_days = np.random.randint(0, TOTAL_DAYS, N_CLEAN_RECORDS)
# Sort dates slightly to mirror natural time-series progression
random_days.sort()
dates = [START_DATE + timedelta(days=int(d)) for d in random_days]

records = []
for i in range(N_CLEAN_RECORDS):
    order_id = f"ORD-{20240001 + i}"
    order_date = dates[i]
    prod = random.choice(PRODUCTS)
    cust = random.choice(CUSTOMERS)
    
    # 85% of transactions occur in customer's primary region/state, 15% in alternate branch
    if random.random() < 0.85:
        region = cust["Region"]
        state = cust["State"]
    else:
        region = random.choice(list(REGION_STATE_MAP.keys()))
        state = random.choice(REGION_STATE_MAP[region])
        
    payment_method = np.random.choice(PAYMENT_METHODS, p=PAYMENT_WEIGHTS)
    
    # Quantity distribution (1 to 10 units, weighted toward smaller purchases)
    quantity = int(np.random.choice(
        [1, 2, 3, 4, 5, 6, 8, 10],
        p=[0.30, 0.25, 0.15, 0.10, 0.10, 0.05, 0.03, 0.02]
    ))
    
    # Discount distribution (0%, 5%, 10%, 15%, 20%)
    discount = float(np.random.choice(
        [0.00, 0.05, 0.10, 0.15, 0.20],
        p=[0.50, 0.20, 0.15, 0.10, 0.05]
    ))
    
    unit_price = prod["Unit_Price"]
    unit_cost = prod["Unit_Cost"]
    
    # Financial calculations
    revenue = round(quantity * unit_price * (1.0 - discount), 2)
    cost = round(quantity * unit_cost, 2)
    profit = round(revenue - cost, 2)
    
    records.append({
        "Order_ID": order_id,
        "Order_Date": order_date.strftime("%Y-%m-%d"),
        "Customer_ID": cust["Customer_ID"],
        "Customer_Name": cust["Customer_Name"],
        "Segment": cust["Segment"],
        "Product_ID": prod["Product_ID"],
        "Product_Name": prod["Product_Name"],
        "Category": prod["Category"],
        "Subcategory": prod["Subcategory"],
        "Region": region,
        "State": state,
        "Quantity": quantity,
        "Unit_Price": unit_price,
        "Discount": discount,
        "Revenue": revenue,
        "Cost": cost,
        "Profit": profit,
        "Payment_Method": payment_method
    })

df_clean = pd.DataFrame(records)

# -----------------------------------------------------------------------------
# 5. Inject Controlled Raw Dataset Anomalies (For Educational Cleaning Pipeline)
# -----------------------------------------------------------------------------
df_raw = df_clean.copy()

# A. Inject exactly 35 duplicate records
duplicate_indices = np.random.choice(df_raw.index, size=35, replace=False)
duplicates = df_raw.loc[duplicate_indices].copy()
df_raw = pd.concat([df_raw, duplicates], ignore_index=True)

# B. Inject 12 missing values in State
missing_state_idx = np.random.choice(range(100, 500), size=12, replace=False)
df_raw.loc[missing_state_idx, "State"] = np.nan

# C. Inject 8 missing values in Payment_Method
missing_pm_idx = np.random.choice(range(600, 1000), size=8, replace=False)
df_raw.loc[missing_pm_idx, "Payment_Method"] = np.nan

# D. Inject 6 whitespace / casing anomalies in Category and Region
df_raw.loc[15, "Category"] = "Technology "
df_raw.loc[42, "Category"] = " furniture "
df_raw.loc[88, "Region"] = "West "
df_raw.loc[120, "Region"] = " central"

# E. Inject 4 non-standard date formats (YYYY/MM/DD)
df_raw.loc[200, "Order_Date"] = df_raw.loc[200, "Order_Date"].replace("-", "/")
df_raw.loc[205, "Order_Date"] = df_raw.loc[205, "Order_Date"].replace("-", "/")

# Shuffle raw records slightly to mimic raw database export
df_raw = df_raw.sample(frac=1.0, random_state=42).reset_index(drop=True)

# -----------------------------------------------------------------------------
# 6. Save Raw & Initial Clean Datasets
# -----------------------------------------------------------------------------
raw_csv_path = os.path.join(DATA_DIR, "raw_sales_data.csv")
clean_csv_path = os.path.join(DATA_DIR, "cleaned_sales_data.csv")
clean_xlsx_path = os.path.join(DATA_DIR, "cleaned_sales_data.xlsx")

df_raw.to_csv(raw_csv_path, index=False)
df_clean.to_csv(clean_csv_path, index=False)
df_clean.to_excel(clean_xlsx_path, index=False, sheet_name="Sales_Data")

print(f"[SUCCESS] Synthetic Data Generation Complete!")
print(f" -> Raw Dataset:     {raw_csv_path} ({len(df_raw)} rows)")
print(f" -> Cleaned CSV:     {clean_csv_path} ({len(df_clean)} rows)")
print(f" -> Cleaned Excel:   {clean_xlsx_path} ({len(df_clean)} rows)")
print(f" -> Columns ({len(df_clean.columns)}): {list(df_clean.columns)}")

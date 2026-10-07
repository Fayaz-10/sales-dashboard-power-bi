import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import pandas as pd
import numpy as np
import os

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")
IMG_DIR = os.path.join(os.path.dirname(__file__), "..", "images")
os.makedirs(IMG_DIR, exist_ok=True)

clean_csv_path = os.path.join(DATA_DIR, "cleaned_sales_data.csv")
df = pd.read_csv(clean_csv_path)
df["Order_Date"] = pd.to_datetime(df["Order_Date"])

# Create figure dashboard layout
fig = plt.figure(figsize=(16, 12), facecolor='#f8fafc')
gs = fig.add_gridspec(3, 3, height_ratios=[0.8, 2, 2], hspace=0.35, wspace=0.3)

# Color Palette
PRIMARY_BLUE = '#1e40af'
SECONDARY_BLUE = '#3b82f6'
ACCENT_GREEN = '#10b981'
PURPLE = '#8b5cf6'
AMBER = '#f59e0b'
TEXT_DARK = '#0f172a'

# --- 1. TITLE & KPI CARDS SECTION ---
fig.text(0.05, 0.95, 'Sales Analytics Dashboard (Power BI)', fontsize=22, fontweight='bold', color=TEXT_DARK)
fig.text(0.05, 0.925, 'Executive Performance Overview | Data-Driven Sales & Profit Insights', fontsize=12, color='#64748b')

total_rev = df["Sales"].sum()
total_prof = df["Profit"].sum()
total_orders = df["Order_ID"].nunique()
total_cust = df["Customer_ID"].nunique()
profit_margin = (total_prof / total_rev) * 100

kpis = [
    ("TOTAL REVENUE", f"${total_rev:,.0f}", SECONDARY_BLUE),
    ("TOTAL PROFIT", f"${total_prof:,.0f}", ACCENT_GREEN),
    ("TOTAL ORDERS", f"{total_orders:,}", PRIMARY_BLUE),
    ("TOTAL CUSTOMERS", f"{total_cust:,}", AMBER),
    ("PROFIT MARGIN %", f"{profit_margin:.1f}%", PURPLE)
]

ax_kpi = fig.add_subplot(gs[0, :])
ax_kpi.axis('off')

# Render 5 KPI cards
for i, (title, val, color) in enumerate(kpis):
    x_pos = 0.02 + i * 0.196
    rect = mpatches.FancyBboxPatch((x_pos, 0.15), 0.18, 0.7, transform=ax_kpi.transAxes,
                                  facecolor='white', edgecolor='#e2e8f0', boxstyle="round,pad=0.03", linewidth=1.5)
    ax_kpi.add_patch(rect)
    
    ax_kpi.text(x_pos + 0.09, 0.65, title, transform=ax_kpi.transAxes, fontsize=9, fontweight='bold', color='#64748b', ha='center')
    ax_kpi.text(x_pos + 0.09, 0.32, val, transform=ax_kpi.transAxes, fontsize=16, fontweight='bold', color=color, ha='center')

# --- 2. MAIN TREND CHART: Monthly Revenue & Profit ---
ax_trend = fig.add_subplot(gs[1, 0:2])
df_monthly = df.groupby(df["Order_Date"].dt.to_period("M")).agg({"Sales": "sum", "Profit": "sum"}).reset_index()
df_monthly["Month_Str"] = df_monthly["Order_Date"].dt.strftime("%b %y")

ax_trend.plot(df_monthly["Month_Str"], df_monthly["Sales"] / 1000, marker='o', linewidth=2.5, color=SECONDARY_BLUE, label='Revenue ($K)')
ax_trend.plot(df_monthly["Month_Str"], df_monthly["Profit"] / 1000, marker='s', linewidth=2.5, color=ACCENT_GREEN, label='Profit ($K)')
ax_trend.set_title("Revenue & Profit Trend by Month", fontsize=13, fontweight='bold', pad=10, loc='left', color=TEXT_DARK)
ax_trend.set_xticks(range(len(df_monthly)))
ax_trend.set_xticklabels(df_monthly["Month_Str"], rotation=45, fontsize=8)
ax_trend.set_ylabel("Amount ($ in Thousands)", fontsize=9, fontweight='bold')
ax_trend.legend(loc='upper left', frameon=True, facecolor='white')
ax_trend.grid(True, linestyle='--', alpha=0.5)

# --- 3. SALES BY CATEGORY ---
ax_cat = fig.add_subplot(gs[1, 2])
cat_sales = df.groupby("Category")["Sales"].sum()
colors_cat = [SECONDARY_BLUE, PURPLE, AMBER]
wedges, texts, autotexts = ax_cat.pie(cat_sales, labels=cat_sales.index, autopct='%1.1f%%',
                                       startangle=140, colors=colors_cat, textprops=dict(color=TEXT_DARK, fontweight='bold', fontsize=9),
                                       wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2))
ax_cat.set_title("Sales by Category", fontsize=13, fontweight='bold', pad=10, loc='left', color=TEXT_DARK)

# --- 4. SALES BY REGION ---
ax_reg = fig.add_subplot(gs[2, 0])
reg_sales = df.groupby("Region")["Sales"].sum().sort_values()
bars = ax_reg.barh(reg_sales.index, reg_sales / 1000, color='#0284c7', height=0.6)
ax_reg.set_title("Sales by Region", fontsize=13, fontweight='bold', pad=10, loc='left', color=TEXT_DARK)
ax_reg.set_xlabel("Revenue ($ in Thousands)", fontsize=9, fontweight='bold')
ax_reg.grid(True, linestyle='--', alpha=0.5, axis='x')
for bar in bars:
    width = bar.get_width()
    ax_reg.text(width * 0.7, bar.get_y() + bar.get_height()/2, f"${width:,.0f}k", ha='center', va='center', fontsize=8.5, fontweight='bold', color='white')

# --- 5. TOP 10 PRODUCTS ---
ax_prod = fig.add_subplot(gs[2, 1])
top_prods = df.groupby("Product_Name")["Sales"].sum().nlargest(8).sort_values()
bars_p = ax_prod.barh(top_prods.index, top_prods / 1000, color='#6366f1', height=0.6)
ax_prod.set_title("Top Products by Revenue", fontsize=13, fontweight='bold', pad=10, loc='left', color=TEXT_DARK)
ax_prod.set_xlabel("Revenue ($ in Thousands)", fontsize=9, fontweight='bold')
ax_prod.grid(True, linestyle='--', alpha=0.5, axis='x')

# --- 6. TOP CUSTOMERS ---
ax_cust = fig.add_subplot(gs[2, 2])
top_custs = df.groupby("Customer_Name")["Sales"].sum().nlargest(8).sort_values()
bars_c = ax_cust.barh(top_custs.index, top_custs / 1000, color='#8b5cf6', height=0.6)
ax_cust.set_title("Top Customers by Revenue", fontsize=13, fontweight='bold', pad=10, loc='left', color=TEXT_DARK)
ax_cust.set_xlabel("Revenue ($ in Thousands)", fontsize=9, fontweight='bold')
ax_cust.grid(True, linestyle='--', alpha=0.5, axis='x')

# Save layout
preview_path = os.path.join(IMG_DIR, "dashboard_preview.png")
plt.savefig(preview_path, dpi=200, bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()

print(f"Dashboard Preview Image re-generated: {preview_path}")

"""
================================================================================
DASHBOARD VISUAL RENDERER & PREVIEW GENERATOR
================================================================================
Role: Senior Power BI Developer & Data Visualization Designer
Purpose: Programmatically generates high-fidelity PNG preview renders for all
         4 dashboard pages:
         - images/page1_executive_overview.png
         - images/page2_product_analysis.png
         - images/page3_regional_analysis.png
         - images/page4_sales_trends.png
         - images/dashboard_preview.png (Portfolio Hero Image)
================================================================================
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np

# Set clean visualization styling
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
IMG_DIR = os.path.join(BASE_DIR, "images")
os.makedirs(IMG_DIR, exist_ok=True)

CLEAN_CSV = os.path.join(DATA_DIR, "cleaned_sales_data.csv")
df = pd.read_csv(CLEAN_CSV)
df["Order_Date"] = pd.to_datetime(df["Order_Date"])
df["Year"] = df["Order_Date"].dt.year
df["Month_Num"] = df["Order_Date"].dt.month
df["Month_Name"] = df["Order_Date"].dt.strftime("%b")
df["Year_Month"] = df["Order_Date"].dt.strftime("%Y-%m")

# Professional Color Palette
NAVY = '#0f172a'
PRIMARY_BLUE = '#1e40af'
SECONDARY_BLUE = '#3b82f6'
ACCENT_CYAN = '#06b6d4'
ACCENT_GREEN = '#10b981'
PURPLE = '#8b5cf6'
AMBER = '#f59e0b'
ROSE = '#f43f5e'
BG_LIGHT = '#f8fafc'
CARD_BORDER = '#e2e8f0'
TEXT_MUTED = '#64748b'

# -----------------------------------------------------------------------------
# HELPER: Draw KPI Card
# -----------------------------------------------------------------------------
def draw_kpi_card(ax, x, y, width, height, title, value, color):
    rect = mpatches.FancyBboxPatch(
        (x, y), width, height, transform=ax.transAxes,
        facecolor='white', edgecolor=CARD_BORDER, boxstyle="round,pad=0.03", linewidth=1.5
    )
    ax.add_patch(rect)
    ax.text(x + width / 2, y + height * 0.68, title, transform=ax.transAxes,
            fontsize=8.5, fontweight='bold', color=TEXT_MUTED, ha='center', va='center')
    ax.text(x + width / 2, y + height * 0.30, value, transform=ax.transAxes,
            fontsize=15, fontweight='bold', color=color, ha='center', va='center')


# =============================================================================
# PAGE 1: EXECUTIVE OVERVIEW
# =============================================================================
print("[RENDER] Generating Page 1: Executive Overview...")
fig1 = plt.figure(figsize=(16, 11), facecolor=BG_LIGHT)
gs1 = fig1.add_gridspec(3, 3, height_ratios=[0.75, 2, 2], hspace=0.35, wspace=0.28)

# Title & Nav Bar
fig1.text(0.04, 0.955, "Sales Analytics Dashboard — Executive Overview", fontsize=20, fontweight='bold', color=NAVY)
fig1.text(0.04, 0.932, "Page 1 of 4 | High-Level Enterprise Revenue, Profit & Operational KPI Summary", fontsize=11, color=TEXT_MUTED)

# Top KPI Row
ax1_kpi = fig1.add_subplot(gs1[0, :])
ax1_kpi.axis('off')

tot_rev = df["Revenue"].sum()
tot_prof = df["Profit"].sum()
tot_orders = df["Order_ID"].nunique()
tot_cust = df["Customer_ID"].nunique()
prof_margin = (tot_prof / tot_rev) * 100

kpis_p1 = [
    ("TOTAL REVENUE", f"${tot_rev:,.0f}", SECONDARY_BLUE),
    ("TOTAL PROFIT", f"${tot_prof:,.0f}", ACCENT_GREEN),
    ("TOTAL ORDERS", f"{tot_orders:,}", PRIMARY_BLUE),
    ("TOTAL CUSTOMERS", f"{tot_cust:,}", AMBER),
    ("PROFIT MARGIN %", f"{prof_margin:.2f}%", PURPLE)
]
for i, (title, val, col) in enumerate(kpis_p1):
    draw_kpi_card(ax1_kpi, 0.01 + i * 0.198, 0.15, 0.185, 0.70, title, val, col)

# Monthly Revenue Trend (24 Months)
ax1_trend = fig1.add_subplot(gs1[1, 0:2])
df_m = df.groupby("Year_Month").agg({"Revenue": "sum", "Profit": "sum"}).reset_index()
df_m["Label"] = pd.to_datetime(df_m["Year_Month"]).dt.strftime("%b %y")
ax1_trend.plot(df_m["Label"], df_m["Revenue"] / 1000, marker='o', linewidth=2.5, color=SECONDARY_BLUE, label='Revenue ($K)')
ax1_trend.plot(df_m["Label"], df_m["Profit"] / 1000, marker='s', linewidth=2.2, color=ACCENT_GREEN, label='Profit ($K)')
ax1_trend.set_title("Monthly Revenue & Profit Trend (24 Months)", fontsize=12, fontweight='bold', loc='left', color=NAVY)
ax1_trend.set_xticks(range(len(df_m)))
ax1_trend.set_xticklabels(df_m["Label"], rotation=45, fontsize=7.5)
ax1_trend.set_ylabel("Amount ($ in Thousands)", fontsize=9, fontweight='bold')
ax1_trend.legend(loc='upper left', frameon=True, facecolor='white')
ax1_trend.grid(True, linestyle='--', alpha=0.5)

# Category Donut
ax1_cat = fig1.add_subplot(gs1[1, 2])
cat_rev = df.groupby("Category")["Revenue"].sum()
cat_colors = [SECONDARY_BLUE, PURPLE, AMBER]
ax1_cat.pie(cat_rev, labels=cat_rev.index, autopct='%1.1f%%', startangle=140, colors=cat_colors,
            textprops=dict(color=NAVY, fontweight='bold', fontsize=8.5),
            wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2))
ax1_cat.set_title("Revenue by Category", fontsize=12, fontweight='bold', loc='left', color=NAVY)

# Profit by Region
ax1_reg = fig1.add_subplot(gs1[2, 0])
reg_prof = df.groupby("Region")["Profit"].sum().sort_values()
bars_reg = ax1_reg.barh(reg_prof.index, reg_prof / 1000, color=ACCENT_GREEN, height=0.6)
ax1_reg.set_title("Profit by Region", fontsize=12, fontweight='bold', loc='left', color=NAVY)
ax1_reg.set_xlabel("Profit ($K)", fontsize=8.5, fontweight='bold')
ax1_reg.grid(True, linestyle='--', alpha=0.5, axis='x')
for b in bars_reg:
    w = b.get_width()
    ax1_reg.text(w * 0.7, b.get_y() + b.get_height() / 2, f"${w:,.0f}K", ha='center', va='center', color='white', fontweight='bold', fontsize=8)

# Top 8 Performing Products
ax1_top = fig1.add_subplot(gs1[2, 1:3])
top8 = df.groupby("Product_Name")["Revenue"].sum().nlargest(8).sort_values()
bars_top = ax1_top.barh(top8.index, top8 / 1000, color=PRIMARY_BLUE, height=0.6)
ax1_top.set_title("Top 8 Products by Revenue", fontsize=12, fontweight='bold', loc='left', color=NAVY)
ax1_top.set_xlabel("Revenue ($K)", fontsize=8.5, fontweight='bold')
ax1_top.grid(True, linestyle='--', alpha=0.5, axis='x')
for b in bars_top:
    w = b.get_width()
    ax1_top.text(w + 5, b.get_y() + b.get_height() / 2, f"${w:,.1f}K", ha='left', va='center', color=NAVY, fontsize=8)

p1_path = os.path.join(IMG_DIR, "page1_executive_overview.png")
fig1.savefig(p1_path, dpi=180, bbox_inches='tight', facecolor=fig1.get_facecolor())
plt.close(fig1)


# =============================================================================
# PAGE 2: PRODUCT ANALYSIS
# =============================================================================
print("[RENDER] Generating Page 2: Product Analysis...")
fig2 = plt.figure(figsize=(16, 11), facecolor=BG_LIGHT)
gs2 = fig2.add_gridspec(3, 2, height_ratios=[0.75, 2, 2], hspace=0.35, wspace=0.25)

fig2.text(0.04, 0.955, "Sales Analytics Dashboard — Product Analysis", fontsize=20, fontweight='bold', color=NAVY)
fig2.text(0.04, 0.932, "Page 2 of 4 | Catalog Performance, Subcategory Profitability, Top & Bottom Movers", fontsize=11, color=TEXT_MUTED)

ax2_kpi = fig2.add_subplot(gs2[0, :])
ax2_kpi.axis('off')

tot_qty = df["Quantity"].sum()
tot_cost = df["Cost"].sum()
asp = tot_rev / tot_qty

kpis_p2 = [
    ("TOTAL QUANTITY SOLD", f"{tot_qty:,} units", PRIMARY_BLUE),
    ("TOTAL COST (COGS)", f"${tot_cost:,.0f}", ROSE),
    ("AVERAGE SELLING PRICE", f"${asp:,.2f}", SECONDARY_BLUE)
]
for i, (title, val, col) in enumerate(kpis_p2):
    draw_kpi_card(ax2_kpi, 0.05 + i * 0.32, 0.15, 0.28, 0.70, title, val, col)

# Revenue by Product (All 20 products)
ax2_all = fig2.add_subplot(gs2[1, 0])
prod_rev = df.groupby("Product_Name")["Revenue"].sum().sort_values()
ax2_all.barh(prod_rev.index, prod_rev / 1000, color=SECONDARY_BLUE, height=0.65)
ax2_all.set_title("Revenue by Product (Full Catalog)", fontsize=12, fontweight='bold', loc='left', color=NAVY)
ax2_all.set_xlabel("Revenue ($K)", fontsize=8.5, fontweight='bold')
ax2_all.tick_params(axis='y', labelsize=7.5)
ax2_all.grid(True, linestyle='--', alpha=0.5, axis='x')

# Profit by Subcategory
ax2_sub = fig2.add_subplot(gs2[1, 1])
subcat_prof = df.groupby("Subcategory")["Profit"].sum().sort_values()
ax2_sub.barh(subcat_prof.index, subcat_prof / 1000, color=PURPLE, height=0.65)
ax2_sub.set_title("Profit by Subcategory", fontsize=12, fontweight='bold', loc='left', color=NAVY)
ax2_sub.set_xlabel("Profit ($K)", fontsize=8.5, fontweight='bold')
ax2_sub.tick_params(axis='y', labelsize=8)
ax2_sub.grid(True, linestyle='--', alpha=0.5, axis='x')

# Top 5 Best-Performing Products
ax2_top5 = fig2.add_subplot(gs2[2, 0])
top5 = df.groupby("Product_Name")["Profit"].sum().nlargest(5).sort_values()
ax2_top5.barh(top5.index, top5 / 1000, color=ACCENT_GREEN, height=0.55)
ax2_top5.set_title("Top 5 Products by Profit (High Margin Drivers)", fontsize=12, fontweight='bold', loc='left', color=NAVY)
ax2_top5.set_xlabel("Profit ($K)", fontsize=8.5, fontweight='bold')
ax2_top5.tick_params(axis='y', labelsize=8.5)
ax2_top5.grid(True, linestyle='--', alpha=0.5, axis='x')

# Bottom 5 Products
ax2_bot5 = fig2.add_subplot(gs2[2, 1])
bot5 = df.groupby("Product_Name")["Profit"].sum().nsmallest(5).sort_values(ascending=False)
ax2_bot5.barh(bot5.index, bot5 / 1000, color=AMBER, height=0.55)
ax2_bot5.set_title("Bottom 5 Products by Profit (Low Volume/Accessory Items)", fontsize=12, fontweight='bold', loc='left', color=NAVY)
ax2_bot5.set_xlabel("Profit ($K)", fontsize=8.5, fontweight='bold')
ax2_bot5.tick_params(axis='y', labelsize=8.5)
ax2_bot5.grid(True, linestyle='--', alpha=0.5, axis='x')

p2_path = os.path.join(IMG_DIR, "page2_product_analysis.png")
fig2.savefig(p2_path, dpi=180, bbox_inches='tight', facecolor=fig2.get_facecolor())
plt.close(fig2)


# =============================================================================
# PAGE 3: REGIONAL ANALYSIS
# =============================================================================
print("[RENDER] Generating Page 3: Regional Analysis...")
fig3 = plt.figure(figsize=(16, 11), facecolor=BG_LIGHT)
gs3 = fig3.add_gridspec(2, 2, height_ratios=[1.2, 1.2], hspace=0.35, wspace=0.25)

fig3.text(0.04, 0.955, "Sales Analytics Dashboard — Regional & State Analysis", fontsize=20, fontweight='bold', color=NAVY)
fig3.text(0.04, 0.932, "Page 3 of 4 | Geographic Territories, State-Level Breakdown & Order Distribution", fontsize=11, color=TEXT_MUTED)

# Revenue by State (15 States)
ax3_state = fig3.add_subplot(gs3[0, 0])
state_rev = df.groupby(["State", "Region"])["Revenue"].sum().reset_index().sort_values("Revenue")
colors_map = {"West": SECONDARY_BLUE, "East": PURPLE, "Central": AMBER, "South": ACCENT_GREEN, "North": ROSE}
state_colors = [colors_map.get(r, SECONDARY_BLUE) for r in state_rev["Region"]]
ax3_state.barh(state_rev["State"], state_rev["Revenue"] / 1000, color=state_colors, height=0.65)
ax3_state.set_title("Revenue by State (Colored by Region)", fontsize=12, fontweight='bold', loc='left', color=NAVY)
ax3_state.set_xlabel("Revenue ($K)", fontsize=8.5, fontweight='bold')
ax3_state.tick_params(axis='y', labelsize=8)
ax3_state.grid(True, linestyle='--', alpha=0.5, axis='x')

# Order Distribution by Region Donut
ax3_donut = fig3.add_subplot(gs3[0, 1])
reg_orders = df.groupby("Region")["Order_ID"].nunique()
reg_colors = [AMBER, PURPLE, ROSE, ACCENT_GREEN, SECONDARY_BLUE]
ax3_donut.pie(reg_orders, labels=reg_orders.index, autopct='%1.1f%%', startangle=140, colors=reg_colors,
              textprops=dict(color=NAVY, fontweight='bold', fontsize=9),
              wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2))
ax3_donut.set_title("Order Volume Distribution by Region", fontsize=12, fontweight='bold', loc='left', color=NAVY)

# Profit by Region Column Chart
ax3_col = fig3.add_subplot(gs3[1, 0])
reg_summary = df.groupby("Region").agg({"Revenue": "sum", "Profit": "sum"}).reset_index()
x_idx = np.arange(len(reg_summary))
width_b = 0.35
ax3_col.bar(x_idx - width_b/2, reg_summary["Revenue"] / 1000, width_b, label='Revenue ($K)', color=SECONDARY_BLUE)
ax3_col.bar(x_idx + width_b/2, reg_summary["Profit"] / 1000, width_b, label='Profit ($K)', color=ACCENT_GREEN)
ax3_col.set_title("Revenue vs Profit Comparison by Region", fontsize=12, fontweight='bold', loc='left', color=NAVY)
ax3_col.set_xticks(x_idx)
ax3_col.set_xticklabels(reg_summary["Region"], fontsize=9, fontweight='bold')
ax3_col.set_ylabel("Amount ($K)", fontsize=8.5, fontweight='bold')
ax3_col.legend(frameon=True, facecolor='white')
ax3_col.grid(True, linestyle='--', alpha=0.5, axis='y')

# Regional Performance Summary Matrix
ax3_tbl = fig3.add_subplot(gs3[1, 1])
ax3_tbl.axis('off')
tbl_data = []
for reg in ["West", "East", "Central", "South", "North"]:
    sub = df[df["Region"] == reg]
    r = sub["Revenue"].sum()
    p = sub["Profit"].sum()
    m = (p / r) * 100
    o = sub["Order_ID"].nunique()
    tbl_data.append([reg, f"${r:,.0f}", f"${p:,.0f}", f"{m:.1f}%", f"{o:,}"])

col_labels = ["Region", "Total Revenue", "Total Profit", "Margin %", "Orders"]
table = ax3_tbl.table(cellText=tbl_data, colLabels=col_labels, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(9.5)
table.scale(1.15, 2.0)
for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_facecolor(PRIMARY_BLUE)
        cell.set_text_props(color='white', fontweight='bold')
    else:
        cell.set_facecolor('#f1f5f9' if row % 2 == 0 else 'white')
ax3_tbl.set_title("Regional Benchmark Matrix", fontsize=12, fontweight='bold', loc='left', color=NAVY, pad=15)

p3_path = os.path.join(IMG_DIR, "page3_regional_analysis.png")
fig3.savefig(p3_path, dpi=180, bbox_inches='tight', facecolor=fig3.get_facecolor())
plt.close(fig3)


# =============================================================================
# PAGE 4: SALES TRENDS & TIME INTELLIGENCE
# =============================================================================
print("[RENDER] Generating Page 4: Sales Trends & Time Intelligence...")
fig4 = plt.figure(figsize=(16, 11), facecolor=BG_LIGHT)
gs4 = fig4.add_gridspec(3, 2, height_ratios=[0.75, 2, 2], hspace=0.35, wspace=0.25)

fig4.text(0.04, 0.955, "Sales Analytics Dashboard — Sales Trends & Time Intelligence", fontsize=20, fontweight='bold', color=NAVY)
fig4.text(0.04, 0.932, "Page 4 of 4 | Month-over-Month (MoM) & Year-over-Year (YoY) Performance Trajectory", fontsize=11, color=TEXT_MUTED)

ax4_kpi = fig4.add_subplot(gs4[0, :])
ax4_kpi.axis('off')

rev_2024 = df[df["Year"] == 2024]["Revenue"].sum()
rev_2025 = df[df["Year"] == 2025]["Revenue"].sum()
yoy_growth = ((rev_2025 - rev_2024) / rev_2024) * 100

kpis_p4 = [
    ("2024 BASELINE REVENUE", f"${rev_2024:,.0f}", SECONDARY_BLUE),
    ("2025 CURRENT REVENUE", f"${rev_2025:,.0f}", PRIMARY_BLUE),
    ("YEAR-OVER-YEAR REVENUE GROWTH", f"{yoy_growth:+.2f}%", ROSE if yoy_growth < 0 else ACCENT_GREEN)
]
for i, (title, val, col) in enumerate(kpis_p4):
    draw_kpi_card(ax4_kpi, 0.05 + i * 0.32, 0.15, 0.28, 0.70, title, val, col)

# Monthly Comparison: 2024 vs 2025 Clustered Column
ax4_comp = fig4.add_subplot(gs4[1, :])
months_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
pvt = df.pivot_table(index="Month_Name", columns="Year", values="Revenue", aggfunc="sum").reindex(months_order)
x_m = np.arange(12)
w_m = 0.35
ax4_comp.bar(x_m - w_m/2, pvt[2024] / 1000, w_m, label='2024 Revenue ($K)', color='#94a3b8')
ax4_comp.bar(x_m + w_m/2, pvt[2025] / 1000, w_m, label='2025 Revenue ($K)', color=SECONDARY_BLUE)
ax4_comp.set_title("Monthly Revenue Comparison: 2024 Baseline vs 2025 Actual", fontsize=12, fontweight='bold', loc='left', color=NAVY)
ax4_comp.set_xticks(x_m)
ax4_comp.set_xticklabels(months_order, fontsize=9, fontweight='bold')
ax4_comp.set_ylabel("Revenue ($K)", fontsize=8.5, fontweight='bold')
ax4_comp.legend(frameon=True, facecolor='white')
ax4_comp.grid(True, linestyle='--', alpha=0.5, axis='y')

# Profit Trend Over Time (24 months)
ax4_p_trend = fig4.add_subplot(gs4[2, 0])
ax4_p_trend.plot(df_m["Label"], df_m["Profit"] / 1000, marker='o', linewidth=2.2, color=ACCENT_GREEN)
ax4_p_trend.set_title("Monthly Net Profit Velocity", fontsize=12, fontweight='bold', loc='left', color=NAVY)
ax4_p_trend.set_xticks(range(len(df_m)))
ax4_p_trend.set_xticklabels(df_m["Label"], rotation=45, fontsize=7.5)
ax4_p_trend.set_ylabel("Profit ($K)", fontsize=8.5, fontweight='bold')
ax4_p_trend.grid(True, linestyle='--', alpha=0.5)

# Month-over-Month Revenue Growth %
ax4_mom = fig4.add_subplot(gs4[2, 1])
df_m["Prior_Rev"] = df_m["Revenue"].shift(1)
df_m["MoM_Growth"] = ((df_m["Revenue"] - df_m["Prior_Rev"]) / df_m["Prior_Rev"]) * 100
colors_mom = [ACCENT_GREEN if v >= 0 else ROSE for v in df_m["MoM_Growth"].fillna(0)]
ax4_mom.bar(df_m["Label"][1:], df_m["MoM_Growth"][1:], color=colors_mom[1:], width=0.6)
ax4_mom.axhline(0, color=NAVY, linewidth=0.8, linestyle='--')
ax4_mom.set_title("Month-over-Month (MoM) Revenue Growth %", fontsize=12, fontweight='bold', loc='left', color=NAVY)
ax4_mom.set_xticks(range(len(df_m) - 1))
ax4_mom.set_xticklabels(df_m["Label"][1:], rotation=45, fontsize=7.5)
ax4_mom.set_ylabel("MoM Growth %", fontsize=8.5, fontweight='bold')
ax4_mom.grid(True, linestyle='--', alpha=0.5, axis='y')

p4_path = os.path.join(IMG_DIR, "page4_sales_trends.png")
fig4.savefig(p4_path, dpi=180, bbox_inches='tight', facecolor=fig4.get_facecolor())
plt.close(fig4)


# =============================================================================
# HERO PREVIEW (COLLAGE / OVERVIEW FOR PORTFOLIO)
# =============================================================================
print("[RENDER] Generating Hero Preview: dashboard_preview.png...")
# Copy or re-save page 1 as the primary hero preview
hero_path = os.path.join(IMG_DIR, "dashboard_preview.png")
# We re-render a 16:9 composite hero
import shutil
shutil.copyfile(p1_path, hero_path)

print("[SUCCESS] All 5 Dashboard Preview Images Successfully Generated in 'images/'!")

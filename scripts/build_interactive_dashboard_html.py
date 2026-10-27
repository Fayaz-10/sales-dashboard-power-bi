"""
================================================================================
INTERACTIVE 4-PAGE HTML DASHBOARD BUILDER
================================================================================
Role: Senior Frontend & BI Visualization Engineer
Purpose: Ingests data/cleaned_sales_data.csv and compiles a full-featured,
         4-page interactive web application (dashboard.html) with Chart.js,
         Tailwind CSS, interactive multi-slicer filtering, and DAX metric logic.
================================================================================
"""

import os
import json
import pandas as pd

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
CLEAN_CSV = os.path.join(DATA_DIR, "cleaned_sales_data.csv")
HTML_PATH = os.path.join(BASE_DIR, "dashboard.html")

df = pd.read_csv(CLEAN_CSV)
records_json = df.to_json(orient="records")

html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sales Analytics Dashboard — Power BI Interactive Preview</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        body {{ font-family: 'Inter', sans-serif; background-color: #f8fafc; }}
        .kpi-card {{ transition: transform 0.2s, box-shadow 0.2s; }}
        .kpi-card:hover {{ transform: translateY(-2px); box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.05); }}
        .tab-btn.active {{ background-color: #1e40af; color: #ffffff; border-color: #1e40af; }}
        .page-container {{ display: none; }}
        .page-container.active {{ display: block; }}
    </style>
</head>
<body class="text-slate-800 p-3 md:p-6 min-h-screen">

    <!-- Top App Bar -->
    <div class="max-w-7xl mx-auto mb-5 bg-white p-5 rounded-2xl shadow-sm border border-slate-200 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
        <div class="flex items-center space-x-3.5">
            <div class="bg-blue-600 text-white p-3 rounded-xl shadow-sm">
                <i data-lucide="bar-chart-3" class="w-7 h-7"></i>
            </div>
            <div>
                <h1 class="text-2xl font-extrabold text-slate-900 tracking-tight">Sales Analytics Dashboard</h1>
                <p class="text-xs font-medium text-slate-500">Power BI 4-Page Enterprise Architecture | Star Schema & 13 DAX Measures</p>
            </div>
        </div>
        <div class="flex flex-wrap items-center gap-2.5">
            <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800">
                <span class="w-2 h-2 rounded-full bg-emerald-500 mr-1.5 animate-pulse"></span> 2,500 Certified Orders
            </span>
            <button onclick="resetFilters()" class="text-xs flex items-center bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold px-3 py-2 rounded-lg border border-slate-300 transition">
                <i data-lucide="rotate-ccw" class="w-3.5 h-3.5 mr-1"></i> Reset Slicers
            </button>
        </div>
    </div>

    <!-- Navigation Tabs -->
    <div class="max-w-7xl mx-auto mb-5 flex flex-wrap gap-2 border-b border-slate-200 pb-3">
        <button onclick="switchTab('page1')" id="tab-page1" class="tab-btn active text-xs md:text-sm font-bold px-4 py-2.5 rounded-xl border border-slate-300 bg-white text-slate-700 transition flex items-center gap-2">
            <i data-lucide="layout-dashboard" class="w-4 h-4"></i> Page 1: Executive Overview
        </button>
        <button onclick="switchTab('page2')" id="tab-page2" class="tab-btn text-xs md:text-sm font-bold px-4 py-2.5 rounded-xl border border-slate-300 bg-white text-slate-700 transition flex items-center gap-2">
            <i data-lucide="box" class="w-4 h-4"></i> Page 2: Product Analysis
        </button>
        <button onclick="switchTab('page3')" id="tab-page3" class="tab-btn text-xs md:text-sm font-bold px-4 py-2.5 rounded-xl border border-slate-300 bg-white text-slate-700 transition flex items-center gap-2">
            <i data-lucide="map-pin" class="w-4 h-4"></i> Page 3: Regional Analysis
        </button>
        <button onclick="switchTab('page4')" id="tab-page4" class="tab-btn text-xs md:text-sm font-bold px-4 py-2.5 rounded-xl border border-slate-300 bg-white text-slate-700 transition flex items-center gap-2">
            <i data-lucide="trending-up" class="w-4 h-4"></i> Page 4: Sales Trends & Growth
        </button>
    </div>

    <!-- Universal Slicers Bar -->
    <div class="max-w-7xl mx-auto mb-6 bg-white p-4 rounded-xl shadow-sm border border-slate-200 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
        <div>
            <label class="block text-[11px] font-bold text-slate-600 uppercase mb-1">Year Slicer</label>
            <select id="slicer-year" onchange="applyFilters()" class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg p-2 font-semibold">
                <option value="ALL">All Years (2024 - 2025)</option>
                <option value="2024">2024 Baseline</option>
                <option value="2025">2025 Actual</option>
            </select>
        </div>
        <div>
            <label class="block text-[11px] font-bold text-slate-600 uppercase mb-1">Region Slicer</label>
            <select id="slicer-region" onchange="applyFilters()" class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg p-2 font-semibold">
                <option value="ALL">All Regions (5)</option>
                <option value="West">West</option>
                <option value="East">East</option>
                <option value="Central">Central</option>
                <option value="South">South</option>
                <option value="North">North</option>
            </select>
        </div>
        <div>
            <label class="block text-[11px] font-bold text-slate-600 uppercase mb-1">Category Slicer</label>
            <select id="slicer-category" onchange="applyFilters()" class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg p-2 font-semibold">
                <option value="ALL">All Categories (3)</option>
                <option value="Technology">Technology</option>
                <option value="Furniture">Furniture</option>
                <option value="Office Supplies">Office Supplies</option>
            </select>
        </div>
        <div>
            <label class="block text-[11px] font-bold text-slate-600 uppercase mb-1">Payment Method</label>
            <select id="slicer-payment" onchange="applyFilters()" class="w-full text-xs bg-slate-50 border border-slate-300 rounded-lg p-2 font-semibold">
                <option value="ALL">All Payment Methods</option>
                <option value="Credit Card">Credit Card</option>
                <option value="Bank Transfer">Bank Transfer</option>
                <option value="PayPal">PayPal</option>
                <option value="Purchase Order">Purchase Order</option>
            </select>
        </div>
    </div>

    <!-- ===================================================================== -->
    <!-- PAGE 1: EXECUTIVE OVERVIEW -->
    <!-- ===================================================================== -->
    <div id="page1" class="page-container active max-w-7xl mx-auto space-y-6">
        <!-- 5 KPI Cards -->
        <div class="grid grid-cols-2 lg:grid-cols-5 gap-4">
            <div class="kpi-card bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                <div class="text-[11px] font-bold text-slate-500 uppercase">Total Revenue</div>
                <div id="p1-kpi-rev" class="text-xl md:text-2xl font-extrabold text-blue-600 mt-1">$0</div>
                <div class="text-[10px] text-slate-400 mt-1 font-mono">SUM(Fact_Sales[Revenue])</div>
            </div>
            <div class="kpi-card bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                <div class="text-[11px] font-bold text-slate-500 uppercase">Total Profit</div>
                <div id="p1-kpi-prof" class="text-xl md:text-2xl font-extrabold text-emerald-600 mt-1">$0</div>
                <div class="text-[10px] text-slate-400 mt-1 font-mono">SUM(Fact_Sales[Profit])</div>
            </div>
            <div class="kpi-card bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                <div class="text-[11px] font-bold text-slate-500 uppercase">Total Orders</div>
                <div id="p1-kpi-orders" class="text-xl md:text-2xl font-extrabold text-indigo-600 mt-1">0</div>
                <div class="text-[10px] text-slate-400 mt-1 font-mono">DISTINCTCOUNT(Order_ID)</div>
            </div>
            <div class="kpi-card bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                <div class="text-[11px] font-bold text-slate-500 uppercase">Total Customers</div>
                <div id="p1-kpi-cust" class="text-xl md:text-2xl font-extrabold text-amber-600 mt-1">0</div>
                <div class="text-[10px] text-slate-400 mt-1 font-mono">DISTINCTCOUNT(Customer_ID)</div>
            </div>
            <div class="kpi-card bg-white p-4 rounded-xl border border-slate-200 shadow-sm col-span-2 lg:col-span-1">
                <div class="text-[11px] font-bold text-slate-500 uppercase">Profit Margin %</div>
                <div id="p1-kpi-margin" class="text-xl md:text-2xl font-extrabold text-purple-600 mt-1">0.00%</div>
                <div class="text-[10px] text-slate-400 mt-1 font-mono">DIVIDE(Profit, Revenue)</div>
            </div>
        </div>

        <!-- Trend Line & Category Donut -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm lg:col-span-2">
                <h3 class="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
                    <i data-lucide="line-chart" class="w-4 h-4 text-blue-600"></i> Monthly Revenue & Profit Trend (24 Months)
                </h3>
                <div class="h-72"><canvas id="p1-chart-trend"></canvas></div>
            </div>
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <h3 class="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
                    <i data-lucide="pie-chart" class="w-4 h-4 text-purple-600"></i> Revenue by Category
                </h3>
                <div class="h-72"><canvas id="p1-chart-category"></canvas></div>
            </div>
        </div>

        <!-- Profit by Region & Top Products -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <h3 class="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
                    <i data-lucide="bar-chart-2" class="w-4 h-4 text-emerald-600"></i> Profit by Region
                </h3>
                <div class="h-72"><canvas id="p1-chart-region"></canvas></div>
            </div>
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <h3 class="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
                    <i data-lucide="award" class="w-4 h-4 text-blue-600"></i> Top 8 Products by Revenue
                </h3>
                <div class="h-72"><canvas id="p1-chart-topprods"></canvas></div>
            </div>
        </div>
    </div>

    <!-- ===================================================================== -->
    <!-- PAGE 2: PRODUCT ANALYSIS -->
    <!-- ===================================================================== -->
    <div id="page2" class="page-container max-w-7xl mx-auto space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="kpi-card bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                <div class="text-[11px] font-bold text-slate-500 uppercase">Total Units Sold</div>
                <div id="p2-kpi-qty" class="text-2xl font-extrabold text-blue-600 mt-1">0 units</div>
                <div class="text-[10px] text-slate-400 mt-1 font-mono">SUM(Fact_Sales[Quantity])</div>
            </div>
            <div class="kpi-card bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                <div class="text-[11px] font-bold text-slate-500 uppercase">Total Cost of Goods (COGS)</div>
                <div id="p2-kpi-cost" class="text-2xl font-extrabold text-rose-600 mt-1">$0</div>
                <div class="text-[10px] text-slate-400 mt-1 font-mono">SUM(Fact_Sales[Cost])</div>
            </div>
            <div class="kpi-card bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                <div class="text-[11px] font-bold text-slate-500 uppercase">Average Selling Price (ASP)</div>
                <div id="p2-kpi-asp" class="text-2xl font-extrabold text-purple-600 mt-1">$0.00</div>
                <div class="text-[10px] text-slate-400 mt-1 font-mono">DIVIDE(Revenue, Quantity)</div>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <h3 class="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
                    <i data-lucide="layers" class="w-4 h-4 text-purple-600"></i> Profit by Subcategory
                </h3>
                <div class="h-80"><canvas id="p2-chart-subcat"></canvas></div>
            </div>
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <h3 class="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
                    <i data-lucide="shopping-cart" class="w-4 h-4 text-blue-600"></i> Revenue by Product Catalog
                </h3>
                <div class="h-80"><canvas id="p2-chart-prod-rev"></canvas></div>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <h3 class="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
                    <i data-lucide="thumbs-up" class="w-4 h-4 text-emerald-600"></i> Top 5 Profit Drivers
                </h3>
                <div class="h-64"><canvas id="p2-chart-top5"></canvas></div>
            </div>
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <h3 class="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
                    <i data-lucide="alert-circle" class="w-4 h-4 text-amber-600"></i> Bottom 5 Profit Movers
                </h3>
                <div class="h-64"><canvas id="p2-chart-bot5"></canvas></div>
            </div>
        </div>
    </div>

    <!-- ===================================================================== -->
    <!-- PAGE 3: REGIONAL ANALYSIS -->
    <!-- ===================================================================== -->
    <div id="page3" class="page-container max-w-7xl mx-auto space-y-6">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <h3 class="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
                    <i data-lucide="map" class="w-4 h-4 text-blue-600"></i> Revenue by State (15 States)
                </h3>
                <div class="h-80"><canvas id="p3-chart-state"></canvas></div>
            </div>
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <h3 class="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
                    <i data-lucide="pie-chart" class="w-4 h-4 text-amber-600"></i> Order Distribution by Region
                </h3>
                <div class="h-80"><canvas id="p3-chart-reg-orders"></canvas></div>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <h3 class="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
                    <i data-lucide="bar-chart" class="w-4 h-4 text-emerald-600"></i> Revenue vs Profit by Region
                </h3>
                <div class="h-72"><canvas id="p3-chart-reg-comp"></canvas></div>
            </div>
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm overflow-x-auto">
                <h3 class="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
                    <i data-lucide="table" class="w-4 h-4 text-indigo-600"></i> Regional Performance Matrix
                </h3>
                <table class="w-full text-left text-xs border-collapse">
                    <thead>
                        <tr class="bg-slate-100 text-slate-700 uppercase font-bold">
                            <th class="p-2.5 rounded-l">Region</th>
                            <th class="p-2.5">Revenue</th>
                            <th class="p-2.5">Profit</th>
                            <th class="p-2.5">Margin %</th>
                            <th class="p-2.5 rounded-r">Orders</th>
                        </tr>
                    </thead>
                    <tbody id="p3-tbl-body" class="divide-y divide-slate-100"></tbody>
                </table>
            </div>
        </div>
    </div>

    <!-- ===================================================================== -->
    <!-- PAGE 4: SALES TRENDS & GROWTH -->
    <!-- ===================================================================== -->
    <div id="page4" class="page-container max-w-7xl mx-auto space-y-6">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="kpi-card bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                <div class="text-[11px] font-bold text-slate-500 uppercase">2024 Baseline Revenue</div>
                <div id="p4-kpi-rev24" class="text-2xl font-extrabold text-slate-600 mt-1">$0</div>
                <div class="text-[10px] text-slate-400 mt-1 font-mono">CALCULATE(Year=2024)</div>
            </div>
            <div class="kpi-card bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                <div class="text-[11px] font-bold text-slate-500 uppercase">2025 Actual Revenue</div>
                <div id="p4-kpi-rev25" class="text-2xl font-extrabold text-blue-600 mt-1">$0</div>
                <div class="text-[10px] text-slate-400 mt-1 font-mono">CALCULATE(Year=2025)</div>
            </div>
            <div class="kpi-card bg-white p-4 rounded-xl border border-slate-200 shadow-sm">
                <div class="text-[11px] font-bold text-slate-500 uppercase">Year-over-Year Growth %</div>
                <div id="p4-kpi-yoy" class="text-2xl font-extrabold text-emerald-600 mt-1">0.00%</div>
                <div class="text-[10px] text-slate-400 mt-1 font-mono">DIVIDE(2025 - 2024, 2024)</div>
            </div>
        </div>

        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
            <h3 class="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
                <i data-lucide="calendar" class="w-4 h-4 text-blue-600"></i> Monthly Revenue Comparison: 2024 Baseline vs 2025 Actual
            </h3>
            <div class="h-72"><canvas id="p4-chart-yoy-comp"></canvas></div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <h3 class="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
                    <i data-lucide="trending-up" class="w-4 h-4 text-emerald-600"></i> Monthly Net Profit Velocity
                </h3>
                <div class="h-64"><canvas id="p4-chart-profit-line"></canvas></div>
            </div>
            <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                <h3 class="text-sm font-bold text-slate-800 mb-4 flex items-center gap-2">
                    <i data-lucide="percent" class="w-4 h-4 text-purple-600"></i> Month-over-Month (MoM) Revenue Growth %
                </h3>
                <div class="h-64"><canvas id="p4-chart-mom"></canvas></div>
            </div>
        </div>
    </div>

    <!-- Live Data Engine & Chart State -->
    <script>
        const RAW_DATA = {records_json};
        let filteredData = [...RAW_DATA];
        const charts = {{}};

        function switchTab(pageId) {{
            document.querySelectorAll('.page-container').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(pageId).classList.add('active');
            document.getElementById('tab-' + pageId).classList.add('active');
            updateActivePage(pageId);
        }}

        function applyFilters() {{
            const y = document.getElementById('slicer-year').value;
            const r = document.getElementById('slicer-region').value;
            const c = document.getElementById('slicer-category').value;
            const p = document.getElementById('slicer-payment').value;

            filteredData = RAW_DATA.filter(row => {{
                const rowYear = row.Order_Date.substring(0, 4);
                if (y !== 'ALL' && rowYear !== y) return false;
                if (r !== 'ALL' && row.Region !== r) return false;
                if (c !== 'ALL' && row.Category !== c) return false;
                if (p !== 'ALL' && row.Payment_Method !== p) return false;
                return true;
            }});

            updateAllPages();
        }}

        function resetFilters() {{
            document.getElementById('slicer-year').value = 'ALL';
            document.getElementById('slicer-region').value = 'ALL';
            document.getElementById('slicer-category').value = 'ALL';
            document.getElementById('slicer-payment').value = 'ALL';
            applyFilters();
        }}

        function updateAllPages() {{
            updatePage1();
            updatePage2();
            updatePage3();
            updatePage4();
        }}

        function updateActivePage(pageId) {{
            if (pageId === 'page1') updatePage1();
            else if (pageId === 'page2') updatePage2();
            else if (pageId === 'page3') updatePage3();
            else if (pageId === 'page4') updatePage4();
        }}

        // --- UPDATE PAGE 1 ---
        function updatePage1() {{
            const rev = filteredData.reduce((s, r) => s + r.Revenue, 0);
            const prof = filteredData.reduce((s, r) => s + r.Profit, 0);
            const orders = new Set(filteredData.map(r => r.Order_ID)).size;
            const custs = new Set(filteredData.map(r => r.Customer_ID)).size;
            const margin = rev > 0 ? (prof / rev) * 100 : 0;

            document.getElementById('p1-kpi-rev').innerText = '$' + Math.round(rev).toLocaleString();
            document.getElementById('p1-kpi-prof').innerText = '$' + Math.round(prof).toLocaleString();
            document.getElementById('p1-kpi-orders').innerText = orders.toLocaleString();
            document.getElementById('p1-kpi-cust').innerText = custs.toLocaleString();
            document.getElementById('p1-kpi-margin').innerText = margin.toFixed(2) + '%';

            // Trend
            const monthly = {{}};
            filteredData.forEach(r => {{
                const ym = r.Order_Date.substring(0, 7);
                if (!monthly[ym]) monthly[ym] = {{ rev: 0, prof: 0 }};
                monthly[ym].rev += r.Revenue;
                monthly[ym].prof += r.Profit;
            }});
            const sortedYM = Object.keys(monthly).sort();
            charts.p1_trend.data.labels = sortedYM;
            charts.p1_trend.data.datasets[0].data = sortedYM.map(k => Math.round(monthly[k].rev));
            charts.p1_trend.data.datasets[1].data = sortedYM.map(k => Math.round(monthly[k].prof));
            charts.p1_trend.update();

            // Category Donut
            const cats = {{}};
            filteredData.forEach(r => {{ cats[r.Category] = (cats[r.Category] || 0) + r.Revenue; }});
            charts.p1_cat.data.labels = Object.keys(cats);
            charts.p1_cat.data.datasets[0].data = Object.values(cats).map(Math.round);
            charts.p1_cat.update();

            // Profit by Region
            const regProf = {{}};
            filteredData.forEach(r => {{ regProf[r.Region] = (regProf[r.Region] || 0) + r.Profit; }});
            charts.p1_reg.data.labels = Object.keys(regProf);
            charts.p1_reg.data.datasets[0].data = Object.values(regProf).map(Math.round);
            charts.p1_reg.update();

            // Top Products
            const prods = {{}};
            filteredData.forEach(r => {{ prods[r.Product_Name] = (prods[r.Product_Name] || 0) + r.Revenue; }});
            const topP = Object.entries(prods).sort((a,b) => b[1] - a[1]).slice(0, 8);
            charts.p1_top.data.labels = topP.map(x => x[0]);
            charts.p1_top.data.datasets[0].data = topP.map(x => Math.round(x[1]));
            charts.p1_top.update();
        }}

        // --- UPDATE PAGE 2 ---
        function updatePage2() {{
            const qty = filteredData.reduce((s, r) => s + r.Quantity, 0);
            const cost = filteredData.reduce((s, r) => s + r.Cost, 0);
            const rev = filteredData.reduce((s, r) => s + r.Revenue, 0);
            const asp = qty > 0 ? rev / qty : 0;

            document.getElementById('p2-kpi-qty').innerText = qty.toLocaleString() + ' units';
            document.getElementById('p2-kpi-cost').innerText = '$' + Math.round(cost).toLocaleString();
            document.getElementById('p2-kpi-asp').innerText = '$' + asp.toFixed(2);

            // Subcategory Profit
            const subcats = {{}};
            filteredData.forEach(r => {{ subcats[r.Subcategory] = (subcats[r.Subcategory] || 0) + r.Profit; }});
            const subEntries = Object.entries(subcats).sort((a,b) => b[1] - a[1]);
            charts.p2_subcat.data.labels = subEntries.map(x => x[0]);
            charts.p2_subcat.data.datasets[0].data = subEntries.map(x => Math.round(x[1]));
            charts.p2_subcat.update();

            // Product Rev
            const prodRev = {{}};
            filteredData.forEach(r => {{ prodRev[r.Product_Name] = (prodRev[r.Product_Name] || 0) + r.Revenue; }});
            const pRevEntries = Object.entries(prodRev).sort((a,b) => b[1] - a[1]);
            charts.p2_prod_rev.data.labels = pRevEntries.map(x => x[0]);
            charts.p2_prod_rev.data.datasets[0].data = pRevEntries.map(x => Math.round(x[1]));
            charts.p2_prod_rev.update();

            // Top 5 and Bottom 5 Profit
            const prodProf = {{}};
            filteredData.forEach(r => {{ prodProf[r.Product_Name] = (prodProf[r.Product_Name] || 0) + r.Profit; }});
            const sortedProf = Object.entries(prodProf).sort((a,b) => b[1] - a[1]);
            const top5 = sortedProf.slice(0, 5);
            const bot5 = sortedProf.slice(-5).reverse();

            charts.p2_top5.data.labels = top5.map(x => x[0]);
            charts.p2_top5.data.datasets[0].data = top5.map(x => Math.round(x[1]));
            charts.p2_top5.update();

            charts.p2_bot5.data.labels = bot5.map(x => x[0]);
            charts.p2_bot5.data.datasets[0].data = bot5.map(x => Math.round(x[1]));
            charts.p2_bot5.update();
        }}

        // --- UPDATE PAGE 3 ---
        function updatePage3() {{
            // State Rev
            const stateRev = {{}};
            filteredData.forEach(r => {{ stateRev[r.State] = (stateRev[r.State] || 0) + r.Revenue; }});
            const stateEntries = Object.entries(stateRev).sort((a,b) => b[1] - a[1]);
            charts.p3_state.data.labels = stateEntries.map(x => x[0]);
            charts.p3_state.data.datasets[0].data = stateEntries.map(x => Math.round(x[1]));
            charts.p3_state.update();

            // Region Orders
            const regOrders = {{}};
            filteredData.forEach(r => {{
                if (!regOrders[r.Region]) regOrders[r.Region] = new Set();
                regOrders[r.Region].add(r.Order_ID);
            }});
            charts.p3_reg_orders.data.labels = Object.keys(regOrders);
            charts.p3_reg_orders.data.datasets[0].data = Object.values(regOrders).map(s => s.size);
            charts.p3_reg_orders.update();

            // Region Comp
            const regRev = {{}};
            const regProf = {{}};
            filteredData.forEach(r => {{
                regRev[r.Region] = (regRev[r.Region] || 0) + r.Revenue;
                regProf[r.Region] = (regProf[r.Region] || 0) + r.Profit;
            }});
            const regions = Object.keys(regRev);
            charts.p3_reg_comp.data.labels = regions;
            charts.p3_reg_comp.data.datasets[0].data = regions.map(k => Math.round(regRev[k]));
            charts.p3_reg_comp.data.datasets[1].data = regions.map(k => Math.round(regProf[k]));
            charts.p3_reg_comp.update();

            // Table
            const tbody = document.getElementById('p3-tbl-body');
            tbody.innerHTML = '';
            regions.forEach(reg => {{
                const r = regRev[reg] || 0;
                const p = regProf[reg] || 0;
                const m = r > 0 ? (p / r) * 100 : 0;
                const o = regOrders[reg] ? regOrders[reg].size : 0;
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-50 transition';
                tr.innerHTML = `
                    <td class="p-2.5 font-bold text-slate-900">${{reg}}</td>
                    <td class="p-2.5 font-medium text-slate-700">$${{Math.round(r).toLocaleString()}}</td>
                    <td class="p-2.5 font-medium text-emerald-600">$${{Math.round(p).toLocaleString()}}</td>
                    <td class="p-2.5 font-semibold text-purple-600">${{m.toFixed(1)}}%</td>
                    <td class="p-2.5 text-slate-600">${{o.toLocaleString()}}</td>
                `;
                tbody.appendChild(tr);
            }});
        }}

        // --- UPDATE PAGE 4 ---
        function updatePage4() {{
            const rev24 = filteredData.filter(r => r.Order_Date.startsWith('2024')).reduce((s,r) => s + r.Revenue, 0);
            const rev25 = filteredData.filter(r => r.Order_Date.startsWith('2025')).reduce((s,r) => s + r.Revenue, 0);
            const yoy = rev24 > 0 ? ((rev25 - rev24) / rev24) * 100 : 0;

            document.getElementById('p4-kpi-rev24').innerText = '$' + Math.round(rev24).toLocaleString();
            document.getElementById('p4-kpi-rev25').innerText = '$' + Math.round(rev25).toLocaleString();
            document.getElementById('p4-kpi-yoy').innerText = (yoy >= 0 ? '+' : '') + yoy.toFixed(2) + '%';
            document.getElementById('p4-kpi-yoy').className = 'text-2xl font-extrabold mt-1 ' + (yoy >= 0 ? 'text-emerald-600' : 'text-rose-600');

            // 2024 vs 2025 Monthly Comparison
            const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
            const m24 = new Array(12).fill(0);
            const m25 = new Array(12).fill(0);
            filteredData.forEach(r => {{
                const d = new Date(r.Order_Date);
                const mIdx = d.getMonth();
                if (d.getFullYear() === 2024) m24[mIdx] += r.Revenue;
                else if (d.getFullYear() === 2025) m25[mIdx] += r.Revenue;
            }});
            charts.p4_yoy_comp.data.labels = months;
            charts.p4_yoy_comp.data.datasets[0].data = m24.map(Math.round);
            charts.p4_yoy_comp.data.datasets[1].data = m25.map(Math.round);
            charts.p4_yoy_comp.update();

            // Monthly Net Profit Velocity
            const monthlyProf = {{}};
            filteredData.forEach(r => {{
                const ym = r.Order_Date.substring(0, 7);
                monthlyProf[ym] = (monthlyProf[ym] || 0) + r.Profit;
            }});
            const sortedYM = Object.keys(monthlyProf).sort();
            charts.p4_profit_line.data.labels = sortedYM;
            charts.p4_profit_line.data.datasets[0].data = sortedYM.map(k => Math.round(monthlyProf[k]));
            charts.p4_profit_line.update();

            // MoM Growth %
            const monthlyRev = {{}};
            filteredData.forEach(r => {{
                const ym = r.Order_Date.substring(0, 7);
                monthlyRev[ym] = (monthlyRev[ym] || 0) + r.Revenue;
            }});
            const momLabels = [];
            const momValues = [];
            for (let i = 1; i < sortedYM.length; i++) {{
                const prev = monthlyRev[sortedYM[i-1]] || 0;
                const curr = monthlyRev[sortedYM[i]] || 0;
                const g = prev > 0 ? ((curr - prev) / prev) * 100 : 0;
                momLabels.push(sortedYM[i]);
                momValues.push(Number(g.toFixed(1)));
            }}
            charts.p4_mom.data.labels = momLabels;
            charts.p4_mom.data.datasets[0].data = momValues;
            charts.p4_mom.data.datasets[0].backgroundColor = momValues.map(v => v >= 0 ? '#10b981' : '#f43f5e');
            charts.p4_mom.update();
        }}

        // Initialize All Charts
        window.addEventListener('DOMContentLoaded', () => {{
            lucide.createIcons();

            // P1 Trend
            charts.p1_trend = new Chart(document.getElementById('p1-chart-trend'), {{
                type: 'line',
                data: {{ labels: [], datasets: [
                    {{ label: 'Revenue ($)', data: [], borderColor: '#3b82f6', tension: 0.2, borderWidth: 2.5, pointRadius: 2 }},
                    {{ label: 'Profit ($)', data: [], borderColor: '#10b981', tension: 0.2, borderWidth: 2, pointRadius: 2 }}
                ] }},
                options: {{ responsive: true, maintainAspectRatio: false }}
            }});

            // P1 Cat Donut
            charts.p1_cat = new Chart(document.getElementById('p1-chart-category'), {{
                type: 'doughnut',
                data: {{ labels: [], datasets: [{{ data: [], backgroundColor: ['#3b82f6', '#8b5cf6', '#f59e0b'] }}] }},
                options: {{ responsive: true, maintainAspectRatio: false }}
            }});

            // P1 Region Bar
            charts.p1_reg = new Chart(document.getElementById('p1-chart-region'), {{
                type: 'bar',
                data: {{ labels: [], datasets: [{{ label: 'Profit ($)', data: [], backgroundColor: '#10b981' }}] }},
                options: {{ responsive: true, maintainAspectRatio: false, indexAxis: 'y' }}
            }});

            // P1 Top Prods
            charts.p1_top = new Chart(document.getElementById('p1-chart-topprods'), {{
                type: 'bar',
                data: {{ labels: [], datasets: [{{ label: 'Revenue ($)', data: [], backgroundColor: '#1e40af' }}] }},
                options: {{ responsive: true, maintainAspectRatio: false, indexAxis: 'y' }}
            }});

            // P2 Subcat
            charts.p2_subcat = new Chart(document.getElementById('p2-chart-subcat'), {{
                type: 'bar',
                data: {{ labels: [], datasets: [{{ label: 'Profit ($)', data: [], backgroundColor: '#8b5cf6' }}] }},
                options: {{ responsive: true, maintainAspectRatio: false, indexAxis: 'y' }}
            }});

            // P2 Prod Rev
            charts.p2_prod_rev = new Chart(document.getElementById('p2-chart-prod-rev'), {{
                type: 'bar',
                data: {{ labels: [], datasets: [{{ label: 'Revenue ($)', data: [], backgroundColor: '#3b82f6' }}] }},
                options: {{ responsive: true, maintainAspectRatio: false, indexAxis: 'y' }}
            }});

            // P2 Top 5
            charts.p2_top5 = new Chart(document.getElementById('p2-chart-top5'), {{
                type: 'bar',
                data: {{ labels: [], datasets: [{{ label: 'Profit ($)', data: [], backgroundColor: '#10b981' }}] }},
                options: {{ responsive: true, maintainAspectRatio: false, indexAxis: 'y' }}
            }});

            // P2 Bot 5
            charts.p2_bot5 = new Chart(document.getElementById('p2-chart-bot5'), {{
                type: 'bar',
                data: {{ labels: [], datasets: [{{ label: 'Profit ($)', data: [], backgroundColor: '#f59e0b' }}] }},
                options: {{ responsive: true, maintainAspectRatio: false, indexAxis: 'y' }}
            }});

            // P3 State
            charts.p3_state = new Chart(document.getElementById('p3-chart-state'), {{
                type: 'bar',
                data: {{ labels: [], datasets: [{{ label: 'Revenue ($)', data: [], backgroundColor: '#3b82f6' }}] }},
                options: {{ responsive: true, maintainAspectRatio: false, indexAxis: 'y' }}
            }});

            // P3 Reg Orders
            charts.p3_reg_orders = new Chart(document.getElementById('p3-chart-reg-orders'), {{
                type: 'doughnut',
                data: {{ labels: [], datasets: [{{ data: [], backgroundColor: ['#f59e0b', '#8b5cf6', '#f43f5e', '#10b981', '#3b82f6'] }}] }},
                options: {{ responsive: true, maintainAspectRatio: false }}
            }});

            // P3 Reg Comp
            charts.p3_reg_comp = new Chart(document.getElementById('p3-chart-reg-comp'), {{
                type: 'bar',
                data: {{ labels: [], datasets: [
                    {{ label: 'Revenue ($)', data: [], backgroundColor: '#3b82f6' }},
                    {{ label: 'Profit ($)', data: [], backgroundColor: '#10b981' }}
                ] }},
                options: {{ responsive: true, maintainAspectRatio: false }}
            }});

            // P4 YoY Comp
            charts.p4_yoy_comp = new Chart(document.getElementById('p4-chart-yoy-comp'), {{
                type: 'bar',
                data: {{ labels: [], datasets: [
                    {{ label: '2024 Baseline ($)', data: [], backgroundColor: '#94a3b8' }},
                    {{ label: '2025 Actual ($)', data: [], backgroundColor: '#3b82f6' }}
                ] }},
                options: {{ responsive: true, maintainAspectRatio: false }}
            }});

            // P4 Profit Line
            charts.p4_profit_line = new Chart(document.getElementById('p4-chart-profit-line'), {{
                type: 'line',
                data: {{ labels: [], datasets: [{{ label: 'Profit ($)', data: [], borderColor: '#10b981', tension: 0.2, borderWidth: 2 }}] }},
                options: {{ responsive: true, maintainAspectRatio: false }}
            }});

            // P4 MoM
            charts.p4_mom = new Chart(document.getElementById('p4-chart-mom'), {{
                type: 'bar',
                data: {{ labels: [], datasets: [{{ label: 'MoM %', data: [], backgroundColor: [] }}] }},
                options: {{ responsive: true, maintainAspectRatio: false }}
            }});

            updateAllPages();
        }});
    </script>
</body>
</html>
"""

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"[SUCCESS] Interactive 4-Page Dashboard HTML compiled: {HTML_PATH}")

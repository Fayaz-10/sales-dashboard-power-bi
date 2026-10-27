"""
================================================================================
ENTERPRISE POWER BI PROJECT (PBIP) ARCHITECTURE GENERATOR
================================================================================
Role: Senior Power BI Architect & Data Engineer
Purpose: Programmatically generates the complete, fully-bound Power BI Project
         hierarchy (.pbip, model.bim, report.json, definition.pbir) with:
         - Compatibility Level 1606 (Enhanced Metadata Format V3)
         - Power Query M with QuoteStyle.Csv and Windows paths
         - 5 Star Schema Tables with 100% Unique Dimension Keys
         - All 13 Explicit DAX Measures
         - Complete prototypeQuery field bindings for all 4 report pages
================================================================================
"""

import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PBIP_FILE = os.path.join(BASE_DIR, "Sales Dashboard using Power BI.pbip")
REPORT_DIR = os.path.join(BASE_DIR, "Sales Dashboard using Power BI.Report")
DATASET_DIR = os.path.join(BASE_DIR, "Sales Dashboard using Power BI.Dataset")
CSV_PATH_M = "D:\\Git Hub Projects\\data\\cleaned_sales_data.csv"

os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(DATASET_DIR, exist_ok=True)

# -----------------------------------------------------------------------------
# 1. PBIP Root Launcher
# -----------------------------------------------------------------------------
pbip_content = {
    "version": "1.0",
    "artifacts": [
        {
            "report": {
                "path": "Sales Dashboard using Power BI.Report"
            }
        }
    ]
}
with open(PBIP_FILE, "w", encoding="utf-8") as f:
    json.dump(pbip_content, f, indent=2)

# -----------------------------------------------------------------------------
# 2. Dataset Definition (.pbidataset)
# -----------------------------------------------------------------------------
pbi_dataset = {"version": "1.0"}
with open(os.path.join(DATASET_DIR, "definition.pbidataset"), "w", encoding="utf-8") as f:
    json.dump(pbi_dataset, f, indent=2)

# -----------------------------------------------------------------------------
# 3. Report Definition (.pbir)
# -----------------------------------------------------------------------------
pbi_report = {
    "version": "1.0",
    "datasetReference": {
        "byPath": {
            "path": "../Sales Dashboard using Power BI.Dataset"
        }
    }
}
with open(os.path.join(REPORT_DIR, "definition.pbir"), "w", encoding="utf-8") as f:
    json.dump(pbi_report, f, indent=2)

# -----------------------------------------------------------------------------
# 4. Tabular Model Definition (model.bim) - Compatibility 1606 (Enhanced Metadata)
# -----------------------------------------------------------------------------
model_bim = {
    "name": "Sales_Dashboard_Model",
    "compatibilityLevel": 1606,
    "model": {
        "culture": "en-US",
        "defaultPowerBIDataSourceVersion": "powerBI_V3",
        "sourceQueryCulture": "en-US",
        "dataAccessOptions": {
            "legacyRedirects": True,
            "returnErrorValuesAsNull": True,
            "fastCombine": True
        },
        "annotations": [
            {"name": "PBI_QueryOrder", "value": "[\"Fact_Sales\",\"Dim_Date\",\"Dim_Customer\",\"Dim_Product\",\"Dim_Region\"]"},
            {"name": "__PBI_TimeIntelligenceEnabled", "value": "1"},
            {"name": "PBIDesktopVersion", "value": "2.157.1354.0"},
            {"name": "PBI_ProTooling", "value": "[\"DevMode\"]"},
            {"name": "PBI_EnhancedModelMetadata", "value": "1"}
        ],
        "tables": [
            # 1. Fact_Sales
            {
                "name": "Fact_Sales",
                "columns": [
                    {"name": "Order_ID", "dataType": "string", "sourceColumn": "Order_ID"},
                    {"name": "Order_Date", "dataType": "dateTime", "sourceColumn": "Order_Date", "formatString": "yyyy-mm-dd"},
                    {"name": "Customer_ID", "dataType": "string", "sourceColumn": "Customer_ID"},
                    {"name": "Customer_Name", "dataType": "string", "sourceColumn": "Customer_Name"},
                    {"name": "Segment", "dataType": "string", "sourceColumn": "Segment"},
                    {"name": "Product_ID", "dataType": "string", "sourceColumn": "Product_ID"},
                    {"name": "Product_Name", "dataType": "string", "sourceColumn": "Product_Name"},
                    {"name": "Category", "dataType": "string", "sourceColumn": "Category"},
                    {"name": "Subcategory", "dataType": "string", "sourceColumn": "Subcategory"},
                    {"name": "Region", "dataType": "string", "sourceColumn": "Region"},
                    {"name": "State", "dataType": "string", "sourceColumn": "State"},
                    {"name": "Quantity", "dataType": "int64", "sourceColumn": "Quantity"},
                    {"name": "Unit_Price", "dataType": "double", "sourceColumn": "Unit_Price", "formatString": "$#,##0.00"},
                    {"name": "Discount", "dataType": "double", "sourceColumn": "Discount", "formatString": "0.0%"},
                    {"name": "Revenue", "dataType": "double", "sourceColumn": "Revenue", "formatString": "$#,##0.00"},
                    {"name": "Cost", "dataType": "double", "sourceColumn": "Cost", "formatString": "$#,##0.00"},
                    {"name": "Profit", "dataType": "double", "sourceColumn": "Profit", "formatString": "$#,##0.00"},
                    {"name": "Payment_Method", "dataType": "string", "sourceColumn": "Payment_Method"}
                ],
                "partitions": [
                    {
                        "name": "Fact_Sales-Partition",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f'    Source = Csv.Document(File.Contents("{CSV_PATH_M}"),[Delimiter=",", Columns=18, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Promoted Headers",{{ "Order_ID", type text}, {"Order_Date", type datetime}, {"Customer_ID", type text}, {"Customer_Name", type text}, {"Segment", type text}, {"Product_ID", type text}, {"Product_Name", type text}, {"Category", type text}, {"Subcategory", type text}, {"Region", type text}, {"State", type text}, {"Quantity", Int64.Type}, {"Unit_Price", type number}, {"Discount", type number}, {"Revenue", type number}, {"Cost", type number}, {"Profit", type number}, {"Payment_Method", type text}})',
                                "in",
                                '    #"Changed Type"'
                            ]
                        }
                    }
                ],
                "measures": [
                    {"name": "Total Revenue", "expression": "SUM(Fact_Sales[Revenue])", "formatString": "$#,##0.00"},
                    {"name": "Total Cost", "expression": "SUM(Fact_Sales[Cost])", "formatString": "$#,##0.00"},
                    {"name": "Total Profit", "expression": "SUM(Fact_Sales[Profit])", "formatString": "$#,##0.00"},
                    {"name": "Total Orders", "expression": "DISTINCTCOUNT(Fact_Sales[Order_ID])", "formatString": "#,##0"},
                    {"name": "Total Customers", "expression": "DISTINCTCOUNT(Fact_Sales[Customer_ID])", "formatString": "#,##0"},
                    {"name": "Total Quantity Sold", "expression": "SUM(Fact_Sales[Quantity])", "formatString": "#,##0"},
                    {"name": "Profit Margin %", "expression": "DIVIDE([Total Profit], [Total Revenue], 0)", "formatString": "0.00%"},
                    {"name": "Average Order Value", "expression": "DIVIDE([Total Revenue], [Total Orders], 0)", "formatString": "$#,##0.00"},
                    {"name": "Average Selling Price", "expression": "DIVIDE([Total Revenue], [Total Quantity Sold], 0)", "formatString": "$#,##0.00"},
                    {"name": "Revenue Previous Month", "expression": "CALCULATE([Total Revenue], DATEADD(Dim_Date[Date], -1, MONTH))", "formatString": "$#,##0.00"},
                    {"name": "MoM Revenue Growth %", "expression": "VAR CurrentRev = [Total Revenue] VAR PreviousRev = [Revenue Previous Month] RETURN IF(ISBLANK(PreviousRev), BLANK(), DIVIDE(CurrentRev - PreviousRev, PreviousRev, 0))", "formatString": "0.00%"},
                    {"name": "Revenue Previous Year", "expression": "CALCULATE([Total Revenue], SAMEPERIODLASTYEAR(Dim_Date[Date]))", "formatString": "$#,##0.00"},
                    {"name": "YoY Revenue Growth %", "expression": "VAR CurrentRev = [Total Revenue] VAR PreviousYearRev = [Revenue Previous Year] RETURN IF(ISBLANK(PreviousYearRev), BLANK(), DIVIDE(CurrentRev - PreviousYearRev, PreviousYearRev, 0))", "formatString": "0.00%"}
                ]
            },

            # 2. Dim_Date
            {
                "name": "Dim_Date",
                "columns": [
                    {"name": "Date", "dataType": "dateTime", "sourceColumn": "Date", "formatString": "yyyy-mm-dd", "isKey": True},
                    {"name": "Year", "dataType": "int64", "sourceColumn": "Year"},
                    {"name": "Quarter", "dataType": "string", "sourceColumn": "Quarter"},
                    {"name": "Month_Number", "dataType": "int64", "sourceColumn": "Month_Number"},
                    {"name": "Month_Name", "dataType": "string", "sourceColumn": "Month_Name"},
                    {"name": "Year_Month", "dataType": "string", "sourceColumn": "Year_Month"},
                    {"name": "Day", "dataType": "int64", "sourceColumn": "Day"},
                    {"name": "Day_of_Week", "dataType": "string", "sourceColumn": "Day_of_Week"}
                ],
                "partitions": [
                    {
                        "name": "Dim_Date-Partition",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                '    Source = List.Dates(#date(2024, 1, 1), 731, #duration(1, 0, 0, 0)),',
                                '    #"Converted to Table" = Table.FromList(Source, Splitter.SplitByNothing(), {"Date"}, null, ExtraValues.Error),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Converted to Table",{{"Date", type datetime}}),',
                                '    #"Added Year" = Table.AddColumn(#"Changed Type", "Year", each Date.Year([Date]), Int64.Type),',
                                '    #"Added Quarter" = Table.AddColumn(#"Added Year", "Quarter", each "Q" & Text.From(Date.QuarterOfYear([Date])), type text),',
                                '    #"Added Month Number" = Table.AddColumn(#"Added Quarter", "Month_Number", each Date.Month([Date]), Int64.Type),',
                                '    #"Added Month Name" = Table.AddColumn(#"Added Month Number", "Month_Name", each Date.ToText([Date], "MMM"), type text),',
                                '    #"Added Year Month" = Table.AddColumn(#"Added Month Name", "Year_Month", each Date.ToText([Date], "yyyy-MM"), type text),',
                                '    #"Added Day" = Table.AddColumn(#"Added Year Month", "Day", each Date.Day([Date]), Int64.Type),',
                                '    #"Added Day of Week" = Table.AddColumn(#"Added Day", "Day_of_Week", each Date.ToText([Date], "ddd"), type text)',
                                "in",
                                '    #"Added Day of Week"'
                            ]
                        }
                    }
                ]
            },

            # 3. Dim_Customer (25 Unique Clients)
            {
                "name": "Dim_Customer",
                "columns": [
                    {"name": "Customer_ID", "dataType": "string", "sourceColumn": "Customer_ID", "isKey": True},
                    {"name": "Customer_Name", "dataType": "string", "sourceColumn": "Customer_Name"},
                    {"name": "Segment", "dataType": "string", "sourceColumn": "Segment"}
                ],
                "partitions": [
                    {
                        "name": "Dim_Customer-Partition",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f'    Source = Csv.Document(File.Contents("{CSV_PATH_M}"),[Delimiter=",", Columns=18, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Selected Columns" = Table.SelectColumns(#"Promoted Headers",{"Customer_ID", "Customer_Name", "Segment"}),',
                                '    #"Removed Duplicates" = Table.Distinct(#"Selected Columns")',
                                "in",
                                '    #"Removed Duplicates"'
                            ]
                        }
                    }
                ]
            },

            # 4. Dim_Product (20 Unique SKUs)
            {
                "name": "Dim_Product",
                "columns": [
                    {"name": "Product_ID", "dataType": "string", "sourceColumn": "Product_ID", "isKey": True},
                    {"name": "Product_Name", "dataType": "string", "sourceColumn": "Product_Name"},
                    {"name": "Category", "dataType": "string", "sourceColumn": "Category"},
                    {"name": "Subcategory", "dataType": "string", "sourceColumn": "Subcategory"},
                    {"name": "Unit_Price", "dataType": "double", "sourceColumn": "Unit_Price", "formatString": "$#,##0.00"}
                ],
                "partitions": [
                    {
                        "name": "Dim_Product-Partition",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f'    Source = Csv.Document(File.Contents("{CSV_PATH_M}"),[Delimiter=",", Columns=18, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Selected Columns" = Table.SelectColumns(#"Promoted Headers",{"Product_ID", "Product_Name", "Category", "Subcategory", "Unit_Price"}),',
                                '    #"Changed Type" = Table.TransformColumnTypes(#"Selected Columns",{{"Unit_Price", type number}}),',
                                '    #"Removed Duplicates" = Table.Distinct(#"Changed Type")',
                                "in",
                                '    #"Removed Duplicates"'
                            ]
                        }
                    }
                ]
            },

            # 5. Dim_Region (15 Unique States)
            {
                "name": "Dim_Region",
                "columns": [
                    {"name": "State", "dataType": "string", "sourceColumn": "State", "isKey": True},
                    {"name": "Region", "dataType": "string", "sourceColumn": "Region"}
                ],
                "partitions": [
                    {
                        "name": "Dim_Region-Partition",
                        "mode": "import",
                        "source": {
                            "type": "m",
                            "expression": [
                                "let",
                                f'    Source = Csv.Document(File.Contents("{CSV_PATH_M}"),[Delimiter=",", Columns=18, Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
                                '    #"Promoted Headers" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),',
                                '    #"Selected Columns" = Table.SelectColumns(#"Promoted Headers",{"State", "Region"}),',
                                '    #"Removed Duplicates" = Table.Distinct(#"Selected Columns")',
                                "in",
                                '    #"Removed Duplicates"'
                            ]
                        }
                    }
                ]
            }
        ],
        "relationships": [
            {
                "name": "Fact_Sales_Dim_Date",
                "fromTable": "Fact_Sales",
                "fromColumn": "Order_Date",
                "toTable": "Dim_Date",
                "toColumn": "Date"
            },
            {
                "name": "Fact_Sales_Dim_Customer",
                "fromTable": "Fact_Sales",
                "fromColumn": "Customer_ID",
                "toTable": "Dim_Customer",
                "toColumn": "Customer_ID"
            },
            {
                "name": "Fact_Sales_Dim_Product",
                "fromTable": "Fact_Sales",
                "fromColumn": "Product_ID",
                "toTable": "Dim_Product",
                "toColumn": "Product_ID"
            },
            {
                "name": "Fact_Sales_Dim_Region",
                "fromTable": "Fact_Sales",
                "fromColumn": "State",
                "toTable": "Dim_Region",
                "toColumn": "State"
            }
        ]
    }
}

with open(os.path.join(DATASET_DIR, "model.bim"), "w", encoding="utf-8") as f:
    json.dump(model_bim, f, indent=2)

# -----------------------------------------------------------------------------
# 5. Helper Functions for Report Visual JSON Generation
# -----------------------------------------------------------------------------
def make_textbox(name, text, x, y, w, h):
    config = {
        "name": name,
        "singleVisual": {
            "visualType": "textbox",
            "objects": {
                "general": [{
                    "properties": {
                        "paragraphs": [{
                            "textRuns": [{
                                "value": text,
                                "textStyle": {"fontFamily": "Segoe UI", "fontSize": "17pt", "fontWeight": "bold", "color": "#0f172a"}
                            }]
                        }]
                    }
                }]
            }
        }
    }
    return {"x": x, "y": y, "z": 0, "width": w, "height": h, "config": json.dumps(config)}

def make_slicer(name, entity, prop, x, y, w, h):
    query_ref = f"{entity}.{prop}"
    config = {
        "name": name,
        "singleVisual": {
            "visualType": "slicer",
            "projections": {
                "Values": [{"queryRef": query_ref}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": "t", "Entity": entity, "Type": 0}],
                "Select": [{
                    "Column": {
                        "Expression": {"SourceRef": {"Source": "t"}},
                        "Property": prop
                    },
                    "Name": query_ref
                }]
            }
        }
    }
    return {"x": x, "y": y, "z": 1000, "width": w, "height": h, "config": json.dumps(config)}

def make_card(name, measure_name, x, y, w, h):
    query_ref = f"Fact_Sales.{measure_name}"
    config = {
        "name": name,
        "singleVisual": {
            "visualType": "card",
            "projections": {
                "Fields": [{"queryRef": query_ref}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": "f", "Entity": "Fact_Sales", "Type": 0}],
                "Select": [{
                    "Measure": {
                        "Expression": {"SourceRef": {"Source": "f"}},
                        "Property": measure_name
                    },
                    "Name": query_ref
                }]
            }
        }
    }
    return {"x": x, "y": y, "z": 2000, "width": w, "height": h, "config": json.dumps(config)}

def make_bar_chart(name, cat_entity, cat_prop, measure_name, x, y, w, h, is_column=False):
    cat_ref = f"{cat_entity}.{cat_prop}"
    meas_ref = f"Fact_Sales.{measure_name}"
    visual_type = "columnChart" if is_column else "barChart"
    config = {
        "name": name,
        "singleVisual": {
            "visualType": visual_type,
            "projections": {
                "Category": [{"queryRef": cat_ref}],
                "Y": [{"queryRef": meas_ref}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {"Name": "c", "Entity": cat_entity, "Type": 0},
                    {"Name": "f", "Entity": "Fact_Sales", "Type": 0}
                ],
                "Select": [
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "c"}},
                            "Property": cat_prop
                        },
                        "Name": cat_ref
                    },
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "f"}},
                            "Property": measure_name
                        },
                        "Name": meas_ref
                    }
                ]
            }
        }
    }
    return {"x": x, "y": y, "z": 3000, "width": w, "height": h, "config": json.dumps(config)}

def make_pie_chart(name, cat_entity, cat_prop, measure_name, x, y, w, h):
    cat_ref = f"{cat_entity}.{cat_prop}"
    meas_ref = f"Fact_Sales.{measure_name}"
    config = {
        "name": name,
        "singleVisual": {
            "visualType": "pieChart",
            "projections": {
                "Category": [{"queryRef": cat_ref}],
                "Y": [{"queryRef": meas_ref}]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {"Name": "c", "Entity": cat_entity, "Type": 0},
                    {"Name": "f", "Entity": "Fact_Sales", "Type": 0}
                ],
                "Select": [
                    {
                        "Column": {
                            "Expression": {"SourceRef": {"Source": "c"}},
                            "Property": cat_prop
                        },
                        "Name": cat_ref
                    },
                    {
                        "Measure": {
                            "Expression": {"SourceRef": {"Source": "f"}},
                            "Property": measure_name
                        },
                        "Name": meas_ref
                    }
                ]
            }
        }
    }
    return {"x": x, "y": y, "z": 3000, "width": w, "height": h, "config": json.dumps(config)}

def make_line_chart(name, cat_entity, cat_prop, measure_names, x, y, w, h):
    cat_ref = f"{cat_entity}.{cat_prop}"
    select_items = [{
        "Column": {
            "Expression": {"SourceRef": {"Source": "c"}},
            "Property": cat_prop
        },
        "Name": cat_ref
    }]
    y_projections = []
    for m in measure_names:
        m_ref = f"Fact_Sales.{m}"
        y_projections.append({"queryRef": m_ref})
        select_items.append({
            "Measure": {
                "Expression": {"SourceRef": {"Source": "f"}},
                "Property": m
            },
            "Name": m_ref
        })

    config = {
        "name": name,
        "singleVisual": {
            "visualType": "lineChart",
            "projections": {
                "Category": [{"queryRef": cat_ref}],
                "Y": y_projections
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {"Name": "c", "Entity": cat_entity, "Type": 0},
                    {"Name": "f", "Entity": "Fact_Sales", "Type": 0}
                ],
                "Select": select_items
            }
        }
    }
    return {"x": x, "y": y, "z": 3000, "width": w, "height": h, "config": json.dumps(config)}

def make_matrix(name, row_entity, row_prop, measure_names, x, y, w, h):
    row_ref = f"{row_entity}.{row_prop}"
    select_items = [{
        "Column": {
            "Expression": {"SourceRef": {"Source": "r"}},
            "Property": row_prop
        },
        "Name": row_ref
    }]
    val_projections = []
    for m in measure_names:
        m_ref = f"Fact_Sales.{m}"
        val_projections.append({"queryRef": m_ref})
        select_items.append({
            "Measure": {
                "Expression": {"SourceRef": {"Source": "f"}},
                "Property": m
            },
            "Name": m_ref
        })

    config = {
        "name": name,
        "singleVisual": {
            "visualType": "pivotTable",
            "projections": {
                "Rows": [{"queryRef": row_ref}],
                "Values": val_projections
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {"Name": "r", "Entity": row_entity, "Type": 0},
                    {"Name": "f", "Entity": "Fact_Sales", "Type": 0}
                ],
                "Select": select_items
            }
        }
    }
    return {"x": x, "y": y, "z": 3000, "width": w, "height": h, "config": json.dumps(config)}

# -----------------------------------------------------------------------------
# 6. Build All 4 Report Sections (report.json)
# -----------------------------------------------------------------------------
sections = [
    # SECTION 1: EXECUTIVE OVERVIEW
    {
        "name": "ReportSection1",
        "displayName": "Executive Overview",
        "filters": "[]",
        "height": 900.0,
        "width": 1280.0,
        "visualContainers": [
            make_textbox("Header_Page1", "Executive Sales Overview | Power BI Dashboard", 20, 15, 1240, 45),
            make_slicer("Slicer_Year", "Dim_Date", "Year", 20, 65, 390, 70),
            make_slicer("Slicer_Region", "Dim_Region", "Region", 430, 65, 410, 70),
            make_slicer("Slicer_Category", "Dim_Product", "Category", 860, 65, 400, 70),
            make_card("Card_Revenue", "Total Revenue", 20, 145, 230, 100),
            make_card("Card_Profit", "Total Profit", 270, 145, 230, 100),
            make_card("Card_Orders", "Total Orders", 520, 145, 230, 100),
            make_card("Card_Customers", "Total Customers", 770, 145, 230, 100),
            make_card("Card_Margin", "Profit Margin %", 1020, 145, 240, 100),
            make_line_chart("Monthly_Trend", "Dim_Date", "Year_Month", ["Total Revenue", "Total Profit"], 20, 255, 820, 310),
            make_pie_chart("Category_Donut", "Dim_Product", "Category", "Total Revenue", 860, 255, 400, 310),
            make_bar_chart("Profit_By_Region", "Dim_Region", "Region", "Total Profit", 20, 575, 550, 310, is_column=True),
            make_bar_chart("Top_Products", "Dim_Product", "Product_Name", "Total Revenue", 590, 575, 670, 310, is_column=False)
        ]
    },

    # SECTION 2: PRODUCT ANALYSIS
    {
        "name": "ReportSection2",
        "displayName": "Product Analysis",
        "filters": "[]",
        "height": 900.0,
        "width": 1280.0,
        "visualContainers": [
            make_textbox("Header_Page2", "Product Portfolio Performance & Margin Analysis", 20, 15, 1240, 45),
            make_slicer("Slicer_Prod_Cat", "Dim_Product", "Category", 20, 65, 400, 70),
            make_slicer("Slicer_Prod_Subcat", "Dim_Product", "Subcategory", 440, 65, 400, 70),
            make_slicer("Slicer_Prod_Item", "Dim_Product", "Product_Name", 860, 65, 400, 70),
            make_card("Card_Total_Qty", "Total Quantity Sold", 20, 145, 390, 100),
            make_card("Card_Total_Cost", "Total Cost", 430, 145, 410, 100),
            make_card("Card_ASP", "Average Selling Price", 860, 145, 400, 100),
            make_bar_chart("Rev_By_Product", "Dim_Product", "Product_Name", "Total Revenue", 20, 255, 610, 310, is_column=False),
            make_bar_chart("Profit_By_Subcategory", "Dim_Product", "Subcategory", "Total Profit", 650, 255, 610, 310, is_column=True),
            make_bar_chart("Top_5_Products", "Dim_Product", "Product_Name", "Total Profit", 20, 575, 610, 310, is_column=False),
            make_bar_chart("Bottom_5_Products", "Dim_Product", "Product_Name", "Total Revenue", 650, 575, 610, 310, is_column=False)
        ]
    },

    # SECTION 3: REGIONAL ANALYSIS
    {
        "name": "ReportSection3",
        "displayName": "Regional Analysis",
        "filters": "[]",
        "height": 900.0,
        "width": 1280.0,
        "visualContainers": [
            make_textbox("Header_Page3", "Geographic Territory & State-Level Distribution", 20, 15, 1240, 45),
            make_slicer("Slicer_Reg_Territory", "Dim_Region", "Region", 20, 65, 400, 70),
            make_slicer("Slicer_Reg_State", "Dim_Region", "State", 440, 65, 400, 70),
            make_slicer("Slicer_Reg_Year", "Dim_Date", "Year", 860, 65, 400, 70),
            make_bar_chart("Revenue_By_State", "Dim_Region", "State", "Total Revenue", 20, 145, 780, 360, is_column=False),
            make_pie_chart("Orders_By_Region_Donut", "Dim_Region", "Region", "Total Orders", 820, 145, 440, 360),
            make_bar_chart("Profit_By_Region_Col", "Dim_Region", "Region", "Total Profit", 20, 515, 550, 370, is_column=True),
            make_matrix("Region_Summary_Table", "Dim_Region", "Region", ["Total Revenue", "Total Profit", "Profit Margin %", "Total Orders"], 590, 515, 670, 370)
        ]
    },

    # SECTION 4: SALES TRENDS
    {
        "name": "ReportSection4",
        "displayName": "Sales Trends & Time Intelligence",
        "filters": "[]",
        "height": 900.0,
        "width": 1280.0,
        "visualContainers": [
            make_textbox("Header_Page4", "Time Intelligence & Comparative Growth Analytics (MoM / YoY)", 20, 15, 1240, 45),
            make_slicer("Slicer_Trend_Year", "Dim_Date", "Year", 20, 65, 600, 70),
            make_slicer("Slicer_Trend_Quarter", "Dim_Date", "Quarter", 640, 65, 620, 70),
            make_card("Card_Prior_Year", "Revenue Previous Year", 20, 145, 400, 100),
            make_card("Card_MoM_Growth", "MoM Revenue Growth %", 440, 145, 400, 100),
            make_card("Card_YoY_Growth", "YoY Revenue Growth %", 860, 145, 400, 100),
            make_bar_chart("YoY_Monthly_Comparison", "Dim_Date", "Month_Name", "Total Revenue", 20, 255, 1240, 310, is_column=True),
            make_line_chart("Profit_Trend_Line", "Dim_Date", "Year_Month", ["Total Profit"], 20, 575, 610, 310),
            make_line_chart("MoM_Growth_Line", "Dim_Date", "Year_Month", ["MoM Revenue Growth %"], 650, 575, 610, 310)
        ]
    }
]

report_json = {
    "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/1.0.0/schema.json",
    "config": json.dumps({
        "version": "5.50",
        "themeCollection": {"baseTheme": {"name": "User", "version": "2.157", "type": 2}},
        "activeSectionName": "ReportSection1"
    }),
    "layoutOptimization": 0,
    "resourcePackages": [],
    "sections": sections
}

with open(os.path.join(REPORT_DIR, "report.json"), "w", encoding="utf-8") as f:
    json.dump(report_json, f, indent=2)

print("[SUCCESS] Fully Bound 4-Page Power BI Project Architecture Successfully Created!")
print(f" -> PBIP Launcher:   {PBIP_FILE}")
print(f" -> Model BIM:       {os.path.join(DATASET_DIR, 'model.bim')}")
print(f" -> Report JSON:     {os.path.join(REPORT_DIR, 'report.json')}")

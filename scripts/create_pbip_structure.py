import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PBIP_FILE = os.path.join(BASE_DIR, "Sales Dashboard using Power BI.pbip")
REPORT_DIR = os.path.join(BASE_DIR, "Sales Dashboard using Power BI.Report")
DATASET_DIR = os.path.join(BASE_DIR, "Sales Dashboard using Power BI.Dataset")
CSV_PATH = os.path.join(BASE_DIR, "data", "cleaned_sales_data.csv").replace("\\", "/")

os.makedirs(REPORT_DIR, exist_ok=True)
os.makedirs(DATASET_DIR, exist_ok=True)

# 1. Create .pbip launcher file
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
with open(PBIP_FILE, "w") as f:
    json.dump(pbip_content, f, indent=2)

# 2. Create Dataset definition (definition.pbidataset)
pbi_dataset = {
  "version": "1.0"
}
with open(os.path.join(DATASET_DIR, "definition.pbidataset"), "w") as f:
    json.dump(pbi_dataset, f, indent=2)

# 3. Create Report definition (definition.pbir)
pbi_report = {
  "version": "1.0",
  "datasetReference": {
    "byPath": {
      "path": "../Sales Dashboard using Power BI.Dataset"
    }
  }
}
with open(os.path.join(REPORT_DIR, "definition.pbir"), "w") as f:
    json.dump(pbi_report, f, indent=2)

# 4. Create model.bim (Tabular Model Definition with Enhanced Metadata Annotations)
model_bim = {
  "name": "Sales_Dashboard_Model",
  "compatibilityLevel": 1567,
  "model": {
    "culture": "en-US",
    "dataAccessOptions": {
      "legacyRedirects": True,
      "returnErrorValuesAsNull": True,
      "fastCombine": True
    },
    "annotations": [
      {
        "name": "PBI_QueryOrder",
        "value": "[\"Fact_Sales\",\"Dim_Date\",\"Dim_Customer\",\"Dim_Product\",\"Dim_Region\"]"
      },
      {
        "name": "__PBI_TimeIntelligenceEnabled",
        "value": "1"
      },
      {
        "name": "PBIDesktopVersion",
        "value": "2.157.1354.0"
      },
      {
        "name": "PBI_ProTooling",
        "value": "[\"DevMode\"]"
      },
      {
        "name": "PBI_EnhancedModelMetadata",
        "value": "1"
      }
    ],
    "tables": [
      {
        "name": "Fact_Sales",
        "columns": [
          {"name": "Order_ID", "dataType": "string", "sourceColumn": "Order_ID"},
          {"name": "Order_Date", "dataType": "dateTime", "sourceColumn": "Order_Date", "formatString": "yyyy-mm-dd"},
          {"name": "Customer_ID", "dataType": "string", "sourceColumn": "Customer_ID"},
          {"name": "Customer_Name", "dataType": "string", "sourceColumn": "Customer_Name"},
          {"name": "Segment", "dataType": "string", "sourceColumn": "Segment"},
          {"name": "Region", "dataType": "string", "sourceColumn": "Region"},
          {"name": "Product_ID", "dataType": "string", "sourceColumn": "Product_ID"},
          {"name": "Product_Name", "dataType": "string", "sourceColumn": "Product_Name"},
          {"name": "Category", "dataType": "string", "sourceColumn": "Category"},
          {"name": "Sub_Category", "dataType": "string", "sourceColumn": "Sub_Category"},
          {"name": "Quantity", "dataType": "int64", "sourceColumn": "Quantity"},
          {"name": "Unit_Price", "dataType": "double", "sourceColumn": "Unit_Price", "formatString": "$#,##0.00"},
          {"name": "Discount", "dataType": "double", "sourceColumn": "Discount", "formatString": "0.0%"},
          {"name": "Sales", "dataType": "double", "sourceColumn": "Sales", "formatString": "$#,##0.00"},
          {"name": "Profit", "dataType": "double", "sourceColumn": "Profit", "formatString": "$#,##0.00"}
        ],
        "partitions": [
          {
            "name": "Fact_Sales-Partition",
            "mode": "import",
            "source": {
              "type": "m",
              "expression": [
                "let",
                f"    Source = Csv.Document(File.Contents(\"{CSV_PATH}\"),[Delimiter=\",\", Columns=15, Encoding=65001, QuoteStyle=QuoteStyle.None]),",
                "    #\"Promoted Headers\" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),",
                "    #\"Changed Type\" = Table.TransformColumnTypes(#\"Promoted Headers\",{{\"Order_ID\", type text}, {\"Order_Date\", type datetime}, {\"Customer_ID\", type text}, {\"Customer_Name\", type text}, {\"Segment\", type text}, {\"Region\", type text}, {\"Product_ID\", type text}, {\"Product_Name\", type text}, {\"Category\", type text}, {\"Sub_Category\", type text}, {\"Quantity\", Int64.Type}, {\"Unit_Price\", type number}, {\"Discount\", type number}, {\"Sales\", type number}, {\"Profit\", type number}})",
                "in",
                "    #\"Changed Type\""
              ]
            }
          }
        ],
        "measures": [
          {
            "name": "Total Revenue",
            "expression": "SUM(Fact_Sales[Sales])",
            "formatString": "$#,##0.00"
          },
          {
            "name": "Total Profit",
            "expression": "SUM(Fact_Sales[Profit])",
            "formatString": "$#,##0.00"
          },
          {
            "name": "Total Orders",
            "expression": "DISTINCTCOUNT(Fact_Sales[Order_ID])",
            "formatString": "#,##0"
          },
          {
            "name": "Total Customers",
            "expression": "DISTINCTCOUNT(Fact_Sales[Customer_ID])",
            "formatString": "#,##0"
          },
          {
            "name": "Profit Margin %",
            "expression": "DIVIDE([Total Profit], [Total Revenue], 0)",
            "formatString": "0.00%"
          },
          {
            "name": "Avg Order Value",
            "expression": "DIVIDE([Total Revenue], [Total Orders], 0)",
            "formatString": "$#,##0.00"
          }
        ]
      },
      {
        "name": "Dim_Date",
        "columns": [
          {"name": "Date", "dataType": "dateTime", "sourceColumn": "Date", "formatString": "yyyy-mm-dd", "isKey": True},
          {"name": "Year", "dataType": "int64", "sourceColumn": "Year"},
          {"name": "Month_Number", "dataType": "int64", "sourceColumn": "Month_Number"},
          {"name": "Month_Name", "dataType": "string", "sourceColumn": "Month_Name"},
          {"name": "Year_Month", "dataType": "string", "sourceColumn": "Year_Month"},
          {"name": "Quarter", "dataType": "string", "sourceColumn": "Quarter"}
        ],
        "partitions": [
          {
            "name": "Dim_Date-Partition",
            "mode": "import",
            "source": {
              "type": "m",
              "expression": [
                "let",
                "    Source = List.Dates(#date(2024, 1, 1), Duration.Days(#date(2025, 12, 31) - #date(2024, 1, 1)) + 1, #duration(1, 0, 0, 0)),",
                "    #\"Converted to Table\" = Table.FromList(Source, Splitter.SplitByNothing(), {\"Date\"}, null, ExtraValues.Error),",
                "    #\"Changed Type\" = Table.TransformColumnTypes(#\"Converted to Table\",{{\"Date\", type datetime}}),",
                "    #\"Added Year\" = Table.AddColumn(#\"Changed Type\", \"Year\", each Date.Year([Date]), Int64.Type),",
                "    #\"Added Month Number\" = Table.AddColumn(#\"Added Year\", \"Month_Number\", each Date.Month([Date]), Int64.Type),",
                "    #\"Added Month Name\" = Table.AddColumn(#\"Added Month Number\", \"Month_Name\", each Date.ToText([Date], \"MMM\"), type text),",
                "    #\"Added Year Month\" = Table.AddColumn(#\"Added Month Name\", \"Year_Month\", each Date.ToText([Date], \"yyyy-MM\"), type text),",
                "    #\"Added Quarter\" = Table.AddColumn(#\"Added Year Month\", \"Quarter\", each \"Q\" & Text.From(Date.QuarterOfYear([Date])), type text)",
                "in",
                "    #\"Added Quarter\""
              ]
            }
          }
        ]
      },
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
                f"    Source = Csv.Document(File.Contents(\"{CSV_PATH}\"),[Delimiter=\",\", Columns=15, Encoding=65001, QuoteStyle=QuoteStyle.None]),",
                "    #\"Promoted Headers\" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),",
                "    #\"Selected Columns\" = Table.SelectColumns(#\"Promoted Headers\",{\"Customer_ID\", \"Customer_Name\", \"Segment\"}),",
                "    #\"Removed Duplicates\" = Table.Distinct(#\"Selected Columns\")",
                "in",
                "    #\"Removed Duplicates\""
              ]
            }
          }
        ]
      },
      {
        "name": "Dim_Product",
        "columns": [
          {"name": "Product_ID", "dataType": "string", "sourceColumn": "Product_ID", "isKey": True},
          {"name": "Product_Name", "dataType": "string", "sourceColumn": "Product_Name"},
          {"name": "Category", "dataType": "string", "sourceColumn": "Category"},
          {"name": "Sub_Category", "dataType": "string", "sourceColumn": "Sub_Category"}
        ],
        "partitions": [
          {
            "name": "Dim_Product-Partition",
            "mode": "import",
            "source": {
              "type": "m",
              "expression": [
                "let",
                f"    Source = Csv.Document(File.Contents(\"{CSV_PATH}\"),[Delimiter=\",\", Columns=15, Encoding=65001, QuoteStyle=QuoteStyle.None]),",
                "    #\"Promoted Headers\" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),",
                "    #\"Selected Columns\" = Table.SelectColumns(#\"Promoted Headers\",{\"Product_ID\", \"Product_Name\", \"Category\", \"Sub_Category\"}),",
                "    #\"Removed Duplicates\" = Table.Distinct(#\"Selected Columns\")",
                "in",
                "    #\"Removed Duplicates\""
              ]
            }
          }
        ]
      },
      {
        "name": "Dim_Region",
        "columns": [
          {"name": "Region", "dataType": "string", "sourceColumn": "Region", "isKey": True}
        ],
        "partitions": [
          {
            "name": "Dim_Region-Partition",
            "mode": "import",
            "source": {
              "type": "m",
              "expression": [
                "let",
                f"    Source = Csv.Document(File.Contents(\"{CSV_PATH}\"),[Delimiter=\",\", Columns=15, Encoding=65001, QuoteStyle=QuoteStyle.None]),",
                "    #\"Promoted Headers\" = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),",
                "    #\"Selected Columns\" = Table.SelectColumns(#\"Promoted Headers\",{\"Region\"}),",
                "    #\"Removed Duplicates\" = Table.Distinct(#\"Selected Columns\")",
                "in",
                "    #\"Removed Duplicates\""
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
        "fromColumn": "Region",
        "toTable": "Dim_Region",
        "toColumn": "Region"
      }
    ]
  }
}

with open(os.path.join(DATASET_DIR, "model.bim"), "w") as f:
    json.dump(model_bim, f, indent=2)

# 5. Create report.json (Visual layout & canvas definitions for Power BI Report)
def build_card_config(table, measure, title):
    return json.dumps({
        "name": title.replace(" ", "_"),
        "singleVisual": {
            "visualType": "card",
            "projections": {
                "Fields": [
                    {
                        "queryRef": f"{table}.{measure}"
                    }
                ]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": "f", "Entity": table, "Type": 0}],
                "Select": [{"Measure": {"Expression": {"SourceRef": {"Source": "f"}}, "Property": measure}, "Name": f"{table}.{measure}"}]
            }
        }
    })

def build_slicer_config(table, column, title):
    return json.dumps({
        "name": title.replace(" ", "_"),
        "singleVisual": {
            "visualType": "slicer",
            "projections": {
                "Values": [
                    {
                        "queryRef": f"{table}.{column}"
                    }
                ]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [{"Name": "t", "Entity": table, "Type": 0}],
                "Select": [{"Column": {"Expression": {"SourceRef": {"Source": "t"}}, "Property": column}, "Name": f"{table}.{column}"}]
            }
        }
    })

def build_chart_config(visual_type, x_table, x_col, y_table, y_measure, title):
    return json.dumps({
        "name": title.replace(" ", "_"),
        "singleVisual": {
            "visualType": visual_type,
            "projections": {
                "Category": [
                    {"queryRef": f"{x_table}.{x_col}"}
                ],
                "Y": [
                    {"queryRef": f"{y_table}.{y_measure}"}
                ]
            },
            "prototypeQuery": {
                "Version": 2,
                "From": [
                    {"Name": "x", "Entity": x_table, "Type": 0},
                    {"Name": "y", "Entity": y_table, "Type": 0}
                ],
                "Select": [
                    {"Column": {"Expression": {"SourceRef": {"Source": "x"}}, "Property": x_col}, "Name": f"{x_table}.{x_col}"},
                    {"Measure": {"Expression": {"SourceRef": {"Source": "y"}}, "Property": y_measure}, "Name": f"{y_table}.{y_measure}"}
                ]
            }
        }
    })

visual_containers = [
    # Header Title
    {
        "x": 20, "y": 15, "z": 0, "width": 1240, "height": 50,
        "config": json.dumps({
            "name": "Header_Title",
            "singleVisual": {
                "visualType": "textbox",
                "objects": {
                    "general": [
                        {
                            "properties": {
                                "paragraphs": [
                                    {
                                        "textRuns": [
                                            {
                                                "value": "Sales Analytics Dashboard",
                                                "textStyle": {"fontFamily": "Segoe UI", "fontSize": "18pt", "fontWeight": "bold", "color": "#0f172a"}
                                            }
                                        ]
                                    }
                                ]
                            }
                        }
                    ]
                }
            }
        })
    },
    # Slicers (Top Bar)
    {"x": 20, "y": 75, "z": 1, "width": 230, "height": 80, "config": build_slicer_config("Dim_Date", "Year", "Year_Slicer")},
    {"x": 270, "y": 75, "z": 2, "width": 230, "height": 80, "config": build_slicer_config("Dim_Region", "Region", "Region_Slicer")},
    {"x": 520, "y": 75, "z": 3, "width": 230, "height": 80, "config": build_slicer_config("Dim_Product", "Category", "Category_Slicer")},
    {"x": 770, "y": 75, "z": 4, "width": 230, "height": 80, "config": build_slicer_config("Dim_Product", "Product_Name", "Product_Slicer")},
    {"x": 1020, "y": 75, "z": 5, "width": 240, "height": 80, "config": build_slicer_config("Dim_Customer", "Customer_Name", "Customer_Slicer")},

    # KPI Cards (Row 1)
    {"x": 20, "y": 165, "z": 6, "width": 230, "height": 110, "config": build_card_config("Fact_Sales", "Total Revenue", "Total_Revenue_Card")},
    {"x": 270, "y": 165, "z": 7, "width": 230, "height": 110, "config": build_card_config("Fact_Sales", "Total Profit", "Total_Profit_Card")},
    {"x": 520, "y": 165, "z": 8, "width": 230, "height": 110, "config": build_card_config("Fact_Sales", "Total Orders", "Total_Orders_Card")},
    {"x": 770, "y": 165, "z": 9, "width": 230, "height": 110, "config": build_card_config("Fact_Sales", "Total Customers", "Total_Customers_Card")},
    {"x": 1020, "y": 165, "z": 10, "width": 240, "height": 110, "config": build_card_config("Fact_Sales", "Profit Margin %", "Profit_Margin_Card")},

    # Main Trend Chart (Center)
    {"x": 20, "y": 285, "z": 11, "width": 820, "height": 300, "config": build_chart_config("lineChart", "Dim_Date", "Year_Month", "Fact_Sales", "Total Revenue", "Monthly_Trend_Chart")},

    # Category Donut Chart
    {"x": 850, "y": 285, "z": 12, "width": 410, "height": 300, "config": build_chart_config("pieChart", "Dim_Product", "Category", "Fact_Sales", "Total Revenue", "Category_Sales_Chart")},

    # Region Bar Chart
    {"x": 20, "y": 595, "z": 13, "width": 390, "height": 295, "config": build_chart_config("barChart", "Dim_Region", "Region", "Fact_Sales", "Total Revenue", "Region_Sales_Chart")},

    # Top Products Bar Chart
    {"x": 420, "y": 595, "z": 14, "width": 420, "height": 295, "config": build_chart_config("barChart", "Dim_Product", "Product_Name", "Fact_Sales", "Total Revenue", "Top_Products_Chart")},

    # Top Customers Bar Chart
    {"x": 850, "y": 595, "z": 15, "width": 410, "height": 295, "config": build_chart_config("barChart", "Dim_Customer", "Customer_Name", "Fact_Sales", "Total Revenue", "Top_Customers_Chart")}
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
  "sections": [
    {
      "name": "ReportSection1",
      "displayName": "Executive Sales Dashboard",
      "filters": "[]",
      "height": 900.0,
      "width": 1280.0,
      "visualContainers": visual_containers
    }
  ]
}

with open(os.path.join(REPORT_DIR, "report.json"), "w") as f:
    json.dump(report_json, f, indent=2)

print("Updated Power BI Project (.pbip) with PBI_EnhancedModelMetadata and type datetime!")

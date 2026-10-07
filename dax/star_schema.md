# Data Model Architecture (Star Schema)

The Power BI Sales Analytics Dashboard utilizes an optimized **Star Schema** data model designed for high performance, clean DAX measure calculation, and intuitive slice-and-dice functionality.

```
       +------------------+
       |     Dim_Date     |
       +------------------+
       | Date (PK)        |
       | Year             |
       | Month_Name       |
       | Quarter          |
       +--------+---------+
                | 1
                |
                | *
+---------------+----------------+       +-------------------+
|           Fact_Sales           |       |   Dim_Customer    |
+--------------------------------+       +-------------------+
| Order_ID                       |       | Customer_ID (PK)  |
| Order_Date (FK) --------------+-------| Customer_Name     |
| Customer_ID (FK) -------------+  * 1  | Segment           |
| Product_ID (FK) --------------+-------+-------------------+
| Region (FK) -------------------+  * 1
| Quantity                       |  * 1  +-------------------+
| Unit_Price                     |-------|    Dim_Product    |
| Discount                       |       +-------------------+
| Sales                          |       | Product_ID (PK)   |
| Profit                         |       | Product_Name      |
+--------------------------------+       | Category          |
                | *                      | Sub_Category      |
                |                        +-------------------+
                | 1
       +--------+---------+
       |    Dim_Region    |
       +------------------+
       | Region (PK)      |
       +------------------+
```

## Entity Details

### 1. Fact_Sales (Fact Table)
Contains transaction-level granular sales data.
- Primary Key: `Order_ID`
- Foreign Keys: `Order_Date`, `Customer_ID`, `Product_ID`, `Region`
- Measures/Metrics: `Quantity`, `Unit_Price`, `Discount`, `Sales`, `Profit`

### 2. Dim_Date (Dimension Table)
Generated via DAX `CALENDAR()` for time intelligence and date filtering.
- Primary Key: `Date`
- Key Columns: `Year`, `Month_Name`, `Year_Month`, `Quarter`, `Day_of_Week`

### 3. Dim_Customer (Dimension Table)
Contains customer attributes.
- Primary Key: `Customer_ID`
- Key Columns: `Customer_Name`, `Segment`

### 4. Dim_Product (Dimension Table)
Contains product attributes and hierarchical categorizations.
- Primary Key: `Product_ID`
- Key Columns: `Product_Name`, `Category`, `Sub_Category`, `Base_Cost`, `Base_Price`

### 5. Dim_Region (Dimension Table)
Geographic region dimensions.
- Primary Key: `Region` (Values: North, South, East, West, Central)

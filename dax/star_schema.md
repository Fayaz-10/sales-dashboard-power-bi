# Star Schema Data Model Architecture

The Power BI Sales Analytics Dashboard is architected as an industry-standard **Star Schema** data model. This relational design decouples high-volume transactional facts from descriptive dimensional attributes, eliminating redundancy, maximizing DAX calculation speed, and guaranteeing intuitive slice-and-dice behavior.

```
       +------------------+
       |     Dim_Date     |
       +------------------+
       | Date (PK)        |
       | Year             |
       | Quarter          |
       | Month_Number     |
       | Month_Name       |
       | Year_Month       |
       | Day              |
       | Day_of_Week      |
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
| State (FK) --------------------+  * 1
| Region                         |  * 1  +-------------------+
| Quantity                       |-------|    Dim_Product    |
| Unit_Price                     |       +-------------------+
| Discount                       |       | Product_ID (PK)   |
| Revenue                        |       | Product_Name      |
| Cost                           |       | Category          |
| Profit                         |       | Subcategory       |
| Payment_Method                 |       | Unit_Cost         |
+--------------------------------+       | Unit_Price        |
                | *                      +-------------------+
                |
                | 1
       +--------+---------+
       |    Dim_Region    |
       +------------------+
       | State (PK)       |
       | Region           |
       +------------------+
```

---

## Entity & Relationship Specifications

### 1. `Fact_Sales` (Central Fact Table)
Stores individual sales order line-item transactions.
- **Grain:** One record per sales transaction order line.
- **Primary / Degenerate Key:** `Order_ID`
- **Foreign Keys:**
  - `Order_Date` -> Links to `Dim_Date[Date]`
  - `Customer_ID` -> Links to `Dim_Customer[Customer_ID]`
  - `Product_ID` -> Links to `Dim_Product[Product_ID]`
  - `State` -> Links to `Dim_Region[State]`
- **Numeric Measures:** `Quantity`, `Unit_Price`, `Discount`, `Revenue`, `Cost`, `Profit`
- **Attribute:** `Payment_Method`

### 2. `Dim_Date` (Calendar Dimension Table)
Provides continuous calendar dates covering the full operational span (`2024-01-01` to `2025-12-31`).
- **Primary Key:** `Date` (Marked as Official Date Table in Power BI)
- **Attributes:** `Year` (2024, 2025), `Quarter` (Q1–Q4), `Month_Number` (1–12), `Month_Name` (Jan–Dec), `Year_Month` (yyyy-MM), `Day` (1–31), `Day_of_Week` (Mon–Sun).
- **Sorting Rule:** `Month_Name` sorted by `Month_Number` to avoid alphabetical ordering.

### 3. `Dim_Customer` (Customer Dimension Table)
Contains customer company master records.
- **Primary Key:** `Customer_ID`
- **Attributes:** `Customer_Name`, `Segment` (`Corporate`, `Consumer`, `Home Office`).

### 4. `Dim_Product` (Product Catalog Dimension Table)
Stores item specifications and hierarchical categorizations.
- **Primary Key:** `Product_ID`
- **Attributes:** `Product_Name`, `Category` (`Technology`, `Furniture`, `Office Supplies`), `Subcategory` (11 distinct subcategories), `Unit_Cost`, `Unit_Price`.

### 5. `Dim_Region` (Geographic Dimension Table)
Maps individual states to their broader macro-economic geographic sales regions.
- **Primary Key:** `State` (15 distinct US States)
- **Attributes:** `Region` (`West`, `East`, `Central`, `South`, `North`).
- **Hierarchy:** `Region` > `State` allows seamless drill-down from macro territory to state-level sales performance.

---

## Relationship Cardinality & Filter Propagation

| From Table (Many *) | From Key Column | To Table (One 1) | To Key Column | Cardinality | Cross Filter Direction | Security / Ambiguity |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| `Fact_Sales` | `Order_Date` | `Dim_Date` | `Date` | Many-to-One (*:1) | Single (`Dim_Date` filters `Fact_Sales`) | Active, Unambiguous |
| `Fact_Sales` | `Customer_ID`| `Dim_Customer`| `Customer_ID`| Many-to-One (*:1) | Single (`Dim_Customer` filters `Fact_Sales`) | Active, Unambiguous |
| `Fact_Sales` | `Product_ID` | `Dim_Product` | `Product_ID` | Many-to-One (*:1) | Single (`Dim_Product` filters `Fact_Sales`) | Active, Unambiguous |
| `Fact_Sales` | `State` | `Dim_Region` | `State` | Many-to-One (*:1) | Single (`Dim_Region` filters `Fact_Sales`) | Active, Unambiguous |

*Note: All cross-filter directions are strictly **Single**, flowing from dimension tables to the central fact table. This strictly prevents bidirectional filter loops and guarantees high query efficiency.*

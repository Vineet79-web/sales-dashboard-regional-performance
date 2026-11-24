# Power BI: Setup and DAX Measures

## 1. Connect
1. Power BI Desktop > **Get Data > PostgreSQL database** (server `localhost`, database `sales_dashboard`).
   - No PostgreSQL? Use **Get Data > Text/CSV** and load `data/orders.csv`, `products.csv`, `returns.csv`, then merge them in Power Query.
2. Load the view **`vw_sales_analysis`** (already joins the 3 tables).
3. Create a calendar table (Modeling > New table):

```DAX
Calendar =
ADDCOLUMNS(
    CALENDAR(DATE(2024,1,1), DATE(2024,12,31)),
    "Year", YEAR([Date]),
    "Month No", MONTH([Date]),
    "Month", FORMAT([Date], "MMM"),
    "Month Start", DATE(YEAR([Date]), MONTH([Date]), 1)
)
```
4. Relationship: `Calendar[Date]` (1) to `vw_sales_analysis[order_date]` (many). Sort `Month` by `Month No`.

## 2. The 10 measures

```DAX
Total Sales = SUM(vw_sales_analysis[net_sales])

Total Orders = DISTINCTCOUNT(vw_sales_analysis[order_id])

Units Sold = SUM(vw_sales_analysis[quantity])

Avg Order Value = DIVIDE([Total Sales], [Total Orders])

Returned Orders = CALCULATE([Total Orders], vw_sales_analysis[is_returned] = 1)

Return Rate % = DIVIDE([Returned Orders], [Total Orders])

Sales Previous Month = CALCULATE([Total Sales], DATEADD('Calendar'[Date], -1, MONTH))

Sales MoM % = DIVIDE([Total Sales] - [Sales Previous Month], [Sales Previous Month])

Region Share % =
DIVIDE([Total Sales], CALCULATE([Total Sales], ALL(vw_sales_analysis[region])))

Avg Discount % = AVERAGE(vw_sales_analysis[discount])
```

## 3. Suggested pages (multipage dashboard)
| Page | Visuals |
|------|---------|
| **Overview** | KPI cards (Total Sales, Orders, AOV, Return Rate %), monthly sales line chart, region map or bar |
| **Regional Performance** | Region bar chart with Region Share %, matrix region x category, MoM % by region |
| **Products** | Top 10 products bar, category treemap, discount vs sales scatter |
| **Returns** | Return Rate % by category, return reasons donut/bar |

## 4. Slicers and drill-down
- Slicers: Region, Category, Month (use the Calendar table).
- Enable drill-down on a hierarchy: Region > Category > Product.
- Turn on "Sync slicers" so filters carry across pages.

## 5. Export
- Save as `sales_dashboard.pbix` (commit it if under 100 MB).
- Export each page as PNG (File > Export > or screenshot) into `powerbi/screenshots/` and link them in the README. Recruiters look at screenshots first.

# Build the Power BI Dashboard (step by step)

Time: about 1 to 2 hours. You need Power BI Desktop (free, Windows): https://powerbi.microsoft.com/desktop

## Step 1: Load the data
1. Open Power BI Desktop > **Home > Get data > Text/CSV**.
2. Pick `data/sales_analysis.csv` > **Load**.
3. In the right-hand **Data** pane, right-click the table > **Rename** > `sales`.

## Step 2: Calendar table and relationship
1. **Home > New table** (or Table tools). Paste the `Calendar = ...` code from `DAX_measures.md` and press Enter.
2. Left side: open **Model view**. Drag `Calendar[Date]` onto `sales[order_date]`.
3. Click `Calendar[Month]` > **Column tools > Sort by column > Month No**.

## Step 3: Add the 10 measures
Select the `sales` table > **Home > New measure** and paste each measure from `DAX_measures.md`, one at a time.
Check each by dragging it into a Card visual.

## Step 4: Build 4 pages (bottom tabs, + to add a page)
| Page | Visuals to add |
|---|---|
| **1 Overview** | 4 **Cards**: Total Sales, Total Orders, Avg Order Value, Return Rate %. **Line chart**: X = `Calendar[Month]`, Y = Total Sales. **Bar chart**: X = region, Y = Total Sales. Slicers: region, category |
| **2 Regional** | **Matrix**: rows = region, columns = category, values = Total Sales. **Column chart**: X = `Calendar[Month]`, Y = Sales MoM %. **Donut**: legend = region, values = Region Share % |
| **3 Products** | **Bar chart**: Y = product_name, X = Total Sales, then Filters pane > Top N = 10. **Treemap**: category by Total Sales. **Table**: product_name, Units Sold, Avg Discount % |
| **4 Returns** | **Bar chart**: category by Return Rate %. **Bar chart**: return_reason by Returned Orders (Filters pane: return_reason is not blank). Cards: Returned Orders, Return Rate % |

Tips: add the same Region and Category slicers to every page (View > Sync slicers). Give each page a title text box.

## Step 5: Save and export
1. **File > Save as** > `sales_dashboard.pbix`.
2. Screenshot each page (Windows key + Shift + S) and save as `page1_overview.png`, `page2_regional.png`, `page3_products.png`, `page4_returns.png`.
3. Optional: **File > Export > Export to PDF**.

## Step 6: Upload to GitHub
1. Open the repo on github.com > open the `powerbi` folder > **Add file > Upload files**.
2. Upload `sales_dashboard.pbix`, then upload the PNGs into `powerbi/screenshots/`.
3. Commit changes. Then add this to the README so the screenshots show:
```
![Overview](powerbi/screenshots/page1_overview.png)
```
4. Tell the interviewer: "The dashboard file is in the repo; here is a walkthrough" and be ready to open the .pbix.

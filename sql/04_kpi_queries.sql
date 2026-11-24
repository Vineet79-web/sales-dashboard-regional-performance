-- KPI and analysis queries (PostgreSQL). Run after 03_analysis_dataset.sql.

-- 1. Monthly sales with month-over-month growth (window function: LAG)
WITH monthly AS (
    SELECT order_month, SUM(net_sales) AS sales
    FROM vw_sales_analysis
    GROUP BY order_month
)
SELECT
    order_month,
    ROUND(sales)                                            AS sales,
    ROUND(100.0 * (sales - LAG(sales) OVER (ORDER BY order_month))
          / NULLIF(LAG(sales) OVER (ORDER BY order_month), 0), 1) AS mom_growth_pct
FROM monthly
ORDER BY order_month;

-- 2. Region performance: sales, orders, avg order value, return rate
SELECT
    region,
    ROUND(SUM(net_sales))                       AS sales,
    COUNT(*)                                    AS orders,
    ROUND(AVG(net_sales))                       AS avg_order_value,
    ROUND(100.0 * AVG(is_returned), 2)          AS return_rate_pct,
    RANK() OVER (ORDER BY SUM(net_sales) DESC)  AS sales_rank
FROM vw_sales_analysis
GROUP BY region
ORDER BY sales_rank;

-- 3. Top 3 products in every category (window function: ROW_NUMBER)
SELECT *
FROM (
    SELECT
        category,
        product_name,
        ROUND(SUM(net_sales)) AS sales,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY SUM(net_sales) DESC) AS rn
    FROM vw_sales_analysis
    GROUP BY category, product_name
) t
WHERE rn <= 3
ORDER BY category, rn;

-- 4. Return rate and return reasons by category
SELECT
    category,
    ROUND(100.0 * AVG(is_returned), 2) AS return_rate_pct,
    COUNT(*) FILTER (WHERE is_returned = 1) AS returned_orders
FROM vw_sales_analysis
GROUP BY category
ORDER BY return_rate_pct DESC;

-- 5. Festival season (Oct-Nov) vs post-festival (Dec) sales change, per region.
--    This is how you would check for a "post-festival drop" - report the number YOUR data gives.
WITH r AS (
    SELECT
        region,
        SUM(net_sales) FILTER (WHERE EXTRACT(MONTH FROM order_date) IN (10, 11)) / 2.0 AS avg_festival_month,
        SUM(net_sales) FILTER (WHERE EXTRACT(MONTH FROM order_date) = 12)               AS december
    FROM vw_sales_analysis
    GROUP BY region
)
SELECT
    region,
    ROUND(avg_festival_month) AS avg_festival_month_sales,
    ROUND(december)           AS december_sales,
    ROUND(100.0 * (december - avg_festival_month) / avg_festival_month, 1) AS change_pct
FROM r
ORDER BY change_pct;

-- 6. Running (cumulative) sales by region
SELECT
    region,
    order_month,
    ROUND(SUM(SUM(net_sales)) OVER (PARTITION BY region ORDER BY order_month)) AS cumulative_sales
FROM vw_sales_analysis
GROUP BY region, order_month
ORDER BY region, order_month;

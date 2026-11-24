-- Joins the 3 tables into one analysis-ready view (this is what Power BI connects to).

DROP VIEW IF EXISTS vw_sales_analysis;

CREATE VIEW vw_sales_analysis AS
SELECT
    o.order_id,
    o.order_date,
    DATE_TRUNC('month', o.order_date)::DATE            AS order_month,
    o.region,
    o.customer_id,
    p.product_id,
    p.product_name,
    p.category,
    p.unit_price,
    o.quantity,
    o.discount,
    ROUND(o.quantity * p.unit_price * (1 - o.discount), 2) AS net_sales,
    CASE WHEN r.return_id IS NOT NULL THEN 1 ELSE 0 END    AS is_returned,
    r.reason                                              AS return_reason
FROM orders o
JOIN products p      ON p.product_id = o.product_id
LEFT JOIN returns r  ON r.order_id   = o.order_id;

-- check
SELECT COUNT(*) AS rows_in_view, ROUND(SUM(net_sales)) AS total_net_sales
FROM vw_sales_analysis;

-- Run from the project root folder with psql so the relative paths work:
--   psql -d sales_dashboard -f sql/02_load_data.sql
-- (\copy reads the files from YOUR machine, no server file permissions needed)

\copy products FROM 'data/products.csv' WITH (FORMAT csv, HEADER true)
\copy orders   FROM 'data/orders.csv'   WITH (FORMAT csv, HEADER true)
\copy returns  FROM 'data/returns.csv'  WITH (FORMAT csv, HEADER true)

-- sanity check
SELECT 'orders' AS tbl, COUNT(*) FROM orders
UNION ALL SELECT 'products', COUNT(*) FROM products
UNION ALL SELECT 'returns',  COUNT(*) FROM returns;

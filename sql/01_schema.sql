-- PostgreSQL: create database first (run once):  CREATE DATABASE sales_dashboard;
-- Then connect to it and run this file.

DROP TABLE IF EXISTS returns;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;

CREATE TABLE products (
    product_id    INT PRIMARY KEY,
    product_name  VARCHAR(100) NOT NULL,
    category      VARCHAR(50)  NOT NULL,
    unit_price    NUMERIC(10,2) NOT NULL
);

CREATE TABLE orders (
    order_id     INT PRIMARY KEY,
    order_date   DATE NOT NULL,
    region       VARCHAR(20) NOT NULL,
    customer_id  INT NOT NULL,
    product_id   INT NOT NULL REFERENCES products(product_id),
    quantity     INT NOT NULL,
    discount     NUMERIC(4,2) NOT NULL
);

CREATE TABLE returns (
    return_id    INT PRIMARY KEY,
    order_id     INT NOT NULL REFERENCES orders(order_id),
    return_date  DATE NOT NULL,
    reason       VARCHAR(50)
);

CREATE INDEX idx_orders_date   ON orders(order_date);
CREATE INDEX idx_orders_region ON orders(region);
CREATE INDEX idx_returns_order ON returns(order_id);

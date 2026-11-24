"""
Joins orders + products + returns into ONE file (data/sales_analysis.csv),
the same columns as the SQL view vw_sales_analysis. Load this single file
into Power BI so no table relationships are needed.

Run:  python export_flat_csv.py
"""
import pandas as pd

orders = pd.read_csv("data/orders.csv", parse_dates=["order_date"])
products = pd.read_csv("data/products.csv")
returns = pd.read_csv("data/returns.csv")

df = orders.merge(products, on="product_id").merge(
    returns[["order_id", "reason"]], on="order_id", how="left")
df["net_sales"] = (df["quantity"] * df["unit_price"] * (1 - df["discount"])).round(2)
df["is_returned"] = df["reason"].notna().astype(int)
df["order_month"] = df["order_date"].dt.to_period("M").dt.to_timestamp().dt.date
df["order_date"] = df["order_date"].dt.date
df = df.rename(columns={"reason": "return_reason"})

cols = ["order_id", "order_date", "order_month", "region", "customer_id",
        "product_id", "product_name", "category", "unit_price", "quantity",
        "discount", "net_sales", "is_returned", "return_reason"]
df[cols].sort_values("order_id").to_csv("data/sales_analysis.csv", index=False)
print("Saved data/sales_analysis.csv:", len(df), "rows")

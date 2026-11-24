"""
Builds preview charts and prints the key findings from the CSV tables.
Run:  python make_charts.py
Output: outputs/charts/*.png  and printed findings.

These are Python (Matplotlib) preview charts of the same KPIs used in the
Power BI dashboard. They are NOT Power BI screenshots.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")
OUT = Path("outputs/charts")
OUT.mkdir(parents=True, exist_ok=True)

orders = pd.read_csv("data/orders.csv", parse_dates=["order_date"])
products = pd.read_csv("data/products.csv")
returns = pd.read_csv("data/returns.csv")

df = orders.merge(products, on="product_id").merge(
    returns[["order_id", "reason"]], on="order_id", how="left")
df["net_sales"] = df["quantity"] * df["unit_price"] * (1 - df["discount"])
df["is_returned"] = df["reason"].notna().astype(int)
df["month"] = df["order_date"].dt.month

# ---- KPIs / findings ----------------------------------------------------
total = df["net_sales"].sum()
by_region = df.groupby("region")["net_sales"].sum().sort_values(ascending=False)
monthly = df.groupby("month")["net_sales"].sum()
festival_avg = monthly[[10, 11]].mean()
dec = monthly[12]
region_m = df.pivot_table(index="region", columns="month", values="net_sales", aggfunc="sum")
region_change = ((region_m[12] - region_m[[10, 11]].mean(axis=1))
                 / region_m[[10, 11]].mean(axis=1) * 100).round(1)
ret_cat = df.groupby("category")["is_returned"].mean().mul(100).round(2).sort_values(ascending=False)

print("Total net sales (Rs):", f"{total:,.0f}")
print("Orders:", len(df), "| Avg order value:", f"{total/len(df):,.0f}")
print("Top region:", by_region.index[0], f"{by_region.iloc[0]/total*100:.1f}% share")
print("Dec vs Oct-Nov monthly avg change (all regions): "
      f"{(dec - festival_avg) / festival_avg * 100:.1f}%")
print("Dec vs Oct-Nov change by region (%):", region_change.to_dict())
print("Return rate by category (%):", ret_cat.to_dict())
print("Overall return rate (%):", round(df['is_returned'].mean() * 100, 2))

# ---- Charts -------------------------------------------------------------
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

plt.figure(figsize=(9, 4.5))
plt.plot(months, monthly.values / 1e6, marker="o")
plt.title("Monthly net sales (Rs million)")
plt.ylabel("Rs million")
plt.tight_layout(); plt.savefig(OUT / "01_monthly_sales.png", dpi=150); plt.close()

plt.figure(figsize=(7, 4.5))
sns.barplot(x=by_region.index, y=by_region.values / 1e6, color="#2a6fb0")
plt.title("Net sales by region (Rs million)")
plt.ylabel("Rs million")
plt.tight_layout(); plt.savefig(OUT / "02_sales_by_region.png", dpi=150); plt.close()

plt.figure(figsize=(7, 4.5))
cat_sales = df.groupby("category")["net_sales"].sum().sort_values(ascending=False)
sns.barplot(x=cat_sales.values / 1e6, y=cat_sales.index, color="#2a6fb0")
plt.title("Net sales by category (Rs million)")
plt.xlabel("Rs million")
plt.tight_layout(); plt.savefig(OUT / "03_sales_by_category.png", dpi=150); plt.close()

plt.figure(figsize=(7, 4.5))
sns.barplot(x=region_change.index, y=region_change.values, color="#c0392b")
plt.title("December vs Oct-Nov monthly average sales, by region (%)")
plt.ylabel("% change")
plt.tight_layout(); plt.savefig(OUT / "04_post_festival_change.png", dpi=150); plt.close()

plt.figure(figsize=(7, 4.5))
sns.barplot(x=ret_cat.values, y=ret_cat.index, color="#e67e22")
plt.title("Return rate by category (%)")
plt.xlabel("% of orders returned")
plt.tight_layout(); plt.savefig(OUT / "05_return_rate_by_category.png", dpi=150); plt.close()

heat = region_m.copy()
heat.columns = months
plt.figure(figsize=(10, 4))
sns.heatmap(heat / 1e6, annot=True, fmt=".1f", cmap="Blues")
plt.title("Net sales by region and month (Rs million)")
plt.tight_layout(); plt.savefig(OUT / "06_region_month_heatmap.png", dpi=150); plt.close()
print("Charts saved to", OUT)

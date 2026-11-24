"""
Generates a SYNTHETIC sales dataset (3 tables) for the Sales Dashboard project.

    orders    : 25,000 rows, 12 months (2024), 5 regions
    products  : 40 products in 5 categories
    returns   : ~6% of orders

The data is synthetic (randomly generated with a festival-season pattern:
higher sales in Oct-Nov, lower in Dec). Say this clearly in your README.
Any insight you quote must come from running the SQL / dashboard on this data.

Run:
    python generate_data.py
Creates: data/orders.csv, data/products.csv, data/returns.csv
"""
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 42
N_ORDERS = 25_000
REGIONS = ["North", "South", "East", "West", "Central"]
CATEGORIES = {
    "Electronics": (3000, 60000),
    "Home & Kitchen": (500, 12000),
    "Fashion": (400, 6000),
    "Beauty": (150, 2500),
    "Sports": (300, 9000),
}
# Relative monthly demand (festival season Oct-Nov, quieter Dec)
MONTH_WEIGHT = {1: .9, 2: .85, 3: .95, 4: 1.0, 5: 1.0, 6: .95,
                7: .95, 8: 1.0, 9: 1.05, 10: 1.35, 11: 1.3, 12: .8}
REGION_WEIGHT = [.22, .20, .20, .22, .16]
RETURN_REASONS = ["Damaged", "Wrong item", "Not as described", "Changed mind", "Late delivery"]


def main():
    rng = np.random.default_rng(SEED)
    out = Path("data")
    out.mkdir(exist_ok=True)

    # ---- products -------------------------------------------------------
    rows = []
    pid = 1
    for cat, (lo, hi) in CATEGORIES.items():
        for i in range(8):
            rows.append({
                "product_id": pid,
                "product_name": f"{cat.split()[0]} Item {i + 1}",
                "category": cat,
                "unit_price": int(rng.integers(lo, hi)),
            })
            pid += 1
    products = pd.DataFrame(rows)

    # ---- orders ---------------------------------------------------------
    days = pd.date_range("2024-01-01", "2024-12-31", freq="D")
    day_w = np.array([MONTH_WEIGHT[d.month] for d in days], dtype=float)
    day_w /= day_w.sum()
    order_dates = rng.choice(days, size=N_ORDERS, p=day_w)

    orders = pd.DataFrame({
        "order_id": np.arange(100001, 100001 + N_ORDERS),
        "order_date": pd.to_datetime(order_dates).date,
        "region": rng.choice(REGIONS, size=N_ORDERS, p=REGION_WEIGHT),
        "customer_id": rng.integers(1000, 9000, size=N_ORDERS),
        "product_id": rng.choice(products["product_id"], size=N_ORDERS),
        "quantity": rng.choice([1, 2, 3, 4, 5], size=N_ORDERS, p=[.55, .25, .1, .06, .04]),
        "discount": rng.choice([0, 0.05, 0.10, 0.20], size=N_ORDERS, p=[.5, .2, .2, .1]),
    }).sort_values("order_date").reset_index(drop=True)

    # ---- returns --------------------------------------------------------
    ret = orders.sample(frac=0.06, random_state=SEED)[["order_id", "order_date"]].copy()
    ret["return_date"] = pd.to_datetime(ret["order_date"]) + pd.to_timedelta(
        rng.integers(2, 15, size=len(ret)), unit="D")
    ret["return_date"] = ret["return_date"].dt.date
    ret["reason"] = rng.choice(RETURN_REASONS, size=len(ret))
    ret = ret.drop(columns="order_date").reset_index(drop=True)
    ret.insert(0, "return_id", np.arange(1, len(ret) + 1))

    orders.to_csv(out / "orders.csv", index=False)
    products.to_csv(out / "products.csv", index=False)
    ret.to_csv(out / "returns.csv", index=False)
    print(f"orders: {len(orders):,} | products: {len(products)} | returns: {len(ret):,}")


if __name__ == "__main__":
    main()

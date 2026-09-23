import duckdb

# Step A: DuckDB se connect ho jao
con = duckdb.connect("data/cafe_analytics.duckdb")

# Step B: Gold View 1 — Revenue by Item
con.execute("""
    CREATE OR REPLACE TABLE gold_revenue_by_item AS
    SELECT 
        item,
        COUNT(*) AS total_orders,
        SUM(quantity) AS total_quantity_sold,
        SUM(price) AS total_revenue,
        ROUND(AVG(price), 2) AS avg_order_value
    FROM silver_orders
    GROUP BY item
    ORDER BY total_revenue DESC
""")

# Step C: Gold View 2 — Revenue by Location
con.execute("""
    CREATE OR REPLACE TABLE gold_revenue_by_location AS
    SELECT 
        location,
        COUNT(*) AS total_orders,
        SUM(price) AS total_revenue
    FROM silver_orders
    GROUP BY location
    ORDER BY total_revenue DESC
""")

# Step D: Gold View 3 — Daily Sales Trend
con.execute("""
    CREATE OR REPLACE TABLE gold_daily_sales AS
    SELECT 
        order_date,
        COUNT(*) AS total_orders,
        SUM(price) AS total_revenue
    FROM silver_orders
    GROUP BY order_date
    ORDER BY order_date
""")

# Step E: Verify — teeno tables ki row counts print karo
for table in ["gold_revenue_by_item", "gold_revenue_by_location", "gold_daily_sales"]:
    count = con.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
    print(f"{table}: {count} rows")

print("Done! Gold layer views created.")

con.close()
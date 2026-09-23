import duckdb
import pandas as pd

# Step A: DuckDB se connect ho jao
con = duckdb.connect("data/cafe_analytics.duckdb")

# Step B: Bronze table ko Pandas DataFrame mein uthao
df = con.execute("SELECT * FROM bronze_orders").df()

print(f"Bronze table mein total rows: {len(df)}")

# Step C: Duplicate rows hatao
# Hum sirf business columns par duplicate check karenge (metadata columns ignore karke)
business_columns = ["order_id", "customer_name", "item", "quantity", "price", "order_date", "payment_method", "location"]
before = len(df)
df = df.drop_duplicates(subset=business_columns)
after = len(df)
print(f"Duplicates removed: {before - after}")

# Step D: Missing payment_method wali rows handle karo
missing_count = df["payment_method"].isna().sum()
print(f"Missing payment_method rows found: {missing_count}")

df["payment_method"] = df["payment_method"].fillna("Unknown")

# Step E: Data types validate/fix karo
df["order_date"] = pd.to_datetime(df["order_date"]).dt.date
df["price"] = df["price"].astype(float)
df["quantity"] = df["quantity"].astype(int)

# Step F: Clean data ko silver_orders table mein save karo
con.execute("CREATE OR REPLACE TABLE silver_orders AS SELECT * FROM df")

result = con.execute("SELECT COUNT(*) FROM silver_orders").fetchone()
print(f"Done! {result[0]} clean rows saved into silver_orders table.")

con.close()
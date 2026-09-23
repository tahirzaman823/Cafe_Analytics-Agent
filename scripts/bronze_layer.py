import pandas as pd
import duckdb
from datetime import datetime

# Step A: Raw CSV file ko read karo
df = pd.read_csv("data/raw_orders.csv")

# Step B: Metadata columns add karo (Bronze layer ki pehchaan)
df["source_file"] = "raw_orders.csv"
df["load_timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Step C: DuckDB se connect ho jao (agar file exist nahi karti to ban jayegi)
con = duckdb.connect("data/cafe_analytics.duckdb")

# Step D: DataFrame ko seedha ek table mein daal do (as-is, koi cleaning nahi)
con.execute("CREATE OR REPLACE TABLE bronze_orders AS SELECT * FROM df")

# Step E: Verify karo — kitni rows gayi
result = con.execute("SELECT COUNT(*) FROM bronze_orders").fetchone()
print(f"Done! {result[0]} rows loaded into bronze_orders table.")

con.close()
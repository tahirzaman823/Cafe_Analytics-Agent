import pandas as pd
import random
from datetime import datetime, timedelta

random.seed(42)  # taake har baar same random data bane (reproducibility)

# Sample values jo humare "menu" aur customers represent karte hain
items = ["Espresso", "Cappuccino", "Latte", "Cold Brew", "Mocha", "Americano", "Croissant", "Muffin"]
item_prices = {"Espresso": 250, "Cappuccino": 350, "Latte": 380, "Cold Brew": 400,
               "Mocha": 420, "Americano": 300, "Croissant": 200, "Muffin": 220}
payment_methods = ["Cash", "Card", "JazzCash", "Easypaisa"]
locations = ["Gulshan Branch", "Clifton Branch", "DHA Branch"]
customer_names = ["Ali", "Sara", "Hamza", "Ayesha", "Bilal", "Zara", "Usman", "Mehak", "Faizan", "Noor"]

rows = []
start_date = datetime(2026, 1, 1)

for order_id in range(1, 201):  # 200 orders generate karenge
    item = random.choice(items)
    quantity = random.randint(1, 3)
    price = item_prices[item] * quantity
    order_date = start_date + timedelta(days=random.randint(0, 90))

    row = {
        "order_id": order_id,
        "customer_name": random.choice(customer_names),
        "item": item,
        "quantity": quantity,
        "price": price,
        "order_date": order_date.strftime("%Y-%m-%d"),
        "payment_method": random.choice(payment_methods),
        "location": random.choice(locations),
    }
    rows.append(row)

df = pd.DataFrame(rows)

# Jaan bujh kar thodi "messiness" daal rahe hain (real duniya jaisi)
duplicate_rows = df.sample(5, random_state=1)      # 5 duplicate orders
df = pd.concat([df, duplicate_rows], ignore_index=True)

missing_indexes = df.sample(6, random_state=2).index
df.loc[missing_indexes, "payment_method"] = None    # 6 rows mein payment method missing

df.to_csv("data/raw_orders.csv", index=False)
print(f"Done! {len(df)} rows generated and saved to data/raw_orders.csv")
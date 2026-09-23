import requests
import json

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2"

# Step A: Schema information define karo (Gold layer ki tables)
SCHEMA_INFO = """
Table: gold_revenue_by_item
Columns: item (text), total_orders (integer), total_quantity_sold (integer), total_revenue (float), avg_order_value (float)

Table: gold_revenue_by_location
Columns: location (text), total_orders (integer), total_revenue (float)

Table: gold_daily_sales
Columns: order_date (date), total_orders (integer), total_revenue (float)
"""

def generate_sql(user_question: str) -> str:
    # Step B: Prompt banao — schema + instructions + sawaal
    prompt = f"""You are a SQL expert. Given the database schema below, write ONE SQL query (DuckDB syntax) that answers the user's question.

{SCHEMA_INFO}

Rules:
- Return ONLY the SQL query, nothing else.
- No explanation, no markdown, no code fences.
- Use only the tables and columns listed above.

Question: {user_question}

SQL:"""

    # Step C: Ollama server ko HTTP request bhejo
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False
        }
    )

    # Step D: Response se SQL text nikaalo
    result = response.json()
    sql_query = result["response"].strip()

    # Step E: Agar model ne galti se markdown code fence add kar diya ho, use hata do
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    return sql_query


# Test karo
if __name__ == "__main__":
    question = "Which item made the most total revenue?"
    print(f"Question: {question}")
    sql = generate_sql(question)
    print(f"Generated SQL:\n{sql}")
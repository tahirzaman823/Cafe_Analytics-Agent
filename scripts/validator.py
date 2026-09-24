import duckdb
import os

# Ye script khud jis folder mein hai, uska absolute path nikalta hai
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Phir ek folder upar jaake "data" folder tak pahunchta hai
DEFAULT_DB_PATH = os.path.join(SCRIPT_DIR, "..", "data", "cafe_analytics.duckdb")


def validate_sql(sql_query: str, db_path: str = DEFAULT_DB_PATH) -> dict:
    """
    SQL query ko validate karta hai bina use asal mein execute kiye (dry-run).
    Return karta hai: {"is_valid": True/False, "error": None ya error message}
    """
    con = duckdb.connect(db_path)

    try:
        con.execute(f"EXPLAIN {sql_query}")
        con.close()
        return {"is_valid": True, "error": None}

    except Exception as e:
        con.close()
        return {"is_valid": False, "error": str(e)}


if __name__ == "__main__":
    valid_query = "SELECT item, total_revenue FROM gold_revenue_by_item ORDER BY total_revenue DESC LIMIT 1"
    result1 = validate_sql(valid_query)
    print("Test 1 (valid query):")
    print(result1)

    print()

    invalid_query = "SELECT item, wrong_column_name FROM gold_revenue_by_item"
    result2 = validate_sql(invalid_query)
    print("Test 2 (invalid query):")
    print(result2)
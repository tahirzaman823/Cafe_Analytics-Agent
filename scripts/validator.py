import duckdb

def validate_sql(sql_query: str, db_path: str = "data/cafe_analytics.duckdb") -> dict:
    """
    SQL query ko validate karta hai bina use asal mein execute kiye (dry-run).
    Return karta hai: {"is_valid": True/False, "error": None ya error message}
    """
    con = duckdb.connect(db_path)

    try:
        # EXPLAIN se DuckDB ko batate hain "check karo, execute mat karo"
        con.execute(f"EXPLAIN {sql_query}")
        con.close()
        return {"is_valid": True, "error": None}

    except Exception as e:
        con.close()
        return {"is_valid": False, "error": str(e)}


# Test karo — ek valid aur ek invalid query se
if __name__ == "__main__":
    # Test 1: Valid query
    valid_query = "SELECT item, total_revenue FROM gold_revenue_by_item ORDER BY total_revenue DESC LIMIT 1"
    result1 = validate_sql(valid_query)
    print("Test 1 (valid query):")
    print(result1)

    print()

    # Test 2: Invalid query (jaan bujh kar galat column naam)
    invalid_query = "SELECT item, wrong_column_name FROM gold_revenue_by_item"
    result2 = validate_sql(invalid_query)
    print("Test 2 (invalid query):")
    print(result2)
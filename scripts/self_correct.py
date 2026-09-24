import requests
from text_to_sql import SCHEMA_INFO, OLLAMA_URL, MODEL_NAME
from validator import validate_sql

MAX_ATTEMPTS = 3


def call_ollama(prompt: str) -> str:
    """Ollama ko ek prompt bhejta hai aur response text wapas deta hai."""
    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL_NAME, "prompt": prompt, "stream": False}
    )
    result = response.json()
    sql = result["response"].strip()
    sql = sql.replace("```sql", "").replace("```", "").strip()
    return sql


def generate_sql_with_self_correction(user_question: str) -> dict:
    """
    Text-to-SQL + Validation + Self-Correction, sab mila kar.
    Return karta hai: final SQL, kitne attempts lage, aur success/fail status.
    """
    # Attempt 1 ka prompt — pehli koshish, koi error context nahi
    prompt = f"""You are a SQL expert. Given the database schema below, write ONE SQL query (DuckDB syntax) that answers the user's question.

{SCHEMA_INFO}

Rules:
- Return ONLY the SQL query, nothing else.
- No explanation, no markdown, no code fences.
- Use only the tables and columns listed above.

Question: {user_question}

SQL:"""

    attempt_log = []

    for attempt_number in range(1, MAX_ATTEMPTS + 1):
        sql_query = call_ollama(prompt)
        validation = validate_sql(sql_query)

        attempt_log.append({
            "attempt": attempt_number,
            "sql": sql_query,
            "is_valid": validation["is_valid"],
            "error": validation["error"]
        })

        if validation["is_valid"]:
            return {
                "success": True,
                "final_sql": sql_query,
                "attempts_used": attempt_number,
                "log": attempt_log
            }

        # Agar invalid hai aur attempts baaki hain, to correction prompt banao
        prompt = f"""You are a SQL expert. Your previous SQL query had an error. Fix it.

{SCHEMA_INFO}

Question: {user_question}

Previous SQL you wrote:
{sql_query}

Error message received:
{validation['error']}

Rules:
- Return ONLY the corrected SQL query, nothing else.
- No explanation, no markdown, no code fences.
- Use only the tables and columns listed above.

Corrected SQL:"""

    # Agar loop khatam ho gaya aur kabhi valid nahi hua
    return {
        "success": False,
        "final_sql": None,
        "attempts_used": MAX_ATTEMPTS,
        "log": attempt_log
    }


# Test karo
if __name__ == "__main__":
    question = "What is the average order value for each item, sorted from highest to lowest?"
    result = generate_sql_with_self_correction(question)

    print(f"Question: {question}\n")
    for entry in result["log"]:
        print(f"--- Attempt {entry['attempt']} ---")
        print(f"SQL: {entry['sql']}")
        print(f"Valid: {entry['is_valid']}")
        if entry["error"]:
            print(f"Error: {entry['error'][:150]}...")
        print()

    print(f"Success: {result['success']}")
    print(f"Attempts used: {result['attempts_used']}")
    if result["success"]:
        print(f"Final SQL: {result['final_sql']}")
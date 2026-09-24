import sys
import os

# scripts/ folder ko Python ke import path mein add karo,
# taake hum text_to_sql.py, validator.py, self_correct.py import kar sakein
SCRIPT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts")
sys.path.append(SCRIPT_DIR)

from flask import Flask, render_template, request
import duckdb
from self_correct import generate_sql_with_self_correction

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "cafe_analytics.duckdb")


@app.route("/", methods=["GET", "POST"])
def home():
    result_data = None
    attempt_log = None
    error_message = None
    question = ""

    if request.method == "POST":
        question = request.form.get("question", "")

        # Step 1: Self-correction pipeline chalao (Text-to-SQL + Validate + Correct)
        sql_result = generate_sql_with_self_correction(question)
        attempt_log = sql_result["log"]

        if sql_result["success"]:
            # Step 2: Ab jo SQL valid hui, use asal mein execute karo (real result lene ke liye)
            con = duckdb.connect(DB_PATH)
            try:
                df = con.execute(sql_result["final_sql"]).df()
                result_data = {
                    "sql": sql_result["final_sql"],
                    "columns": df.columns.tolist(),
                    "rows": df.values.tolist(),
                    "attempts_used": sql_result["attempts_used"]
                }
            except Exception as e:
                error_message = f"Query valid thi lekin execute karte waqt error aayi: {e}"
            finally:
                con.close()
        else:
            error_message = f"3 attempts ke baad bhi valid SQL nahi ban payi."

    return render_template(
        "index.html",
        question=question,
        result_data=result_data,
        attempt_log=attempt_log,
        error_message=error_message
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)
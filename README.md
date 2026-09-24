# ☕ Cafe Analytics Agent

**Ask your business data questions in plain English — no SQL required.**

Cafe Analytics Agent is a small, self-contained analytics system built to demonstrate — in practice — how a self-correcting Text-to-SQL pipeline works end to end: from raw, messy transaction data all the way to a validated SQL query and a business-ready answer, surfaced through a web dashboard.

It was built as a hands-on learning project to internalize the concepts behind a larger research proposal ([FoodSQL-Agent](#background--motivation)) before scaling the same architecture up to a full food-delivery analytics system.

---

## What This Project Actually Does

Instead of a business user writing SQL to answer questions like *"Which item made the most revenue?"*, they simply type the question in plain English. Behind the scenes, the system:

1. Takes raw, unclean transaction data and turns it into trustworthy, analysis-ready tables through a layered cleaning pipeline.
2. Converts the user's natural-language question into a SQL query using a locally-run language model, guided by the database's schema.
3. Validates that query against the database *before* running it, catching mistakes early.
4. If the query is invalid, feeds the exact error back to the model and asks it to correct itself — retrying up to three times.
5. Executes the final, validated query and returns the answer, along with a full trace of every attempt it took to get there.
6. Displays all of this — the question, the correction attempts, the final SQL, and the result — on a simple web page.

The interesting part isn't the final answer — it's watching the system reason through its own mistakes and fix them.

---

## Architecture

The project follows a **Medallion Architecture**: data moves through three progressively cleaner and more useful layers, with each layer preserved separately so nothing is ever silently overwritten.

```
Raw CSV (synthetic coffee shop orders)
        │
        ▼
┌───────────────┐   Data is stored exactly as received,
│  Bronze Layer │   with source and load-time metadata attached.
└───────────────┘   Nothing is cleaned or changed here.
        │
        ▼
┌───────────────┐   Duplicates are removed, missing values are
│  Silver Layer │   handled explicitly, and data types are validated
└───────────────┘   so downstream calculations can be trusted.
        │
        ▼
┌───────────────┐   Clean data is pre-aggregated into business-ready
│  Gold Layer   │   summary views (revenue by item, by location, by day)
└───────────────┘   so questions can be answered quickly and simply.
        │
        ▼
┌─────────────────────────────────────────────┐
│  Text-to-SQL Agent (runs on the Gold layer)  │
│                                               │
│  Question → Generate SQL → Validate (dry-run)│
│      ▲                          │            │
│      └── Correct on error ──────┘            │
│          (max 3 attempts)                    │
└─────────────────────────────────────────────┘
        │
        ▼
   Flask Dashboard (question in → answer + trace out)
```

---

## Key Capabilities

- **Layered data cleaning pipeline** — raw data is never modified in place; each stage produces its own clean, inspectable output, so any step can be traced back to its source.
- **Schema-aware question answering** — the model is only ever shown the relevant table structure, keeping it focused and reducing the chance of it guessing at columns that don't exist.
- **Pre-execution query validation** — every generated query is checked with a dry-run before it ever touches real data, so nothing invalid gets executed.
- **Self-correction on failure** — when a query fails validation, the exact error is handed back to the model so it can fix its own mistake, rather than the system giving up or guessing blindly.
- **Full attempt transparency** — every retry, every error, and the final working query are all visible, not hidden behind a single "here's your answer" response.
- **Runs entirely locally** — the language model runs on-device, so there's no per-query API cost and no data leaves the machine.

---

## Project Structure

```
Cafe_Analytics-Agent/
├── data/
│   ├── raw_orders.csv          # Synthetic raw transaction data
│   └── cafe_analytics.duckdb   # Bronze / Silver / Gold tables
├── scripts/
│   ├── generate_data.py        # Creates the synthetic dataset
│   ├── bronze_layer.py         # Loads raw data as-is, with metadata
│   ├── silver_layer.py         # Cleans and validates the data
│   ├── gold_layer.py           # Builds business-ready summary tables
│   ├── text_to_sql.py          # Converts a question into SQL
│   ├── validator.py            # Dry-run validates SQL before execution
│   └── self_correct.py         # Ties generation + validation into a retry loop
├── dashboard/
│   ├── app.py                  # Flask backend
│   └── templates/
│       └── index.html          # Question box, correction trace, and results
└── README.md
```

---

## About the Data

The dataset is **synthetically generated** — it represents a fictional coffee shop with orders across three branches, eight menu items, and four payment methods. It's intentionally seeded with a small amount of realistic messiness (duplicate rows, missing payment method values) so the cleaning stage has something real to do.

| Stage | Row Count | Notes |
|---|---|---|
| Raw | 205 | Includes 5 duplicate orders, 6 rows with missing payment method |
| Cleaned (Silver) | 200 | Duplicates removed, missing values labeled `Unknown` |
| Gold summaries | 3 tables | Revenue by item, by location, and by day |

---

## Getting Started

### Prerequisites

- Python 3.10+
- [Ollama](https://ollama.com) installed and running locally
- A pulled local model (this project uses `llama3.2`)

### Setup

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd Cafe_Analytics-Agent

# 2. Create and activate an environment
conda create -n sql-agent-env python=3.10
conda activate sql-agent-env

# 3. Install dependencies
pip install pandas duckdb flask requests

# 4. Make sure Ollama is running and the model is pulled
ollama serve            # run in a separate terminal, keep it running
ollama pull llama3.2
```

### Build the Data Pipeline

Run each stage in order, from the project root:

```bash
python scripts/generate_data.py   # creates the raw dataset
python scripts/bronze_layer.py    # loads it as-is into the database
python scripts/silver_layer.py    # cleans it
python scripts/gold_layer.py      # builds the summary views
```

### Launch the Dashboard

```bash
python dashboard/app.py
```

Then open **http://127.0.0.1:5000** in your browser and ask a question.

### Example Questions (Tested)

These were run against the dashboard and confirmed to work:

1. *"Which item made the most total revenue?"*
2. *"What is the average order value for each item, sorted from highest to lowest?"*
3. *"How many total orders were placed for Latte?"*
4. *"Which item sold the lowest quantity overall?"*
5. *"Which location has the most orders?"*
6. *"What is the total revenue for the Clifton Branch?"*
7. *"Rank all locations by total revenue."*
8. *"Show me the daily sales trend."*
9. *"Which single day had the highest revenue?"*
10. *"What was the total revenue in the last 30 days of the data?"*

> Local models occasionally need one or two correction attempts on more complex questions (like #10, which involves date filtering) — that's expected, and the dashboard's correction trace shows exactly how it self-corrects.

---

## How the Self-Correction Loop Works

This is the core idea the project is built around:

1. The question and database schema are sent to the model, which generates a SQL query.
2. The query is checked with an `EXPLAIN` dry-run — it's tested for validity without being executed against real data.
3. If it's valid, it's run immediately and the result is returned.
4. If it's invalid, the exact error message is sent back to the model along with its previous attempt, and it's asked to produce a corrected query.
5. This repeats up to **3 times**. If no valid query is produced by then, the system reports failure transparently rather than returning an incorrect answer.

Every attempt — valid or not — is logged and shown on the dashboard, so the correction process itself is visible, not just the final result.

---

## Background & Motivation

This project is a simplified, practical companion to a university final-year research proposal on **self-correcting Text-to-SQL systems for food-delivery data analytics**. That larger project compares a fine-tuned small language model against a large closed model (GPT-4o) across accuracy, cost, and latency, using a Medallion data pipeline and the same generate → validate → correct loop demonstrated here — at a larger scale and with formal evaluation.

This repository exists to prove out and internalize that workflow on a small, understandable dataset before building the full-scale version.

---

## Possible Extensions

- Swap the local model for a closed API model (e.g. GPT-4o) and compare accuracy, cost, and latency.
- Add evaluation metrics: Execution Accuracy, Valid SQL Rate, Fix Rate, Average Attempts per question.
- Expand the dataset to include riders/deliveries for a food-delivery use case.
- Add authentication and multi-user support to the dashboard.
- Containerize the app with Docker for easier deployment.

---

## License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for the full text. In short: you're free to use, copy, modify, and distribute this project, including for commercial purposes, as long as the original copyright notice is kept.
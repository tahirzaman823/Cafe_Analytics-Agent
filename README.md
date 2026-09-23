# ☕ Cafe Analytics Agent

A beginner-friendly analytics system designed to demonstrate how a real-world data analytics workflow works in the background.

The project allows cafe data to move through a structured data pipeline and eventually enables users to ask questions in natural language and receive analytics results.

The main purpose is to **understand the complete workflow**, not simply build a final application.

---

## 🎯 Project Goal

The goal of **Cafe Analytics Agent** is to practically understand how different components of a modern data analytics system work together.

The project demonstrates:

- Data ingestion
- Data cleaning
- Data transformation
- Medallion Architecture
- Data storage
- SQL analytics
- Natural-language questions
- Local LLM usage
- Text-to-SQL
- SQL validation
- Self-correction
- Result generation

---

# 🔄 Overall Workflow

The planned system will follow this workflow:

```text
Cafe Data
    ↓
🥉 Bronze Layer
    ↓
🥈 Silver Layer
    ↓
🥇 Gold Layer
    ↓
DuckDB
    ↓
Natural Language Question
    ↓
Llama 3.2
    ↓
SQL Query
    ↓
SQL Validation
    ↓
Self-Correction
    ↓
Analytics Result
    ↓
User
```

---

# 🏗️ Medallion Architecture

The project uses a simplified **Medallion Architecture** consisting of three layers.

```text
             Cafe Data
                 │
                 ▼
        ┌─────────────────┐
        │  🥉 Bronze      │
        │   Raw Data      │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  🥈 Silver      │
        │  Clean Data     │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  🥇 Gold        │
        │ Analytics Data  │
        └────────┬────────┘
                 │
                 ▼
              DuckDB
```

## 🥉 Bronze Layer

The Bronze layer stores the original/raw cafe data.

Example:

```text
CSV
 ↓
Bronze
 ↓
Raw Data
```

The purpose is to preserve the source data before major transformations.

---

## 🥈 Silver Layer

The Silver layer contains cleaned and validated data.

Possible operations include:

- Removing duplicate records
- Handling basic data-quality issues
- Validating data types
- Standardizing data
- Handling missing values

Workflow:

```text
Bronze
   ↓
Cleaning & Validation
   ↓
Silver
```

---

## 🥇 Gold Layer

The Gold layer contains analytics-ready data.

For example:

```text
Cafe
Total Orders
Total Revenue
Average Order Value
Popular Products
```

The Gold layer is designed to make business analytics easier.

```text
Silver
   ↓
Business Transformation
   ↓
Gold
```

---

# 🤖 Local LLM

## Ollama

**Ollama** is used to run a language model locally on the computer.

The project uses Ollama so that the language model can be accessed from the local development environment.

---

## Llama 3.2

The `llama3.2` model has been downloaded using:

```bash
ollama pull llama3.2
```

The model will later be used to demonstrate:

```text
Natural Language
       ↓
      LLM
       ↓
      SQL
```

For example:

```text
User:
Which cafe generated the highest revenue?
```

The system will eventually use the LLM to generate an SQL query that can be validated and executed against the analytics data.

---

# 🗄️ Database & Analytics

The project will use **DuckDB** as the analytical database.

The planned workflow is:

```text
Gold Data
    ↓
DuckDB
    ↓
SQL Query
    ↓
Result
```

DuckDB will allow the system to execute analytical SQL queries on the prepared cafe data.

---

# 🔍 SQL Validation

Generated SQL should not simply be executed immediately.

The planned workflow is:

```text
Generated SQL
      ↓
SQL Validation
      ↓
Is SQL valid?
    /     \
  YES      NO
   ↓        ↓
Execute   Error
            ↓
       Correction
```

This allows the system to identify SQL problems before producing the final result.

---

# 🔁 Self-Correction

One of the main concepts demonstrated by this project is **SQL self-correction**.

The simplified workflow is:

```text
User Question
      ↓
Generate SQL
      ↓
Validate SQL
      ↓
   ┌──┴──┐
   │     │
 Valid  Invalid
   │     │
   ↓     ↓
Execute Error
         ↓
     Correction
         ↓
      New SQL
         ↓
      Validate
```

If the generated SQL contains an error, the error information can be used to generate a corrected query.

---

# 📊 Example Questions

The final system will be designed to answer questions such as:

```text
Which cafe generated the highest revenue?
```

```text
What is the total revenue?
```

```text
Which product was sold the most?
```

```text
What was the average order value?
```

```text
Which cafe had the highest number of orders?
```

These questions demonstrate how a user can interact with analytics data without manually writing SQL.

---

# 🧩 Main Components

| Component | Purpose |
|---|---|
| Python | Data processing and application logic |
| Pandas | Data cleaning and transformation |
| CSV | Initial raw data format |
| Medallion Architecture | Organizing data into Bronze, Silver, and Gold |
| Parquet | Structured data storage |
| DuckDB | Analytical SQL database |
| Ollama | Local LLM runtime |
| Llama 3.2 | Natural-language processing / SQL generation |
| SQL | Data querying |
| Validator | Checking generated SQL |
| Self-Correction | Repairing invalid SQL |
| Backend | Connecting components |
| Frontend | User interaction |

---

# 📁 Planned Project Structure

```text
cafe-analytics-agent/
│
├── data/
│   ├── raw/
│   ├── silver/
│   └── gold/
│
├── src/
│   ├── generate_data.py
│   ├── bronze.py
│   ├── silver.py
│   ├── gold.py
│   ├── database.py
│   ├── text_to_sql.py
│   ├── validator.py
│   └── correction.py
│
├── app/
│   ├── backend/
│   └── frontend/
│
├── requirements.txt
└── README.md
```

> This is the planned structure. The project will be developed gradually, one component at a time.

---

# 🖥️ Development Environment

The project is being developed using:

- Windows
- WSL (Windows Subsystem for Linux)
- Python virtual environment
- Ollama
- Llama 3.2

The Python environment and required libraries have already been prepared.

---

# 📈 Data Flow

The complete data movement will eventually look like this:

```text
Raw Cafe Data
      ↓
    Bronze
      ↓
 Data Cleaning
      ↓
    Silver
      ↓
 Data Transformation
      ↓
     Gold
      ↓
    DuckDB
      ↓
User Question
      ↓
Llama 3.2
      ↓
Generated SQL
      ↓
SQL Validation
      ↓
Self-Correction if Required
      ↓
SQL Execution
      ↓
Analytics Result
      ↓
User
```

At every stage, the project focuses on understanding:

- Where the data came from
- What format the data has
- Which component receives it
- What processing occurs
- Where the data is stored
- How the next component receives it
- How the final result reaches the user

---

# 🎓 Learning Objectives

By completing this project, the main goal is to understand:

### Data Engineering

- Raw data
- Data cleaning
- Data transformation
- Data quality
- Bronze/Silver/Gold architecture

### Databases

- Tables
- SQL
- Analytical queries
- DuckDB

### LLM

- Local LLM
- Ollama
- Llama 3.2
- Natural-language questions
- Text-to-SQL

### Application Workflow

- Frontend
- Backend
- Data processing
- Database
- Result generation

### Reliability

- SQL validation
- Error handling
- Self-correction

---

# 🚧 Current Progress

## Completed

- [x] Project concept defined
- [x] Beginner-friendly scope defined
- [x] Python environment prepared
- [x] Required libraries installed
- [x] Ollama installed
- [x] Llama 3.2 downloaded
- [x] WSL development environment selected
- [x] Medallion Architecture added

## Next Steps

- [ ] Create cafe dataset
- [ ] Create Bronze layer
- [ ] Create Silver layer
- [ ] Create Gold layer
- [ ] Connect Gold data with DuckDB
- [ ] Connect Llama 3.2 with Python
- [ ] Build Natural Language → SQL workflow
- [ ] Add SQL validation
- [ ] Add self-correction
- [ ] Build simple backend
- [ ] Build simple frontend
- [ ] Test the complete workflow

---

# 📌 Development Approach

This project will be developed **step-by-step**.

The complete application will not be built at once.

For each step:

1. Understand what we are building
2. Understand why it is required
3. Understand what happens in the background
4. Create the required folder/file
5. Write the code for that step
6. Run the code
7. Verify the output
8. Understand the result
9. Move to the next step

The main purpose is to understand the **system and data flow**, rather than simply copying code.

---

# 🚀 Future Improvements

After the basic workflow is working, the project can be expanded with:

- More cafe datasets
- More complex SQL queries
- Multiple related tables
- Better data-quality checks
- More advanced validation
- Query history
- Analytics dashboard
- Performance measurements
- More advanced local models
- Improved natural-language understanding

---

## 📌 Project Status

**Current Stage:** Environment & Architecture Setup

**Project Name:** Cafe Analytics Agent

**Main Architecture:** Medallion Architecture

**Local LLM:** Llama 3.2

**LLM Runtime:** Ollama

**Development Environment:** Windows + WSL

**Status:** 🚧 In Development

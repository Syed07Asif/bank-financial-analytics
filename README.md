# Bank Financial Analytics

A end-to-end data analyst portfolio project simulating a retail bank's customer, account, and transaction data — built to mirror how a real financial data analyst works, from infrastructure to insight.

**Stack:** PostgreSQL · Docker · Python (Faker) · Power BI

---

## Overview

This project models a fictional bank with customers, accounts, transactions, and branches. It demonstrates a full analytics pipeline:

1. A containerized PostgreSQL database (via Docker) stores the data
2. Realistic synthetic data is generated with Python, including segment-based account balances and a small percentage of flagged/anomalous transactions
3. SQL views form a semantic layer — pre-aggregated, analysis-ready data
4. Power BI connects directly to those views to build an interactive dashboard

The goal was to practice the same workflow a financial analyst uses day-to-day: schema design, data modeling, SQL analysis, and BI reporting — not just isolated queries.

## Architecture

```
Docker
 └── PostgreSQL container (bank_postgres)
       ├── Raw tables: branches, customers, accounts, transactions
       └── Views: vw_customer_segment_summary
                   vw_monthly_transaction_trend
                   vw_flagged_transactions
                   vw_branch_transaction_summary
 └── pgAdmin container (bank_pgadmin) — GUI for querying/inspecting data

Python (generate_data.py)
 └── Generates 500 customers, ~1,000 accounts, ~50,000 transactions
     with Faker + psycopg2, inserted directly into Postgres

Power BI Desktop
 └── Connects to Postgres views over localhost:5433
 └── Overview dashboard: KPI cards, segment analysis, monthly trend,
     flagged transactions, branch performance
```

## Dashboard

*(Add 1-2 screenshots of your dashboard here, e.g. `![Dashboard](screenshots/overview.png)`)*

**Includes:**
- KPI cards: total balance, customer count, account count, average balance per customer
- Average balance by customer segment (Retail / Premium / Business)
- Monthly transaction volume trend
- Flagged (high-risk) transactions table
- Top branches by transaction volume

## Data Model

4 normalized tables with foreign key relationships:

- `branches` — bank branch locations
- `customers` — customer demographics and segment (Retail/Premium/Business)
- `accounts` — linked to customers and branches; balance correlates with segment
- `transactions` — linked to accounts; ~3% randomly flagged as high-value anomalies

## SQL Views

| View | Purpose |
|---|---|
| `vw_customer_segment_summary` | Customer counts, account counts, and balances by segment |
| `vw_monthly_transaction_trend` | Transaction volume and value grouped by month |
| `vw_flagged_transactions` | Individual high-risk transactions with customer/branch context |
| `vw_branch_transaction_summary` | Transaction volume and value by branch |

Full SQL: [`schema.sql`](schema.sql) (tables) and [`views.sql`](views.sql) (views).

## Running This Project Yourself

**Requirements:** Docker Desktop, Python 3.8+, Power BI Desktop (Windows)

```bash
# 1. Start the database
docker compose up -d

# 2. Install Python dependencies
pip install faker psycopg2-binary

# 3. Apply the schema (via psql, pgAdmin, or any Postgres client)
#    Run schema.sql, then views.sql, against the bank_project database

# 4. Generate synthetic data
python generate_data.py
```

Then open `Bank-analytics.pbix` in Power BI Desktop and connect it to `localhost:5433` / `bank_project` (user: `analyst`).

> Note: the Postgres container maps to host port **5433** (not the default 5432) to avoid conflicts with any existing local Postgres installation.

## What This Project Demonstrates

- Relational schema design with proper normalization and foreign key constraints
- Synthetic/ETL data generation in Python, loaded directly into Postgres
- SQL: joins across multiple tables, aggregation, date-based grouping, view creation as a semantic layer
- Containerized infrastructure with Docker Compose (multi-service: database + admin GUI)
- BI dashboard design: KPI-first layout, consistent theming, appropriate visual choice per question (cards, bar/line charts, and a detail table for row-level inspection)

## Project Structure

```
bank-analyst-project/
├── docker-compose.yml       # Postgres + pgAdmin containers
├── schema.sql               # Table definitions
├── views.sql                # Analytical views
├── generate_data.py         # Synthetic data generation
├── finance_dark_theme.json  # Power BI custom theme
├── Bank-analytics.pbix      # Power BI dashboard file
└── README.md
``
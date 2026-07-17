import psycopg2
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

# --- Connect to Postgres running in Docker ---
# Note: from your own machine (outside Docker), we use '127.0.0.1' with port 5433
# (our host port mapping), not the internal container port 5432.
conn = psycopg2.connect(
    host="127.0.0.1",
    port=5433,
    dbname="bank_project",
    user="analyst",
    password="analyst_pw"
)
cur = conn.cursor()

# --- 1. Branches ---
branches = [
    ("Downtown Branch", "New York", "Northeast"),
    ("Uptown Branch", "New York", "Northeast"),
    ("Lakeside Branch", "Chicago", "Midwest"),
    ("Riverside Branch", "Austin", "South"),
    ("Hillview Branch", "San Francisco", "West"),
]
branch_ids = []
for name, city, region in branches:
    cur.execute(
        "INSERT INTO branches (branch_name, city, region) VALUES (%s, %s, %s) RETURNING branch_id",
        (name, city, region)
    )
    branch_ids.append(cur.fetchone()[0])

# --- 2. Customers ---
segments = ["Retail", "Premium", "Business"]
customer_ids = []
for _ in range(500):
    first = fake.first_name()
    last = fake.last_name()
    dob = fake.date_of_birth(minimum_age=18, maximum_age=80)
    join_date = fake.date_between(start_date="-5y", end_date="today")
    city = fake.city()
    segment = random.choices(segments, weights=[0.6, 0.25, 0.15])[0]  # retail most common

    cur.execute(
        """INSERT INTO customers (first_name, last_name, date_of_birth, join_date, city, segment)
           VALUES (%s, %s, %s, %s, %s, %s) RETURNING customer_id""",
        (first, last, dob, join_date, city, segment)
    )
    customer_ids.append(cur.fetchone()[0])

# --- 3. Accounts ---
# Fetch each customer's segment so balance can depend on it
cur.execute("SELECT customer_id, segment FROM customers")
customer_segments = dict(cur.fetchall())

account_ids = []
account_types = ["Checking", "Savings"]

balance_ranges = {
    "Retail": (100, 8000),
    "Premium": (5000, 40000),
    "Business": (10000, 60000),
}

for cust_id in customer_ids:
    segment = customer_segments[cust_id]
    low, high = balance_ranges[segment]

    num_accounts = random.randint(1, 3)
    for _ in range(num_accounts):
        acc_type = random.choice(account_types)
        branch_id = random.choice(branch_ids)
        open_date = fake.date_between(start_date="-5y", end_date="today")
        balance = round(random.uniform(low, high), 2)

        cur.execute(
            """INSERT INTO accounts (customer_id, branch_id, account_type, open_date, balance)
               VALUES (%s, %s, %s, %s, %s) RETURNING account_id""",
            (cust_id, branch_id, acc_type, open_date, balance)
        )
        account_ids.append(cur.fetchone()[0])

# --- 4. Transactions ---
transaction_types = ["Deposit", "Withdrawal", "Transfer", "Payment"]
channels = ["Online", "ATM", "Branch", "Mobile"]
merchant_categories = ["Groceries", "Utilities", "Entertainment", "Travel", "Restaurants", "Rent", "Salary", "Other"]

for acc_id in account_ids:
    num_transactions = random.randint(30, 70)
    for _ in range(num_transactions):
        days_ago = random.randint(0, 365)
        tx_date = datetime.now() - timedelta(days=days_ago, hours=random.randint(0, 23))

        is_flagged = random.random() < 0.03  # ~3% flagged as unusual

        if is_flagged:
            amount = round(random.uniform(5000, 20000), 2)  # unusually large
        else:
            amount = round(random.uniform(5, 800), 2)

        tx_type = random.choice(transaction_types)
        merchant = random.choice(merchant_categories)
        channel = random.choice(channels)

        cur.execute(
            """INSERT INTO transactions
               (account_id, transaction_date, amount, transaction_type, merchant_category, channel, is_flagged)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (acc_id, tx_date, amount, tx_type, merchant, channel, is_flagged)
        )

conn.commit()
cur.close()
conn.close()
print("Data generation complete.")
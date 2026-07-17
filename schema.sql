CREATE TABLE branches (
    branch_id SERIAL PRIMARY KEY,
    branch_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    region VARCHAR(100) NOT NULL
);

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    date_of_birth DATE NOT NULL,
    join_date DATE NOT NULL,
    city VARCHAR(100),
    segment VARCHAR(20) CHECK (segment IN ('Retail', 'Premium', 'Business'))
);

CREATE TABLE accounts (
    account_id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL REFERENCES customers(customer_id),
    branch_id INT NOT NULL REFERENCES branches(branch_id),
    account_type VARCHAR(20) CHECK (account_type IN ('Checking', 'Savings')),
    open_date DATE NOT NULL,
    balance NUMERIC(12,2) NOT NULL DEFAULT 0
);

CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    account_id INT NOT NULL REFERENCES accounts(account_id),
    transaction_date TIMESTAMP NOT NULL,
    amount NUMERIC(12,2) NOT NULL,
    transaction_type VARCHAR(20) CHECK (transaction_type IN ('Deposit', 'Withdrawal', 'Transfer', 'Payment')),
    merchant_category VARCHAR(50),
    channel VARCHAR(20) CHECK (channel IN ('Online', 'ATM', 'Branch', 'Mobile')),
    is_flagged BOOLEAN DEFAULT FALSE
);

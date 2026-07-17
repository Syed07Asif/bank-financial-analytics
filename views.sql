CREATE VIEW vw_customer_segment_summary AS
SELECT
    c.segment,
    COUNT(DISTINCT c.customer_id) AS num_customers,
    COUNT(a.account_id) AS num_accounts,
    ROUND(SUM(a.balance), 2) AS total_balance,
    ROUND(AVG(a.balance), 2) AS avg_balance_per_account
FROM customers c
JOIN accounts a ON c.customer_id = a.customer_id
GROUP BY c.segment;

CREATE VIEW vw_monthly_transaction_trend AS
SELECT
    DATE_TRUNC('month', transaction_date) AS month,
    COUNT(*) AS num_transactions,
    ROUND(SUM(amount), 2) AS total_amount,
    ROUND(AVG(amount), 2) AS avg_amount
FROM transactions
GROUP BY DATE_TRUNC('month', transaction_date);

CREATE VIEW vw_flagged_transactions AS
SELECT
    t.transaction_id,
    t.account_id,
    t.transaction_date,
    t.amount,
    t.transaction_type,
    t.channel,
    c.customer_id,
    c.first_name,
    c.last_name,
    c.segment,
    br.branch_name,
    br.city,
    br.region
FROM transactions t
JOIN accounts a ON t.account_id = a.account_id
JOIN customers c ON a.customer_id = c.customer_id
JOIN branches br ON a.branch_id = br.branch_id
WHERE t.is_flagged = TRUE;

CREATE VIEW vw_branch_transaction_summary AS
SELECT
    br.branch_name,
    br.city,
    br.region,
    COUNT(t.transaction_id) AS num_transactions,
    ROUND(SUM(t.amount), 2) AS total_amount
FROM transactions t
JOIN accounts a ON t.account_id = a.account_id
JOIN branches br ON a.branch_id = br.branch_id
GROUP BY br.branch_name, br.city, br.region;


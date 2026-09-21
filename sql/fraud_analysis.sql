-- ============================================================
-- FRAUD DETECTION IN FINANCIAL DATA
-- SQL ANALYSIS
-- ============================================================

USE fraud_detection;


-- ============================================================
-- 1. DATASET OVERVIEW
-- ============================================================

SELECT
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_cases,
    ROUND(
        SUM(is_fraud) * 100.0 / COUNT(*),
        2
    ) AS fraud_rate_percent
FROM transactions;


-- ============================================================
-- 2. FRAUD TRANSACTIONS BY TYPE
-- ============================================================

SELECT
    transaction_type,
    COUNT(*) AS fraud_transactions,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*)
         FROM transactions
         WHERE is_fraud = 1),
        2
    ) AS fraud_percentage
FROM transactions
WHERE is_fraud = 1
GROUP BY transaction_type
ORDER BY fraud_transactions DESC;


-- ============================================================
-- 3. FRAUD VS NON-FRAUD TRANSACTION AMOUNT
-- ============================================================

SELECT
    CASE
        WHEN is_fraud = 1 THEN 'Fraud'
        ELSE 'Non-Fraud'
    END AS transaction_category,
    COUNT(*) AS transaction_count,
    ROUND(AVG(amount), 2) AS avg_transaction_amount,
    ROUND(MAX(amount), 2) AS max_transaction_amount,
    ROUND(SUM(amount), 2) AS total_transaction_amount
FROM transactions
GROUP BY is_fraud
ORDER BY is_fraud DESC;


-- ============================================================
-- 4. SENDER BALANCE DROP > ₹50K
-- ============================================================

SELECT
    CASE
        WHEN (sender_balance_before - sender_balance_after) > 50000
        THEN 'Balance Drop > ₹50K'
        ELSE 'Balance Drop <= ₹50K'
    END AS balance_drop_category,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(
        SUM(is_fraud) * 100.0 / COUNT(*),
        2
    ) AS fraud_rate_percent
FROM transactions
GROUP BY
    CASE
        WHEN (sender_balance_before - sender_balance_after) > 50000
        THEN 'Balance Drop > ₹50K'
        ELSE 'Balance Drop <= ₹50K'
    END
ORDER BY fraud_cases DESC;


-- ============================================================
-- 5. RECIPIENT BALANCE UNCHANGED
-- ============================================================

SELECT
    CASE
        WHEN recipient_balance_before = recipient_balance_after
        THEN 'Recipient Balance Unchanged'
        ELSE 'Recipient Balance Changed'
    END AS recipient_balance_category,
    COUNT(*) AS transaction_count,
    SUM(is_fraud) AS fraud_cases,
    ROUND(
        SUM(is_fraud) * 100.0 / COUNT(*),
        2
    ) AS fraud_rate_percent
FROM transactions
GROUP BY
    CASE
        WHEN recipient_balance_before = recipient_balance_after
        THEN 'Recipient Balance Unchanged'
        ELSE 'Recipient Balance Changed'
    END
ORDER BY fraud_cases DESC;


-- ============================================================
-- 6. COMBINED FRAUD-RISK RULE
-- Recipient balance unchanged
-- AND sender balance drops by more than ₹50K
-- ============================================================

SELECT
    COUNT(*) AS flagged_transactions,
    SUM(is_fraud) AS confirmed_fraud_cases,
    ROUND(
        SUM(is_fraud) * 100.0 / COUNT(*),
        2
    ) AS fraud_rate_percent
FROM transactions
WHERE recipient_balance_before = recipient_balance_after
  AND (sender_balance_before - sender_balance_after) > 50000;


-- ============================================================
-- 7. HIGH-RISK ACCOUNTS
-- Accounts with cumulative transfers above ₹10M
-- ============================================================

SELECT
    sender_account_id,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_cases,
    ROUND(SUM(amount), 2) AS total_transfer_amount
FROM transactions
WHERE transaction_type = 'TRANSFER'
GROUP BY sender_account_id
HAVING SUM(amount) > 10000000
ORDER BY total_transfer_amount DESC;


-- ============================================================
-- 8. HIGH-RISK ACCOUNTS WITH FRAUD CASES
-- ============================================================

SELECT
    sender_account_id,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_cases,
    ROUND(SUM(amount), 2) AS total_transfer_amount
FROM transactions
GROUP BY sender_account_id
HAVING SUM(amount) > 10000000
ORDER BY total_transfer_amount DESC;

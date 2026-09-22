# Fraud Detection in Financial Data | SQL

## 📌 Project Overview

This project analyzes 6.1 million simulated financial transactions using SQL to identify fraudulent transaction patterns and high-risk accounts.

The analysis focuses on transaction behavior, sender balance changes, recipient balance behavior, fraud concentration, and cumulative transaction values at the account level.

---

## 🎯 Business Objective

The objective is to identify suspicious transaction patterns that can be used as transaction-monitoring rules in a fintech environment.

Key areas analyzed:

- Fraud transaction volume and rate
- Fraud patterns by transaction type
- Transaction amount differences between fraud and non-fraud cases
- Large sender balance drops
- Unchanged recipient balances
- Combined fraud-risk indicators
- High-risk accounts with cumulative transfers above ₹10M

---

## 📊 Dataset

The project uses a synthetically generated dataset containing:

| Metric | Value |
|---|---:|
| Total Transactions | 6,100,000 |
| Fraud Cases | 7,985 |
| Fraud Rate | 0.13% |
| Dataset Period | 2025 |
| Number of Columns | 11 |

### Main Columns

- `transaction_id`
- `transaction_date`
- `sender_account_id`
- `recipient_account_id`
- `transaction_type`
- `amount`
- `sender_balance_before`
- `sender_balance_after`
- `recipient_balance_before`
- `recipient_balance_after`
- `is_fraud`

---

## 🔍 Key Fraud Indicators

### 1. Recipient Balance Unchanged

Transactions where:


recipient_balance_before = recipient_balance_after

were investigated as a suspicious pattern.

---

### 2. Sender Balance Drop > ₹50K

Transactions where:


sender_balance_before - sender_balance_after > 50000

were analyzed as another risk indicator.

---

### 3. Combined Fraud-Risk Rule

A transaction was flagged when both conditions were satisfied:


Recipient balance unchanged
AND
Sender balance drop > ₹50,000

---

## 💰 High-Risk Accounts

Sender accounts with cumulative transaction values above ₹10M were identified using account-level aggregation.

The analysis identified five high-volume accounts exceeding the ₹10M monitoring threshold.

These accounts were further analyzed for:

- Transaction volume
- Cumulative transfer value
- Fraud cases

High transaction volume or cumulative value is treated as a **risk indicator for monitoring**, not automatic proof of fraud.

---

## 📈 Key Findings

### Fraud Volume

- 7,985 fraudulent transactions were identified out of 6.1 million transactions.
- Overall simulated fraud rate was 0.13%.

### Transaction Type

Fraudulent transactions were:

- TRANSFER: 5,582 cases (69.91%)
- CASH_OUT: 2,403 cases (30.09%)

### Transaction Amount

Average transaction amount:

- Fraud: ₹149,532
- Non-Fraud: ₹16,667

### Balance Drop

Among transactions with sender balance drops above ₹50K:

- 339,605 transactions were identified.
- 7,985 were fraudulent.
- Fraud rate was 2.35%.

---

## 🛠️ Tech Stack

- **MySQL** — SQL analysis and aggregation
- **Python** — Synthetic dataset generation
- **Pandas** — Data generation and validation
- **NumPy** — Randomized transaction generation
- **VS Code** — Development environment
- **Git & GitHub** — Version control

---

## 📌 Business Monitoring Rules

| Rule | Purpose |
|---|---|
| Recipient balance unchanged | Identify unusual balance behavior |
| Sender balance drop > ₹50K | Detect large balance movements |
| Both conditions satisfied | Flag high-risk transactions |
| Cumulative transfers > ₹10M | Identify high-volume accounts |

These rules are intended as **risk-screening indicators** that could be combined with additional signals in a production fraud-monitoring system.

---

## 👨‍💻 Author

**Nitin Pal**

B.Tech — Chemical Engineering  
Delhi Technological University

Skills demonstrated:

`SQL` `MySQL` `Python` `Pandas` `NumPy` `Data Analytics` `Fraud Analytics`

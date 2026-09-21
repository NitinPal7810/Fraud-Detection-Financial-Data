import os
import numpy as np
import pandas as pd

# ============================================================
# FRAUD DETECTION FINANCIAL DATASET GENERATOR
# ============================================================

np.random.seed(42)

# Dataset configuration
TOTAL_TRANSACTIONS = 6_100_000
FRAUD_TRANSACTIONS = 7_985
CHUNK_SIZE = 100_000

OUTPUT_DIR = "data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "transactions.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Remove old CSV if it exists
if os.path.exists(OUTPUT_FILE):
    os.remove(OUTPUT_FILE)

print("=" * 60)
print("FRAUD DETECTION DATASET GENERATION")
print("=" * 60)
print(f"Total transactions : {TOTAL_TRANSACTIONS:,}")
print(f"Fraud transactions : {FRAUD_TRANSACTIONS:,}")
print(f"Output file        : {OUTPUT_FILE}")
print("=" * 60)

# ------------------------------------------------------------
# Select exact fraud transaction positions
# ------------------------------------------------------------

fraud_positions = np.random.choice(
    TOTAL_TRANSACTIONS,
    size=FRAUD_TRANSACTIONS,
    replace=False
)

fraud_positions.sort()

# ------------------------------------------------------------
# High-risk accounts
# These accounts will receive enough TRANSFER transactions
# to cross ₹10M cumulative transfer value.
# ------------------------------------------------------------

high_risk_accounts = np.array([
    199991,
    199992,
    199993,
    199994,
    199995
])

# ------------------------------------------------------------
# Generate data in chunks
# ------------------------------------------------------------

header_written = False

for start in range(0, TOTAL_TRANSACTIONS, CHUNK_SIZE):

    end = min(start + CHUNK_SIZE, TOTAL_TRANSACTIONS)

    size = end - start

    global_positions = np.arange(start, end)

    # --------------------------------------------------------
    # Transaction IDs
    # --------------------------------------------------------

    transaction_ids = np.arange(start + 1, end + 1)

    # --------------------------------------------------------
    # Account IDs
    # --------------------------------------------------------

    sender_accounts = np.random.randint(
        100001,
        200001,
        size=size
    )

    recipient_accounts = np.random.randint(
        200001,
        300001,
        size=size
    )

    # --------------------------------------------------------
    # Force some transactions to high-risk accounts
    # --------------------------------------------------------

    high_risk_mask = np.random.rand(size) < 0.002

    high_risk_count = high_risk_mask.sum()

    if high_risk_count > 0:

        sender_accounts[high_risk_mask] = np.random.choice(
            high_risk_accounts,
            size=high_risk_count
        )

    # --------------------------------------------------------
    # Transaction types
    # --------------------------------------------------------

    transaction_types = np.random.choice(
        ["TRANSFER", "PAYMENT", "CASH_OUT", "DEPOSIT"],
        size=size,
        p=[0.40, 0.30, 0.20, 0.10]
    )

    # High-risk accounts should primarily perform TRANSFERs
    transaction_types[high_risk_mask] = "TRANSFER"

    # --------------------------------------------------------
    # Transaction amounts
    # --------------------------------------------------------

    amounts = np.random.lognormal(
        mean=9.2,
        sigma=1.0,
        size=size
    )

    amounts = np.clip(
        amounts,
        100,
        500000
    )

    amounts = np.round(
        amounts,
        2
    )

    # Give high-risk accounts larger transfer amounts
    # so cumulative value exceeds ₹10M.
    if high_risk_count > 0:

        high_risk_amounts = np.random.uniform(
            100000,
            300000,
            size=high_risk_count
        )

        amounts[high_risk_mask] = np.round(
            high_risk_amounts,
            2
        )

    # --------------------------------------------------------
    # Sender balances
    # --------------------------------------------------------

    sender_balance_before = np.random.uniform(
        5000,
        3000000,
        size=size
    )

    sender_balance_before = np.round(
        sender_balance_before,
        2
    )

    sender_balance_after = (
        sender_balance_before - amounts
    )

    # Prevent negative balances
    negative_mask = sender_balance_after < 0

    sender_balance_before[negative_mask] = (
        amounts[negative_mask]
        + np.random.uniform(
            1000,
            100000,
            size=negative_mask.sum()
        )
    )

    sender_balance_before = np.round(
        sender_balance_before,
        2
    )

    sender_balance_after = np.round(
        sender_balance_before - amounts,
        2
    )

    # --------------------------------------------------------
    # Recipient balances
    # --------------------------------------------------------

    recipient_balance_before = np.random.uniform(
        5000,
        3000000,
        size=size
    )

    recipient_balance_before = np.round(
        recipient_balance_before,
        2
    )

    recipient_balance_after = np.round(
        recipient_balance_before + amounts,
        2
    )

    # --------------------------------------------------------
    # Fraud flag
    # --------------------------------------------------------

    is_fraud = np.zeros(
        size,
        dtype=np.int8
    )

    fraud_mask = np.isin(
        global_positions,
        fraud_positions
    )

    is_fraud[fraud_mask] = 1

    # --------------------------------------------------------
    # Deliberate fraud patterns
    #
    # Pattern 1:
    # Recipient balance remains unchanged
    #
    # Pattern 2:
    # Sender balance drops by more than ₹50,000
    # --------------------------------------------------------

    fraud_count_chunk = fraud_mask.sum()

    if fraud_count_chunk > 0:

        fraud_amounts = np.random.uniform(
            50001,
            250000,
            size=fraud_count_chunk
        )

        fraud_amounts = np.round(
            fraud_amounts,
            2
        )

        amounts[fraud_mask] = fraud_amounts

        # Sender balance deliberately drops significantly
        fraud_sender_before = (
            fraud_amounts
            + np.random.uniform(
                50000,
                500000,
                size=fraud_count_chunk
            )
        )

        fraud_sender_before = np.round(
            fraud_sender_before,
            2
        )

        sender_balance_before[fraud_mask] = (
            fraud_sender_before
        )

        sender_balance_after[fraud_mask] = np.round(
            fraud_sender_before - fraud_amounts,
            2
        )

        # Recipient balance intentionally unchanged
        fraud_recipient_before = np.random.uniform(
            50000,
            2000000,
            size=fraud_count_chunk
        )

        fraud_recipient_before = np.round(
            fraud_recipient_before,
            2
        )

        recipient_balance_before[fraud_mask] = (
            fraud_recipient_before
        )

        recipient_balance_after[fraud_mask] = (
            fraud_recipient_before
        )

        # Fraud transactions mostly TRANSFER / CASH_OUT
        fraud_types = np.random.choice(
            ["TRANSFER", "CASH_OUT"],
            size=fraud_count_chunk,
            p=[0.70, 0.30]
        )

        transaction_types[fraud_mask] = fraud_types

    # --------------------------------------------------------
    # Transaction dates
    # --------------------------------------------------------

    dates = pd.date_range(
        start="2025-01-01",
        periods=365,
        freq="D"
    )

    transaction_dates = np.random.choice(
        dates,
        size=size
    )

    transaction_dates = pd.to_datetime(
        transaction_dates
    ).strftime("%Y-%m-%d")

    # --------------------------------------------------------
    # Create DataFrame
    # --------------------------------------------------------

    df = pd.DataFrame({
        "transaction_id": transaction_ids,
        "transaction_date": transaction_dates,
        "sender_account_id": sender_accounts,
        "recipient_account_id": recipient_accounts,
        "transaction_type": transaction_types,
        "amount": amounts,
        "sender_balance_before": sender_balance_before,
        "sender_balance_after": sender_balance_after,
        "recipient_balance_before": recipient_balance_before,
        "recipient_balance_after": recipient_balance_after,
        "is_fraud": is_fraud
    })

    # --------------------------------------------------------
    # Save chunk
    # --------------------------------------------------------

    df.to_csv(
        OUTPUT_FILE,
        mode="a",
        index=False,
        header=not header_written
    )

    header_written = True

    processed = end

    print(
        f"Generated {processed:,} / "
        f"{TOTAL_TRANSACTIONS:,} transactions"
    )

# ============================================================
# FINAL VERIFICATION
# ============================================================

print("\n" + "=" * 60)
print("DATASET GENERATION COMPLETE")
print("=" * 60)

fraud_total = 0
total_rows = 0

for chunk in pd.read_csv(
    OUTPUT_FILE,
    usecols=["is_fraud"],
    chunksize=200_000
):
    total_rows += len(chunk)
    fraud_total += int(
        chunk["is_fraud"].sum()
    )

fraud_rate = (
    fraud_total / total_rows
) * 100

print(f"Total rows        : {total_rows:,}")
print(f"Fraud cases       : {fraud_total:,}")
print(f"Fraud rate        : {fraud_rate:.2f}%")
print(f"File created      : {OUTPUT_FILE}")
print("=" * 60)


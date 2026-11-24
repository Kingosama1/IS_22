
import pandas as pd


def load_transactions_from_excel(file_path):
    # Step 1: Read the Excel file
    df = pd.read_excel(file_path)

    # Normalize column names
    df.columns = df.columns.astype(str).str.strip().str.lower()

    # Check that the required column exists
    if "items" not in df.columns:
        raise ValueError("Excel file must contain an 'items' column")

    transactions = []
    transaction_ids = []

    # Step 2: Read transactions row by row
    for index, row in df.iterrows():

        tid = row["tid"] if "tid" in df.columns else index + 1
        raw_items = row["items"]

        # Skip empty rows
        if pd.isna(raw_items):
            continue

        # Step 3: Clean the items string
        items_string = str(raw_items).strip()

        # Remove surrounding quotes and brackets
        items_string = items_string.strip('"').strip("'")
        items_string = items_string.strip("{}[]")

        # Step 4: Split items
        items = [
            item.strip().strip('"').strip("'")
            for item in items_string.split(",")
            if item.strip()
        ]

        # Step 5: Store transaction
        if items:
            transactions.append(items)
            transaction_ids.append(tid)

    return transactions, transaction_ids


# Main execution
if __name__ == "__main__":

    transactions, transaction_ids = load_transactions_from_excel(
        "Horizontal_Format.xlsx"
    )

    print("Transactions loaded successfully!")
    print("Total Transactions:", len(transactions))

    print("\nFirst 5 Transactions:")

    for tid, transaction in zip(
        transaction_ids[:5],
        transactions[:5]
    ):
        print(tid, transaction)

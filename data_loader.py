import pandas as pd

def load_transactions_from_excel():
    df = pd.read_excel("Horizontal_Format_8_Transactions.xlsx")
    df.columns = df.columns.astype(str).str.strip().str.lower()
    transactions = []
    transaction_ids = []
    for index, row in df.iterrows():
        tid = row["tid"]
        rawItems = row["items"]
        if pd.isna(rawItems):
            continue
        items_string = str(rawItems)
        items_string = items_string.strip('"').strip("'")
        items = [
            item.strip().strip('"').strip("'")
            for item in items_string.split(",")
            if item.strip()
        ]
        if items:
            transactions.append(items)
            transaction_ids.append(tid)
    return transactions, transaction_ids

#transactions, transaction_ids = load_transactions_from_excel()
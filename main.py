from data_loader import load_transactions_from_excel

def main():
    transactions, transaction_ids = load_transactions_from_excel()
#Display transactions
    print("Transactions:")
    print(transactions)
    print("\nTransaction IDs:")
    print(transaction_ids)

if __name__ == "__main__":
    main()
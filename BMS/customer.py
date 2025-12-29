from file_handler import read_accounts, STATEMENTS_FILE
import os


# ---------- VIEW ACCOUNT DETAILS ----------

def view_account(user_id):
    accounts = read_accounts()

    for acc in accounts:
        if acc["user_id"] == user_id:
            print("\n--- Account Details ---")
            print(f"Account No   : {acc['account_no']}")
            print(f"Name         : {acc['name']}")
            print(f"Account Type : {acc['account_type']}")
            print(f"Balance      : ₹{acc['balance']}")
            print(f"Status       : {acc['status']}")
            return acc["account_no"]

    print("❌ Account not found")
    return None


# ---------- CHECK BALANCE ----------

def check_balance(user_id):
    accounts = read_accounts()

    for acc in accounts:
        if acc["user_id"] == user_id:
            print(f"\n💰 Available Balance: ₹{acc['balance']}")
            return

    print("❌ Account not found")


# ---------- VIEW BANK STATEMENT ----------

def view_statement(account_no):
    print("\n--- Bank Statement ---")

    if not os.path.exists(STATEMENTS_FILE):
        print("No transactions found")
        return

    found = False
    with open(STATEMENTS_FILE, "r") as file:
        for line in file:
            data = line.strip().split(",")
            if data[1] == account_no:
                found = True
                print(
                    f"TxnID: {data[0]} | "
                    f"Type: {data[2]} | "
                    f"Amount: ₹{data[3]} | "
                    f"Date: {data[4]} | "
                    f"Balance: ₹{data[5]}"
                )

    if not found:
        print("No transactions for this account")

from file_handler import read_accounts, write_accounts, log_activity,  LOGS_FILE
import os


# ---------- CREATE NEW ACCOUNT ----------

def create_account():
    print("\n--- Create New Account ---")

    name = input("Enter Customer Name: ")
    user_id = input("Create User ID: ")
    pin = input("Create PIN: ")
    account_type = input("Account Type (Savings/Current): ")
    balance = float(input("Initial Deposit Amount: "))

    accounts = read_accounts()

    # Generate account number
    if accounts:
        last_acc_no = int(accounts[-1]["account_no"])
        account_no = str(last_acc_no + 1)
    else:
        account_no = "1001"

    # Check unique user_id
    for acc in accounts:
        if acc["user_id"] == user_id:
            print("❌ User ID already exists")
            return

    new_account = {
        "account_no": account_no,
        "name": name,
        "user_id": user_id,
        "pin": pin,
        "account_type": account_type,
        "balance": balance,
        "status": "Active"
    }

    accounts.append(new_account)
    write_accounts(accounts)

    log_activity("admin", "Admin", f"Created Account {account_no}")
    print(f"✅ Account created successfully. Account No: {account_no}")


# ---------- VIEW ALL ACCOUNTS ----------

def view_accounts():
    print("\n--- All Bank Accounts ---")
    accounts = read_accounts()

    if not accounts:
        print("No accounts found.")
        return

    for acc in accounts:
        print(
            f"Acc No: {acc['account_no']} | "
            f"Name: {acc['name']} | "
            f"User ID: {acc['user_id']} | "
            f"Type: {acc['account_type']} | "
            f"Balance: ₹{acc['balance']} | "
            f"Status: {acc['status']}"
        )


# ---------- ACTIVATE / DEACTIVATE ACCOUNT ----------

def change_account_status():
    print("\n--- Change Account Status ---")
    account_no = input("Enter Account Number: ")

    accounts = read_accounts()
    found = False

    for acc in accounts:
        if acc["account_no"] == account_no:
            found = True
            print(f"Current Status: {acc['status']}")

            if acc["balance"] <= 0:
                deposit_needed = input("Account has negative balance. Deposit required to activate. Proceed? (y/n): ")
                if deposit_needed.lower() != 'y':
                    print("❌ Operation cancelled")
                    return 
                else:
                    amount = float(input("Enter deposit amount: "))
                    acc["balance"] += amount
                    print(f"✅ Deposited ₹{amount}. New Balance: ₹{acc['balance']}")
                    new_status = "Active"
            else:
                new_status = input("Enter New Status (Active/Inactive): ")

            if new_status not in ["Active", "Inactive"]:
                print("❌ Invalid status")
                return

            acc["status"] = new_status
            write_accounts(accounts)
            log_activity("admin", "Admin", f"Changed status of {account_no} to {new_status}")
            print("✅ Account status updated")
            return

    if not found:
        print("❌ Account not found")


# ---------- VIEW LOGS ----------

def view_logs():
    print("\n--- System Logs ---")
    if not os.path.exists(LOGS_FILE):
        print("No logs available")
        return

    with open(LOGS_FILE, "r") as file:
        for line in file:
            print(line.strip())

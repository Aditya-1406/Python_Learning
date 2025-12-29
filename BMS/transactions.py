from file_handler import read_accounts, write_accounts, add_statement, log_activity


# ---------- DEPOSIT ----------

def deposit(account_no, amount):
    if amount <= 0:
        print("❌ Invalid deposit amount")
        return

    accounts = read_accounts()

    for acc in accounts:
        if acc["account_no"] == account_no and acc["status"] == "Active":
            acc["balance"] += amount
            write_accounts(accounts)

            add_statement(account_no, "Deposit", amount, acc["balance"])
            log_activity(acc["user_id"], "Customer", f"Deposited {amount}")

            print(f"✅ Deposit successful. New Balance: ₹{acc['balance']}")
            return

    print("❌ Account not found or inactive")


# ---------- WITHDRAW ----------

def withdraw(account_no, amount):
    if amount <= 0:
        print("❌ Invalid withdrawal amount")
        return

    accounts = read_accounts()

    for acc in accounts:
        if acc["account_no"] == account_no and acc["status"] == "Active":
            if acc["balance"] < amount:
                print("❌ Insufficient balance")
                return

            acc["balance"] -= amount
            write_accounts(accounts)

            add_statement(account_no, "Withdraw", amount, acc["balance"])
            log_activity(acc["user_id"], "Customer", f"Withdrew {amount}")

            print(f"✅ Withdrawal successful. New Balance: ₹{acc['balance']}")
            return

    print("❌ Account not found or inactive")


# ---------- TRANSFER ----------

def transfer(from_acc_no, to_acc_no, amount):
    if amount <= 0:
        print("❌ Invalid transfer amount")
        return

    accounts = read_accounts()
    sender = receiver = None

    for acc in accounts:
        if acc["account_no"] == from_acc_no:
            sender = acc
        if acc["account_no"] == to_acc_no:
            receiver = acc

    if not sender or not receiver:
        print("❌ One or both accounts not found")
        return

    if sender["status"] != "Active" or receiver["status"] != "Active":
        print("❌ One or both accounts are inactive")
        return

    if sender["balance"] < amount:
        print("❌ Insufficient balance")
        return

    sender["balance"] -= amount
    receiver["balance"] += amount
    write_accounts(accounts)

    add_statement(from_acc_no, "Transfer Out", amount, sender["balance"])
    add_statement(to_acc_no, "Transfer In", amount, receiver["balance"])

    log_activity(sender["user_id"], "Customer", f"Transferred {amount} to {to_acc_no}")

    print("✅ Transfer successful")

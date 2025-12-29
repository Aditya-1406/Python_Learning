import os
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# Ensure data directory exists
os.makedirs(DATA_DIR, exist_ok=True)



ACCOUNTS_FILE = os.path.join(DATA_DIR, "accounts.txt")
LOGS_FILE = os.path.join(DATA_DIR, "logs.txt")
STATEMENTS_FILE = os.path.join(DATA_DIR, "statements.txt")


# ---------- ACCOUNTS ----------

def read_accounts():
    accounts = []
    if not os.path.exists(ACCOUNTS_FILE):
        return accounts

    with open(ACCOUNTS_FILE, "r") as file:
        for line in file:
            line = line.strip()
            if line:
                data = line.split(",")
                accounts.append({
                    "account_no": data[0],
                    "name": data[1],
                    "user_id": data[2],
                    "pin": data[3],
                    "account_type": data[4],
                    "balance": float(data[5]),
                    "status": data[6]
                })
    return accounts


def write_accounts(accounts):
    with open(ACCOUNTS_FILE, "w") as file:
        for acc in accounts:
            line = f"{acc['account_no']},{acc['name']},{acc['user_id']},{acc['pin']}," \
                   f"{acc['account_type']},{acc['balance']},{acc['status']}\n"
            file.write(line)


# ---------- LOGS ----------

def log_activity(user_id, role, action):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOGS_FILE, "a") as file:
        file.write(f"{timestamp},{user_id},{role},{action}\n")


# ---------- STATEMENTS ----------

def generate_transaction_id():
    return "TXN" + datetime.now().strftime("%Y%m%d%H%M%S")


def add_statement(account_no, txn_type, amount, balance):
    txn_id = generate_transaction_id()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(STATEMENTS_FILE, "a") as file:
        file.write(f"{txn_id},{account_no},{txn_type},{amount},{timestamp},{balance}\n")

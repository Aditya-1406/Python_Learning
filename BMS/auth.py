from getpass import getpass
from file_handler import read_accounts, log_activity

# Hardcoded Admin Credentials
ADMIN_USER = "admin"
ADMIN_PIN = "admin123"


# ---------- ADMIN LOGIN ----------

def admin_login():
    print("\n--- Admin Login ---")
    user_id = input("Enter Admin ID: ")
    pin = getpass("Enter Admin PIN: ")

    if user_id == ADMIN_USER and pin == ADMIN_PIN:
        log_activity(user_id, "Admin", "Login Success")
        print("✅ Admin login successful")
        return True
    else:
        log_activity(user_id, "Admin", "Login Failed")
        print("❌ Invalid admin credentials")
        return False


# ---------- CUSTOMER LOGIN ----------

def customer_login():
    print("\n--- Customer Login ---")
    user_id = input("Enter User ID: ")
    pin = getpass("Enter PIN: ")

    accounts = read_accounts()

    for acc in accounts:
        if acc["user_id"] == user_id and acc["pin"] == pin:
            if acc["status"] != "Active":
                log_activity(user_id, "Customer", "Login Failed - Inactive Account")
                print("❌ Account is inactive. Contact admin.")
                return None

            log_activity(user_id, "Customer", "Login Success")
            print("✅ Customer login successful")
            return acc  # return customer account data

    log_activity(user_id, "Customer", "Login Failed")
    print("❌ Invalid user ID or PIN")
    return None

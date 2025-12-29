from auth import admin_login, customer_login
from admin import create_account, view_accounts, change_account_status, view_logs
from customer import view_account, check_balance, view_statement
from transactions import deposit, withdraw, transfer


def admin_menu():
    while True:
        print("""
        ===== ADMIN MENU =====
        1. Create New Account
        2. View All Accounts
        3. Activate / Deactivate Account
        4. View Logs
        5. Logout
        """)

        choice = input("Enter choice: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            view_accounts()
        elif choice == "3":
            change_account_status()
        elif choice == "4":
            view_logs()
        elif choice == "5":
            print("🔒 Admin logged out")
            break
        else:
            print("❌ Invalid choice")


def customer_menu(account):
    user_id = account["user_id"]
    account_no = account["account_no"]

    while True:
        print("""
        ===== CUSTOMER MENU =====
        1. View Account Details
        2. Check Balance
        3. Deposit Money
        4. Withdraw Money
        5. Transfer Money
        6. View Bank Statement
        7. Logout
        """)

        choice = input("Enter choice: ")

        if choice == "1":
            view_account(user_id)

        elif choice == "2":
            check_balance(user_id)

        elif choice == "3":
            amount = float(input("Enter deposit amount: "))
            deposit(account_no, amount)

        elif choice == "4":
            amount = float(input("Enter withdrawal amount: "))
            withdraw(account_no, amount)

        elif choice == "5":
            to_acc = input("Enter receiver account number: ")
            amount = float(input("Enter transfer amount: "))
            transfer(account_no, to_acc, amount)

        elif choice == "6":
            view_statement(account_no)

        elif choice == "7":
            print("🔒 Customer logged out")
            break

        else:
            print("❌ Invalid choice")


def main():
    while True:
        print("""
        ===== BANK MANAGEMENT SYSTEM =====
        1. Admin Login
        2. Customer Login
        3. Exit
        """)

        choice = input("Enter choice: ")

        if choice == "1":
            if admin_login():
                admin_menu()

        elif choice == "2":
            account = customer_login()
            if account:
                customer_menu(account)

        elif choice == "3":
            print("🙏 Thank you for using Bank Management System")
            break

        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    main()

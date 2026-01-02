from services import *
from auth import *
from admin import *
from member import *
from getpass import getpass

def admin_interface():
    user_id = int(input("Enter Admin ID: "))
    password = getpass("Enter Admin Password: ")
    if not check_admin(user_id, password):
        return

    while True:
        print("\n=== Admin Interface ===")
        print("1. Member Menu")
        print("2. Book Menu")
        print("3. Loan Menu")
        print("4. Exit Admin Interface")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            member_menu()
        elif choice == '2':
            book_menu()
        elif choice == '3':
            loan_menu()
        elif choice == '4':
            break

def member_interface():
    user_id = int(input("Enter Member ID: "))
    password = getpass("Enter Member Password: ")
    if not check_member(user_id, password):
        return

    while True:
        print("\n=== Member Interface ===")
        print("1. Self Menu")
        print("2. Book Menu")
        print("3. Loan Menu")
        print("4. Exit Member Interface")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            self_menu(user_id)
        elif choice == '2':
            book_menu_mm()
        elif choice == '3':
            loan_menu_mm(user_id)
        elif choice == '4':
            break


def main():
    while True:
        print("\n=== Library Management System ===")
        print("1. Admin Login")
        print("2. Member Login")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            admin_interface()
        elif choice == '2':
            member_interface()
        elif choice == '3':
            print("Exiting the system. Goodbye!")
            conn.close()
            break

if __name__ == "__main__":
    main()




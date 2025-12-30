from services import *

def self_menu(member_id):
    while True:
        print("\n--- Member Menu ---")
        print("1. View My Details")
        print("2. Go Back")
        choice = input("Enter your choice (1-2): ").strip()
        if choice == '1':
            get_member(member_id)
        elif choice == '2':
            break

def book_menu_mm():
    while True:
        print("\n--- Book Menu ---")
        print("1. List Books")
        print("2. Search Book")
        print("3. Go Back")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            list_books()
        elif choice == '2':
            get_book()
        elif choice == '3':
            break

def loan_menu_mm(member_id):
    while True:
        print("\n--- Loan Menu ---")
        print("1. List My Loans")
        print("2. Go Back")

        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            list_loan_byid(member_id)
        elif choice == '2':
            break
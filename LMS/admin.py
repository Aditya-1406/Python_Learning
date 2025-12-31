from services import *




def member_menu():

    while True:
        print("\n--- Member Menu ---")
        print("1. Create new Account")
        print("2. Member List")
        print("3. Search Account")
        print("4. Delete Account")
        print("5. Go Back")

        choice = input("Enter your choice (1-5): ").strip() 

        if choice == '1':
                add_member()
        elif choice == '2':
                list_members()
        elif choice == '3':
                member_id = int(input("Enter member ID to fetch: "))
                get_member(member_id)
        elif choice == '4':
                remove_member()
        elif choice == '5':
            break

def book_menu():
    while True:
        print("\n--- Book Menu ---")
        print("1. Add Book")
        print("2. List Books")
        print("3. Search Book")
        print("4. Delete Book")
        print("5. Update Book")
        print("6. Go Back")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            add_book()
        elif choice == '2':
            list_books()
        elif choice == '3':
            get_book()
        elif choice == '4':
            remove_book()
        elif choice == '5':
            update_book_copies_admin()
        elif choice == '6':
            break

def loan_menu():
    while True:
        print("\n--- Loan Menu ---")
        print("1. Create Loan")
        print("2. List Loans")
        print("3. List Loans by id")
        print("4. Returned book")
        print("5. Delete Loan")
        print("6. Go Back")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            create_loan_admin()
        elif choice == '2':
            list_all_loans_admin()
        elif choice == '3':
            member_id = int(input("Enter member Id to fetch: "))
            list_loan_byid(member_id)
        elif choice == '4':
            mark_loan_returned_admin()
        elif choice == '5':
            delete_loan_admin()
        elif choice == '6':
            break

        
from datetime import datetime, timedelta
from repo import *
from Logs import *
from Error import InvalidPass
import re 


pattern = '^(?=.*[A-Za-z0-9])(?=.*[^A-Za-z0-9]).{8,}$'




#for the members
def add_member():
    """Add a new member (admin only). Returns the new member_id."""
    name = input("Enter member name: ").strip().capitalize()
    email = input("Enter member email: ").strip().lower()
    try:
        password = input("Enter member password: ").strip()
        if ((re.match(pattern,password))== None):
            raise InvalidPass
    except InvalidPass as e:
        print("Password must contain minimum 8 letter, a special symbol, digit and letters")
        return None
    
    

    role = input("Enter member role (member/admin): ").strip().lower()

    try:
        member_id = create_member(name, email, password, role)
        print(f"✅ Member added with ID: {member_id}")
        member_log_create(name, email, password, role,member_id)
        return member_id
    except ValueError as e:
        print(f"❌ Error adding member: {e}")
        return None

def remove_member():
    """Remove a member by id (admin only)."""
    try:
        member_id = int(input("Enter member ID to delete: "))
    except ValueError:
        print("❌ Invalid member ID.")
        return

    try:
        rows_deleted = delete_member(member_id)
        if rows_deleted:
            print(f"✅ Member with ID {member_id} deleted.")
            member_log_delete(member_id)
        else:
            print(f"❌ No member found with ID {member_id}.")
    except ValueError as e:
        print(f"❌ Error deleting member: {e}")

def list_members():
    """List all members (admin only)."""
    members = list_all_members()
    if not members:
        print("No members found.")
        return

    print("Members:")
    for member in members:
        print(f"ID: {member['member_id']}, Name: {member['name']}, Email: {member['email']}, Role: {member['role']}")

def get_member(member_id):
    """Get member details by id (admin only)."""

    member = get_member_by_id(member_id)
    if member:
        print(f"Member Details - ID: {member['member_id']}, Name: {member['name']}, Email: {member['email']}, Role: {member['role']}")
    else:
        print(f"❌ No member found with ID {member_id}.")


# for the books
def list_books():
    """List all books."""
    books = list_all_books()
    if not books:
        print("No books found.")
        return

    print("Books:")
    for book in books:
        print(f"ID: {book['book_id']}, Title: {book['title']}, Author: {book['author']}, ISBN: {book['isbn']}, Copies Available: {book['copies_available']}")

def add_book():
    """Add a new book (admin only). Returns the new book_id."""
    isbn = input("Enter book ISBN: ").strip()
    title = input("Enter book title: ").strip().title()
    author = input("Enter book author: ").strip().title()
    try:
        copies_available = int(input("Enter number of copies available: "))
        if copies_available < 0:
            raise ValueError
    except ValueError:
        print("❌ Invalid number of copies. Must be a non-negative integer.")
        return None

    try:
        book_id = create_book(isbn, title, author, copies_available)
        print(f"✅ Book added with ID: {book_id}")
        book_log_created(book_id,isbn, title, author, copies_available)
        return book_id
    except ValueError as e:
        print(f"❌ Error adding book: {e}")
        return None
    
def remove_book():
    """Remove a book by id (admin only)."""
    try:
        book_id = int(input("Enter book ID to delete: "))
    except ValueError:
        print("❌ Invalid book ID.")
        return

    try:
        rows_deleted = delete_book(book_id)
        if rows_deleted:
            print(f"✅ Book with ID {book_id} deleted.")
            book_log_delete(book_id)
        else:
            print(f"❌ No book found with ID {book_id}.")
    except ValueError as e:
        print(f"❌ Error deleting book: {e}")

def get_book():
    """Get book details by id (admin only)."""
    try:
        book_id = int(input("Enter book ID to fetch: "))
    except ValueError:
        print("❌ Invalid book ID.")
        return

    book = get_book_by_id(book_id)
    if book:
        print(f"Book Details - ID: {book['book_id']}, Title: {book['title']}, Author: {book['author']}, ISBN: {book['isbn']}, Copies Available: {book['copies_available']}")
    else:
        print(f"❌ No book found with ID {book_id}.")

def update_book_copies_admin(): 
    """Update book copies (admin only)."""
    try:
        book_id = int(input("Enter book ID to update: "))
    except ValueError:
        print("❌ Invalid book ID.")
        return

    try:
        new_copies = int(input("Enter new number of copies available: "))
        if new_copies < 0:
            raise ValueError
    except ValueError:
        print("❌ Invalid number of copies. Must be a non-negative integer.")
        return

    try:
        rows_updated = update_book_copies(book_id, new_copies)
        if rows_updated:
            print(f"✅ Book with ID {book_id} updated to {new_copies} copies available.")
            book_log_update(book_id,new_copies)
        else:
            print(f"❌ No book found with ID {book_id}.")
    except ValueError as e:
        print(f"❌ Error updating book: {e}")


# for loans


def create_loan_admin():
    """Create a loan for a member (admin only)."""
    try:
        member_id = int(input("Enter member ID: "))
        book_id = int(input("Enter book ID: "))
    except ValueError:
        print("❌ Invalid member ID or book ID.")
        return

    # 1) Validate member exists
    member = get_member_by_id(member_id)
    if member is None:
        print(f"❌ Invalid member ID: {member_id}. Please add the member first.")
        return

    # 2) Validate book exists and availability
    book = get_book_by_id(book_id)
    if book is None:
        print(f"❌ Invalid book ID: {book_id}. Please add the book first.")
        return
    if book['copies_available'] <= 0:
        print(f"❌ No copies available for book ID {book_id}.")
        return

    # 3) Proceed to create the loan
    try:
        borrowed_on = datetime.now().strftime("%Y-%m-%d")
        due_on = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        loan_id = create_loan(borrowed_on, due_on, member_id, book_id)
        print(f"✅ Loan created with ID: {loan_id}")
        loan_log_created(loan_id,borrowed_on, due_on, member_id, book_id)
        return loan_id
    except ValueError as e:
        print(f"❌ Error creating loan: {e}")
        return None

    
def list_loan_byid(member_id):
    """List all loans for a given member (admin only)."""
    loans = get_loan_by_id(member_id)  # SELECT * FROM loan WHERE member_id = ?
    
    if not loans:
            print(f"❌ No loans found for member ID {member_id}.")
            return

    print(f"Loans for member ID {member_id}:")
    for loan in loans:
            if loan['is_paid']:
                print(
                    f"Loan ID: {loan['loan_id']}, Book ID: {loan['book_id']}, "
                    f"Borrowed On: {loan['borrowed_on']}, Due On: {loan['due_on']}, "
                    f"Returned On: {loan['returned_on']}"
                    f" Fine Amount: {loan['fine']}, Payment Status: Paid"
                )
            else:
                print(
                f"Loan ID: {loan['loan_id']}, Book ID: {loan['book_id']}, "
                f"Borrowed On: {loan['borrowed_on']}, Due On: {loan['due_on']}, "
                f"Returned On: {loan['returned_on']}"
                f" Fine Amount: {loan['fine']}, Payment Status: Not Paid"
            )




def list_all_loans_admin():
    """List all loans (admin only)."""
    loans = list_all_loans()
    if not loans:
        print("No loans found.")
        return

    print("Loans:")
    for loan in loans:
        if loan['is_paid']:
            print(f"ID: {loan['loan_id']}, Member ID: {loan['member_id']}, Book ID: {loan['book_id']}, Borrowed On: {loan['borrowed_on']}, Due On: {loan['due_on']}, Returned On: {loan['returned_on']}, Fine Amount: {loan['fine']}, Payment Status: Paid")
        else:
            print(f"ID: {loan['loan_id']}, Member ID: {loan['member_id']}, Book ID: {loan['book_id']}, Borrowed On: {loan['borrowed_on']}, Due On: {loan['due_on']}, Returned On: {loan['returned_on']}, Fine Amount: {loan['fine']}, Payment Status: Not Paid")


def mark_loan_returned_admin():
    """Mark a loan as returned (admin only)."""
    try:
        loan_id = int(input("Enter loan ID to mark as returned: "))
    except ValueError:
        print("❌ Invalid loan ID.")
        return

    returned_on = input("Enter return date (YYYY-MM-DD): ").strip()

    try:
        rows_updated = mark_loan_returned(loan_id, returned_on)
        fine_cal = cal_fine(loan_id)
        fine_cost = fetch_fine(loan_id)
        if rows_updated and fine_cal:
            print(f"✅ Loan with ID {loan_id} marked as returned on {returned_on}, with a fine of amount {fine_cost[0]}")
        else:
            print(f"❌ No loan found with ID {loan_id}.")

        succ = input("Are you paying now (YES/NO) : ")
        if succ == "YES":
            if(payment(loan_id,1)):
                loan_log_updated(loan_id,returned_on, fine_cost[0], succ)
                print(f"✅ Loan with ID {loan_id} marked as returned on {returned_on}, with a fine of amount {fine_cost[0]} has been cleared")
        else:
            payment(loan_id,0)
            succ = "NO"
            loan_log_updated(loan_id,returned_on, fine_cost[0], succ)
            print(f"✅ Loan with ID {loan_id} marked as returned on {returned_on}, with a fine of amount {fine_cost[0]} has been pending")
            
        
    except ValueError as e:
        print(f"❌ Error marking loan as returned: {e}")

def delete_loan_admin():
    """Delete a loan by id (admin only)."""
    try:
        loan_id = int(input("Enter loan ID to delete: "))
    except ValueError:
        print("❌ Invalid loan ID.")
        return

    try:
        rows_deleted = delete_loan(loan_id)
        if rows_deleted:
            print(f"✅ Loan with ID {loan_id} deleted.")
            loan_log_delete(loan_id)
        else:
            print(f"❌ No loan found with ID {loan_id}.")
    except ValueError as e:
        print(f"❌ Error deleting loan: {e}")
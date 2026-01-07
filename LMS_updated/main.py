# lms/cli.py
from db import Database
from repo import MemberRepository, BookRepository, LoanRepository
from services import *
from models import Member, Book, Loan
from services import now_iso, plus_days_iso, calulate_fine
from auth import (
    login_user,
    logout_user,
    get_current_user,
    admin_only,
    member_only
)

# ---------- INITIAL SETUP ----------
def init_services():
    db = Database()
    db.migrate()

    mem_ser = MemberRepository(db)
    book_ser = BookRepository(db)
    loan_ser = LoanRepository(db)

    mem_ser = MemberService(mem_ser)
    book_ser = BookService(book_ser)
    loan_ser = LoanService(mem_ser,book_ser,loan_ser)

    # AUTO CREATE ADMIN
    admin = mem_ser.get_by_email("admin@innova.com")
    if not admin:
        mem_ser.create_member(
            Member(None, "System Admin", "admin@innova.com", "admin123", "admin")
        )
        print("👑 Default admin created")
        print("➡ Email: admin@innova.com | Password: admin123")

    return mem_ser, book_ser, loan_ser


# ---------- AUTH ----------

memid = None
def login(mem_ser : MemberService):
    email = input("Email: ")
    password = input("Password: ")

    user = mem_ser.get_by_email(email)
    if not user or user.password != password:
        print("❌ Invalid credentials")
        return

    login_user(user)
    if user.role == 'member':
        global memid
        memid = user.member_id
    else:
        memid = None
    print(f"✅ Logged in as {user.name} ({user.role})")


# ---------- ADMIN FUNCTIONS ----------
@admin_only
def add_book(book_ser : BookService):
    book_ser.create_book(
        Book(
            None,
            input("ISBN: "),
            input("Title: "),
            input("Author: "),
            int(input("Copies: "))
        )
    )
    print("✔️ Book added")


@admin_only
def delete_book(book_ser : BookService):
    book_ser.delete_book(int(input("Book ID: ")))
    print("✔️ Book deleted")


@admin_only
def get_book_by_id(book_ser : BookService):
    book = book_ser.get_by_id(int(input("Book ID: ")))
    print(book or "❌ Not found")


@admin_only
def get_book_by_isbn(book_ser : BookService):
    book = book_ser.get_by_isbn(input("ISBN: "))
    print(book or "❌ Not found")


@member_only
def list_all_books(book_ser : BookService):
    book_ser.list_all_book()


@admin_only
def add_member(mem_ser : MemberService):
    mem_ser.create_member(
        Member(
            None,
            input("Name: "),
            input("Email: "),
            input("Password: "),
            input("Role (admin/member): ")
        )
    )
    print("✔️ Member added")


@admin_only
def list_members(mem_ser : MemberService):
    mem_ser.list_all_members()


@admin_only
def get_member_by_id(mem_ser : MemberService):
    if memid == None:
        mem_ser.get_by_id(int(input("Member ID: ")))
    else:
        mem_ser.get_by_id(memid)

@admin_only
def get_member_by_email(mem_ser: MemberService):
    mem_ser.get_by_email(input("Enter the mail Id : "))

@admin_only
def update_member_role(mem_ser : MemberService):
    mem_ser.update_role(
        int(input("Member ID: ")),
        input("New Role (admin/member): ")
    )
    print("✔️ Role updated")


@admin_only
def delete_member(mem_ser : MemberService):
    mem_ser.delete_user(int(input("Member ID: ")))
    print("✔️ Member deleted")


# ---------- LOANS ----------
@member_only
def borrow_book(book_ser : BookService, loan_ser : LoanService, mem_ser : MemberService):
    user = mem_ser.get_by_id(memid)
    book_id = int(input("Book ID: "))

    loan_ser.create_loan(
        Loan(
            None,
            now_iso(),
            plus_days_iso(14),
            None,
            0,
            False,
            user.member_id,
            book_id
        )
    )
    print("✔️ Book borrowed")


@member_only
def my_loans(loan_ser : LoanService):
    if memid == None:
        loan_ser.list_active_by_member(int(input("Enter the Member id:  ")))
    else:
        loan_ser.list_active_by_member(memid)


@admin_only
def get_loan_by_id(loan_ser : LoanService):
    loan_ser.get_by_id(int(input("Enter the loan id : ")))


@admin_only
def mark_returned(book_ser : BookService, loan_ser : LoanService):
    loan_id = int(input("Loan ID: "))
    loan = loan_ser.get_by_id(loan_id)
    return_Date = input("Enter the Return date %Y-%m-%d : ")
    is_return = loan_ser.mark_returned(loan_id, return_Date)
    book_ser.increment_copy(loan.book_id)
    if is_return:
        fine = calulate_fine(loan.borrowed_on,loan.returned_on)
        loan_ser.set_fine(loan_id,fine)
        print("✔️ Book returned")


@admin_only
def set_paid(loan_ser : LoanService):
    loan_id = int(input("Loan ID: "))
    loan_ser.set_paid(loan_id, True)

@admin_only
def delete_loan(loan_ser : LoanService):
    loan_ser.delete(int(input("Loan ID: ")))
    print("✔️ Loan deleted")


# ---------- MENU ----------
def main():
    mem_ser, book_ser, loan_ser = init_services()

    menus = {
        "guest": {
            "1": ("Login", lambda: login(mem_ser)),
            "5": ("Exit", exit),
        },
        "member": {
            "1": ("List Books", lambda: list_all_books(book_ser)),
            "2": ("Borrow Book", lambda: borrow_book(book_ser, loan_ser,mem_ser)),
            "3": ("My Loans", lambda: my_loans(loan_ser)),
            "4": ("Logout", logout_user),
            "5": ("Exit", exit),
        },
        "admin": {

            "1": ("Add Book", lambda: add_book(book_ser)),
            "2": ("List Books", lambda: list_all_books(book_ser)),
            "3": ("Get Book By ID", lambda: get_book_by_id(book_ser)),
            "4": ("Get Book By ISBN", lambda: get_book_by_isbn(book_ser)),
            "5": ("Delete Book", lambda: delete_book(book_ser)),
            "6": ("Add Member", lambda: add_member(mem_ser)),
            "7": ("List Members", lambda: list_members(mem_ser)),
            "8": ("Get Member By ID", lambda: get_member_by_id(mem_ser)),
            "9": ("Get Member By email", lambda: get_member_by_email(mem_ser)),
            "10": ("Update Member Role", lambda: update_member_role(mem_ser)),
            "11": ("Delete Member", lambda: delete_member(mem_ser)),
            "12": ("List Loans", lambda: my_loans(loan_ser)),
            "13": ("Get Loan By ID", lambda: get_loan_by_id(loan_ser)),
            "14": ("Mark Returned", lambda: mark_returned(book_ser, loan_ser)),
            "15": ("Set Paid", lambda: set_paid(loan_ser)),
            "16": ("Delete Loan", lambda: delete_loan(loan_ser)),
            "17": ("Logout", logout_user),
            "18": ("Exit", exit),
        },
    }

    while True:
        user = get_current_user()
        role = user.role if user else "guest"
        menu = menus[role]

        print(f"\n📚 LMS CLI ({role.upper()})")
        for k, v in menu.items():
            print(f"{k}. {v[0]}")

        action = menu.get(input("Choose: "))
        if action:
            action[1]()
        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    main()


# lms/__main__.py
from .db import Database
from .models import Member, Book
from .repo import MemberRepository, BookRepository, LoanRepository
from .services import LoanService

def main():
    db = Database()
    db.migrate()

    members = MemberRepository(db)
    books = BookRepository(db)
    loans = LoanRepository(db)
    service = LoanService(db, members, books, loans)

    # Create demo records
    alice_id = members.create(Member(member_id=None, name="Alice", email="alice@example.com", password="plaintext", role="member"))
    book_id = books.create(Book(book_id=None, isbn="978-0132350884", title="Clean Code", author="Robert C. Martin", copies_available=2))

    # Borrow a book
    loan_id = service.borrow_book(member_id=alice_id, book_id=book_id, loan_days=7)
    print(f"Loan created: {loan_id}")

    # Return a book
    service.return_book(loan_id)
    print("Book returned.")

if __name__ == "__main__":
    main()

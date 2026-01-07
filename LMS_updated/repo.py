
import sqlite3
from typing import List, Optional
from db import Database
from models import Member, Book, Loan

class MemberRepository:
    def __init__(self, db: Database):
        self.db = db

    def create(self, member: Member):
        q = "INSERT INTO member(name, email, password, role) VALUES (?, ?, ?, ?)"
        with self.db.connect() as conn:
            cur = conn.execute(q, (member.name, member.email, member.password, member.role))
            return cur.lastrowid

    def get_by_id(self, member_id: int):
        with self.db.connect() as conn:
            row = conn.execute("SELECT * FROM member WHERE member_id = ?", (member_id,)).fetchone()
            return self._to_member(row) if row else None

    def get_by_email(self, email: str) -> Optional[Member]:
        with self.db.connect() as conn:
            row = conn.execute("SELECT * FROM member WHERE email = ?", (email,)).fetchone()
            return self._to_member(row) if row else None

    def list(self) -> List[Member]:
        with self.db.connect() as conn:
            rows = conn.execute("SELECT * FROM member ORDER BY name").fetchall()
            return [self._to_member(r) for r in rows]

    def update_role(self, member_id: int, role: str) -> None:
        with self.db.connect() as conn:
            cur = conn.execute("UPDATE member SET role = ? WHERE member_id = ?", (role, member_id))
            return cur.rowcount

    def delete(self, member_id: int) -> None:
        with self.db.connect() as conn:
           cur =  conn.execute("DELETE FROM member WHERE member_id = ?", (member_id,))
           return cur.rowcount
    @staticmethod
    def _to_member(row: sqlite3.Row) -> Member:
        return Member(
            member_id=row["member_id"],
            name=row["name"],
            email=row["email"],
            password=row["password"],
            role=row["role"],
        )


class BookRepository:
    def __init__(self, db: Database):
        self.db = db

    def create(self, book: Book) -> int:
        q = "INSERT INTO book(isbn, title, author, copies_available) VALUES (?, ?, ?, ?)"
        with self.db.connect() as conn:
            cur = conn.execute(q, (book.isbn, book.title, book.author, book.copies_available))
            return cur.lastrowid

    def get_by_id(self, book_id: int) -> Optional[Book]:
        with self.db.connect() as conn:
            row = conn.execute("SELECT * FROM book WHERE book_id = ?", (book_id,)).fetchone()
            return self._to_book(row) if row else None

    def get_by_isbn(self, isbn: str) -> Optional[Book]:
        with self.db.connect() as conn:
            row = conn.execute("SELECT * FROM book WHERE isbn = ?", (isbn,)).fetchone()
            return self._to_book(row) if row else None

    def list(self) -> List[Book]:
        with self.db.connect() as conn:
            rows = conn.execute("SELECT * FROM book ORDER BY title").fetchall()
            return [self._to_book(r) for r in rows]

    def update_copies(self, book_id: int, copies_available: int) -> None:
        with self.db.connect() as conn:
            conn.execute(
                "UPDATE book SET copies_available = ? WHERE book_id = ?",
                (copies_available, book_id),
            )

    def increment_copy(self, book_id: int) -> None:
        with self.db.connect() as conn:
           cur = conn.execute(
                "UPDATE book SET copies_available = copies_available + 1 WHERE book_id = ?",
                (book_id,),
            )
           return cur.rowcount

    def decrement_copy(self, book_id: int) -> None:
        with self.db.connect() as conn:
            conn.execute(
                """
                UPDATE book
                SET copies_available = CASE
                    WHEN copies_available > 0 THEN copies_available - 1
                    ELSE copies_available
                END
                WHERE book_id = ?
                """,
                (book_id,),
            )

    def delete(self, book_id: int) -> None:
        with self.db.connect() as conn:
            cur=conn.execute("DELETE FROM book WHERE book_id = ?", (book_id,))
            return cur.rowcount
    @staticmethod
    def _to_book(row: sqlite3.Row) -> Book:
        return Book(
            book_id=row["book_id"],
            isbn=row["isbn"],
            title=row["title"],
            author=row["author"],
            copies_available=row["copies_available"],
        )


class LoanRepository:
    def __init__(self, db: Database):
        self.db = db

    def create(self, loan: Loan) -> int:
        q = """
        INSERT INTO loan(borrowed_on, due_on, returned_on, fine, is_paid, member_id, book_id)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        with self.db.connect() as conn:
            cur = conn.execute(q, (
                loan.borrowed_on,
                loan.due_on,
                loan.returned_on,
                loan.fine,
                1 if loan.is_paid else 0,
                loan.member_id,
                loan.book_id,
            ))
            return cur.lastrowid

    def get_by_id(self, loan_id: int) -> Optional[Loan]:
        with self.db.connect() as conn:
            row = conn.execute("SELECT * FROM loan WHERE loan_id = ?", (loan_id,)).fetchone()
            return self._to_loan(row) if row else None

    def list_active_by_member(self, member_id: int) -> List[Loan]:
        with self.db.connect() as conn:
            rows = conn.execute(
                "SELECT * FROM loan WHERE member_id = ? AND returned_on IS NULL ORDER BY due_on",
                (member_id,),
            ).fetchall()
            return [self._to_loan(r) for r in rows]

    def mark_returned(self, loan_id: int, returned_on: str):
        with self.db.connect() as conn:
            conn.execute("UPDATE loan SET returned_on = ? WHERE loan_id = ?", (returned_on, loan_id))
            row = conn.execute("SELECT * FROM loan WHERE loan_id = ?", (loan_id,)).fetchone()
            return self._to_loan(row)

    def set_fine(self, loan_id: int, fine: int) -> None:
        with self.db.connect() as conn:
            conn.execute("UPDATE loan SET fine = ? WHERE loan_id = ?", (fine, loan_id))

    def set_paid(self, loan_id: int, is_paid: bool) -> None:
        with self.db.connect() as conn:
            conn.execute("UPDATE loan SET is_paid = ? WHERE loan_id = ?", (1 if is_paid else 0, loan_id))

    def delete(self, loan_id: int) -> None:
        with self.db.connect() as conn:
            conn.execute("DELETE FROM loan WHERE loan_id = ?", (loan_id,))

    @staticmethod
    def _to_loan(row: sqlite3.Row) -> Loan:
        return Loan(
            loan_id=row["loan_id"],
            borrowed_on=row["borrowed_on"],
            due_on=row["due_on"],
            returned_on=row["returned_on"],
            fine=row["fine"],
            is_paid=bool(row["is_paid"]),
            member_id=row["member_id"],
            book_id=row["book_id"],
        )

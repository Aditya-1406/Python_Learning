
from datetime import datetime, timedelta
import sqlite3

# Open one connection for this module.
# Keep it open while your app runs; close it explicitly when you're done.
conn = sqlite3.connect('lms.db')
conn.row_factory = sqlite3.Row  # Optional: lets you access columns by name
cursor = conn.cursor()

# Always enable foreign keys on this connection.
cursor.execute('PRAGMA foreign_keys = ON;')


# ---------- Repo for books ----------

def create_book(isbn, title, author, copies_available):
    """Insert a new book. Returns the new book_id."""
    if copies_available is None or copies_available < 0:
        raise ValueError("copies_available must be >= 0")

    try:
        cursor.execute(
            '''
            INSERT INTO book (isbn, title, author, copies_available)
            VALUES (?, ?, ?, ?)
            ''',
            (isbn, title, author, copies_available)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError as e:
        # Handles UNIQUE (isbn) or CHECK constraints
        # Keep it simple: re-raise with a clearer message
        raise ValueError(f"Failed to create book: {e}")


def get_book_by_id(book_id):
    """Fetch a book by id. Returns a sqlite3.Row or None."""
    cursor.execute('SELECT * FROM book WHERE book_id = ?', (book_id,))
    return cursor.fetchone()


def update_book_copies(book_id, new_copies):
    """Update copies_available. Ensures non-negative."""
    if new_copies is None or new_copies < 0:
        raise ValueError("new_copies must be >= 0")

    cursor.execute(
        '''
        UPDATE book
        SET copies_available = ?
        WHERE book_id = ?
        ''',
        (new_copies, book_id)
    )
    conn.commit()
    return cursor.rowcount  # 1 if updated, 0 if book_id not found


def delete_book(book_id):
    """
    Delete a book by id.
    NOTE: will fail if there are loans referencing this book (FK constraint),
    unless you defined ON DELETE CASCADE (not set in your schema).
    """
    try:
        cursor.execute('DELETE FROM book WHERE book_id = ?', (book_id,))
        conn.commit()
        return cursor.rowcount  # 1 if deleted, 0 if not found
    except sqlite3.IntegrityError as e:
        # FK violation (active loans exist)
        raise ValueError(f"Cannot delete book: {e}")


def list_all_books():
    """Return all books as a list of sqlite3.Row."""
    cursor.execute('SELECT * FROM book')
    return cursor.fetchall()




# Repo for members

def create_member(name, email, password, role='member'):
    """Insert a new member. Returns the new member_id."""
    try:
        cursor.execute(
            '''
            INSERT INTO member (name, email, password, role)
            VALUES (?, ?, ?, ?)
            ''',
            (name, email, password, role)
        )
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError as e:
        # Handles UNIQUE (email) or CHECK constraints
        raise ValueError(f"Failed to create member: {e}")

def get_member_by_id(member_id):
    """Fetch a member by id. Returns a sqlite3.Row or None."""
    cursor.execute('SELECT * FROM member WHERE member_id = ?', (member_id,))
    return cursor.fetchone()

def list_all_members():
    """Return all members as a list of sqlite3.Row."""
    cursor.execute('SELECT * FROM member')
    return cursor.fetchall()

def delete_member(member_id):
    """
    Delete a member by id.
    NOTE: will fail if there are loans referencing this member (FK constraint),
    unless you defined ON DELETE CASCADE (not set in your schema).
    """
    try:
        cursor.execute('DELETE FROM member WHERE member_id = ?', (member_id,))
        conn.commit()
        return cursor.rowcount  # 1 if deleted, 0 if not found
    except sqlite3.IntegrityError as e:
        # FK violation (active loans exist)
        raise ValueError(f"Cannot delete member: {e}")


# Repo for loans

def create_loan(borrowed_on, due_on, member_id, book_id):
    """Insert a new loan. Returns the new loan_id."""
    try:
        row = cursor.execute('''SELECT copies_available FROM book WHERE book_id = ?''', (book_id,)).fetchone()
        if row is None:
            raise ValueError("Book not found.")
        if row[0] <= 0:
            raise ValueError("No copies available for this book.")

        cursor.execute(
            '''
            INSERT INTO loan (borrowed_on, due_on, member_id, book_id)
            VALUES (?, ?, ?, ?)
            ''',
            (borrowed_on, due_on, member_id, book_id)
        )

        cursor.execute('''
            UPDATE book
            SET copies_available = copies_available - 1
            WHERE book_id = ? AND copies_available > 0
        ''', (book_id,))
        
        conn.commit()
        return cursor.lastrowid
    except sqlite3.IntegrityError as e:
        # Handles FK constraints
        raise ValueError(f"Failed to create loan: {e}")
    
def get_loan_by_id(member_id):
    """Fetch a loan by id. Returns a sqlite3.Row or None."""
    cursor.execute('SELECT * FROM loan WHERE member_id = ?', (member_id,))
    return cursor.fetchall()

def list_all_loans():
    """Return all loans as a list of sqlite3.Row."""
    cursor.execute('SELECT * FROM loan')
    return cursor.fetchall()

def mark_loan_returned(loan_id, returned_on):
    """Mark a loan as returned by setting returned_on date."""
    cursor.execute(
        '''
        UPDATE loan
        SET returned_on = ?
        WHERE loan_id = ?
        ''',
        (returned_on, loan_id)
    )
    cursor.execute('''
        UPDATE book 
        SET copies_available = copies_available + 1
        WHERE book_id = (SELECT book_id FROM loan WHERE loan_id = ?)
        ''', (loan_id,))           
    conn.commit()
    return cursor.rowcount  # 1 if updated, 0 if loan_id not found

def delete_loan(loan_id):
    """Delete a loan by id."""
    cursor.execute('DELETE FROM loan WHERE loan_id = ?', (loan_id,))
    conn.commit()
    return cursor.rowcount  # 1 if deleted, 0 if not found

def cal_fine(loan_id):
    '''Çalculating the fine'''
    PER_DAY = 10
    row = cursor.execute('''SELECT * FROM loan where loan_id = ?''',(loan_id,)).fetchone() # 6 col -->fine 7--> is paid

    ret_on = datetime.strptime(row['returned_on'], "%Y-%m-%d")
    bor_on = datetime.strptime(row['borrowed_on'], "%Y-%m-%d")
    delta = (ret_on-bor_on)
    days = delta.days
    fine_cost = 0
    if days> 14 :
        days -=  14
        fine_cost = days * PER_DAY
    
    cursor.execute('''UPDATE loan SET fine = ? WHERE  loan_id = ?''', (fine_cost,loan_id))
    conn.commit()
    return cursor.rowcount
 

def fetch_fine(loan_id):
    cursor.execute('''SELECT fine FROM loan WHERE loan_id = ?''',(loan_id,))
    return cursor.fetchone()


# ---------- Lifecycle helper ----------

def close_connection():
    """Call this when your program is shutting down."""
    try:
        cursor.close()
    finally:
        conn.close()

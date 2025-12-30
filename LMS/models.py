import sqlite3

conn = sqlite3.connect('lms.db')
cursor = conn.cursor()


cursor.execute('PRAGMA foreign_keys = ON;')
# create member table

cursor.execute('''
    CREATE TABLE IF NOT EXISTS member (
               member_id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT NOT NULL,
               email TEXT UNIQUE NOT NULL,
               password TEXT NOT NULL,
               role TEXT CHECK( role IN ('member','admin') ) NOT NULL
            )
''')

# create book table

cursor.execute('''
    CREATE TABLE IF NOT EXISTS book(
               book_id INTEGER PRIMARY KEY AUTOINCREMENT,
               isbn TEXT UNIQUE NOT NULL,
               title TEXT NOT NULL,
                author TEXT NOT NULL,
               copies_available INTEGER NOT NULL check(copies_available >= 0)
               )
''')

# create loan table

cursor.execute('''
    CREATE TABLE IF NOT EXISTS loan(
               loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
               borrowed_on TEXT NOT NULL,
               due_on TEXT NOT NULL,
               returned_on TEXT,
               member_id INTEGER,
                book_id INTEGER,
                FOREIGN KEY (member_id) REFERENCES member(member_id),
                FOREIGN KEY (book_id) REFERENCES book(book_id)
               )
''')

conn.commit()
conn.close()
import sqlite3
from resourses.db_connection_manager import DbConn

# conn = sqlite3.connect(':memory:')


def create_books_table():
    with DbConn('sqlite3_database.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("""CREATE TABLE IF NOT EXISTS books (  id integer primary key autoincrement,
                                                    name text type UNIQUE,
                                                    author text not null,
                                                    read_status integer not null)"""
                           )
            print("Table created")
        except Exception as e:
            print("Table already exist or unable to create new table: \n", e)


def add_book(book_name, author):
    with DbConn('sqlite3_database.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO books (name, author, read_status) VALUES (:name, :author, :read_status)",
                           {"author": author, "name": book_name, "read_status": 0})
        except sqlite3.IntegrityError:
            print("Cant add book, books name should be unique: ", book_name)


def change_read_status(book_name, author, read_status):
    with DbConn('sqlite3_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""UPDATE books SET read_status = :read_status WHERE name = :name 
        AND author = :author""",
                       {"author": author, "name": book_name, "read_status": read_status})


def return_books_list():
    with DbConn('sqlite3_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM books")
        return [i for i in cursor.fetchall()]


def clean_db():
    with DbConn('sqlite3_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books")


def drop_db():
    with DbConn('sqlite3_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE books")
        create_books_table()


def delete_book(book_name):
    with DbConn('sqlite3_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM books WHERE name=?', (book_name,))



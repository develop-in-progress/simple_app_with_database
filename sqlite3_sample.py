import sqlite3
from resourses.db_connection_manager import DbConn
from datetime import datetime
import random
from string import printable

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


def create_reading_time_table():
    with DbConn('sqlite3_database.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.execute("""CREATE TABLE IF NOT EXISTS reading (  id integer primary key autoincrement,
                                                                    reading_time text,
                                                                    name text unique, 
                                                                    FOREIGN KEY(name) REFERENCES books(name) )""")
        except Exception as e:
            print("Table already exist or unable to create new table: \n", e)


def create_cross_books_table():
    with DbConn('sqlite3_database.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.execute("""CREATE TABLE IF NOT EXISTS cross_books (  name text not null, read_date not null, 
            FOREIGN KEY(name) REFERENCES books(name) FOREIGN KEY(read_date) REFERENCES reading(reading_time) )""")
        except Exception as e:
            print("Table already exist or unable to create new table: \n", e)


def add_book(book_name, author):
    with DbConn('sqlite3_database.db') as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO books (name, author, read_status) VALUES (:name, :author, :read_status)",
                           {"author": author, "name": book_name, "read_status": 0})
            cursor.execute("INSERT INTO reading (reading_time, name) VALUES (:reading_time, :name)",
                           {"reading_time": datetime.now(), "name": book_name})
            cursor.execute("INSERT INTO cross_books (name, read_date) VALUES (:name, :read_date)",
                           {"read_date": datetime.now(), "name": book_name})
        except sqlite3.IntegrityError:
            print("Cant add book, books name should be unique: ", book_name)


def change_read_status(book_name, author, read_status):
    with DbConn('sqlite3_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""UPDATE books SET read_status = :read_status WHERE name = :name 
        AND author = :author""",
                       {"author": author, "name": book_name, "read_status": read_status})


def get_name_and_reading_time_from_cross_table(name):
    with DbConn('sqlite3_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""select * from cross_books where name = :name""", {"name": name})
        return [i for i in cursor.fetchall()]


def return_books_list_and_time():
    with DbConn('sqlite3_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("""select books.name, books.author, reading_time from reading, 
                            books  where books.name = reading.name""")
        # SELECT books.name, books.author, reading_time FROM books JOIN reading ON books.name = reading.name
        return cursor.fetchall()


def clean_db():
    with DbConn('sqlite3_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM books")


def show_reading_time(name):
    with DbConn('sqlite3_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("select reading_time from reading where name = :name", {"name":name})
        return f'start : {cursor.fetchone()[0]} and now is : {datetime.now()}'


def drop_db():
    with DbConn('sqlite3_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DROP TABLE books")
        cursor.execute("DROP TABLE reading")
        create_books_table()
        create_reading_time_table()
        create_cross_books_table()


def delete_book(book_name):
    with DbConn('sqlite3_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM books WHERE name=?', (book_name,))
        cursor.execute('DELETE FROM reading WHERE name=?', (book_name,))
        cursor.execute('DELETE FROM cross_books WHERE name=?', (book_name,))


def start_recording_time():
    with DbConn('sqlite3_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO reading VALUES (:reading_time)", {"reading_time": datetime.now})


def return_time():
    with DbConn('sqlite3_database.db') as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM reading")


def create_a_lot_of_books():

    # author, book_name = [i for i in range(100000)]
    with DbConn('sqlite3_database.db') as conn:
        cursor = conn.cursor()

        try:
            for i in range(100):
                author = printable[random.randint(1, 44):random.randint(40, 99)]
                book_name = printable[random.randint(1, 44):random.randint(40, 99)]
                cursor.execute("INSERT INTO books (name, author, read_status) VALUES (:name, :author, :read_status)",
                           {"author": author, "name": book_name, "read_status": 0})
                cursor.execute("INSERT INTO reading (reading_time, name) VALUES (:reading_time, :name)",
                           {"reading_time": datetime.now(), "name": book_name})
                cursor.execute("INSERT INTO cross_books (name, read_date) VALUES (:name, :read_date)",
                           {"read_date": datetime.now(), "name": book_name})
        except sqlite3.IntegrityError:
            print("Cant add book, books name should be unique: ", book_name)

# with DbConn('sqlite3_database.db') as conn:
#     cursor = conn.cursor()
#     cursor.execute("PRAGMA foreign_keys;")
#     print(cursor.fetchall())

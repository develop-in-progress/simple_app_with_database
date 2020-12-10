from sqlite3_sample import *


note = """Select mode:
        -q: for quit
        -a: add book
        -c: change read status (any int except 0 -> mark as read)
        -l: list of book in db
        -d: delete book \n ------>:"""


def main():
    create_books_table()
    clean_db()
    user_input = input(note)
    while user_input != 'q':
        print()
        if user_input == 'a':
            name = input('Enter name : ')
            author = input("Enter author :")
            add_book(name, author)
            print(return_books_list())
        elif user_input == 'c':
            name = input('Enter name : ')
            author = input("Enter author :")
            starus = input("Enter status :")
            change_read_status(name, author, starus)
        elif user_input == 'd':
            name = input('Enter name : ')
            delete_book(name)
        elif user_input == 'l':
            print(return_books_list())
        else:
            print('Enter valid query')
        user_input = input(note)


if __name__ == '__main__':
    main()

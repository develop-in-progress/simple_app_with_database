from sqlite3_sample import *


note = """Select mode:
        -q: for quit
        -a: add book
        -c: change read status (any int except 0 -> mark as read)
        -l: list of book in db
        -w: drop table
        -t: shows reading time
        -g: get data from cross table - books name and start reading date
        -d: delete book \n ------>:"""


def main():
    create_books_table()
    create_reading_time_table()
    create_cross_books_table()
    user_input = input(note)
    while user_input != 'q':
        print()
        if user_input == 'a':
            name = input('Enter name : ')
            author = input("Enter author :")
            add_book(name, author)
            print(return_books_list_and_time())

        elif user_input == 'g':
            name = input('Enter name : ')
            print(get_name_and_reading_time_from_cross_table(name))
        elif user_input == 'c':
            name = input('Enter name : ')
            author = input("Enter author :")
            starus = input("Enter status :")
            change_read_status(name, author, starus)
        elif user_input == 'd':
            name = input('Enter name : ')
            delete_book(name)
        elif user_input == 'l':
            print(return_books_list_and_time())
        elif user_input == 'w':
            drop_db()
        elif user_input == 't':
            name = input('Enter books name : ')
            print(show_reading_time(name))
        elif user_input == 'generate':
            create_a_lot_of_books()
        else:
            print('Enter valid query')
        user_input = input(note)


if __name__ == '__main__':
    main()

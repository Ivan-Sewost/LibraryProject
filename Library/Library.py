import psycopg2


class Library:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="books",
            user="postgres",
            password="Ваш пароль",
            port="5432"
        )
        self.cursor = self.conn.cursor()
        print('Библиотека подключена')

    def get_all_books(self):
        self.cursor.execute("""
            SELECT books.title, authors.name, books.year, books.available 
            FROM books 
            JOIN authors ON authors.id = books.author_id
        """)
        books = self.cursor.fetchall()
        for book in books:
            if book[3] == True:
                status = 'Доступна'
            else:
                status = 'Выдана'
            print(f'{book[0]} - {book[1]} ({book[2]}) - {status}')

    def get_available_books(self):
        self.cursor.execute("""SELECT books.title, authors.name, books.year 
        FROM books 
        JOIN authors ON authors.id = books.author_id
        WHERE books.available = true""")
        books = self.cursor.fetchall()
        print('ДОСТУПНЫЕ КНИГИ')
        for book in books:
            print(f'{book[0]} - {book[1]} ({book[2]})')

    def add_book(self):
        print('Добавьте новую книгу')
        title = input('Название:')
        self.cursor.execute("""SELECT id, name FROM authors""")
        authors = self.cursor.fetchall()
        for author in authors:
            print(f'{author[0]}. {author[1]}')
        author_id = int(input("ID автора: "))
        year = int(input('Введите дату издания книги:'))
        isbn = input('ISBN:')
        self.cursor.execute("""
            INSERT INTO books (title, author_id, year, isbn, available)
            VALUES (%s, %s, %s, %s, %s)
        """, (title, author_id, year, isbn, True))
        self.conn.commit()
        print(f'Книга ({title}) добавлена')

    def borrow_book(self):

        self.cursor.execute("""SELECT books.id, books.title, authors.name, books.year FROM books 
        JOIN authors ON authors.id = books.author_id
        WHERE books.available = true""")
        books = self.cursor.fetchall()
        print('Все доступные книги')
        for book in books:
            print(f'{book[0]} - {book[1]} ({book[2]})')
        id_books = int(input('Введити ID книги которую хотите взять:'))
        book_found = False
        for book in books:
            if book[0] == id_books:
                book_found = True
                break
        if book_found:

            self.cursor.execute("""UPDATE books 
            SET available = false
             WHERE id = %s
             RETURNING title""", (id_books,))

            title = self.cursor.fetchone()[0]
            self.conn.commit()
            print(f'Книга: {title}, выдана')
        else:
            print("Данной книги нет в ассортименте ")

    def return_book(self):
        self.cursor.execute("""SELECT books.id, books.title, authors.name, books.year FROM books 
        JOIN authors ON authors.id = books.author_id
        WHERE books.available = false""")
        books = self.cursor.fetchall()
        for book in books:
            print(f'{book[0]} - {book[1]} ({book[2]})')
        id_books = int(input('Введити ID книги которую хотите вернуть:'))
        book_found = False
        for book in books:
            if book[0] == id_books:
                book_found = True
                break
        if book_found:

            self.cursor.execute("""UPDATE books 
            SET available = true
            WHERE id = %s
            RETURNING title""", (id_books,))
            title = self.cursor.fetchone()[0]
            self.conn.commit()
            print(f'Книга: {title}, возвращена')
        else:
            print("Данной книги нет в ассортименте ")


def main():
    lib = Library()

    while True:
        print("\n" + "=" * 50)
        print("📚 БИБЛИОТЕЧНАЯ СИСТЕМА")
        print("=" * 50)
        print("1. Все книги")
        print("2. Доступные книги")
        print("3. Добавить книгу")
        print("4. Выдать книгу")
        print("5. Вернуть книгу")
        print("0. Выход")
        print("=" * 50)

        choice = input("Ваш выбор: ")

        if choice == '1':
            lib.get_all_books()
        elif choice == '2':
            lib.get_available_books()
        elif choice == '3':
            lib.add_book()
        elif choice == '4':
            lib.borrow_book()
        elif choice == '5':
            lib.return_book()
        elif choice == '0':
            print("До свидания!")
            break
        else:
            print(" Неверный выбор!")

    lib.cursor.close()
    lib.conn.close()


if __name__ == "__main__":
    main()
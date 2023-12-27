import pandas


def get_reader(conn):
    return pandas.read_sql(
        '''
        SELECT * FROM reader
        ''', conn)


def get_book_reader(conn, reader_id):
    # выбираем и выводим записи о том, какие книги брал читатель
    return pandas.read_sql(
        '''
        WITH get_authors( book_id, authors_name)
        AS(
        SELECT book_id, GROUP_CONCAT(author_name)
        FROM author JOIN book_author USING(author_id)
        GROUP BY book_id
        )
        SELECT title AS Название, authors_name AS Авторы,
        borrow_date AS Дата_выдачи, return_date AS Дата_возврата,
        book_reader_id
        FROM
        reader
        JOIN book_reader USING(reader_id)
        JOIN book USING(book_id)
        JOIN get_authors USING(book_id)
        WHERE reader.reader_id = :id
        ORDER BY 3
        ''', conn, params={"id": reader_id})

# для обработки данных о новом читателе

def return_book(conn, book_reader_id):
    cur = conn.cursor()

    cur.execute("""
            SELECT book_id
            FROM book_reader
            WHERE book_reader_id = :book_reader_id
        """, {"book_reader_id": book_reader_id})
    book_id = cur.fetchone()[0]

    cur.execute("""
        UPDATE book_reader 
        SET return_date = DATE("now")
        WHERE book_reader_id = :book_reader_id
    """, {"book_reader_id": book_reader_id})

    cur.execute("""
        UPDATE book
        SET available_numbers = available_numbers + 1
        WHERE book_id = :book_id
    """, {"book_id": book_id})

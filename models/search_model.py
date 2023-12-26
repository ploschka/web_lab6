import pandas
import sqlite3


def borrow_book(conn: sqlite3.Connection, book_id, reader_id):
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO book_reader(book_id, reader_id, borrow_date)
        VALUES (:book_id, :reader_id, DATE("now"))
    """, {"book_id": book_id, "reader_id": reader_id})

    cur.execute("""
        UPDATE book
        SET available_numbers = available_numbers - 1
        WHERE book_id = :book_id
    """, {"book_id": book_id})


def get_all_books_info(conn: sqlite3.Connection):
    return pandas.read_sql('''
        SELECT *
        FROM book
        JOIN book_author USING (book_id)
        JOIN author USING (author_id)
        JOIN genre USING (genre_id)
        JOIN publisher USING (publisher_id)
    ''', conn)


def search_books_info(conn: sqlite3.Connection,
                      genre_ids: list[int] = None,
                      author_ids: list[int] = None,
                      publisher_ids: list[int] = None):
    params = []

    genre_join_condition = "ON book.genre_id = genre.genre_id"
    if genre_ids:
        arg_part = ",".join(["?"] * len(genre_ids))
        genre_join_condition += " AND book.genre_id IN (" + arg_part + ")"
        params += genre_ids

    author_join_condition = "ON book.book_id = get_authors.book_id"
    if author_ids:
        arg_part = ",".join(["?"] * len(author_ids))
        author_join_condition += " AND author_id IN (" + arg_part + ")"
        params += author_ids

    publisher_join_condition = "ON book.publisher_id = publisher.publisher_id"
    if publisher_ids:
        arg_part = ",".join(["?"] * len(publisher_ids))
        publisher_join_condition += " AND book.publisher_id IN (" + \
            arg_part + ")"
        params += publisher_ids

    query = f'''
        WITH get_authors(book_id, authors_name, author_id)
        AS(
            SELECT book_id, GROUP_CONCAT(author_name), author_id
            FROM author JOIN book_author USING(author_id)
            GROUP BY book_id
        )
        SELECT *
        FROM book
        JOIN get_authors {author_join_condition}
        JOIN genre {genre_join_condition}
        JOIN publisher {publisher_join_condition}
    '''

    return pandas.read_sql(query, conn, params=params)

import sqlite3


def create_reader(conn, reader_name):
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO reader(reader_name)
        VALUES (:reader_name)
    """, {"reader_name": reader_name})
    return cur.lastrowid

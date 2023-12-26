import sqlite3

CONNECTION = None


def get_db_connection():
    global CONNECTION
    if CONNECTION is None:
        CONNECTION = sqlite3.connect('library.sqlite', check_same_thread=False)
    return CONNECTION

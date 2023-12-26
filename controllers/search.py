from app import app
from flask import request, render_template, session, redirect, url_for
from models import search_model
from utils import get_db_connection


@app.route('/search', methods=['get'])
def search():
    conn = get_db_connection()

    all_books = search_model.get_all_books_info(conn)

    selected_genres = request.values.getlist("genre_id", type=int)
    selected_authors = request.values.getlist("author_id", type=int)
    selected_publishers = request.values.getlist("publisher_id", type=int)

    if request.values.get("reset"):
        selected_genres = []
        selected_authors = []
        selected_publishers = []

    searched_books = search_model.search_books_info(
        conn,
        genre_ids=selected_genres,
        author_ids=selected_authors,
        publisher_ids=selected_publishers,
    )

    return render_template(
        "search.jinja",
        searched_books=searched_books,
        all_books=all_books,
        zip=zip,
        selected_genres=selected_genres,
        selected_authors=selected_authors,
        selected_publishers=selected_publishers,
    )


@app.route('/search', methods=['post'])
def search_post():
    conn = get_db_connection()
    book_id = request.values.get("book_id")
    search_model.borrow_book(conn, book_id, session["reader_id"])
    return redirect(url_for("search"))

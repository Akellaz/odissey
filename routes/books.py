from flask import Blueprint, render_template, request, redirect, url_for
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from itertools import groupby
import sys
import subprocess

books_bp = Blueprint('books', __name__)

# Инициализация базы данных
engine = create_engine('sqlite:///ak_data.db?check_same_thread=False')
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

# Импорт моделей
try:
    from database_setup import Base, Book
    Base.metadata.bind = engine
except ImportError:
    # Альтернативный импорт если файл в другой директории
    pass

@books_bp.route('/books')
@books_bp.route('/books/')
def showBooks():
    try:
        books = db_session.query(Book).order_by(Book.date).all()

        # Группировка по дате
        sorted_books = sorted(books, key=lambda x: x.date)
        grouped_books = []
        for key, group in groupby(sorted_books, lambda x: x.date):
            grouped_books.append({"date": key, "books": list(group)})

        return render_template("tg_books.html", books=grouped_books)
    except Exception as e:
        return f"Error: {e}"

@books_bp.route('/books/new/', methods=['GET', 'POST'])
def newBook():
    if request.method == 'POST':
        newBook = Book(name=request.form['name'], date=request.form['date'], time=request.form['time'])
        db_session.add(newBook)
        db_session.commit()
        return redirect(url_for('books.showBooks'))
    else:
        return render_template('tg_newBook.html')

@books_bp.route("/books/<int:book_id>/edit/", methods=['GET', 'POST'])
def editBook(book_id):
    editedBook = db_session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedBook.name = request.form['name']
        if "author" in request.form and request.form["author"]:
            editedBook.author = request.form["author"]
        if "time" in request.form and request.form["time"]:
            editedBook.time = request.form["time"]
        
        db_session.add(editedBook)
        db_session.commit()
        return redirect(url_for('books.showBooks'))
    else:
        return render_template('tg_editBook.html', book=editedBook)

@books_bp.route('/books/<int:book_id>/delete/', methods=['GET', 'POST'])
def deleteBook(book_id):
    bookToDelete = db_session.query(Book).filter_by(id=book_id).one()
    if request.method == 'POST':
        db_session.delete(bookToDelete)
        db_session.commit()
        return redirect(url_for('books.showBooks', book_id=book_id))
    else:
        return render_template('tg_deleteBook.html', book=bookToDelete)

@books_bp.route('/ak_bot')
def ak_bot():
    subprocess.Popen([sys.executable, 'ak_bot.py'], shell=True)
    return render_template("tg_books.html")

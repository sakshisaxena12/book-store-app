from flask import Blueprint, request, jsonify

from models import db, Book

books_bp = Blueprint('books', __name__)


# List all books
@books_bp.route('/books', methods=['GET'])
def list_books():
    books = Book.query.all()
    book_list = [{"id": book.id, "title": book.title, "author": book.author, "price": book.price} for book in books]
    return jsonify(book_list)


# Get book details by ID
@books_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if book:
        book_info = {"id": book.id, "title": book.title, "author": book.author, "price": book.price}
        return jsonify(book_info)
    return jsonify({"message": "Book not found"}), 404


# Add a new book (admin only)
@books_bp.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    title = data['title']
    author = data['author']
    price = data['price']

    new_book = Book(title=title, author=author, price=price)
    db.session.add(new_book)
    db.session.commit()

    return jsonify({"message": "Book added successfully"})


# Update book details by ID (admin only)
@books_bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    title = data['title']
    author = data['author']
    price = data['price']

    book = Book.query.get(book_id)
    if book:
        book.title = title
        book.author = author
        book.price = price
        db.session.commit()
        return jsonify({"message": "Book updated successfully"})
    return jsonify({"message": "Book not found"}), 404


# Delete a book by ID (admin only)
@books_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book deleted successfully"})
    return jsonify({"message": "Book not found"}), 404

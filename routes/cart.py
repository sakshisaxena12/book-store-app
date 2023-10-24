from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import db, Cart, Book

cart_bp = Blueprint('cart', __name__)


# List items in the user's shopping cart
@cart_bp.route('/cart', methods=['GET'])
@jwt_required
def list_cart_items():
    current_user = get_jwt_identity()
    cart_items = Cart.query.filter_by(user_id=current_user).all()
    cart_item_details = []
    for item in cart_items:
        book = Book.query.get(item.book_id)
        if book:
            cart_item_details.append({'book_id': book.id, 'title': book.title, 'quantity': item.quantity})

    return jsonify(cart_items=cart_item_details), 200


# Add a book to the shopping cart
@cart_bp.route('/add_to_cart', methods=['POST'])
@jwt_required
def add_to_cart():
    current_user = get_jwt_identity()
    data = request.get_json()
    book_id = data.get('book_id')
    quantity = data.get('quantity', 1)

    book = Book.query.get(book_id)
    if not book:
        return jsonify(message="Book not found"), 404

    user_cart = Cart.query.filter_by(user_id=current_user, book_id=book.id).first()
    if user_cart:
        user_cart.quantity += quantity
    else:
        user_cart = Cart(user_id=current_user, book_id=book.id, quantity=quantity)

    db.session.add(user_cart)
    db.session.commit()
    return jsonify(message="Book added to cart successfully"), 200


# Update the quantity of a book in the shopping cart
@cart_bp.route('/update_item', methods=['PUT'])
@jwt_required
def update_cart_item():
    current_user = get_jwt_identity()
    data = request.get_json()
    book_id = data.get('book_id')
    new_quantity = data.get('quantity')

    book = Book.query.get(book_id)
    if not book:
        return jsonify(message='Book not found'), 404

    user_cart = Cart.query.filter_by(user_id=current_user, book_id=book.id).first()
    if not user_cart:
        return jsonify(message='Book is not in the cart'), 404

    user_cart.quantity = new_quantity
    db.session.commit()
    return jsonify(message='Cart item updated successfully'), 200


# Remove a book from the shopping cart
@cart_bp.route('/remove_item', methods=['DELETE'])
@jwt_required
def remove_cart_item():
    current_user = get_jwt_identity()
    cart_item_id = request.args.get('cart_item_id')
    cart_item = Cart.query.filter_by(id=cart_item_id, user_id=current_user).first()
    if not cart_item:
        return jsonify({"message": "Cart item not found"}), 404

    db.session.delete(cart_item)
    db.session.commit()
    return jsonify({"message": "Cart item removed"})

from flask import Blueprint, request, jsonify
from models import db, Order
from flask_jwt_extended import jwt_required, get_jwt_identity

orders_bp = Blueprint('orders', __name__)


# List orders for the current user
@orders_bp.route('/orders', methods=['GET'])
@jwt_required
def list_orders():
    current_user = get_jwt_identity()
    orders = Order.query.filter_by(user_id=current_user).all()
    order_list = [{"id": order.id, "status": order.status} for order in orders]
    return jsonify(order_list)


# Create a new order
@orders_bp.route('/add_order', methods=['POST'])
@jwt_required
def create_order():
    current_user = get_jwt_identity()
    data = request.get_json()
    status = data.get('status', 'pending')
    new_order = Order(user_id=current_user, status=status)
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Order created"})


# Get details of a specific order
@orders_bp.route('/orders/<int:order_id>', methods=['GET'])
@jwt_required
def get_order(order_id):
    current_user = get_jwt_identity()
    order = Order.query.filter_by(id=order_id, user_id=current_user).first()
    if not order:
        return jsonify({"message": "Order not found"}), 404

    order_info = {"id": order.id, "status": order.status}
    return jsonify(order_info)


# Update the status of a specific order
@orders_bp.route('/orders/<int:order_id>', methods=['PUT'])
@jwt_required
def update_order(order_id):
    current_user = get_jwt_identity()
    data = request.get_json()
    status = data.get('status')
    order = Order.query.filter_by(id=order_id, user_id=current_user).first()
    if not order:
        return jsonify({"message": "Order not found"}), 404

    order.status = status
    db.session.commit()
    return jsonify({"message": "Order updated"})


# Delete a specific order
@orders_bp.route('/orders/<int:order_id>', methods=['DELETE'])
@jwt_required
def delete_order(order_id):
    current_user = get_jwt_identity()
    order = Order.query.filter_by(id=order_id, user_id=current_user).first()
    if not order:
        return jsonify({"message": "Order not found"}), 404

    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted"})

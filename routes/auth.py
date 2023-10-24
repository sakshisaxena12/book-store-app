from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User

auth_bp = Blueprint('auth', __name__)


# User registration
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"message": "Username already exists"}), 400

    new_user = User(username=username, password=generate_password_hash(password))
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered"})


# User login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return jsonify(access_token=access_token, refresh_token=refresh_token)

    return jsonify({"message": "Invalid credentials"}), 401

# @auth_bp.route('/logout', methods=['POST'])
# @jwt_required
# def logout():
#     jti = get_raw_jwt()['jti']
#
#     if not is_token_blacklisted(jti):
#         blacklisted_tokens.add(jti)
#
#     return jsonify(message="Successfully logged out")


# Token refresh
# @auth_bp.route('/refresh', methods=['POST'])
# @jwt_refresh_token_required
# def refresh():
#     current_user = get_jwt_identity()
#     access_token = create_access_token(identity=current_user)
#     return jsonify(access_token=access_token)


# # User profile (protected route)
# @auth_bp.route('/profile', methods=['GET'])
# @jwt_required
# def user_profile():
#     current_user = get_jwt_identity()
#     return jsonify({"message": "User profile for".format(current_user)})

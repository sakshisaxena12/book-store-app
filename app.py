from flask import Flask
from flask_jwt_extended import JWTManager

from config import Config
from models import db
from routes import auth, books, cart, orders

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.config['SECRET_KEY'] = 'book_store_secret'

# Initialize the JWT manager
jwt = JWTManager(app)

# Create the database tables
with app.app_context():
    db.create_all()

app.register_blueprint(auth.auth_bp)
app.register_blueprint(books.books_bp)
app.register_blueprint(cart.cart_bp)
app.register_blueprint(orders.orders_bp)

if __name__ == '__main__':
    app.run(debug=True)

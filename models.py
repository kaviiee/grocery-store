from flask_login import UserMixin
from datetime import datetime
from extensions import db

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.Column(db.String, default="user", nullable=False)
    def __repr__(self):
        return '<User %r>' % self.id
    
class Categories(db.Model):
    id = db.Column(db.Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    img_url = db.Column(db.String, nullable=True)

class Products(db.Model):
    id = db.Column(db.Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    manufacture_date = db.Column(db.DateTime, nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=False)
    rate_per_unit=db.Column(db.Float, nullable=False)
    available_quantity=db.Column(db.Integer, nullable=False)
    category_id=db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=False)
    categories=db.relationship("Categories", backref='products', primaryjoin='Products.category_id == Categories.id')

class Carts(db.Model):
    id = db.Column(db.Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    creation_date = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String, nullable=False)
    users = db.relationship("Users", backref=db.backref("carts", lazy=True), primaryjoin='Carts.user_id == Users.id')

class Cart_items(db.Model):
    id = db.Column(db.Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey("carts.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    carts = db.relationship("Carts", backref=db.backref("cart_items", lazy=True), primaryjoin='Cart_items.cart_id == Carts.id')
    products = db.relationship("Products", backref=db.backref("cart_items", lazy=True), primaryjoin='Cart_items.product_id == Products.id')

class Transactions(db.Model):
    id = db.Column(db.Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), unique=True, nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Boolean, nullable=False)
    users=db.relationship("Users", backref=db.backref('transactions', lazy=True), primaryjoin='Transactions.user_id == Users.id')

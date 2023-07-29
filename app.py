from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery_store.db'
db=SQLAlchemy(app)
db.init_app(app)
app.app_context().push()

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String, nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Task %r>' % self.id
    
class Users(db.Model):
    id = db.Column(db.Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
class Transactions(db.Model):
    id = db.Column(db.Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey=("Users.id"), unique=True, nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    amount = db.Column(db.Boolean, nullable=False)
    users=db.relationship("Users", backref=db.backref('transactions', lazy=True))

class Products(db.Model):
    id = db.Column(db.Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey=("Users.id"), unique=True, nullable=False)
    transaction_date = db.Column(db.DateTime, nullable=False)
    amount = db.Column(db.Boolean, nullable=False)
    users=db.relationship("Users", backref=db.backref('transactions', lazy=True))

@app.route("/categories")
def categories():
    # Fetch all categories from the database?
    # Display a template with a list of categories
    pass

@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    # Add a new category to the database
    # Redirect to categories after successful addition
    pass

@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    # Edit an existing category in the database
    # Redirect to categories after successful edit
    pass

@app.route("/delete_category/<int:category_id>", methods=["POST"])
def delete_category(category_id):
    # Delete an existing category from the database
    # Redirect to categories after successful deletion
    pass

@app.route("/products")
def products():
    # Fetch all products from the database
    # Display a template with a list of products
    pass

@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    # Add a new product to the database
    # Redirect to products after successful addition
    pass

@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    # Edit an existing product in the database
    # Redirect to products after successful edit
    pass

@app.route("/delete_product/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    # Delete an existing product from the database
    # Redirect to products after successful deletion
    pass

@app.route("/search")
def search():
    # Implement search functionality based on user input
    # Display matching sections/products in the template
    pass

@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    # Add a product to the user's shopping cart
    # Redirect to the cart view after successful addition
    pass

@app.route("/cart")
def cart():
    # Display the user's shopping cart with selected products
    # Allow the user to remove items or proceed to checkout
    pass

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    # Process the user's cart and create a transaction record
    # Deduct quantities from the inventory, handle out of stock cases
    # Show the total amount to be paid for the transaction
    pass

if __name__ == "__main__":
    app.run(debug=True)
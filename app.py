from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exists
from flask_migrate import Migrate
from datetime import datetime

app = Flask(__name__)
app.secret_key="KEY"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery_store.db'
db=SQLAlchemy(app)
migrate=Migrate(app,db)
#db.init_app(app)
#app.app_context().push()
    
class Users(db.Model):
    id = db.Column(db.Integer, nullable=False, autoincrement=True, unique=True, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    is_admin = db.Column(db.String, default="user", nullable=False)
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

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Authenticate user credentials
        user = authenticate_user(username, password)

        if user:
            # Set user session and redirect to the appropriate page
            if user["is_admin"]=="admin":
                # Admin dashboard or manage sections/products page
                return redirect(url_for("admin_dashboard"))
            else:
                # Regular user dashboard or shopping page
                return redirect(url_for("user_dashboard"))
        #else:
           # flash("User does not exist. Please signup.", "error")

    return render_template("login.html")

# Helper function to authenticate user
def authenticate_user(username, password):
    # Get the user record from the database based on the username
    user = Users.query.filter_by(username=username).first()
    if user:
        # Check if the provided password matches the stored password
        if user.password == password:
            # Return the user's details if authenticated
            return {
                "id": user.id,
                "username": user.username,
                "is_admin": user.is_admin
            }
        else:
            flash("Invalid password, please try again.")

    else:
        flash("User does not exist, please signup.")
    # Return None if authentication fails
    return None

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        is_admin = request.form.get("role")
        # Check if the username is already taken
        if is_username_taken(username):
            flash("Username is already taken. Please choose a different username.", "error")
        else:
            # Create a new user in the database
            create_user(username, password, is_admin)
            flash("Account created successfully! Please login.", "success")
            return redirect(url_for("login"))

    return render_template("signup.html")

# Helper function to check if username is already taken
def is_username_taken(username):
    # Query the database to check if the username exists and return boolean output
    return db.session.query(exists().where(Users.username == username)).scalar()

# Helper function to create a new user in the database
def create_user(username, password, is_admin):
    # Create a new user object using the User model
    new_user = Users(username=username, password=password, is_admin=is_admin)

    # Add the new user to the database session
    db.session.add(new_user)

    try:
        # Commit the changes to the database
        db.session.commit()
        return True  # Return True to indicate success
    except:
        # Rollback the changes in case of an error
        db.session.rollback()
        return False  # Return False to indicate failure

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
    #db.create_all()
    app.run(debug=True)
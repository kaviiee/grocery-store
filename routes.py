from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import db, Users, Categories, Products, Carts, Cart_items, Transactions
from sqlalchemy import exists
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from extensions import login_manager

routes = Blueprint('routes', __name__)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@routes.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@routes.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Authenticate user credentials
        user = authenticate_user(username, password)

        if user:
            user_obj = Users.query.filter_by(username=username).first()

            # Log in the user using Flask-Login
            login_user(user_obj)
            if user["role"]=="admin":
                # Admin dashboard or manage sections/products page
                return redirect(url_for("routes.admin_home"))
            else:
                # Regular user dashboard or shopping page
                return redirect(url_for("routes.user_dashboard"))

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
                "role": user.role
            }
        else:
            flash("Invalid password, please try again.")

    else:
        flash("User does not exist, please signup.")
    # Return None if authentication fails
    return None

@routes.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role")
        # Check if the username is already taken
        if is_username_taken(username):
            flash("Username is already taken. Please choose a different username.", "error")
        else:
            # Create a new user in the database
            success=create_user(username, password, role)
            if success:
                flash("Account created successfully! Please login.", "success")
                return redirect(url_for("routes.login"))
            else:
                flash("There was an error creating your account, please try again", "failure")
                return redirect(url_for("routes.signup"))


    return render_template("signup.html")

# Helper function to check if username is already taken
def is_username_taken(username):
    # Query the database to check if the username exists and return boolean output
    return db.session.query(exists().where(Users.username == username)).scalar()

# Helper function to create a new user in the database
def create_user(username, password, role):
    # Create a new user object using the User model
    new_user = Users(username=username, password=password, role=role)

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

@routes.route("/admin_home", methods=["GET", "POST"])
@login_required
def admin_home():
    return render_template("admin_home.html")

@routes.route("/admin_categories")
@login_required
def admin_categories():
    cats=Categories.query.all()
    # Fetch all categories from the database?
    # Display a template with a list of categories
    return render_template("admin_categories.html", cats=cats)

@routes.route("/add_category", methods=["GET", "POST"])
def add_category():
    name = request.form.get("add_category")
    img_url = request.form.get("img_url")
    if category_exists(name):
        flash("Category already exists")
    else:
        success=create_category(name, img_url)
        if success:
            flash("Category successfully added", "success")
            return redirect(url_for("routes.admin_categories"))
        else:
            flash("Could not add category, please try again", "error")
            return redirect(url_for("routes.admin_categories"))
    return redirect(url_for("routes.admin_categories"))

def category_exists(name):
        return db.session.query(exists().where(Categories.name == name)).scalar()

def create_category(name, img_url):
     
    new_category = Categories(name=name, img_url=img_url)
    db.session.add(new_category)
    try:
        # Commit the changes to the database
        db.session.commit()
        return True  # Return True to indicate success
    except:
        # Rollback the changes in case of an error
        db.session.rollback()
        return False  # Return False to indicate failure

@routes.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    # Edit an existing category in the database
    # Redirect to categories after successful edit
    pass

@routes.route("/delete_category/<int:category_id>", methods=["POST"])
def delete_category(category_id):
    # Delete an existing category from the database
    # Redirect to categories after successful deletion
    pass

@routes.route("/products")
def products():
    # Fetch all products from the database
    # Display a template with a list of products
    return render_template("products.html")

@routes.route("/add_product", methods=["GET", "POST"])
def add_product():
    # Add a new product to the database
    # Redirect to products after successful addition
    pass

@routes.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    # Edit an existing product in the database
    # Redirect to products after successful edit
    pass

@routes.route("/delete_product/<int:product_id>", methods=["POST"])
def delete_product(product_id):
    # Delete an existing product from the database
    # Redirect to products after successful deletion
    pass

@routes.route("/search")
def search():
    # Implement search functionality based on user input
    # Display matching sections/products in the template
    pass

@routes.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    # Add a product to the user's shopping cart
    # Redirect to the cart view after successful addition
    pass

@routes.route("/cart")
def cart():
    # Display the user's shopping cart with selected products
    # Allow the user to remove items or proceed to checkout
    pass

@routes.route("/checkout", methods=["GET", "POST"])
def checkout():
    # Process the user's cart and create a transaction record
    # Deduct quantities from the inventory, handle out of stock cases
    # Show the total amount to be paid for the transaction
    pass
from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import db, Users, Categories, Products, Carts, Cart_items, Transactions
from sqlalchemy import exists
from datetime import datetime
from sqlalchemy.orm import joinedload
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
            flash("Category added successfully", "success")
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
    category = Categories.query.get_or_404(category_id)
    if request.method=="POST":
        category.name=request.form["edit_category"]
        category.img_url=request.form["img_url"]
        try:
            db.session.commit()
            flash("Category edited sucessfully", "success")
            return redirect(url_for("routes.admin_categories"))
        except:
            db.session.rollback()
            flash("Could not edit category, please try again", "error")
        return redirect(url_for("routes.admin_categories"))
    
    cats=Categories.query.all()
    return render_template("admin_categories.html", category=category, cats=cats)

@routes.route("/delete_category/<int:category_id>")
def delete_category(category_id):
    category = Categories.query.filter_by(id=category_id).first()
    db.session.delete(category)
    try:
        db.session.commit()
        flash("Category deleted sucessfully", "success")
        return redirect(url_for("routes.admin_categories"))
    except:
        db.session.rollback()
        flash("Could not delete category, please try again", "error")
        return redirect(url_for("routes.admin_categories"))
    return redirect(url_for("routes.admin_categories"))

@routes.route("/admin_products", methods=["GET", "POST"])
@login_required
def admin_products():
    if request.method == "POST":
        field = request.form.get("field")
        value = request.form.get("value")

        if field and value:
            if field == "category":
                # Handle category search differently
                category = Categories.query.filter_by(name=value).first()
                if category is None:
                    flash("Category does not exist. Please add the category or enter a valid category name", "failure")
                    return redirect(url_for("routes.admin_products"))

                products = category.products
                flash("Search successful", "success")
            else:
                attribute = getattr(Products, field)
                products = Products.query.options(joinedload(Products.categories)).filter(attribute==value).all()
                flash("Search successful", "success")

        else:
            flash("please enter a value", "error")
            products = Products.query.options(joinedload(Products.categories)).order_by(Products.category_id).all()
    else:
        products = Products.query.options(joinedload(Products.categories)).order_by(Products.category_id).all()
    if not products:
        flash("No Products found. Add them.","success")
    products_grouped = {}
    for product in products:
        category_name = product.categories.name
        if category_name not in products_grouped:
            products_grouped[category_name] = []
        products_grouped[category_name].append(product)
    # Fetch all products from the database
    # Display a template with a list of products
    return render_template("admin_products.html", products_grouped=products_grouped)

@routes.route("/add_product", methods=["GET", "POST"])
def add_product():
    name = request.form.get("add_product")
    category = request.form.get("category")
    manufacture_date = request.form.get("mfg_date")
    expiry_date = request.form.get("expiry_date")
    rate_per_unit = request.form.get("rate")
    unit = request.form.get("unit")
    available_quantity = request.form.get("qty")
    if product_exists(name):
        flash("Product already exists, edit it instead")
    else:
        success=create_product(name, category, manufacture_date, expiry_date, rate_per_unit, unit, available_quantity)
        if success:
            flash("Product added successfully", "success")
            return redirect(url_for("routes.admin_products"))
        else:
            flash("Could not add Product, please try again", "error")
            return redirect(url_for("routes.admin_products"))
    return redirect(url_for("routes.admin_products"))

def product_exists(name):
        return db.session.query(exists().where(Products.name == name)).scalar()

def create_product(name, category, manufacture_date, expiry_date, rate_per_unit, unit, available_quantity):
    category=Categories.query.filter_by(name=category).first()
    if category:
        manufacture_date = datetime.strptime(manufacture_date, '%Y-%m-%d').date()
        expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d').date()

        new_product = Products(name=name, manufacture_date=manufacture_date, expiry_date=expiry_date, rate_per_unit=rate_per_unit, unit=unit, available_quantity=available_quantity, category_id=category.id)
        db.session.add(new_product)
        try:
            # Commit the changes to the database
          db.session.commit()
          return True  # Return True to indicate success
        except Exception as e:
            # Rollback the changes in case of an error,
            db.session.rollback()
            print("Exception ", e)
            return False  # Return False to indicate failure
    else:
        flash('Category does not exist. Add it', "error")
        return False

@routes.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    prod = Products.query.get_or_404(product_id)
    if request.method=="POST":
        #prod.name=request.form["edit_product"]
        prod.name = request.form.get("edit_product")
        category = request.form.get("category")
        manufacture_date = request.form.get("mfg_date")
        expiry_date = request.form.get("expiry_date")
        prod.manufacture_date = datetime.strptime(manufacture_date, '%Y-%m-%d').date()
        prod.expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d').date()
        prod.rate_per_unit = request.form.get("rate")
        prod.unit = request.form.get("unit")
        prod.available_quantity = request.form.get("qty")
        prod.category_id=Categories.query.filter_by(name=category).first().id
        #category.img_url=request.form["img_url"]
        try:
            db.session.commit()
            flash("Product edited sucessfully", "success")
            return redirect(url_for("routes.admin_products"))
        except:
            db.session.rollback()
            flash("Could not edit category, please try again", "error")
        return redirect(url_for("routes.admin_products"))
    products = Products.query.options(joinedload(Products.categories)).order_by(Products.category_id).all()
    products_grouped = {}
    for product in products:
        category_name = product.categories.name
        if category_name not in products_grouped:
            products_grouped[category_name] = []
        products_grouped[category_name].append(product)
    return render_template("admin_products.html", prod=prod, products_grouped=products_grouped)


@routes.route("/delete_product/<int:product_id>")
def delete_product(product_id):
    prod = Products.query.filter_by(id=product_id).first()
    db.session.delete(prod)
    try:
        db.session.commit()
        flash("Product deleted sucessfully", "success")
        return redirect(url_for("routes.admin_products"))
    except:
        db.session.rollback()
        flash("Could not delete product, please try again", "error")
        return redirect(url_for("routes.admin_products"))
    return redirect(url_for("routes.admin_products"))

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

@routes.route("/admin_contactus")
def contactus():
    return render_template("admin_contactus.html")
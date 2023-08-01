from flask import Flask
from models import Users
from routes import routes
from extensions import login_manager, migrate, db
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

def create_app():
    app = Flask(__name__)
    app.secret_key = "KEY"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery_store.db'
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.login_view = 'routes.login'  # Set the login view function name
    login_manager.init_app(app)
    # Load the user object from the database
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    app.register_blueprint(routes)
    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)

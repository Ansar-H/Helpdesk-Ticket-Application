from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config


# Initialising the database and login manager
db = SQLAlchemy()
login_manager = LoginManager()
# Redirects to login view if the user is not authenticated
login_manager.login_view = 'auth.login'

def create_app(config_class=Config):
    # The factory function to create and configure the Flask app
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialising extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Importing and registering blueprints
    from app.routes.main import bp as main_bp
    from app.routes.auth import bp as auth_bp
    from app.routes.tickets import bp as tickets_bp

    # Main, Auth, and Ticket management routes
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(tickets_bp)

    # The user loader function for Flask-Login
    @login_manager.user_loader
    def load_user(id):
        # Loads a user from the db by ID
        from app.models import User
        return User.query.get(int(id))
    
    # Returns the configured app instance
    return app
from flask import Flask

from app.config import Config
from app.extensions import db, login_manager, bcrypt, migrate
from app.models import User


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please login to continue."
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))
    
    from app.auth.routes import auth_bp
    from app.dashboard.routes import dashboard_bp
    from app.transactions.routes import transaction_bp
    from app.categories.routes import category_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(category_bp)

    return app
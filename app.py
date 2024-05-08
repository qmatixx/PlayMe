from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_login import LoginManager
import os

db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()

login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"

def create_app():

    # create the app
    app = Flask(__name__)
    dir = os.path.abspath(os.path.dirname(__file__))
    db_path = os.path.join(dir, 'data', 'users.db')
    app.config['SQLALCHEMY_DATABASE_URI'] = str('sqlite:///' + db_path).replace('\\', '//')
    secret_key = os.urandom(32)
    app.config['SECRET_KEY'] = secret_key

    app.app_context().push()

    # initialize
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)   

    db.create_all()

    from view.routes import main
    from view.users_routes import users

    app.register_blueprint(main)
    app.register_blueprint(users)

    return app
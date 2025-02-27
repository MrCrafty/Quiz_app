from datetime import datetime
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_cors import CORS

db = SQLAlchemy()
DB_NAME = 'database.db'


def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True)
    app.secret_key = "this is the secret key for the app"
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    app.config['JWT_TOKEN_LOCATION'] = [
        'cookies', 'headers', 'json', 'query_string']
    jwt = JWTManager(app)

    # Login manager initializing and defining user_loader function to return the active user
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    from .models import User

    @login_manager.user_loader
    def user_loader(id):
        return User.query.get(int(id))

    # Loading and registering Routes that are created in different files

    from .auth import auth
    app.register_blueprint(auth, url_prefix="/")
    from .api import api
    app.register_blueprint(api, url_prefix="/api")
    create_database(app)
    with app.app_context():
        manager = User.query.filter_by(email="admin@store.com").all()
        if (manager == []):
            admin = User(email="admin@store.com",
                         password="adminmanager", role="admin")
            new_user = User(email="user@store.com",
                            password="useruser", role="user", xp={"name": "Store User", "address": "123 Main Street", "pincode": "123456"})
            db.session.add(admin)
            db.session.add(new_user)
            db.session.commit()
    return app


def create_database(app):
    if not path.exists('./' + DB_NAME):
        with app.app_context():
            db.create_all()
        print("Database created Successfully")

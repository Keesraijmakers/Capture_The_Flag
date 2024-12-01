from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "ctfdatabase"
DB_USER = "administrator"
DB_PASSWD = "Welkom!01"
DB_IP = "192.168.2.4"
DB_PORT = 3306


def create_website():
    website = Flask(__name__)
    website.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    website.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWD}@{DB_IP}:{DB_PORT}/{DB_NAME}"
    db.init_app(website)

    from .views import views
    from .auth import auth

    website.register_blueprint(views, url_prefix='/')
    website.register_blueprint(auth, url_prefix='/')

    from .models import student, challenges, studentpoints

    with website.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(website)

    @login_manager.user_loader
    def load_user(id):
        return student.query.get(int(id))

    return website
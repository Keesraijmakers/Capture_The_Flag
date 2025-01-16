#importing libraries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from kubernetes import config


#constants
db = SQLAlchemy()
DB_NAME = "ctfdatabasev2"
DB_USER = "administrator"
DB_PASSWD = "Welkom!01"
DB_IP = "192.168.2.4"
DB_PORT = 3306


#initation function
def create_website():
    #website
    website = Flask(__name__)
    #database
    website.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    website.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWD}@{DB_IP}:{DB_PORT}/{DB_NAME}"
    #kubernetes
    config.load_kube_config(config_file="/home/student/.kube/config")
    #instance
    db.init_app(website)
    #imports
    from .views import views
    from .auth import auth
    from .models import student, challenges, studentpoints, student_challenges
    #routing
    website.register_blueprint(views, url_prefix='/')
    website.register_blueprint(auth, url_prefix='/')
    #creating database coupling
    with website.app_context():
        db.create_all()
    #login manager 
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(website)

    @login_manager.user_loader
    def load_user(StudentNumber):
        return student.query.get(int(StudentNumber))

    return website
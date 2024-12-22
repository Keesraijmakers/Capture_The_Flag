#importing libraries
from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from .models import challenges, studentpoints, student
from .functions import get_username, get_nodes, get_pods, create_pod, delete_pods, label_pod, expose_pod, delete_service, get_address
import time

#routing
views = Blueprint('views', __name__)

#route home page
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    Challenges = challenges.query.all()
    return render_template("home.html", user=current_user, challenges=Challenges)

#route scoreboard
@views.route('/scoreboard', methods=['GET', 'POST'])
@login_required
def scoreboard():
    Students = student.query.all()
    Scoreboards = studentpoints.query.all()
    return render_template("scoreboard.html", user=current_user, students=Students, scoreboards=Scoreboards)

#route challenge
@views.route('/challenge/<id>', methods=['GET', 'POST'])
def challenge(id):  
    if request.method  == 'GET':
        Challenges = challenges.query.all()
        username = get_username(current_user)
        get_pods(username)
        delete_service(username)
        delete_pods(username)
        get_pods(username)
        create_pod(username)
        get_pods(username)
        time.sleep(10)
        get_pods(username)
        label_pod(username)
        expose_pod(username)
        address = get_address(username)
        return render_template("challenge.html", user=current_user, challengeid=int(id), challenges=Challenges, address=address)

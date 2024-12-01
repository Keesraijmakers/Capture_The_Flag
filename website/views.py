from flask import Blueprint, render_template
from flask_login import login_required, current_user
from . import db
from .models import challenges, studentpoints, student

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    Challenges = challenges.query.all()
    return render_template("home.html", user=current_user, challenges=Challenges)

@views.route('/scoreboard', methods=['GET', 'POST'])
@login_required
def scoreboard():
    Scoreboard = studentpoints.query.all()
    User = current_user.get_id()
    return render_template("scoreboard.html", user=current_user, User=User, scoreboards=Scoreboard)

@views.route('/challenge/<id>', methods=['GET', 'POST'])
def challenge(id):  
    Challenges = challenges.query.all()
    return render_template("challenge.html", user=current_user, challenge_id=id, challenges=Challenges)
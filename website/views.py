from flask import Blueprint, render_template
from flask_login import login_required, current_user
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
    Students = student.query.all()
    Scoreboards = studentpoints.query.all()
    return render_template("scoreboard.html", user=current_user, students=Students, scoreboards=Scoreboards)

@views.route('/challenge/<id>', methods=['GET', 'POST'])
def challenge(id):  
    Challenges = challenges.query.all()
    return render_template("challenge.html", user=current_user, challengeid=int(id), challenges=Challenges)
#importing libraries
from flask import Blueprint, render_template, request, flash
from flask_login import login_required, current_user
from .models import challenges, studentpoints, student_challenges
from .functions import get_username, create_pod, label_pod, expose_pod, connect_to_shellinabox, get_studentnumber, delete_namespace, get_ip_address, get_port_address
from . import db
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
    StudentPoints = studentpoints.query.order_by(studentpoints.TotalPoints.desc()).all()
    return render_template("scoreboard.html", user=current_user, studentpoints=StudentPoints)

#route challenge
@views.route('/challenge/<id>', methods=['GET', 'POST'])
def challenge(id):  
    if request.method  == 'GET':
        Challenges = challenges.query.all()
        username = get_username(current_user)
        create_pod(username,id)
        time.sleep(10)
        label_pod(username)
        expose_pod(username)
        challenge_address = get_ip_address(username)
        challenge_port = get_port_address(username)
        address = connect_to_shellinabox(challenge_port)
        return render_template("challenge.html", user=current_user, Challengenumber=int(id), challenges=Challenges, address=address, challenge_port=challenge_port, challenge_address=challenge_address)

    if request.method  == 'POST' and "stop_challenge" in request.form:
        Challenges = challenges.query.all()
        username = get_username(current_user)
        delete_namespace(username)
        return render_template("challenge.html", user=current_user, Challengenumber=int(id), challenges=Challenges)


    if request.method  == 'POST' and "hidden_flag"  in request.form:
        Challenges = challenges.query.all()
        username = get_username(current_user)
        studentnumber = get_studentnumber(current_user)
        Attempt_Hidden_flag = request.form.get('hidden_flag')
        DB_hidden_flag = db.session.execute(db.select(challenges.ChallengeFlag).filter_by(Challengenumber=int(id))).scalar_one()
        if str(Attempt_Hidden_flag) == str(DB_hidden_flag):
            flash('You found the hidden flag, well done', category='success')
            if not student_challenges.query.filter_by(StudentNumber=studentnumber, ChallengeNumber=int(id)).first():
                update_score = student_challenges(StudentNumber=studentnumber, ChallengeNumber=int(id), IsCompleted=1)
                db.session.add(update_score)
                db.session.commit()
        else:
            flash('Wrong hidden flag, please try again.', category='error')
        return render_template("challenge.html", user=current_user, Challengenumber=int(id), challenges=Challenges)

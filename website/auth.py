#importing libraries
from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import student, studentpoints
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


#routing
auth = Blueprint('auth', __name__)


#route login
@auth.route('/login', methods=['GET', 'POST'])
def login():
    #check user login function
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = student.query.filter_by(StudentUsername=username).first()
        if user:
            if check_password_hash(user.StudentPassword, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect login, try again.', category='error')
        else:
            flash('Incorrect login, try again.', category='error')

    return render_template("login.html", user=current_user)


#route logout
@auth.route('/logout')
@login_required
def logout():
    #log user out function
    logout_user()
    return redirect(url_for('auth.login'))


#route sign up
@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    #create user function
    if request.method == 'POST':
        username = request.form.get('Username')
        name = request.form.get('Name')
        studentnumber = request.form.get('StudentNumber')
        password1 = request.form.get('Password1')
        password2 = request.form.get('Password2')

        user = student.query.filter_by(StudentNumber=studentnumber).first()
        if user:
            flash('Studentnumber already exists.', category='error')
        elif len(username) < 4:
            flash('Username must be greater than 3 characters.', category='error')
        elif len(name) < 1:
            flash('Fill in name.', category='error')
        elif len(studentnumber) < 1:
            flash('Fill in studentnumber', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = student(StudentNumber=studentnumber, StudentUsername=username, StudentName=name, StudentPassword=generate_password_hash(
                password1, method='scrypt', salt_length=16))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)
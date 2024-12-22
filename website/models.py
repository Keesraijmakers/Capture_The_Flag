#importing libraries
from . import db
from flask_login import UserMixin

#creating a student model for database usage with UserMixin for authentication
class student(db.Model, UserMixin):
    StudentDBNumber = db.Column(db.Integer, primary_key=True)
    StudentNumber = db.Column(db.String(100), unique=True)
    StudentUsername = db.Column(db.String(100), unique=True)
    StudentName = db.Column(db.String(100))
    StudentPassword = db.Column(db.String(150))
    Challenge1 = db.Column(db.Integer, default=0)
    Challenge2 = db.Column(db.Integer, default=0)
    Challenge3 = db.Column(db.Integer, default=0)
    Challenge4 = db.Column(db.Integer, default=0)
    Challenge5 = db.Column(db.Integer, default=0)
    #creating a softlink for foreign key relation that doesn't exist in the database
    id = StudentDBNumber

#creating a challenge model for database usage
class challenges(db.Model):
    ChallengesId = db.Column(db.Integer, primary_key=True)
    ChallengeNumber = db.Column(db.Integer)
    ChallengeName = db.Column(db.String(100))
    ChallengeFlag = db.Column(db.Integer)
    ChallengeWorth = db.Column(db.Integer)

#creating a studenpoints model for database usage
class studentpoints(db.Model):
    StudentDBNumber = db.Column(db.Integer, primary_key=True)
    StudentName = db.Column(db.String(150))
    StudentNumber = db.Column(db.String(150))
    TotalScore = db.Column(db.Integer)
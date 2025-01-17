#importing libraries
from . import db
from flask_login import UserMixin

#creating a student model for database usage with UserMixin for authentication
class student(db.Model, UserMixin):
    StudentNumber = db.Column(db.Integer, primary_key=True)
    StudentUsername = db.Column(db.String(45), unique=True)
    StudentName = db.Column(db.String(45))
    StudentPassword = db.Column(db.String(250))
    studentchallenges = db.relationship('student_challenges')

    #function get id gives the StudenNumber as id for UserMixin login and authentication
    def get_id(self):
        return (self.StudentNumber)

#creating a challenge model for database usage
class challenges(db.Model):
    Challengenumber = db.Column(db.Integer, primary_key=True)
    ChallengeName = db.Column(db.String(45))
    ChallengeFlag = db.Column(db.String(45))
    ChallengeWorth = db.Column(db.Integer)
    ChallengeDescription = db.Column(db.String(800))
    studentchallenges = db.relationship('student_challenges')

#creating a student_challenges model for database usage
class student_challenges(db.Model):
    StudentNumber = db.Column(db.Integer, db.ForeignKey("student.StudentNumber"), primary_key=True)
    ChallengeNumber = db.Column(db.Integer, db.ForeignKey("challenges.Challengenumber"))
    IsCompleted = db.Column(db.Integer)

#creating a studenpoints model for database usage
class studentpoints(db.Model):
    StudentNumber = db.Column(db.Integer, primary_key=True)
    StudentUsername = db.Column(db.String(45))
    StudentName = db.Column(db.String(45))
    TotalPoints = db.Column(db.Integer)
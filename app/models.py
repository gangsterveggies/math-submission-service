from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
import enum

class SubmissionType(enum.Enum):
  wrong = 1
  correct = 2

class AccountType(enum.Enum):
  student = 1
  instructor = 2
  admin = 3

###
# Users
###

@login.user_loader
def load_user(id):
  return User.query.get(int(id))

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  last_seen = db.Column(db.DateTime, default=datetime.utcnow)
  account_type = db.Column(db.Enum(AccountType))
  submissions = db.relationship('Submission', backref='user', lazy='dynamic')

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  def problem_submissions(self, problem):
    return Submission.query.filter_by(
      user_id=self.id).filter_by(
        problem_id=problem.id).order_by(
          Submission.timestamp.desc())

  @staticmethod
  def is_admin(u):
    return u.is_authenticated and u.account_type == AccountType.admin

  def __repr__(self):
    return '<User {}>'.format(self.username)

class Problem(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(50))
  statement = db.Column(db.String(400))
  answer = db.Column(db.Integer)
  contest_id = db.Column(db.Integer, db.ForeignKey('contest.id'))
  submissions = db.relationship('Submission', backref='problem', lazy='dynamic')

  def __repr__(self):
    return '<Problem {}>'.format(self.title)

class Contest(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(50))
  problems = db.relationship('Problem', backref='contest', lazy='dynamic')
  start_date = db.Column(db.DateTime)
  end_date = db.Column(db.DateTime)

  def __repr__(self):
    return '<Contest {}>'.format(self.title)

class Submission(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  problem_id = db.Column(db.Integer, db.ForeignKey('problem.id'))
  result = db.Column(db.Enum(SubmissionType))
  answer = db.Column(db.Integer)
  timestamp = db.Column(db.DateTime, default=datetime.utcnow)

  def result_str(self):
    if self.result == SubmissionType.wrong:
      return "Wrong Answer"
    elif self.result == SubmissionType.correct:
      return "Correct Answer"
    else:
      raise Exception('Invalid SubmissionType {}'.format(str(self.result)))

  def check_answer(self, answer):
    if answer == self.problem.answer:
      self.result = SubmissionType.correct
    else:
      self.result = SubmissionType.wrong

  def __repr__(self):
    return '<Submission {} to {}>'.format(self.user, self.problem)

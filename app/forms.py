from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, DateTimeField, TextAreaField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember_me = BooleanField('Remember Me')
  submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  email = StringField('Email', validators=[DataRequired(), Email()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField(
    'Repeat Password', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Register')

  def validate_username(self, username):
    user = User.query.filter_by(username=username.data).first()
    if user is not None:
      raise ValidationError('Please use a different username.')

  def validate_email(self, email):
    user = User.query.filter_by(email=email.data).first()
    if user is not None:
      raise ValidationError('Please use a different email address.')

class NewContestForm(FlaskForm):
  title = StringField('Title', validators=[DataRequired()])
  start_date = DateTimeField('Start Date', validators=[DataRequired()])
  end_date = DateTimeField('End Date', validators=[DataRequired()])
  submit = SubmitField('Create Contest')

class NewProblemForm(FlaskForm):
  title = StringField('Title', validators=[DataRequired()])
  statement = TextAreaField('Statement', validators=[Length(min=0, max=400)])
  answer = IntegerField('Answer', validators=[DataRequired()])
  submit = SubmitField('Create Contest')

class SubmitProblemForm(FlaskForm):
  answer = IntegerField('Answer', validators=[DataRequired()])
  submit = SubmitField('Submit Answer')

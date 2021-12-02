from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm, NewContestForm, NewProblemForm
from app.models import User, AccountType, Contest, Problem
from app.helpers import admin_required
from datetime import datetime

@app.before_request
def before_request():
  if current_user.is_authenticated:
    current_user.last_seen = datetime.utcnow()
    db.session.commit()

@app.route('/')
@app.route('/index')
def index():
  contests = Contest.query.all()
  return render_template('index.html', contests=contests)

###
# Users
###

@app.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password')
      return redirect(url_for('login'))
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('index')
    return redirect(next_page)  
  return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
  logout_user()
  return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data, account_type=AccountType.student)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Congratulations, you are now a registered user!')
    return redirect(url_for('login'))
  return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
  user = User.query.filter_by(username=username).first_or_404()
  return render_template('user.html', user=user)

###
# Contests
###

@app.route('/contest/<contest_id>')
@login_required
def contest(contest_id):
  contest = Contest.query.filter_by(id=contest_id).first_or_404()
  return render_template('contest.html', contest=contest)

@app.route('/problem/<problem_id>')
@login_required
def problem(problem_id):
  problem = Problem.query.filter_by(id=problem_id).first_or_404()
  return render_template('problem.html', problem=problem)

@app.route('/new_contest', methods=['GET', 'POST'])
@admin_required
def new_contest():
  form = NewContestForm()
  if form.validate_on_submit():
    contest = Contest(title=form.title.data, start_date=form.start_date.data, end_date=form.end_date.data)
    db.session.add(contest)
    db.session.commit()
    flash('Contest created')
    return redirect(url_for('contest', contest_id=contest.id))
  return render_template('new_contest.html', title='Create Contest', form=form)

@app.route('/contest/<contest_id>/new_problem', methods=['GET', 'POST'])
@admin_required
def new_problem(contest_id):
  contest = Contest.query.filter_by(id=contest_id).first_or_404()
  form = NewProblemForm()
  if form.validate_on_submit():
    problem = Problem(title=form.title.data, statement=form.statement.data, answer=form.answer.data, contest=contest)
    db.session.add(problem)
    db.session.commit()
    flash('Problem created')
    return redirect(url_for('problem', problem_id=problem.id))
  return render_template('new_problem.html', title='New Contest', form=form)


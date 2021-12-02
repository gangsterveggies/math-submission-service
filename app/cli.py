import click, os
from datetime import datetime
from app import app, db
from app.models import User, AccountType, Problem, Contest, Submission

@app.cli.command('setup-debug')
@click.option('--confirm', prompt='This command resets all data from the databse (don\'t run in production!). Are you sure you want to do it? [y/N]')
def setup_debug(confirm):
  if confirm == 'y' or confirm == 'Y':
    click.echo('Deleting data from all tables')
    User.query.delete()
    Problem.query.delete()
    Contest.query.delete()
    Submission.query.delete()
    db.session.commit()

    click.echo('Setting up default admin with user/password: admin/admin')
    admin_user = User(username='admin', email='admin@admin.com', account_type=AccountType.admin)
    admin_user.set_password('admin')
    db.session.add(admin_user)
    db.session.commit()

    click.echo('Setting up default test with user/password: test/test')
    test_user = User(username='test', email='test@test.com', account_type=AccountType.student)
    test_user.set_password('test')
    db.session.add(test_user)
    db.session.commit()

    click.echo('Setting up default contest with dummy problem')
    contest = Contest(title='Test Contest', start_date=datetime.fromisoformat('2021-12-03T10:00:00'), end_date=datetime.fromisoformat('2021-12-03T14:00:00'))
    problem = Problem(title='2 + 2', statement='Add 2 to 2', answer=4, contest=contest)
    db.session.add(contest)
    db.session.add(problem)
    db.session.commit()

@app.cli.command('open-mail-server')
def open_mail_server():
  os.system('python -m smtpd -n -c DebuggingServer localhost:8025')

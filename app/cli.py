import click, os
from app import app, db
from app.models import User, AccountType, Problem, Contest

@app.cli.command('setup-debug')
@click.option('--confirm', prompt='This command resets all data from the databse (don\'t run in production!). Are you sure you want to do it? [y/N]')
def setup_debug(confirm):
  if confirm == 'y' or confirm == 'Y':
    click.echo('Deleting data from all tables')
    User.query.delete()
    Problem.query.delete()
    Contest.query.delete()
    db.session.commit()

    click.echo('Setting up default admin with user/password: admin/admin')
    admin = User(username='admin', email='admin@admin.com', account_type=AccountType.admin)
    admin.set_password('admin')
    db.session.add(admin)
    db.session.commit()

@app.cli.command('open-mail-server')
def open_mail_server():
  os.system('python -m smtpd -n -c DebuggingServer localhost:8025')

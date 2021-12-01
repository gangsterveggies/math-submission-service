import os
from app import app

@app.cli.command('open-mail-server')
def open_mail_server():
  os.system('python -m smtpd -n -c DebuggingServer localhost:8025')

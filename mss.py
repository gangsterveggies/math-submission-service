from app import app, db, cli
from app.models import User, Problem, Contest, Submission

@app.shell_context_processor
def make_shell_context():
  return {'db': db, 'User': User, 'Problem': Problem, 'Contest': Contest, 'Submission': Submission}

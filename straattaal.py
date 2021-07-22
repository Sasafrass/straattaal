"""Main entrypoint for the entire flask application."""
from app import create_app, db

from app.models import User, Word

app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Return the parameters used in an interactive command line session for testing purposes."""
    return {"db": db, "User": User, "Word": Word}

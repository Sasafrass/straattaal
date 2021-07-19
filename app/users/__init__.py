"""Main initialization entrypoint for the users blueprint."""
from flask import Blueprint

bp = Blueprint("users", __name__)

from app.users import routes

"""Main initialization entrypoint for the authentication blueprint."""
from flask import Blueprint

bp = Blueprint("auth", __name__)

from app.auth import routes

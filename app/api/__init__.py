"""Main initialization entrypoint for the API."""
from flask import Blueprint

bp = Blueprint("api", __name__)

from app.api import users, slang

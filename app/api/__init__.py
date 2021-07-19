from flask import Blueprint

from app.api import slang, users

bp = Blueprint("api", __name__)

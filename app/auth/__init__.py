from flask import Blueprint

from app.auth import routes

bp = Blueprint("auth", __name__)

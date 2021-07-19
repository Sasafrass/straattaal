from flask import Blueprint

from app.users import routes

bp = Blueprint("users", __name__)

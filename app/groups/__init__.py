from flask import Blueprint

from app.groups import routes

bp = Blueprint(
    "groups", __name__, static_folder="static"
)  # , static_url_path='/groups/static')

from flask import Blueprint

bp = Blueprint(
    "groups", __name__, static_folder="static"
)  # , static_url_path='/groups/static')

from app.groups import routes

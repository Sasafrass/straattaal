from flask import render_template
from app.users import bp


@bp.route("/main")
def main():
    return "Main users page."

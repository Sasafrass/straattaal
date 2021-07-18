from flask import redirect, render_template, url_for
from flask_login import current_user, login_required
from app.models import User
from app.users import bp


@bp.route("/main")
@login_required
def main():
    # Automatically redirect to the current user's profile.
    return redirect(url_for("users.users", username=current_user.username))


@bp.route("/<username>")
@login_required
def users(username):
    user = User.query.filter_by(username=username).first_or_404()

    return render_template("users/user.html", user=user)
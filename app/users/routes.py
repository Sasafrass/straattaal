"""Module containing all the routes for the users blueprint."""
from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.models import User, Word
from app.users import bp


# TODO: MOVE THIS VARIABLE SOMEWHERE ELSE.
WORDS_PER_PAGE = 25


@bp.route("/main")
@login_required
def main():
    """Implement main route for the users blueprint. Redirects to the current user."""
    # Automatically redirect to the current user's profile.
    return redirect(url_for("users.users", username=current_user.username))


@bp.route("/<username>")
@login_required
def users(username):
    """Implement the /users/username route to view any user's profile.
    
    Args:
        username: The username provided in the url for the desired user profile.
    """
    user = User.query.filter_by(username=username).first_or_404()
    user_id = user.get_id()
    page = request.args.get("page", 1, type=int)
    words = Word.query.filter_by(user_id=user_id).paginate(page, WORDS_PER_PAGE, False)

    # TODO: Find new way of passing the words and meanings e.g. as tuples.
        # Or just query the meanings db model instead.

    return render_template("users/user.html", user=user, words=words.items)


# articles = (
#     Article.query.filter_by(newspaper=newspaper)
#     .order_by(Article.published_date.desc().nullslast())
#     .paginate(page, POSTS_PER_PAGE, False)
# )

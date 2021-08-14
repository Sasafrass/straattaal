"""Module containing all the routes for the users blueprint."""
from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app import db
from app.models import Meaning, User, Word
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

    # To get both meaning and the actual word, we have to join the meaning and word tables.
    word_meanings = Meaning.query\
        .join(Word, Meaning.word_id==Word.id)\
        .add_columns(Word.word, Meaning.meaning)\
        .filter_by(user_id=user_id)\
        .paginate(page, WORDS_PER_PAGE, False)

    raw_sql_meanings = None
    # raw_sql_meanings = db.session.execute('SELECT meaning, word, meaning.user_id ' \
    #     'FROM meaning ' \
    #     'INNER JOIN word ' \
    #     'ON meaning.word_id = word.id')

    if raw_sql_meanings:
        return render_template("users/user.html", user=user, word_meanings=raw_sql_meanings)#.items)
    else:
        return render_template("users/user.html", user=user, word_meanings=word_meanings.items)


# articles = (
#     Article.query.filter_by(newspaper=newspaper)
#     .order_by(Article.published_date.desc().nullslast())
#     .paginate(page, POSTS_PER_PAGE, False)
# )

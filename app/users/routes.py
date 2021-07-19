from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required
from app.models import User, Slang
from app.users import bp


# TODO: MOVE THIS VARIABLE SOMEWHERE ELSE.
WORDS_PER_PAGE = 25


@bp.route("/main")
@login_required
def main():
    # Automatically redirect to the current user's profile.
    return redirect(url_for("users.users", username=current_user.username))


@bp.route("/<username>")
@login_required
def users(username):
    user = User.query.filter_by(username=username).first_or_404()
    user_id = user.get_id()
    page = request.args.get("page", 1, type=int)
    words = Slang.query.filter_by(user_id=user_id).paginate(page, WORDS_PER_PAGE, False)

    return render_template("users/user.html", user=user, words=words.items)


# articles = (
#     Article.query.filter_by(newspaper=newspaper)
#     .order_by(Article.published_date.desc().nullslast())
#     .paginate(page, POSTS_PER_PAGE, False)
# )

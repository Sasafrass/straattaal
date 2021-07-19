"""Module containing all routes that belong to the groups blueprint."""
from flask import redirect, render_template, url_for
from flask_login import login_required, current_user
from app.groups.forms import CreateGroupForm
from app import db
from app.models import Group
from app.groups import bp


@bp.route("/main", methods=["GET"])
@login_required
def groups():
    """Render the main groups route and page."""
    return render_template("groups/main.html", title="Groups")


@bp.route("/create", methods=["GET", "POST"])
@login_required
def create():
    """Render the route to create a new group."""
    form = CreateGroupForm()

    if form.validate_on_submit():
        # Process form
        user_id = current_user.get_id()
        group_name = form.group_name.data
        group = Group(name=group_name)

        db.session.add(group)
        db.session.commit()

        # TODO: Find the newly added corresponding group id.
        # TODO: Add user id and group id to groups table?
        # TODO: Or should that be done automatically with foreign key mapping?

        # TODO: Redirect to the new group page
        # return redirect(url_for("groups.groups"))

        return redirect(url_for("groups.groups"))

    return render_template("groups/create.html", title="Create Group", form=form)

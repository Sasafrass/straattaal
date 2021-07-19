"""Module containing all forms belonging to the groups blueprint."""
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CreateGroupForm(FlaskForm):
    """Create an HTML form to create a new group."""

    group_name = StringField("Group Name", validators=[DataRequired()])
    submit = SubmitField("Create Group")

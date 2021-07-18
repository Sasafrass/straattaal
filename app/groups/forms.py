from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class CreateGroupForm(FlaskForm):
    group_name = StringField("Group Name", validators=[DataRequired()])
    submit = SubmitField("Create Group")

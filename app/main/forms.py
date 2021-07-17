from flask_wtf import FlaskForm
from wtforms import SubmitField


class GenerateSlangForm(FlaskForm):
    submit = SubmitField("Generate Slang")

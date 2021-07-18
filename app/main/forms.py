from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class GenerateSlangForm(FlaskForm):
    """Submit form to generate a new slang word."""
    submit_generate = SubmitField("Generate Slang")


class MeaningForm(FlaskForm):
    """Submit form to persist your word and meaning to database."""
    word = StringField("Word", validators=[DataRequired()])
    meaning = StringField("Meaning")
    submit_meaning = SubmitField("Save Word And Meaning")
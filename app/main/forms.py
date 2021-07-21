"""Contains all forms displayed in the main blueprint."""
from flask_wtf import FlaskForm, FlaskForm
from wtforms import StringField, SubmitField, SelectField


class GenerateSlangForm(FlaskForm):
    """Submit form to generate a new slang word."""

    submit_generate = SubmitField("Generate Slang")


class ChooseModelField(FlaskForm):
    """Select form to choose the generator model."""

    def __init__(self, *args, **kwargs):
        super(ChooseModelField, self).__init__(*args, **kwargs)
        self.select_model.choices = [
            "Straattaal",
            "Plaatsnamen",
            "Nederlandse woorden",
            "Familienamen",
        ]
        self.select_model.default = "Straattaal"
        # print("REINITIALIZED")

    select_model = SelectField("Models")


class MeaningForm(FlaskForm):
    """Submit form to persist your word and meaning to database."""

    word = StringField("Word")  # , validators=[DataRequired()])
    meaning = StringField("Meaning")
    submit_meaning = SubmitField("Save Word And Meaning")

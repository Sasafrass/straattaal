"""Contains all forms displayed in the main blueprint."""
from flask_wtf import FlaskForm, FlaskForm
from wtforms import StringField, SubmitField, SelectField


class GenerateSlangForm(FlaskForm):
    """Submit form to generate a new slang word."""

    def set_button_text(self, model_type: str) -> str:
        """Build the text that will be set in the button depending on model type.
        
        Args:
            model_type: Type of the model that is being used.
        """

        button_text = f"Generate {model_type.capitalize()} Word"
        return button_text

    submit_generate = SubmitField()


class ChooseModelField(FlaskForm):
    """Select form to choose the generator model."""

    def __init__(self, *args, **kwargs):
        """Initialize a SelectField."""
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

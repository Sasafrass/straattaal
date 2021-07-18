import requests
from flask import render_template
from app import db
from app.main import bp
from app.main.forms import GenerateSlangForm, MeaningForm


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
def index():
    generate_slang_form = GenerateSlangForm()
    meaning_form = MeaningForm()

    kwargs = {
        'title': 'Home',
        'generate_slang_form': generate_slang_form,
        'meaning_form': meaning_form,
    }

    if generate_slang_form.submit_generate.data and generate_slang_form.validate():
        # TODO: Might be overkill to use an API call here rather than internal call.
        response = requests.get("http://localhost:5000/api/generate_slang")
        response = response.json()
        slang_word = response["slang_word"]
        meaning_form.word.data = slang_word

        return render_template(
            "index.html", 
            slang_word=slang_word, 
            **kwargs,
        )

    if meaning_form.submit_meaning.data and meaning_form.validate():
        print("Successfully submitted the meaning form")

        return render_template(
            "index.html", 
            **kwargs,
        )

    return render_template(
        "index.html", 
        slang_word="", 
        **kwargs
        )

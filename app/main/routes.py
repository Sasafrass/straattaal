import requests
from flask import render_template
from app import db
from app.main import bp
from app.main.forms import GenerateSlangForm


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
def index():
    form = GenerateSlangForm()

    if form.validate_on_submit():
        # TODO: Might be overkill to use an API call here rather than internal call.
        response = requests.get("http://localhost:5000/api/generate_slang")
        response = response.json()
        slang_word = response["slang_word"]

        return render_template(
            "index.html", title="Home", slang_word=slang_word, form=form
        )

    return render_template("index.html", title="Home", slang_word="", form=form)

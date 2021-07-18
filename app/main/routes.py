import requests
from flask import flash, redirect, render_template, session, url_for
from flask_login import login_required, current_user
from app import db
from app.main import bp
from app.main.forms import GenerateSlangForm, MeaningForm
from app.models import Slang


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
@login_required
def index():
    generate_slang_form = GenerateSlangForm()
    meaning_form = MeaningForm()

    # Frequently used keyword arguments for rendering templates.
    kwargs = {
        "title": "Home",
        "generate_slang_form": generate_slang_form,
        "meaning_form": meaning_form,
    }

    if generate_slang_form.submit_generate.data and generate_slang_form.validate():
        # TODO: Might be overkill to use an API call here rather than internal call.
        response = requests.get("http://localhost:5000/api/generate_slang")
        response = response.json()
        slang_word = response["slang_word"]

        # Set slang word in meaning_form for visual purposes and in session for retrieval.
        meaning_form.word.data = slang_word
        session["slang_word"] = slang_word

        return render_template(
            "index.html",
            slang_word=slang_word,
            **kwargs,
        )

    elif meaning_form.submit_meaning.data and meaning_form.validate():

        # Persist word and meaning to database.
        slang_word = session.get("slang_word", None)
        user_id = current_user.get_id()

        if not slang_word:
            flash("You haven't generated a slang word yet...")
            return redirect(url_for("main.index"))

        word_and_meaning = Slang(
            word=slang_word,
            meaning=meaning_form.meaning.data,
            user_id=user_id,
        )
        db.session.add(word_and_meaning)
        db.session.commit()

        del session['slang_word']

        return render_template(
            "index.html",
            **kwargs,
        )

    return render_template("index.html", slang_word="", **kwargs)


@bp.route("/set/")
def set():
    """Route to test setting a value in session management."""
    session["key"] = "value"
    return "ok"


@bp.route("/get")
def get():
    """Route to test getting a value in session management."""
    return session.get("key", "not set")

"""Module containing all the routes for the main blueprint."""
# import requests
from flask import flash, redirect, render_template, session, url_for
from flask_login import login_required, current_user
from wtforms.validators import ValidationError
from app import db
from app.api.slang import generate_slang_internal
from app.main import bp
from app.main.forms import GenerateSlangForm, MeaningForm, ChooseModelField
from app.models import Meaning, Model, Word


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
@login_required
def index():
    """Implement the index route for the main blueprint - serves as the homepage."""
    generate_slang_form = GenerateSlangForm()
    meaning_form = MeaningForm()
    model_form = ChooseModelField()

    # Frequently used keyword arguments for rendering templates.
    kwargs = {
        "title": "Home",
        "generate_slang_form": generate_slang_form,
        "meaning_form": meaning_form,
        "model_form": model_form,
    }

    if model_form.validate():
        print(f"Was selected : {model_form.select_model.data}")
        model_type = model_form.select_model.data
        model_form.select_model.object_data = model_type
        session["model_type"] = model_type

    # Persist model_type through re-clicking generate_slang and other refreshing
    if "model_type" in session:
        model_type = session["model_type"]
        model_form.select_model.object_data = model_type
        model_form.select_model.data = model_type
    # If we haven't seta single model_type, set default.
    else:
        model_type = model_form.select_model.default
        session["model_type"] = model_type

    # Change generate_slang_form button text.
    generate_slang_form.submit_generate.label.text = generate_slang_form.set_button_text(model_type=model_type)

    if generate_slang_form.submit_generate.data and generate_slang_form.validate():
        # # TODO: Might be overkill to use an API call here rather than internal call.
        # response = requests.get("http://localhost:5000/api/generate_slang")
        # response = response.json()
        # slang_word = response["slang_word"]
        slang_word = generate_slang_internal(session.get("model_type", None))

        # Set slang word in meaning_form for visual purposes and in session for retrieval.
        meaning_form.word.data = slang_word
        session["slang_word"] = slang_word

        return render_template(
            "index.html",
            slang_word=slang_word,
            model_type=model_type,
            **kwargs,
        )

    elif meaning_form.submit_meaning.data and meaning_form.validate():

        # Persist word and meaning to database.
        slang_word = session.get("slang_word", None)
        model_type = session.get("model_type", None)
        meaning = meaning_form.meaning.data
        user_id = current_user.get_id()

        if not slang_word:
            flash("You haven't generated a slang word yet...")
            return redirect(url_for("main.index"))

        # TODO: Refactor this database persistence functionality to a separate method.
        # Check if our model_type already exists in database, if not: create.
        model = Model.query.filter_by(model_type=model_type).first()
        if model is None:
            model_db_model = Model(
                model_type=model_type
            )
            db.session.add(model_db_model)
            db.session.commit()
            model = Model.query.filter_by(model_type=model_type).first()
            # Check for persistence:
            # TODO: Potentially flush and/or refresh db session.
            if model is None:
                raise ValidationError("Model should've been added. Please flush or refresh.")
        model_id = model.id

        # Check if our word already exists in database, if not: create.
        word = Word.query.filter_by(word=slang_word).first()
        if word is None:
            word_db_model = Word(
                word=slang_word,
                model_id=model_id,
                user_id=user_id,
            )
            db.session.add(word_db_model)
            db.session.commit()
            # Check for persistence:
            # TODO: Potentially flush and/or refresh db session.
            word = Word.query.filter_by(word=slang_word).first()
            if model is None:
                raise ValidationError("Word should've been added. Please flush or refresh.")
        word_id = word.id

        # Update the meaning table.
        meaning_db_model = Meaning(
            meaning=meaning,
            user_id=user_id,
            word_id=word_id,
        )
        db.session.add(meaning_db_model)
        db.session.commit()

        del session["slang_word"]

        return render_template(
            "index.html",
            model_type=model_type,
            **kwargs,
        )

    return render_template("index.html", slang_word="", model_type=model_type, **kwargs)


@bp.route("/set/")
def set():
    """Route to test setting a value in session management."""
    session["key"] = "value"
    return "ok"


@bp.route("/get")
def get():
    """Route to test getting a value in session management."""
    return session.get("key", "not set")

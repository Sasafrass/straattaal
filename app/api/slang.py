from flask import jsonify
from app.api import bp

from app.ml_models.rnn.loaded_rnn_model import return_loaded_model, load_model
from app.ml_models.rnn.helpers import random_choice
from app.ml_models.rnn.generate import generate_word


@bp.route("/generate_slang", methods=["GET"])
def generate_slang():
    """Generate and return a new slang word."""

    # TODO Should not load model every time a word is queried
    # I know nothing of flask, can we save the model upon starting the app?

    model, dataset = load_model()

    new_word = generate_word(
        model=model,
        dataset=dataset,
        start_letter='random',
        max_len=20,  # TODO: Fix this.
        temperature=0.3,
    )

    # TODO: Return a json containing the word.
    ret = jsonify(slang_word=new_word)

    return ret

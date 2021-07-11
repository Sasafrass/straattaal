from flask import jsonify
from app.api import bp

from app.ml_models.rnn.loaded_rnn_model import return_loaded_model
from app.ml_models.rnn.helpers import random_choice
from app.ml_models.rnn.generate import generate_word


@bp.route("/generate_slang", methods=["GET"])
def generate_slang():
    """Generate and return a new slang word."""
    model, ALL_LETTERS = return_loaded_model()
    N_LETTERS = len(ALL_LETTERS) + 1

    new_word = generate_word(
        model=model,
        N_LETTERS=N_LETTERS,
        ALL_LETTERS=ALL_LETTERS,
        start_letter=random_choice(ALL_LETTERS),
        maxn=20,  # TODO: Fix this.
        temp=1,  # TODO: Fix the temperature.
    )

    # TODO: Return a json containing the word.
    ret = jsonify(slang_word=new_word)

    return ret

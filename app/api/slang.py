from flask import jsonify
from app.api import bp

from app.ml_models.rnn.loaded_rnn_model import return_loaded_model
from app.ml_models.rnn.generate import generate_word

N_LETTERS = 27  # TODO: Fix the hardcoded number of letters.
ALL_LETTERS = (
    "vtdlcg bnuhrzmjskpefiçxoway"  # TODO: Fix the hardcoded set of ALL letters.
)


@bp.route("/generate_slang", methods=["GET"])
def generate_slang():
    """Generate and return a new slang word."""
    model = return_loaded_model()
    
    new_word = generate_word(
        model=model,
        N_LETTERS=N_LETTERS,
        ALL_LETTERS=ALL_LETTERS,
        start_letter="l",  # TODO: Fix this to random letter.
        maxn=20,  # TODO: Fix this.
        temp=0.5,  # TODO: Fix the temperature.
    )

    # TODO: Return a json containing the word.
    ret = jsonify(slang_word=new_word)

    return ret

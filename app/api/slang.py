"""Functionality to generate slang words."""
from flask import jsonify, session
from app.api import bp

from app.ml_models.rnn.loaded_rnn_model import load_model
from app.ml_models.rnn.data_tools import WordLevelDataset
from app.ml_models.rnn.generate import generate_word


@bp.route("/generate_slang", methods=["GET"])
def generate_slang():
    """Generate and return a new slang word."""
    # Return a json containing the newly generated word.
    new_word = generate_slang_internal()
    ret = jsonify(slang_word=new_word)

    return ret


def generate_slang_internal():
    """Implement internal call to generate and return a new slang word instead of API call."""
    # Retrieve model from the session if it's already stored there.
    if not (
        session.get("model", None)
        and session.get("vocab", None)
        and session.get("dataset", None)
    ):
        print("Model isn't stored in session! Loading...")
        model, vocab = load_model()
        session["model"] = model
        session["vocab"] = vocab

        # Load both "existing" Dutch words and straattaal words to check
        existing = WordLevelDataset(
            prefix="data",
            filename_datasets=["straattaal.txt", "dutch.txt"],
            vocabulary=vocab,
        ).all_words_to_set()
        session["dataset"] = existing
    else:
        print("Retrieving model from the session...")
        model = session["model"]
        vocab = session["vocab"]
        existing = session["dataset"]

    found_one = False
    max_words = 10

    for _ in range(max_words):
        new_word = generate_word(
            model=model,
            vocabulary=vocab,
            start_letter="random",
            max_len=20,  # TODO: Fix this. (?)
            temperature=0.3,
        )
        if new_word not in existing:
            found_one = True
            break
    if not found_one:
        print(f"Warning! Could not find a non-existing word with n={max_words}")

    return new_word

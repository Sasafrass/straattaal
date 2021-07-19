from flask import jsonify

from app.api import bp
from app.ml_models.rnn.data_tools import WordLevelDataset
from app.ml_models.rnn.generate import generate_word
from app.ml_models.rnn.loaded_rnn_model import load_model


@bp.route("/generate_slang", methods=["GET"])
def generate_slang():
    """Generate and return a new slang word."""

    # TODO Should not load model every time a word is queried
    # I know nothing of flask, can we save the model upon starting the app?

    model, vocab = load_model()

    # TODO Same as above, should not load dataset every time a word is queried.

    # Load both "existing" Dutch words and straattaal words to check
    existing = WordLevelDataset(
        prefix="data",
        filename_datasets=["straattaal.txt", "dutch.txt"],
        vocabulary=vocab,
    ).all_words_to_set()
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
    # TODO: Return a json containing the word.
    ret = jsonify(slang_word=new_word)

    return ret

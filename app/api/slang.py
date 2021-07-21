"""Functionality to generate slang words."""
from collections import defaultdict

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


def generate_slang_internal(model_type=None):
    """Implement internal call to generate and return a new slang word instead of API call."""

    # Functionality to convert model selection to filename for load_model.
    model_filename_dict = {
        "Straattaal": "2021_straattaal_epoch100.pt",
        "Plaatsnamen": "plaatsnamen_epoch10.pt",
        "Nederlandse woorden": "pretrained_dutch_epoch3.pt",
        "Familienamen": "familienamen_epoch4.pt",
    }
    vocab_filename_dict = defaultdict(lambda: "vocabulary.txt")
    vocab_filename_dict["Familienamen"] = "vocabulary_extended.txt"

    # Up to interpretation: which do we consider "existing"?
    existing_dict = defaultdict(
        lambda: ["straattaal.txt", "dutch.txt", "plaatsnamen.txt"]
    )
    existing_dict["Familienamen"] = ["familienamen.txt"]

    # Retrieve model from the session if it's already stored there.
    if not (
        session.get("model" + model_type, None)
        and session.get("vocab" + model_type, None)
        and session.get("dataset", None)
    ):
        print("Model isn't stored in session! Loading...")
        model, vocab = load_model(
            model_filename_dict[model_type],
            filename_vocab=vocab_filename_dict[model_type],
        )
        session["model" + model_type] = model
        session["vocab" + model_type] = vocab

        # Load both "existing" Dutch words and straattaal words to check
        existing = WordLevelDataset(
            prefix="data",
            filename_datasets=existing_dict[model_type],
            vocabulary=vocab,
        ).all_words_to_set()
        session["dataset"] = existing
    else:
        print("Retrieving model from the session...")
        model = session["model" + model_type]
        vocab = session["vocab" + model_type]
        existing = session["dataset"]

    found_one = False
    max_words = 10

    for _ in range(max_words):
        new_word = generate_word(
            model=model,
            vocabulary=vocab,
            start_letter="random",
            max_len=20,  # TODO: Fix this. (?)
            temperature=0.35,
        )
        if new_word not in existing:
            found_one = True
            break
    if not found_one:
        print(f"Warning! Could not find a non-existing word with n={max_words}")

    return new_word

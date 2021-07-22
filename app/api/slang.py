"""Functionality to generate slang words."""
from collections import defaultdict

from flask import jsonify, session
from app.api import bp

from app.ml_models.rnn.loaded_rnn_model import load_model
from app.ml_models.rnn.data_tools import WordLevelDataset
from app.ml_models.rnn.vocabulary import Vocabulary
from app.ml_models.rnn.generate import generate_word

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
existing_dict = defaultdict(lambda: ["straattaal.txt", "dutch.txt", "plaatsnamen.txt"])
existing_dict["Familienamen"] = ["familienamen.txt"]


@bp.route("/generate_slang", methods=["GET"])
def generate_slang():
    """Generate and return a new slang word."""
    # Return a json containing the newly generated word.
    new_word = generate_slang_internal()
    ret = jsonify(slang_word=new_word)

    return ret


def _retrieve_info_from_session(model_type: str):
    """Retrieve model from the session if it's already stored there.

    Args:
        model_type: Model name for storing/looking up the associated model, vocabulary and "illegal" dataset.
    """
    if not (
        session.get("model" + model_type, None)
        and session.get("vocab" + model_type, None)
        and session.get("dataset" + model_type, None)
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
        session["dataset" + model_type] = existing
    else:
        print("Retrieving model from the session...")
        model = session["model" + model_type]
        vocab = session["vocab" + model_type]
        existing = session["dataset" + model_type]
    return model, vocab, existing


def generate_nonexistent_word(model: nn.Module, vocab: Vocabulary, existing: set, max_words=10) -> str:
    """Try to generate a nonexistent word using the provided model.

    Args:
        model: Recurrent model.
        vocab: Vocabulary object.
        existing: Set of words we don't want to generate.
        max_words: Maximum amount of attempts at generating a novel word.
    """
    found_one = False

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


def generate_slang_internal(model_type: str = None) -> str:
    """Implement internal call to generate and return a new slang word instead of API call.

    Args:
        model_type: string representing the type of the pre-trained model.
                    One of [Straattaal, Plaatsnamen, Nederlandse woorden, Familienamen]
    """
    info = _retrieve_info_from_session(model_type)
    new_word = generate_nonexistent_word(*info, max_words=10)

    # Proper capitalization
    if model_type == "Plaatsnamen":
        new_word = " ".join(subword.capitalize() for subword in new_word.split())
    elif model_type == "Familienamen":
        subnames = new_word.split()
        new_word = " ".join(
            subword.capitalize() if i == len(subnames) - 1 else subword
            for i, subword in enumerate(subnames)
        )
    return new_word

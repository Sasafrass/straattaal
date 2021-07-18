import os

import torch

from app.ml_models.rnn.vocabulary import Vocabulary
from app.ml_models.rnn.rnn_model import RNN, RNNAnna


def load_model(
    filename_model: str = "2021_straattaal_epoch100.pt",
    filename_vocab: str = "vocabulary.txt",
    device: str = "cpu",
):
    """
    From a given path for filename of the model and the vocabulary, loads a model and vocabulary for inference.
    The vocabulary size should be the same as the model vocabulary size, otherwise an error is thrown.

    Args:
        model_name: Filename of the model.
        filename_vocab: Filename of the vocabulary.
        device: CUDA device name to map to, probably 'cpu'.
    """
    path = os.path.join(os.path.abspath(os.getcwd()), "app", "ml_models", "rnn")
    path_model = os.path.join(path, filename_model)
    path_vocab = os.path.join(os.path.abspath(os.getcwd()), "data", filename_vocab)

    v = Vocabulary()
    v.load(prefix=".", filename_vocab=path_vocab)

    checkpoint = torch.load(path_model, map_location=torch.device(device))
    checkpoint_model = checkpoint["model_state_dict"]
    model_vocab_size, embedding_size = checkpoint_model["_embedding.weight"].shape

    # Will work for single-layer RNNs for now.
    hidden_size = checkpoint_model["lstm.bias_hh_l0"].shape[0]
    if embedding_size != v.size:
        raise ValueError(
            f"Model vocab size {model_vocab_size} does not match vocabulary file size {v.size}"
        )
    m = RNNAnna(v.size, hidden_size, embedding_size=embedding_size)
    m.load_state_dict(checkpoint_model)
    m.eval()
    return m, v


def return_loaded_model():
    # Variables for trained RNN model.
    n_hidden = 128  # TODO: Fix the hardcoded hidden dimensionality.

    # Construct correct path to model file.
    # TODO: Fix the hardcoded cwd path!
    cwd_path = os.path.abspath(os.getcwd())
    cwd_path = os.path.join(cwd_path, "app", "ml_models", "rnn")
    timestamp = "2019-11072021"
    model_path = timestamp + "_straattaal.pth"
    letter_path = timestamp + "_all_letters.txt"

    final_letter_path = os.path.join(cwd_path, letter_path)
    with open(final_letter_path, "r") as file:
        all_letters = file.read()
    n_letters = len(all_letters) + 1

    final_model_path = os.path.join(cwd_path, model_path)
    # Actually load the model.
    model = RNN(n_letters, n_hidden, n_letters)
    model.load_state_dict(torch.load(final_model_path))
    model.eval()

    return model, all_letters

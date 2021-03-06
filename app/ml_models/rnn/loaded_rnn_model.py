"""Code to load pytorch models."""
import os
from typing import List

import torch

from app.ml_models.rnn.vocabulary import Vocabulary
from app.ml_models.rnn.rnn_model import RNN, RNNAnna


def load_model(
    filename_model: str = "2021_straattaal_epoch100.pt",
    filename_vocab: str = "vocabulary.txt",
    device: str = "cpu",
    extra_path: List[str] = [],
    abs_path: bool = False,
):
    """From a given path for filename of the model and the vocabulary, loads a model and vocabulary for inference.

    The vocabulary size should be the same as the model vocabulary size, otherwise an error is thrown.

    Args:
        model_name: Filename of the model.
        filename_vocab: Filename of the vocabulary.
        device: CUDA device name to map to, probably 'cpu'.
        extra_path: Relative path to squeeze between cwd and "app". Used for notebooks.
        abs_path: Whether to use the exact path filenames (handy during training from python script).
    """
    path = os.path.join(
        os.path.abspath(os.getcwd()),
        *extra_path,
        "app",
        "ml_models",
        "rnn",
        "pretrained",
    )
    path_model = os.path.join(path, filename_model) if not abs_path else filename_model
    path_vocab = (
        os.path.join(os.path.abspath(os.getcwd()), *extra_path, "data", filename_vocab)
        if not abs_path
        else filename_vocab
    )

    v = Vocabulary()
    v.load(prefix=".", filename_vocab=path_vocab)
    m = init_torch_model_from_path(path_model, v, device=device)
    m.eval()
    return m, v


def init_torch_model_from_path(path_model: str, v: Vocabulary, device: str = "cpu"):
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
    return m


def return_loaded_model():
    """Legacy model loader."""
    # Variables for trained RNN model.
    n_hidden = 128  # TODO: Fix the hardcoded hidden dimensionality.

    # Construct correct path to model file.
    # TODO: Fix the hardcoded cwd path!
    cwd_path = os.path.abspath(os.getcwd())
    cwd_path = os.path.join(cwd_path, "app", "ml_models", "rnn", "pretrained")
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

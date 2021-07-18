import os

import torch

from app.ml_models.rnn.data_tools import WordLevelDataset
from app.ml_models.rnn.rnn_model import RNN, RNNAnna


def load_model(model_name: str = "2021_straattaal_epoch100.pt", device: str = "cpu"):
    """
    Args:
        model_name: Filename of the model.
        device: CUDA device name to map to, probably cpu.
    """
    path = os.path.join(os.path.abspath(os.getcwd()), "app", "ml_models", "rnn")
    path = os.path.join(path, model_name)
    dataset = WordLevelDataset("data/", "straattaal.txt")
    # TODO: Fix hardcoded hidden size
    m = RNNAnna(dataset.vocabulary_size, 128)
    checkpoint = torch.load(path, map_location=torch.device(device))
    m.load_state_dict(checkpoint["model_state_dict"])
    m.eval()
    return m, dataset


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

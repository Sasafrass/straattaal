import os
import torch
from app.ml_models.rnn.rnn_model import RNN


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

import os
import torch
from app.ml_models.rnn.rnn_model import RNN


def return_loaded_model():
    # Variables for trained RNN model.
    n_hidden = 128  # TODO: Fix the hardcoded hidden dimensionality.
    n_letters = 27  # TODO: Fix the hardcoded number of letters.

    # Construct correct path to model file.
    # TODO: Fix the hardcoded cwd path!
    cwd_path = os.path.abspath(os.getcwd())
    cwd_path = os.path.join(cwd_path, "app", "ml_models", "rnn")
    model_path = "2337-26062021_model.pth"
    PATH = os.path.join(cwd_path, model_path)

    # Actually load the model.
    model = RNN(n_letters, n_hidden, n_letters)
    model.load_state_dict(torch.load(PATH))
    model.eval()

    return model

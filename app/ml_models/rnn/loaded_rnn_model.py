import os
import torch
from app.ml_models.rnn.rnn_model import RNN, RNNAnna
from app.ml_models.rnn.data_tools import WordLevelDataset


def load_model(model_name='pretrained_NL_epoch5.pt'):
    path = os.path.join(os.path.abspath(os.getcwd()),
                        "app", "ml_models", "rnn")
    path = os.path.join(path, model_name)
    dataset = WordLevelDataset('data/', 'straattaal.txt')
    # TODO: Fix hardcoded hidden size
    m = RNNAnna(dataset.vocabulary_size, 128)
    checkpoint = torch.load(path)
    m.load_state_dict(checkpoint['model_state_dict'])
    m.eval()
    return m, dataset


def return_loaded_model():
    # Variables for trained RNN model.
    n_hidden = 128  # TODO: Fix the hardcoded hidden dimensionality.

    # Construct correct path to model file.
    # TODO: Fix the hardcoded cwd path!
    cwd_path = os.path.abspath(os.getcwd())
    cwd_path = os.path.join(cwd_path, "app", "ml_models", "rnn")
    timestamp = '2019-11072021'
    model_path = timestamp + '_straattaal.pth'
    letter_path = timestamp + '_all_letters.txt'

    final_letter_path = os.path.join(cwd_path, letter_path)
    with open(final_letter_path, 'r') as file:
        all_letters = file.read()
    n_letters = len(all_letters) + 1

    final_model_path = os.path.join(cwd_path, model_path)
    # Actually load the model.
    model = RNN(n_letters, n_hidden, n_letters)
    model.load_state_dict(torch.load(final_model_path))
    model.eval()

    return model, all_letters

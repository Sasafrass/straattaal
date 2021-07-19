"""Functionality for locally training files."""
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from app.ml_models.rnn.data_tools import WordLevelDataset
from app.ml_models.rnn.vocabulary import Vocabulary
from app.ml_models.rnn.train import train
from app.ml_models.rnn.rnn_model import RNNAnna


def run():
    """Run a simple training loop."""
    v = Vocabulary()
    v.build(prefix=".", filename_source="data/familienamen.txt",filename_destination="vocabulary_extended.txt")
    dataset = WordLevelDataset(prefix="data/", filename_datasets=["familienamen.txt"], vocabulary=v)
    # Currently only batch size 1 works
    train_loader = DataLoader(dataset, 1, shuffle=True)
    rnn = RNNAnna(dataset.vocabulary.size, hidden_size=128)
    train(
        rnn,
        train_loader,
        dataset,
        epochs=5,
        device="cuda",
        name="familienamen",
        save_every=1,
        print_every=3000,
    )


if __name__ == "__main__":
    # TODO Argparser
    run()

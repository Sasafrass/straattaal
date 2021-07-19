"""Functionality for locally training files."""
import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from app.ml_models.rnn.data_tools import WordLevelDataset
from app.ml_models.rnn.train import train
from app.ml_models.rnn.rnn_model import RNNAnna


def run():
    """Run a simple training loop."""
    dataset = WordLevelDataset(prefix="data/", filename_datasets=["plaatsnamen.txt"])
    # Currently only batch size 1 works
    train_loader = DataLoader(dataset, 1, shuffle=True)
    rnn = RNNAnna(dataset.vocabulary.size, hidden_size=128)
    train(
        rnn,
        train_loader,
        dataset,
        epochs=20,
        device="cuda",
        name="plaatsnamen",
        save_every=2,
        print_every=3000,
    )


if __name__ == "__main__":
    # TODO Argparser
    run()

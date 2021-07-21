"""Functionality for locally training files."""
import argparse

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
    # Parse command line arguments
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('--filename_source', type=str, default='data/familienamen.txt',
                    help='File to pull the training data file from.')
    PARSER.add_argument('--filename_datasets', type=str, default='familienamen.txt',
                    help='File to pull the dataset from.')
    PARSER.add_argument('--dir', type=str, default='my_own_model',
                    help='main directory to save intermediate results')
    run()

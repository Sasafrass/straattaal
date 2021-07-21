"""Functionality for locally training files."""
import argparse
from typing import List

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from app.ml_models.rnn.data_tools import WordLevelDataset
from app.ml_models.rnn.vocabulary import Vocabulary
from app.ml_models.rnn.train import train
from app.ml_models.rnn.rnn_model import RNNAnna


def run(
    filename_source: str = "data/familienamen.txt",
    filename_datasets: List[str] = ["familienamen.txt"],
    name: str = "familienamen",
    device: str = "cpu",
):
    """Run a simple training loop.

    Args:
        filename_source: File to pull the training data from.
        filename_datasets: Files to pull the datasets from.
        name: Name to pass to the actual train function.
        device: Device to run the network on: cpu or cuda/gpu.
    """
    v = Vocabulary()
    v.build(
        prefix=".",
        filename_source=filename_source,
        filename_destination="vocabulary_extended.txt",
    )
    dataset = WordLevelDataset(
        prefix="data/", filename_datasets=filename_datasets, vocabulary=v
    )
    # Currently only batch size 1 works
    train_loader = DataLoader(dataset, 1, shuffle=True)
    rnn = RNNAnna(dataset.vocabulary.size, hidden_size=128)
    train(
        rnn,
        train_loader,
        dataset,
        epochs=5,
        device=device,
        name=name,
        save_every=1,
        print_every=3000,
    )


if __name__ == "__main__":
    # Parse command line arguments
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument(
        "--device",
        type=str,
        default="cpu",
        help="Device to run the network on: cpu or cuda/gpu.",
    )
    PARSER.add_argument(
        "--filename_datasets",
        nargs="+",
        default=["familienamen.txt"],
        help="Files to pull the datasets from. Can be passed as space separated list.",
    )
    PARSER.add_argument(
        "--filename_source",
        type=str,
        default="data/familienamen.txt",
        help="File to pull the training data from.",
    )
    PARSER.add_argument(
        "--name",
        type=str,
        default="my_own_model",
        help="Name to pass to the actual train function.",
    )
    ARGS = PARSER.parse_args()
    run(
        filename_source=ARGS.filename_source,
        filename_datasets=ARGS.filename_datasets,
        name=ARGS.name,
        device=ARGS.device,
    )

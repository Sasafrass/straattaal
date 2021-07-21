"""Functionality for locally training files."""
import argparse
import os
from typing import List

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from app.ml_models.rnn.data_tools import WordLevelDataset
from app.ml_models.rnn.vocabulary import Vocabulary
from app.ml_models.rnn.train import train
from app.ml_models.rnn.loaded_rnn_model import init_torch_model_from_path
from app.ml_models.rnn.rnn_model import RNNAnna


def _run(**kwargs) -> None:
    """Run a simple training loop."""
    # Preliminary checks
    if kwargs["batch_size"] != 1:
        raise ValueError(
            "Batch size 1 is not implemented. Want to help out? https://github.com/Sasafrass/straattaal/issues/22"
        )

    # Build or load vobaulary

    v = Vocabulary()
    try:
        v.load(prefix=kwargs["data_directory"], filename_vocab=kwargs["filename_vocab"])
    except FileNotFoundError:
        v.build(
            prefix=kwargs["data_directory"],
            filename_datasets=kwargs["filename_datasets"],
            filename_destination=kwargs["filename_vocab"]
        )

    # Build training set and dataloader.
    dataset = WordLevelDataset(
        prefix=kwargs["data_directory"],
        filename_datasets=kwargs["filename_datasets"],
        vocabulary=v,
    )

    if kwargs["num_training_steps"] is not None:
        # Steps = epochs * (data set size / batch size)
        # Hence Epochs = steps / (data set size / batch size)
        kwargs["epochs"] = kwargs["num_training_steps"] // (
            len(dataset) / kwargs["batch_size"]
        )

    train_loader = DataLoader(dataset, kwargs["batch_size"], shuffle=True)

    # Set the stage
    if not os.path.exists("models"):
        os.makedirs("models")

    # Build or load model
    if kwargs["model_startpoint"] is not None:
        rnn = init_torch_model_from_path(
            kwargs["model_startpoint"], v, device=kwargs["device"]
        )
    else:
        rnn = RNNAnna(dataset.vocabulary.size, hidden_size=kwargs["hidden_size"])

    # Train.
    train(
        rnn,
        train_loader,
        dataset,
        print_every=3000,
        save_directory="models",
        **kwargs,
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
        default=["dutch.txt"],
        help="Files to pull the datasets from. Can be passed as space separated list.",
    )
    PARSER.add_argument(
        "--filename_vocab",
        type=str,
        default="vocabulary.txt",
        help="File to get the vocabulary from. If the file does not exist, it will be created from the given train sets.",
    )
    PARSER.add_argument(
        "--data_directory",
        type=str,
        default="data",
        help="Prefix for the directory in which the data and vocabulary is stored.",
    )
    PARSER.add_argument(
        "--model_name",
        type=str,
        default="my_own_model",
        help="Name used for storing intermediate models in the models/ directory.",
    )
    PARSER.add_argument(
        "--model_startpoint",
        type=str,
        default=None,
        help="If this is set, a model is loaded from this path as a starting point for training.",
    )
    PARSER.add_argument(
        "--num_epochs",
        type=int,
        default=10,
        help="Number of epochs for training.",
    )
    PARSER.add_argument(
        "--batch_size",
        type=int,
        default=1,
        help="Batch size.",
    )
    PARSER.add_argument(
        "--num_training_steps",
        type=int,
        default=None,
        help="Number of steps for training. Overrides --num_epochs if set.",
    )
    PARSER.add_argument(
        "--save_every",
        type=int,
        default=2,
        help="Epochs to complete before saving an intermediate model statedict.",
    )
    PARSER.add_argument(
        "--learning_rate",
        type=float,
        default=0.0005,
        help="Learning rate for the SGD optimizer.",
    )
    PARSER.add_argument(
        "--momentum",
        type=float,
        default=0.9,
        help="Momentum for the SGD optimizer.",
    )
    PARSER.add_argument(
        "--hidden_size",
        type=int,
        default=128,
        help="Hidden size of the recurrent model.",
    )
    _run(**vars(PARSER.parse_args()))

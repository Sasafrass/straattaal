"""Contains function to train a recurrent model given a dataset."""
import os

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from tqdm import tqdm

from app.ml_models.rnn.data_tools import WordLevelDataset
from app.ml_models.rnn.generate import generate_word
from app.ml_models.rnn.rnn_model import RNNAnna


def sample_some_words(
    rnn, vocabulary, word_amt: int = 10, temperature=0.35, device="cpu"
):
    """Sample a few words from a (still training) RNN model and prints them.

    Args:
        rnn: Recurrent model.
        vocabulary: Vocabulary object.
        word_amt: How many words to print.
        temperature: The temperature at which to generate words.
        device: Torch CUDA device.
    """
    for _ in range(word_amt):
        print(
            "\t",
            generate_word(
                rnn,
                vocabulary,
                start_letter="random",
                temperature=temperature,
                device=device,
            ),
        )


def train(
    rnn,
    dataloader: torch.utils.data.DataLoader,
    dataset: torch.utils.data.Dataset,
    learning_rate: float = 0.0005,
    momentum: float = 0.9,
    num_epochs: int = 500,
    device: str = "cpu",
    model_name: str = "straattaal",
    save_every: int = 50,
    print_every: int = 10000,
    **kwargs,
):
    """Train a full RNN model.

    Args:
        dataloader: Pytorch dataloader to iterate over the dataset.
        dataset: Dataset to be used for training and to generate a word.
        learning_rate: Learning rate to be used for training the model.
        epochs: Number of epochs to run our dataloader for.
        device: Device on which to run our model. Default is 'cpu', but can be set to GPU if one is available.
        name: Name to be used for the saved model.
        save_every: After every multitude of this number we save a version of the model.
        print_every: After every multitude of this number we print the loss.
    """
    rnn = rnn.to(device)

    # With CrossEntropyLoss we don't need (manual) one-hot
    criterion = nn.CrossEntropyLoss()

    # Use SGD optimizer so we don't need manual param updates.
    optimizer = torch.optim.SGD(rnn.parameters(), lr=learning_rate, momentum=momentum)
    for epoch in range(num_epochs):
        total_loss = 0
        rnn.train()
        for i, (input_line_tensor, target_line_tensor) in tqdm(
            enumerate(dataloader), total=len(dataloader)
        ):
            optimizer.zero_grad()
            input_line_tensor = input_line_tensor.to(device)
            target_line_tensor = target_line_tensor.to(device)

            # Run model ye olde way
            # output, _  = rnn(input_line_tensor)
            # loss = criterion(output.permute(1, 2, 0), target_line_tensor.permute(1,0))

            # Run model ye newe way
            loss = 0
            hidden = None
            for char_pos in range(input_line_tensor.size(1)):
                # TODO unsqueeze is necessary for batch size 1
                # Make this generic for larger batch size (it will also be faster on bigger dataset)
                output, hidden = rnn(
                    input_line_tensor[:, char_pos].unsqueeze(1), hidden
                )
                character_loss = criterion(
                    output.permute(1, 2, 0),
                    target_line_tensor[:, char_pos].unsqueeze(1).permute(1, 0),
                )
                loss += character_loss

            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            if (i + 1) % print_every == 0:
                print("Loss", total_loss / i)
                sample_some_words(rnn, dataset.vocabulary)
                rnn.train()

        # TODO plot loss... maybe.... store it somewhere.... im too lazy
        if epoch % save_every == 0:
            print(f"Epoch {epoch} loss", total_loss / i)
            sample_some_words(rnn, dataset.vocabulary)
            torch.save(
                {
                    "epoch": epoch,
                    "model_state_dict": rnn.state_dict(),
                    "optimizer_state_dict": optimizer.state_dict(),
                },
                os.path.join(kwargs["save_directory"], f"{model_name}_statedict_{epoch}.pt"),
            )

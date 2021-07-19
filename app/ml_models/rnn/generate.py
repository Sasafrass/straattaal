"""Contains functions to generate new words given a recurrent model."""
from random import choice as choose

import torch


def next_char(out, temperature):
    """Sample the next character in the word.

    Args:
        out: Tensor of shape (hidden_size x voc_size), pre-softmax output of the recurrent model at the current step.
        temperature: Temperature for non-argmax sampling.
    """
    # Softmax of the last dimension
    if torch.distributions.Uniform(0, 1).sample() < temperature:
        probs = torch.softmax((out), -1)
        # probs = torch.softmax(temperature*(out), -1) # This is good for randomness (temperature < 1)
        choice = torch.multinomial(probs.squeeze(0), 1)
    else:
        choice = torch.argmax(out, dim=2)
    return choice


def generate_word(
    model, vocabulary, start_letter=None, max_len=20, temperature=0.25, device="cpu"
):
    """Generate a new word.

    Args:
        model: Pre-trained Recurrent Neural Network model.
        vocabulary: Vocabulary object (see vocabulary.py).
        start_letter: (Set of) letter(s) to start the word with.
                      If set to a single letter, start the word with that letter.
                      If set to "random", a random letter from the vocabulary object will be chosen.
                      If it consists of several letters, one of the letters will be chosen.
        max_len: Maximum number of letters to be used.
        temp: Temperature used for sampling.
        device: torch device string
    """
    # Evaluation mode
    model.eval()
    # no gradient
    with torch.no_grad():
        # Hidden stuff initialized to None (pytorch makes this zeros automatically)
        h = None
        it = 0

        # Always generate the Beginning of Word token first and feed it to the RNN
        idxs = (
            torch.Tensor([vocabulary.char_to_idx_dict["<BOS>"]])
            .long()
            .unsqueeze(0)
            .to(device)
        )

        out, h = model(idxs, h)

        choice = torch.Tensor([-99])

        # Generate a random choice from the vocabulary and put it in the to-be-fed IDXs
        if start_letter == "random":
            letters_idx = (
                torch.Tensor(
                    [vocabulary.char_to_idx_dict[choose("abcdefghijklmnopqrstuvwxyz")]]
                )
                .long()
                .unsqueeze(0)
                .to(device)
            )

        # Generate a random choice from the input
        elif start_letter is not None:
            # TODO Should be able to start with a string, not just single letter. (Give user the option to choose between behaviours)
            letters_idx = (
                torch.Tensor([vocabulary.char_to_idx_dict[choose(start_letter)]])
                .long()
                .unsqueeze(0)
                .to(device)
            )

        # Let the RNN decide for this first round.
        else:
            choice = next_char(out, temperature)
            letters_idx = choice.to(device)

        # Check if the token is an EOS token.
        while choice.item() != vocabulary.char_to_idx_dict["<EOS>"] and it < max_len:
            # Pass the latest character to the model, store new hidden stuff.
            out, h = model(letters_idx[it:], h)
            choice = next_char(out, temperature)
            letters_idx = torch.cat((letters_idx, choice), 0)
            it += 1

        output_string = letters_idx.squeeze(1).tolist()
    return vocabulary.convert_to_string(output_string).split("<EOS>")[0]

import torch
from helpers import get_input_tensor
from rnn_model import RNN
from random import choice as choose


def next_char(out, temperature):
    # Softmax of the last dimension
    if temperature != 0 and torch.distributions.Uniform(0, 1).sample() < temperature:
        probs = torch.softmax((out), -1)  # / temperature
        choice = torch.multinomial(probs.squeeze(0), 1)
        # Does same as this I think
        #probs = torch.softmax(output, 1)
        #dist = torch.distributions.Categorical(probs)
        #pick = dist.sample()
    else:
        choice = torch.argmax(out, dim=2)
    return choice


def generate_word(model, dataset, start_letter=None,  max_len=20, temperature=0.25):
    """Generate a new word.

    Args:
        model: Pre-trained Recurrent Neural Network model.
        dataset: WordLevelDataset object 
        start_letter: Letter to start the word with.
        max_len: Maximum number of letters to be used.
        temp: Temperature used for sampling.
    """
    # Evaluation mode
    model.eval()
    # no gradient
    with torch.no_grad():
        # Hidden stuff initialized to None (pytorch makes this zeros automatically)
        h = None
        it = 0

        # Always generate the Beginning of Word token first and feed it to the RNN
        begin_letter = "<BOS>"
        idxs = [dataset.char_to_idx_dict[begin_letter]]
        out, h = model(torch.Tensor(idxs).long().unsqueeze(0), h)

        choice = torch.Tensor([-99])

        # Generate or feed the next character
        if start_letter == 'random':
            # Generate a random choice from the vocabulary and put it in the to-be-fed IDXs
            idxs = [dataset.char_to_idx_dict[choose(dataset.vocabulary)]]
            letters_idx = torch.Tensor(idxs).long().unsqueeze(0)
        elif start_letter is not None:
            if len(start_letter) == 1:
                # Put the given letter in the to-be-fed IDXS
                idxs = [dataset.char_to_idx_dict[start_letter]]
                letters_idx = torch.Tensor(idxs).long().unsqueeze(0)
            else:
                idxs = [dataset.char_to_idx_dict[choose(start_letter)]]
                letters_idx = torch.Tensor(idxs).long().unsqueeze(0)
        else:
            # Let the RNN decide for this first round.
            choice = next_char(out, temperature)
            letters_idx = choice

        while choice.item() != dataset.char_to_idx_dict["<EOS>"] and it < max_len:
            # Pass the latest character to the model, store new hidden stuff.
            out, h = model(letters_idx[it:], h)

            # This is the relevant char (the last one)
            out = out[-1, :, :].unsqueeze(0)
            choice = next_char(out, temperature)

            letters_idx = torch.cat((letters_idx, choice), 0)
            it += 1

        output_string = letters_idx.squeeze(1).tolist()
    return dataset.convert_to_string(output_string)


# # TODO: Move this piece of code to generate.py?
# slang_reader = SlangReader()
# files = slang_reader.find_files("data")
# for filename in files:
#     # TODO: This will end up only parsing a single file anyways.
#     # TODO: Either concatenate those or rewrite to specific file.
#     lines = slang_reader.read_lines(filename)

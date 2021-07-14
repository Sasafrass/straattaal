import torch
from app.ml_models.rnn.helpers import get_input_tensor
from app.ml_models.rnn.rnn_model import RNN
from random import choice as choose


def next_char(out, temperature):
    # Softmax of the last dimension
    if torch.distributions.Uniform(0, 1).sample() < temperature:
        probs = torch.softmax((out), -1)  # / temperature
        choice = torch.multinomial(probs.squeeze(0), 1)
        # Does same as this I think
        #probs = torch.softmax(output, 1)
        #dist = torch.distributions.Categorical(probs)
        #pick = dist.sample()
    else:
        choice = torch.argmax(out, dim=2)
    return choice


def generate_word(model, dataset, start_letter=None,  max_len=20, temperature=0.25, device='cpu'):
    """Generate a new word.

    Args:
        model: Pre-trained Recurrent Neural Network model.
        dataset: WordLevelDataset object 
        start_letter: Letter to start the word with.
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
        idxs = torch.Tensor([dataset.char_to_idx_dict["<BOS>"]]
                            ).long().unsqueeze(0).to(device)
        out, h = model(idxs, h)

        choice = torch.Tensor([-99])

        # Generate a random choice from the vocabulary and put it in the to-be-fed IDXs
        if start_letter == 'random':
            letters_idx = torch.Tensor(
                [dataset.char_to_idx_dict[choose("abcdefghijklmnopqrstuvwxyz")]]
            ).long().unsqueeze(0).to(device)

        # Generate a random choice from the input
        elif start_letter is not None:
            letters_idx = torch.Tensor(
                [dataset.char_to_idx_dict[choose(start_letter)]]
            ).long().unsqueeze(0).to(device)

        # Let the RNN decide for this first round.
        else:
            choice = next_char(out, temperature)
            letters_idx = choice.to(device)

        # Check if the token is an EOS token.
        while choice.item() != dataset.char_to_idx_dict["<EOS>"] and it < max_len:
            # Pass the latest character to the model, store new hidden stuff.
            out, h = model(letters_idx[it:], h)
            choice = next_char(out, temperature)
            letters_idx = torch.cat((letters_idx, choice), 0)
            it += 1

        output_string = letters_idx.squeeze(1).tolist()
    return dataset.convert_to_string(output_string).split('<EOS>')[0]


# # TODO: Move this piece of code to generate.py?
# slang_reader = SlangReader()
# files = slang_reader.find_files("data")
# for filename in files:
#     # TODO: This will end up only parsing a single file anyways.
#     # TODO: Either concatenate those or rewrite to specific file.
#     lines = slang_reader.read_lines(filename)

import torch
from app.ml_models.rnn.file_readers import SlangReader
from app.ml_models.rnn.helpers import get_input_tensor
from app.ml_models.rnn.rnn_model import RNN


def generate_word(
    model: RNN,
    N_LETTERS: int,
    ALL_LETTERS: set,
    start_letter: str = "a",
    maxn: int = 20,
    temp: float = 1,
) -> str:
    """Generate a new Slang word.

    Args:
        model: Pre-trained Recurrent Neural Network model.
        N_LETTERS: Number of unique letters found in the training corpus.
        ALL_LETTERS: All letters found in the training data.
        start_letter: Letter to start the word with.
        maxn: Maximum number of letters to be used.
        temp: Temperature used for sampling.
    """
    with torch.no_grad():
        input = get_input_tensor(
            start_letter,
            N_LETTERS=N_LETTERS,
            ALL_LETTERS=ALL_LETTERS,
        )
        hidden = model.initHidden()
        output_name = start_letter
        for i in range(maxn):
            output, hidden = model(input[0], hidden)
            if temp != 1:
                # print("use temp")
                probs = torch.softmax(output, 1) / temp
                dist = torch.distributions.Categorical(probs)
                pick = dist.sample()
            else:
                topv, topi = output.topk(1)
                pick = topi[0][0]
            if pick == N_LETTERS - 1:
                break
            else:
                letter = ALL_LETTERS[pick]
                output_name += letter
            input = get_input_tensor(
                letter,
                N_LETTERS=N_LETTERS,
                ALL_LETTERS=ALL_LETTERS,
                )

        return output_name


def random_choice(item):
    """Pick at random from list or string.

    Args:
        l (str, list): string or list.

    Returns:
        [char or item]: if input is a string, a random character will be
            returned. If a list, a random item is returned
    """
    return item[torch.randint(len(item), size=[1])]

# # TODO: Move this piece of code to generate.py?
# slang_reader = SlangReader()
# files = slang_reader.find_files("data")
# for filename in files:
#     # TODO: This will end up only parsing a single file anyways.
#     # TODO: Either concatenate those or rewrite to specific file.
#     lines = slang_reader.read_lines(filename)

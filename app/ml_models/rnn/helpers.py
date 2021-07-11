import torch


def get_input_tensor(line: str, N_LETTERS: int, ALL_LETTERS: set) -> torch.Tensor:
    """Create an input tensor from the start letter.

    Args:
        line: ..
        N_LETTERS: Number of unique letters found in the training corpus.
        ALL_LETTERS: All letters found in the training data.
    """
    tensor = torch.zeros(len(line), 1, N_LETTERS)
    for li in range(len(line)):
        letter = line[li]
        tensor[li][0][ALL_LETTERS.find(letter)] = 1

    return tensor


def random_choice(item):
    """Pick at random from list or string.

    Args:
        l (str, list): string or list.

    Returns:
        [char or item]: if input is a string, a random character will be
            returned. If a list, a random item is returned
    """
    return item[torch.randint(len(item), size=[1])]

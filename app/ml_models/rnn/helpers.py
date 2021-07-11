import torch


def get_input_tensor(line: str, N_LETTERS: int, ALL_LETTERS: set) -> torch.Tensor:
    """Create an input tensor from the start letter.

    Args:
        line: ..
        N_LETTERS: Number of letters the word should be.
        ALL_LETTERS: All letters found in the training data.
    """
    tensor = torch.zeros(len(line), 1, N_LETTERS)
    for li in range(len(line)):
        letter = line[li]
        tensor[li][0][ALL_LETTERS.find(letter)] = 1

    return tensor


def random_choice(l):
    return l[torch.randint(len(l), size=[1])]

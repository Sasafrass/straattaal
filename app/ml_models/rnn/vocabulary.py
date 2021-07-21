"""Defines a Vocabulary object."""
import os
from typing import List


class Vocabulary:
    """A helper for building/loading vocabulary files. Deals with conversion from indices to words/characters."""

    def build(
        self,
        prefix: str = "../../../data/",
        filename_datasets: List[str] = ["dutch.txt"],
        filename_destination: str = "dutch_vocab.txt",
        overwrite: bool = False,
        lower: bool = True,
    ):
        """
        Initialize a Vocabulary object by building it from a source (text) file containing all possible characters.

        Args:
            prefix: The prefix to the folder containing the source file.
            filename_datasets: A list of source filenames to be appended to the prefix. Final vocabulary is intersection of all files.
            filename_destination: Full filename of destination of vocabulary file.
        """
        filename_destination = os.path.join(prefix, filename_destination)

        if os.path.exists(filename_destination) and not overwrite:
            raise ValueError(
                f"Vocabulary file {filename_destination} already exists! Use option overwrite to overwrite existing vocabulary."
            )

        chars = set()
        for filename_dataset in filename_datasets:
            filename_dataset = os.path.join(prefix, filename_dataset)

            with open(filename_dataset, "r", encoding="utf-8") as f:
                if not lower:
                    chars.update(set(f.read()))
                else:
                    chars.update(set(f.read().lower()))
        chars.difference_update(set('\n\t"'))

        # Sort the vocabulary
        chars = "".join(sorted(chars))

        with open(filename_destination, "w", encoding="utf-8") as f:
            f.write(chars)

        # TODO Paths, paths, I dont like them
        self.load(prefix=".", filename_vocab=filename_destination)

    def load(
        self, prefix: str = "../../../data/", filename_vocab: str = "vocabulary.txt"
    ):
        """
        Initialize the Vocabulary object from pre-existing vocabulary file.

        Args:
            prefix: The prefix to the folder containing the vocabulary file
            filename_vocab: Full filename of vocabulary to be appended to the prefix.
        """
        filename_vocab = os.path.join(prefix, filename_vocab)
        with open(filename_vocab, "r", encoding="utf-8") as f:
            self.vocabulary = list(f.read())
        self.vocabulary += ["<BOS>", "<EOS>"]

        self.char_to_idx_dict = {ch: i for i, ch in enumerate(self.vocabulary)}
        self.idx_to_char_dict = {i: ch for i, ch in enumerate(self.vocabulary)}
        self.size = len(self.vocabulary)

    def convert_to_string(self, char_idxs):
        """Convert an indexed representation of the characters to the actual characters.

        Args:
            char_ix: Iterable of ints (indices) that represent characters.
        """
        result = "".join(self.idx_to_char_dict[ix] for ix in char_idxs)
        return result

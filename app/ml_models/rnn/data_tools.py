import os
from typing import List

import torch
from torch.utils.data import Dataset

from app.ml_models.rnn.vocabulary import Vocabulary


class WordLevelDataset(Dataset):
    def __init__(
        self,
        prefix: str = "../../../data/",
        filename_datasets: List[str] = ["straattaal.txt"],
        vocabulary: Vocabulary = None,
        filename_vocab: str = "vocabulary.txt",
    ):
        """
        Initialize a WordLevelDataset object and accompanying Vocabulary object if necessary.

        Args:
            prefix: The prefix to the folder containing the dataset.
            filename_datasets: A list of full filenames of datasets to be appended to the prefix.
            vocabulary: Optional Vocabulary object (see vocabulary.py). If set to None, vocabulary will be loaded from filename_vocab.
            filename_vocab: Optional, only necessary if the vocabulary argument is None. Full filename of vocabulary to be appended to the prefix.

        """
        self.words = []
        for filename_dataset in filename_datasets:
            filename_dataset = os.path.join(prefix, filename_dataset)

            with open(filename_dataset, "r", encoding="utf-8") as f:
                lines = f.read().strip().lower()
                self.words += [s.strip().replace("\t", "") for s in lines.split("\n")]

        if vocabulary is not None:
            self.vocabulary = vocabulary
        else:
            self.vocabulary = Vocabulary()
            self.vocabulary.load(prefix, filename_vocab)

        self.char_to_idx_dict = self.vocabulary.char_to_idx_dict
        self.idx_to_char_dict = self.vocabulary.idx_to_char_dict

    def __len__(self):
        return len(self.words)

    def __getitem__(self, i):
        """Override Torch DataLoader function to return a single datapoint.

        Args:
            i: The index to the desired element.
        """
        s1 = [self.char_to_idx_dict[z] for z in ["<BOS>"] + list(self.words[i])]
        s2 = [self.char_to_idx_dict[z] for z in list(self.words[i]) + ["<EOS>"]]
        return torch.LongTensor(s1), torch.LongTensor(s2)

    def all_words_to_set(self):
        return set(self.words)

import torch
import os
from torch.utils.data import Dataset, DataLoader
from collections import Counter


class WordLevelDataset(Dataset):
    def __init__(self,
                 prefix: str = '../../../data/',
                 filename_dataset: str = 'straattaal.txt',
                 filename_vocab: str = 'vocabulary.txt'):
        """Initialize a WordLevelDataset object.
        
        Args:
            prefix: The prefix to the folder containing the dataset.
            filename_dataset: Full filename of dataset to be appended to the prefix.
            filename_vocab: Full filename of vocabulary to be appended to the prefix.
        """
        filename_dataset = os.path.join(prefix, filename_dataset)
        filename_vocab = os.path.join(prefix, filename_vocab)

        with open(filename_dataset, 'r', encoding='utf-8') as f:
            lines = f.read().strip().lower()
            self.words = [s.strip().replace('\t', '')
                          for s in lines.split("\n")]
        with open(filename_vocab, 'r', encoding='utf-8') as f:
            self.vocabulary = list(f.read())
        self.vocabulary += ['<BOS>', '<EOS>']
        self.vocabulary_size = len(self.vocabulary)
        self.char_to_idx_dict = {ch: i for i, ch in enumerate(self.vocabulary)}
        self.idx_to_char_dict = {i: ch for i, ch in enumerate(self.vocabulary)}

    def __len__(self):
        return len(self.words)

    def __getitem__(self, i):
        """Override Torch DataLoader function to return a single datapoint.
        
        Args:
            i: The index to the desired element.
        """
        s1 = [
            self.char_to_idx_dict[z]
            for z in ["<BOS>"] + list(self.words[i])
        ]
        s2 = [
            self.char_to_idx_dict[z]
            for z in list(self.words[i]) + ["<EOS>"]
        ]
        return torch.LongTensor(s1), torch.LongTensor(s2)

    def convert_to_string(self, char_ix):
        """Convert an indexed representation of the characters to the actual characters.
        
        Args:
            char_ix: ?Iterable? with indices that represent characters.
        """  
        
        result = "".join(self.idx_to_char_dict[ix] for ix in char_ix)
        return result


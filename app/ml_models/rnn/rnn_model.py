"""Defines recurrent models."""
import torch
import torch.nn as nn


class RNN(nn.Module):
    """Legacy model."""

    def __init__(self, input_size, hidden_size, output_size):
        """Initialize manual RNN model of specified dimensionality."""
        super(RNN, self).__init__()

        self.hidden_size = hidden_size
        self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
        self.i2o = nn.Linear(hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)
        self.tanh = nn.Tanh()
        self.dropout = nn.Dropout(0.1)

    def forward(self, input, hidden):
        """Do forward pass."""
        combined = torch.cat((input, hidden), 1)
        hidden = self.tanh(self.i2h(combined))
        output = self.i2o(hidden)
        output = self.dropout(output)
        output = self.softmax(output)
        return output, hidden

    def initHidden(self):
        """Initialize hidden state with zeros."""
        return torch.zeros(1, self.hidden_size)


class RNNAnna(nn.Module):
    """Basic pytorch RNN model."""

    def __init__(
        self,
        vocab_size: int,
        hidden_size: int,
        train_embeddings: bool = False,
        embedding_size: int = None,
    ):
        """Initialize an single-layer RNNAnna model. Improved take on a traditional RNN.

        Args:
            vocab_size: Size of the vocabulary to be used.
            hidden_size: Number of units in the hidden layer.
            train_embeddings: Whether to train the actual embeddings
            embedding_size: Number of units for the (character) embeddings. One-hot embeddings are used by default if embedding_size=None.
        """
        super(RNNAnna, self).__init__()

        if embedding_size is None:
            self._embedding = nn.Embedding(vocab_size, vocab_size)
            self._embedding.weight.data = torch.eye(vocab_size)
            self.lstm = nn.RNN(vocab_size, hidden_size, 1, batch_first=False)
        else:
            self._embedding = nn.Embedding(vocab_size, embedding_size)
            self.lstm = nn.RNN(embedding_size, hidden_size, 1, batch_first=False)

        self._embedding.weight.requires_grad = train_embeddings
        self.dropout = nn.Dropout(0.1)
        self.final = nn.Linear(hidden_size, vocab_size)
        self.hidden_size = hidden_size

    def forward(self, x, hidden=None):
        """Do a forward pass of input x.

        Args:
            x: Tensor of any dimensionality, containing indices between 0 and vocab_size.
            h: Initial hidden state. If set to None, torch will initialize it for you, no need to worry about dimensions.
        """
        x = self._embedding(x)
        out, hidden = self.lstm(x, hidden)
        return self.final(self.dropout(out)), hidden

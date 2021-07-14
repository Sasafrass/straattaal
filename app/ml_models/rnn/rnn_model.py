import torch

import torch.nn as nn


class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RNN, self).__init__()

        self.hidden_size = hidden_size
        self.i2h = nn.Linear(input_size + hidden_size, hidden_size)
        self.i2o = nn.Linear(hidden_size, output_size)
        self.softmax = nn.LogSoftmax(dim=1)
        self.tanh = nn.Tanh()
        self.dropout = nn.Dropout(0.1)

    def forward(self, input, hidden):
        combined = torch.cat((input, hidden), 1)
        hidden = self.tanh(self.i2h(combined))
        output = self.i2o(hidden)
        output = self.dropout(output)
        output = self.softmax(output)
        return output, hidden

    def initHidden(self):
        return torch.zeros(1, self.hidden_size)


class RNNAnna(nn.Module):
    def __init__(
        self,
        vocab_size,
        hidden_size,
        train_embeddings=False,
    ):
        super(RNNAnna, self).__init__()
        self._embedding = nn.Embedding(vocab_size, vocab_size)
        self._embedding.weight.data = torch.eye(vocab_size)
        self._embedding.weight.requires_grad = train_embeddings

        self.lstm = nn.RNN(vocab_size, hidden_size, 1, batch_first=False)
        self.dropout = nn.Dropout(0.1)
        self.final = nn.Linear(hidden_size, vocab_size)
        self.hidden_size = hidden_size

    def forward(self, x, hidden=None):
        x = self._embedding(x)
        out, hidden = self.lstm(x, hidden)
        return self.final(self.dropout(out)), hidden

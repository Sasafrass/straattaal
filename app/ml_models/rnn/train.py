import torch.nn as nn
import torch
from torch.utils.data import DataLoader
from tqdm import tqdm 

from app.ml_models.rnn.data_tools import WordLevelDataset
from app.ml_models.rnn.rnn_model import RNNAnna
from app.ml_models.rnn.generate import generate_word


def train(rnn,
          dataloader,
          dataset,
          learning_rate=0.0005,
          epochs=500,
          device='cpu'):

    # With CrossEntropyLoss we don't need (manual) one-hot
    criterion = nn.CrossEntropyLoss()

    # Use SGD optimizer so we don't need manual param updates.
    optimizer = torch.optim.SGD(
        rnn.parameters(), lr=learning_rate, momentum=0.9)
    for epoch in range(epochs):
        total_loss = 0
        rnn.train()
        for i, (input_line_tensor, target_line_tensor) in tqdm(enumerate(dataloader), total=len(dataloader)):
            optimizer.zero_grad()
            input_line_tensor = input_line_tensor.to(device)
            target_line_tensor = target_line_tensor.to(device)

            # loss = 0
            # print(input_line_tensor.shape,target_line_tensor.shape)
            # hidden = None
            # for Z in range(input_line_tensor.size(1)):
            #     output, hidden = rnn(input_line_tensor[:,Z].unsqueeze(1), hidden)
            #     l = criterion(output, target_line_tensor[:,Z].unsqueeze(1))
            #     loss += l

            output, _ = rnn(input_line_tensor, None)
            # Rehape in correct shape for crossentropyloss.
            loss = criterion(output.permute(1, 2, 0),
                             target_line_tensor.permute(1, 0))
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            if (i% 10000) == 0:
                for _ in range(10):
                    print('\t', generate_word(
                        rnn, dataset, start_letter="afhklmnopqrstu", temperature=0.3, device=device))
                rnn.train()
                

        if epoch % 25 == 0:
            print(total_loss / i)
            for _ in range(10):
                print('\t', generate_word(
                    rnn, dataset, start_letter="abcdefghijklmnoprstuvwz", temperature=0.3, device=device))
        torch.save({
            'epoch': epoch,
            'model_state_dict': rnn.state_dict(),
            'optimizer_state_dict': optimizer.state_dict()
        }, f"statedict_{epoch}.pt")


if __name__ == "__main__":
    hi = WordLevelDataset('../../../data/', 'straattaal.txt')

    # Currently only batch size 1 works
    hi_loader = DataLoader(hi, 1, shuffle=True)
    rnn = RNNAnna(hi.vocabulary_size, 64, 128)
    train(rnn, hi_loader, hi)

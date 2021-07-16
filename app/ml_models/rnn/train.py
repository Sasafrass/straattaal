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
          device='cpu',
          name='straattaal',
          save_every=50,
          print_every=10000):

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

            # Run model ye olde way
            #output, _  = rnn(input_line_tensor)
            #loss = criterion(output.permute(1, 2, 0), target_line_tensor.permute(1,0))

            # Run model ye new way
            loss = 0
            hidden = None
            for char_pos in range(input_line_tensor.size(1)):
                # TODO unsqueeze is necessary for batch size 1
                # Make this generic for larger batch size (it will also be faster on bigger dataset)
                output, hidden = rnn(
                    input_line_tensor[:, char_pos].unsqueeze(1), hidden)
                l = criterion(output.permute(
                    1, 2, 0), target_line_tensor[:, char_pos].unsqueeze(1).permute(1, 0))
                loss += l

            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            if (i+1) % print_every == 0:
                print('Loss', total_loss / i)
                for _ in range(10):
                    print('\t', generate_word(
                        rnn, dataset, start_letter="afhklmnopqrstu", temperature=0.3, device=device))
                rnn.train()

        # TODO plot loss... maybe.... store it somewhere.... im too lazy
        if epoch % save_every == 0:
            print('Loss', total_loss / i)
            for _ in range(10):
                print('\t', generate_word(
                    rnn, dataset, start_letter="abcdefghijklmnoprstuvwz", temperature=0.3, device=device))

            # TODO Save this to some generic spot, not just aat cwd...
            torch.save({
                'epoch': epoch,
                'model_state_dict': rnn.state_dict(),
                'optimizer_state_dict': optimizer.state_dict()
            }, f"{name}_statedict_{epoch}.pt")


if __name__ == "__main__":
    hi = WordLevelDataset('../../../data/', 'straattaal.txt')

    # Currently only batch size 1 works
    hi_loader = DataLoader(hi, 1, shuffle=True)
    rnn = RNNAnna(hi.vocabulary_size, 64, 128)
    train(rnn, hi_loader, hi)

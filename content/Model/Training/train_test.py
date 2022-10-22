# Import tqdm for progress bar
#from tqdm.auto import tqdm
import torch
from torch import nn

# Set the seed and start the timer
#torch.manual_seed(42)
def train(model, epoch, train_loader):
    # Set the number of epochs (we'll keep this small for faster training times)
    epochs = epoch

    loss_fn = nn.CrossEntropyLoss() # this is also called "criterion"/"cost function" in some places
    # loss_fn = nn.BCELoss()
    #loss_fn = nn.SoftMarginLoss()
    optimizer = torch.optim.SGD(params=model.parameters(), lr=0.1)

    # Create training and testing loop
    for epoch in range(epochs):
        print(f"Epoch: {epoch}\n-------")
        ### Training
        train_loss = 0
        # Add a loop to loop through training batches
        for batch, (X, y) in enumerate(train_loader):

            print(X.shape)
            print(y.shape)
            # 1. Forward pass
            y_pred = model(X)

            # 2. Calculate loss (per batch)
            loss = loss_fn(y_pred, y.reshape(10))
            train_loss += loss # accumulatively add up the loss per epoch 

            # 3. Optimizer zero grad
            optimizer.zero_grad()

            # 4. Loss backward
            loss.backward()

            # 5. Optimizer step
            optimizer.step()

                # Print out how many samples have been seen
                # if batch % 400 == 0:
                #     print(f"Looked at {batch * len(X)}/{len(train_dataloader.dataset)} samples")

        # Divide total train loss by length of train dataloader (average loss per batch per epoch)
        train_loss /= len(train_loader)

    print(f"\nTrain loss: {train_loss:.5f}")
        
        ### Testing
        # Setup variables for accumulatively adding up loss and accuracy 
    return model


def test(model, test_set):
    count = 0.0

    for i in range(len(test_set)):
      tns, label = test_set.__getitem__(i)
      pred = model.predict(tns.reshape(1,3,224,224))
      if pred == label.item():
        count +=1
    pct=count/len(test_set)
    pct*=100

    print(f"Test acc: {pct}%\n")
# Source: https://pytorch.org/tutorials/beginner/basics/optimization_tutorial.html
import torch


def train_loop(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    dataloader_size_quarter = len(dataloader) / 4
    # Set the model to training mode - important for batch normalization and dropout layers
    # Unnecessary in this situation but added for best practices
    model.train()
    objects_passed = 0
    metrics = []
    for batch, (X, y) in enumerate(dataloader):
        # Compute prediction and loss
        pred = model(X)
        loss = loss_fn(pred, y)

        # Backpropagation
        loss.backward()
        optimizer.step()
        optimizer.zero_grad()

        objects_passed += len(X)
        if batch in [0, len(dataloader) - 1, dataloader_size_quarter - 1,
                     2 * dataloader_size_quarter - 1, 3 * dataloader_size_quarter - 1]:
            print(f"loss: {loss.item():>7f}  [{objects_passed:>5d}/{size:>5d}]")
            metrics.append(
                {
                    'loss': loss.item()
                }
            )

    return metrics


def test_loop(dataloader, model, loss_fn):
    # Set the model to evaluation mode - important for batch normalization and dropout layers
    # Unnecessary in this situation but added for best practices
    model.eval()
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    test_loss, correct = 0, 0

    # Evaluating the model with torch.no_grad() ensures that no gradients are computed during test mode
    # also serves to reduce unnecessary gradient computations and memory usage for tensors with requires_grad=True
    with torch.no_grad():
        for X, y in dataloader:
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()

    test_loss /= num_batches
    correct /= size
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")

    return {
        'Accuracy': correct,
        'loss': test_loss
    }


import torch

class NeuralNet(torch.nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()

        self.l1 = torch.nn.Linear(input_size, hidden_size)
        self.l2 = torch.nn.Linear(hidden_size, hidden_size)
        self.l3 = torch.nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        out = self.l1(x)
        out = torch.relu(out)
        
        out = self.l2(out)
        out = torch.relu(out)

        out = self.l3(out)

        return out
import torch
import torch.nn as nn
import torch.optim as optim
import torch.functional as F

class Mlp(nn.Module):
    def __init__(self, input_dim, output_dim, hidden_dim=[64, 64], drop_out=0.0):
        super(Mlp, self).__init__()

        self.fc1 = nn.Linear(input_dim, hidden_dim[0])
        self.fc2 = nn.Linear(hidden_dim[0], hidden_dim[1])
        self.fc3 = nn.Linear(hidden_dim[1], output_dim)

        self.dropout = nn.Dropout(drop_out)
        self.batch_norm1 = nn.BatchNorm1d(hidden_dim[0])
        self.batch_norma2 = nn.BatchNorm1d(hidden_dim[1])

    def forward(self, x):
        x = self.fc1(x)
        x = self.batch_norm1(x)
        x = F.relu(x)
        x = self.dropout(x)

        x = self.fc2(x)
        x = self.batch_norma2(x)
        x = F.relu(x)
        x = self.dropout(x)
        return F.softmax(x, dim=1)



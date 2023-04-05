import numpy as np
import pickle
import pandas as pd

from collections import OrderedDict
from typing import List, Tuple

import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset


DEVICE = torch.device("cpu")  # Try "cuda" to train on GPU
CLASSES = (True, False)

FEATURES = ['duration', 'orig_bytes', 'resp_bytes', 'missed_bytes', 'orig_pkts', 'orig_ip_bytes', 'resp_pkts', 'resp_ip_bytes', 'proto_icmp', 'proto_tcp', 'proto_udp', 'conn_state_OTH', 'conn_state_REJ',
            'conn_state_RSTO', 'conn_state_RSTOS0', 'conn_state_RSTR', 'conn_state_RSTRH', 'conn_state_S0', 'conn_state_S1', 'conn_state_S2', 'conn_state_S3', 'conn_state_SF', 'conn_state_SH', 'conn_state_SHR']

CLASS = 'label'


class IotDataset(Dataset):
    def __init__(self, file_name):
        df = pd.read_csv(file_name)

        x = df[FEATURES].values
        y = df[CLASS].values

        self.validateOnly = df[CLASS].value_counts().shape[0] < 2

        self.x_train = torch.tensor(x, dtype=torch.float32)
        self.y_train = torch.tensor(y, dtype=torch.long)

    def __len__(self):
        return len(self.y_train)

    def __getitem__(self, idx):
        return self.x_train[idx], self.y_train[idx]



class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear_relu_stack = nn.Sequential(
            nn.Linear(len(FEATURES), 32),
            nn.ReLU(),
            nn.Linear(32, 16),
            nn.ReLU(),
            nn.Linear(16, 2),
            nn.Sigmoid()
        )

    def forward(self, x):
        logits = self.linear_relu_stack(x)
        return logits


class MultilayerPerceptronLearner():
    def __init__(self, datasetFile):
        dataset = IotDataset(datasetFile)
        self.validateOnly = dataset.validateOnly
        # validation_size = len(dataset) // 10
        self.datasetSize = len(dataset)
        # train_dataset, validation_dataset = random_split(
        # dataset, (train_size, validation_size), torch.Generator().manual_seed(42))

        self.train_loader = DataLoader(
            dataset, batch_size=100, shuffle=False)
        # self.validation_loader = DataLoader(validation_dataset, batch_size=100)

        self.model = Net().to(DEVICE)

    def getModelBytes(self):
        return pickle.dumps([val.cpu().numpy() for _, val in self.model.state_dict().items()])

    def _makeModel(self, parameters):
        model = Net().to(DEVICE)
        params_dict = zip(model.state_dict().keys(), parameters)
        state_dict = OrderedDict({k: torch.Tensor(v) for k, v in params_dict})
        model.load_state_dict(state_dict, strict=True)
        return model

    def _score(self, net):
        # criterion = torch.nn.CrossEntropyLoss()
        correct, total, loss = 0, 0, 0.0
        net.eval()
        with torch.no_grad():
            for features, labels in self.train_loader:
                features, labels = features.to(DEVICE), labels.to(DEVICE)
                outputs = net(features)
                # loss += criterion(outputs, labels).item()
                _, predicted = torch.max(outputs.data, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        # loss /= self.train_size
        accuracy = correct / total
        return accuracy

    def score(self):
        return self._score(self.model)

    def scoreModel(self, weightsBytes):
        return self._score(self._makeModel(pickle.loads(weightsBytes)))

    def updateModel(self, raw_models):
        # raw_models = [( bytes weights, uint256 score )]

        numWeights = len(self.model.state_dict())
        weights, scores = [[] for _ in range(numWeights)], []
        for _, raw_weights, score, _ in raw_models:
            weight = pickle.loads(raw_weights)
            for i, w in enumerate(weight):
                weights[i].append(w)
            scores.append(score)

        avg_weights = [np.average(i, axis = 0) for i in weights]
        self.model = self._makeModel(avg_weights)


    def train(self):
        if self.validateOnly:
            # If dataset does not contain both classes, do not train
            return
        criterion = torch.nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(self.model.parameters())
        self.model.train()
        epochs = 1
        for epoch in range(epochs):
            correct, total, epoch_loss = 0, 0, 0.0
            for features, labels in self.train_loader:
                features, labels = features.to(DEVICE), labels.to(DEVICE)
                optimizer.zero_grad()
                outputs = self.model(features)
                loss = criterion(outputs, labels)
                loss.backward()
                optimizer.step()
                # Metrics
                epoch_loss += loss
                total += labels.size(0)
                correct += (torch.max(outputs.data, 1)
                            [1] == labels).sum().item()
            epoch_loss /= self.datasetSize
            epoch_acc = correct / total
            print(
                f"Epoch {epoch+1}: train loss {epoch_loss}, accuracy {epoch_acc}")


if __name__ == "__main__":
    l = MultilayerPerceptronLearner(
        "/home/raghav/projects/federated_learning_blockchain/dataset/iot23_01.csv")

    for k, val in l.model.state_dict().items():
        r = val.cpu().numpy()
        print(type(r), r.shape, r.size, type(r[0]))

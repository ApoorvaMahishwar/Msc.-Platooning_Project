import dgl
import torch
import torch.tensor as tt
import torch.nn as nn
import torch.nn.functional as F

from dgl.nn import GraphConv
from dgl.heterograph import DGLHeteroGraph
from typing import Tuple

def main():

    graph, train_mask, val_mask, test_mask, labels, features, num_classes = data_definitions(True)

    model = GCN(features.shape[1], 16, num_classes)

    train(model, graph, features, labels, train_mask, val_mask, test_mask) 

    #own_data()

    #call2

    #...etc

def own_data():
    g = dgl.graph(([1, 2, 1, 1, 4, 4, 3, 2], [2, 3, 3, 4, 3, 5, 5, 4]), device='cuda')
    print(g)
    print("-------")
    print(g.edata)
    print("-------")
    print(g.device)


def data_definitions(GPU = False) -> Tuple[DGLHeteroGraph, tt, tt, tt, tt, tt, int]:

    import dgl.data

    print("------------------------------------------------------")
    print("Importing data from dgl.data:\n")
    dataset = dgl.data.CoraGraphDataset()
    if GPU:
        print("Using GPU!")
        try:
            g = dataset[0].to('cuda')
        except:
            print("No CUDA supported device found!")
            g = dataset[0]
    else:
        print("Using CPU!")
        g = dataset[0]

    train_mask = g.ndata['train_mask']
    val_mask = g.ndata['val_mask']
    test_mask = g.ndata['test_mask']
    
    labels = g.ndata['label']
    features = g.ndata['feat']

    num_classes = dataset.num_classes

    print("\nData downloaded & imported")
    print("------------------------------------------------------\n")

    return g, train_mask, val_mask, test_mask, labels, features, num_classes

def train(model, g, features, labels, train_mask, val_mask, test_mask):

    # try to copy the defined model to gpu
    try:
        cuda = torch.device('cuda')
        model = model.cuda()
        print(f"Found CUDA device: \"{cuda}\". Copied model to GPU: \n")
    except:
        # In case of failure to detect CUDA capable device:
        print("Did not find a supported CUDA device -> Using CPU-based model.")

    #@model.parameters(): iterable model containing the needed parameters to optimize.
    #@lr: learning rate. 
    optimizer = torch.optim.Adam(model.parameters(), lr=0.1)

    loss_fn = torch.nn.MSELoss()
    best_val_acc = 0
    best_test_acc = 0

    for it in range(1500):

        logits = model(g, features)

        pred = logits.argmax(1)
        
        loss = F.cross_entropy(logits[train_mask], labels[train_mask])

        train_acc = (pred[train_mask] == labels[train_mask]).float().mean()
        val_acc = (pred[val_mask] == labels[val_mask]).float().mean()
        test_acc = (pred[test_mask] == labels[test_mask]).float().mean()

        if best_val_acc < val_acc:
            best_val_acc = val_acc
            best_test_acc = test_acc

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if it % 100 == 0:
            print(f'In epoch {it}, loss: {loss:.3f}, val_acc: {val_acc:.3f}, best_val_acc: {best_val_acc:.3f}, test_acc: {test_acc:.3f}, best_test_acc: {best_test_acc:.3f}')




class GCN(nn.Module):
    def __init__(self, in_feats, h_feats, num_classes):
        super(GCN, self).__init__()
        self.conv1 = GraphConv(in_feats, h_feats)
        self.conv2 = GraphConv(h_feats, num_classes)

    def forward(self, g, in_feat):
        h = self.conv1(g, in_feat)
        h = F.relu(h)
        h = self.conv2(g, h)
        return h


if __name__ == "__main__":
    main()

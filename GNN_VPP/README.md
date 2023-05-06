# Graph Neural Network Solution for VPP
This proposed solution is the main idea behind the master's porject, it is based on [Graph Neural Networks (GNN)](https://ieeexplore.ieee.org/abstract/document/4700287).

## Graph Neural Networks
GNN are a powerful neural network architecture dealing exlusively with graph data in neural network solvable tasks. They are able to work not only with the shallow information of the graph (weights, parameters, ...etc) but also including the underlying information of the relationships between the nodes, while keeping the same stadandards and simplicity of using typical neural network methods.

### Deep Graph Library (DGL)
The standard library for tackling GNN is [DGL](https://www.dgl.ai/). It is a very popular tool with a rich toolset and a large user community.
In our implementation we use DGL for implementing the VPP solution. DGL can use one of the following backends: [TensorFlow](https://www.tensorflow.org/) , [PyTorch](https://pytorch.org/) or [MXNet](https://mxnet.apache.org/versions/1.8.0/).

#### Setting up DGL:
[Setting up DGL](https://www.dgl.ai/pages/start.html) is straight forward, in our case we use DGL in Linux with PyTorch as backend. For setting up DGL and PyTorch with GPU (CUDA) accelration support please refer to [Install PyTorch](https://pytorch.org/) section.


#### Running Example
The script ``dgl_GCN_demo.py`` is an example of a simple [Graph Convolutional Network (GCN)](https://tkipf.github.io/graph-convolutional-networks/) implementation. it includes 2 convolution layers that trains a model and performs classification on the ``CoraGraphDataset``.
The script is a typical implementation like any other CNN. We define the data to be used, train, validate and test the neural network afterward.
We can run the example by simply:
```sh
(project_venv)$ python dgl_GCN.demo.py
```
This runs the pipeline and prints out the following output:
```sh
Using backend: pytorch
------------------------------------------------------
Importing data from dgl.data:

  NumNodes: 2708
  NumEdges: 10556
  NumFeats: 1433
  NumClasses: 7
  NumTrainingSamples: 140
  NumValidationSamples: 500
  NumTestSamples: 1000
Done loading data from cached files.
Using GPU!

Data downloaded & imported
------------------------------------------------------

Found CUDA device: "cuda". Copied model to GPU: 

In epoch 0, loss: 1.945, val_acc: 0.196, best_val_acc: 0.196, test_acc: 0.242, best_test_acc: 0.242
In epoch 100, loss: 0.000, val_acc: 0.770, best_val_acc: 0.778, test_acc: 0.765, best_test_acc: 0.791
In epoch 200, loss: 0.000, val_acc: 0.768, best_val_acc: 0.778, test_acc: 0.769, best_test_acc: 0.791
In epoch 300, loss: 0.000, val_acc: 0.768, best_val_acc: 0.778, test_acc: 0.769, best_test_acc: 0.791
In epoch 400, loss: 0.000, val_acc: 0.768, best_val_acc: 0.778, test_acc: 0.768, best_test_acc: 0.791
In epoch 500, loss: 0.000, val_acc: 0.770, best_val_acc: 0.778, test_acc: 0.768, best_test_acc: 0.791
In epoch 600, loss: 0.000, val_acc: 0.766, best_val_acc: 0.778, test_acc: 0.768, best_test_acc: 0.791
In epoch 700, loss: 0.000, val_acc: 0.766, best_val_acc: 0.778, test_acc: 0.769, best_test_acc: 0.791
In epoch 800, loss: 0.000, val_acc: 0.766, best_val_acc: 0.778, test_acc: 0.770, best_test_acc: 0.791
In epoch 900, loss: 0.000, val_acc: 0.766, best_val_acc: 0.778, test_acc: 0.771, best_test_acc: 0.791
In epoch 1000, loss: 0.000, val_acc: 0.766, best_val_acc: 0.778, test_acc: 0.771, best_test_acc: 0.791
In epoch 1100, loss: 0.000, val_acc: 0.766, best_val_acc: 0.778, test_acc: 0.771, best_test_acc: 0.791
In epoch 1200, loss: 0.000, val_acc: 0.766, best_val_acc: 0.778, test_acc: 0.769, best_test_acc: 0.791
In epoch 1300, loss: 0.000, val_acc: 0.766, best_val_acc: 0.778, test_acc: 0.769, best_test_acc: 0.791
In epoch 1400, loss: 0.000, val_acc: 0.766, best_val_acc: 0.778, test_acc: 0.770, best_test_acc: 0.791
```

### VPP with GNN
The Vehicle Platooning Problem (VPP) is described as the ability of vehicles to form groups and share road segments to reach certain targets (can be different) coming from certain routes (can be different). This is always with the intention of minimizing the costs of traveling and CO-2 emissions besides other benifits. In OR-Solutions (e.g: ILP) this is represented as a constraint called the ``saving_factor`` that is intended to influence the solver when providing the optimal platoons.
The directory ``../ILP_VPP/`` provides an example solution for solving the VPP problem using an Integer and Linear Program implemented in ``python`` and using the ``Gurobi`` optimization library.
The VPP road network can be represented naturally as an oriented graph with the stations as nodes and the road segments as edges. On the other hand the vehicles can be looked at as actors in the road network.
That being said, it is also a natural choice to tackle such a problem using GNN architectures especially to remedy certain cons of exact solutions such as the ILP solution.
Based on [multiple readings](https://github.com/GeminiLight/ml4co-survey) concerning solving Combinatorial Optimization (CO) Problems such as the Vehicle Routing Problem (VRP) it is to be observed that the code ideas behind the main proposed methods can be devided in 2 categories:
1. Using a message-passing neural networks + a search method:
	This category tries to solve the VRP by mixing the supervised nature of Graph Convolutional- and Attention Networks (GCN - GAT) with the unsupervised nature of a search method such as Tree Search. GAT in this case is allowing the graph nodes to catch the information of their neighborhoods by an attention transformer that is able to perform multi-head neighborhood features aggreagation along the way while training resulting in a more informative representation (embeddings) of the graph. The search method is now able to use these embeddings to run a constrained search to find the optimal routes for each vehicle.
	The message passing mechanism in this category of methods is variant (other propositions used for example RNN as the message passing network from the edges to the nodes).
2. Using a message-passing neural networks + Reinforcement Learning (RL):
	This category uses the same concept regarding the message passing part but uses a different way to find the optimal path for the vehicle by treating the problem as a single player game that can be trained to find the optimal path by its own. The RL model is trained under a reward/penalization regime.
	The RL methods varies depending on the CO problem at hand and the goals to be achieved (policy-based, actor-critic method...etc.) but can be of course classified under this category.

### Our Formulation of the VPP
Our proposal for solving the VPP can be boiled down to these points:

1. Data definition:
In our case we would like to define the exploration environment as a directed graph that maps the road network into nodes representing the cities and edges representing the the road between them. The distance between 2 respective cities is represented by a weight on the edge.

2. Reward function:
This environment needs to have a reward mechanism (reward function) that can be defined as the negative value of the distance, the larger the traveled distance the larger our loss. However the Platooning aspect should also be introduced and can be done by encouraging the agents with a high reward for platooning.
When the agent reachs the target node (goal city) this should be signaled by a terminal state.

3. Masking function:
It should also be known to the agents that visiting non-adjacent cities is not permitted, therfore a masking function that updates the permitted cities should be added.

4. Common Policy:
A (common) decision of which next step to take should also concider the cooperative aspect of solving the VPP this is where Multi-Agent Reinforcement Learning (MARL) is introduced, which allows a shared policy/reward between agents when cooperating to solve the VPP for a given road network.

5. Terminal states:
Terminal states can be defined (so far) by nodes that are targets (goal city) or a city that does not have any links to other cities, in the first case the goal has been reached and in the latter the agent should be signaled to be dead and therefore not influence the learning of the other agents.

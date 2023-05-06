from gurobipy import *
import networkx as nx
import matplotlib.pyplot as plt
from typing import Tuple, Dict
from database.connection import Neo4jConnection
import database.db_credentials as dbc


def main():

    # use "definitions()" to create own network
    # road network import
    #road_network, saving_factor, every_value, draw = definitions()

    # use Neo4jConnection to use a neo4j database
    graph, vehicles, vehicle_locations = Neo4jConnection.get_data(dbc.DB_URL, dbc.DB_USERNAME, dbc.DB_PW)

    # vehicles are defined like this: VEHICLE_ID: (START_NODE, END_NODE)
    group = {1: (1, 5), 2: (4, 3), 3: (2, 5), 4: (1, 5)}
    # example of 2 vehicles with ID 1 and 2, first vehicle starts at node 1 and ends
    # at node 3, second vehicle starts at 4 and ends at 3

    # run the model and return variables and model
    #model, x, y = optimization_model(road_network, group, saving_factor)

    # generate output
    #output_text(road_network, group, model, x, y, every_value)

    #if draw:
    #    draw_network(road_network)

def definitions() -> Tuple[nx.DiGraph, float, bool, bool]:
    '''
    This function defines the road network as well as some needed parameters.

    Returns:
    -------

    graph: nx.DiGraph
        The road network graph representation:
            - coords represent the coordinates of a certain (x,y).
            - weight represent the distance between the 2 nodes (i.e: places).

    saving_factor: float
        Cost saving factor as a constraint.

    every_value: bool
        Wether to show every value including variables equal to zero.

    draw: bool
        Wether to draw the graph using matplotlib.
    '''

    # define here, if the output should show EVERY variable or just the ones, which are not equal to zero
    every_value = False
    draw = True
    # saving factor for model (standard is 0.1!)
    saving_factor = 0.1

    graph = nx.DiGraph()

    # define the network here:
    # every node needs an ID and it's coordinates: (node_ID, {"coords":[y_coordinate, x_coordinate]})
    # input is a list of nodes:
    graph.add_nodes_from([(1, {"coords": [1, 1]}), (2, {"coords": [1, 2]}), (3, {"coords": [2, 1]}), (4, {"coords": [2, 2]}), (5, {"coords": [3, 2]})])

    # define edges here, every edge needs the starting node and the ending node, also the weight!
    graph.add_edges_from([(1, 2, {'weight': 10}), (2, 3, {'weight': 90}), (1, 3, {'weight': 100}),
                          (1, 4, {'weight': 40}), (4, 3, {'weight': 40}), (4, 5, {'weight': 40}),
                          (3, 5, {'weight': 10}), ((2, 4, {'weight': 40}))])

    return graph, saving_factor, every_value, draw


# the model to be optimized
def optimization_model(road_network, group, saving_factor=0.1):

    # model init
    # Model is the constructor of class nx.Model
    model = Model("Routing")
    x = {}
    y = {}

    # initiate the variables with costs
    for edge in road_network.edges():

        x[edge] = {}
        y[edge] = model.addVar(vtype=GRB.BINARY, obj=saving_factor * road_network.get_edge_data(*edge)["weight"])

        for h, locations in group.items():
            x[edge][h] = model.addVar(vtype=GRB.BINARY, lb=0, obj=(1 - saving_factor) * road_network.get_edge_data(*edge)["weight"])

    model.update()

    # flow condition
    for v in road_network.nodes():
        for h, locations in group.items():
            if locations[0] == v:
                b = 1
            elif locations[1] == v:
                b = -1
            else:
                b = 0
            model.addConstr(quicksum(x[edge][h] for edge in road_network.out_edges(v)) - quicksum(x[edge][h] for edge in road_network.in_edges(v)) == b, name='flow_' + str(v) + "_" + str(h))

    # buying of edge
    for edge in road_network.edges():
        for h, locations in group.items():
            model.addConstr(x[edge][h] <= y[edge])

    # optimize the model
    print("---------------------------------------")
    model.optimize()
    print("---------------------------------------")

    return model, x, y


def output_text(road_network: nx.DiGraph, group: Dict, model, x: Dict, y: Dict, every_value=True) -> None:
    # print optimal solution:
    print("Optimal solution value: " + str(model.ObjVal))

    # generate output lines to show variables
    if every_value:
        for e in road_network.edges():
            print("edge " + str(e) + " has value: " + str(y[e].X))
            for h, locations in group.items():
                print("vehicle " + str(h) + " on the edge " + str(e) + " has : " + str(x[e][h].X))
    else:
        for e in road_network.edges():
            if y[e].X > 0.99:
                print("edge " + str(e) + " has value: " + str(y[e].X))
                for h, locations in group.items():
                    print("vehicle " + str(h) + " on the edge " + str(e) + " has : " + str(x[e][h].X))

def draw_network(graph: nx.DiGraph) -> None:
    '''
    Function to draw the network using nx.Drawing and matplotlib.pyplot utilities.

    Parameters:
    -----------
    graph: nx.DiGraph
        The graph to be drawn.
    '''
    positions = dict([( u,(d["coords"][0], d["coords"][1])) for u, d in graph.nodes(data=True)])
    e_labels = dict([( (u, v), d["weight"]) for u, v, d in graph.edges(data=True)])

    # nodes
    nx.draw_networkx(graph, positions, with_labels=True)

    # edges
    #nx.draw_networkx_edges(G, pos, edgelist=elarge, width=6)
    nx.draw_networkx_edge_labels(graph, positions, edge_labels=e_labels)

    # labels
    nx.draw_networkx_nodes(graph, positions, node_color='b')

    plt.axis("off")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()


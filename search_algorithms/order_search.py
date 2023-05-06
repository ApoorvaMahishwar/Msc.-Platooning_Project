# search_algorithms/order_search.py

class PermuteSearch:
    """
    Apply permutation then run route creation.
    """

    @staticmethod
    def CreateStructure(graph, permutation):
        """
        Creates a dict structure from the given graph and permutation.

        :param graph: the network graph.
        :param permutation: given permutation of a certain truck.
        :returns: reconstruction, the created .
        """
        reconstruction = {}

        for node in graph.nodes():
            adj_nodes = list(graph[node])
            reconstruction[node] = [elm for elm in permutation if elm in adj_nodes]

        return reconstruction

    @staticmethod
    def CreateRoute(org, dest, graph, permutation):
        """
        Construct a route from a given graph
        starting from origin and reaching destination
        based on a given permutation

        :param org: the origin of the truck.
        :param dest: destination of the truck.
        :param graph: given road network.
        :param permutation: permutation order of the truck.
        :returns: route, the produced route.
        """

        route = []
        reconstruction = PermuteSearch.CreateStructure(graph, permutation)
        route.append(org)
        naughty_nodes = []
        while dest not in route:
            adj_nodes = reconstruction[org]
            naughty_nodes.append(org)
            [adj_nodes.remove(naughty_node) for naughty_node in naughty_nodes if naughty_node in adj_nodes]

            for adj in adj_nodes:
                if adj not in route:
                    route.append(adj)
                    org = adj
                    break

            if adj_nodes == []:
                route.pop(-1)
                org = route[-1]

        return route

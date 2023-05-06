#search_algorithms/embed_search.py


class EmbedSearch:
    """
    Embed permutation into the graph then run route creation.
    """

    @staticmethod
    def EmbedWeights(org, graph, permutation):
        """
        Add permutation order as weights of graph.

        :param org: route's origin of a certain truck.
        :param graph: given unweighted graph.
        :param permutation: given permutation for a certain truck.
        :returns: w_graph: weighted graph.
        """

        w_graph = graph
        w_graph.nodes[org]['weight'] = 0
        for node in permutation:
            if node != org:
                w_graph.nodes[node]['weight'] = permutation.index(node) + 1

        return w_graph

    @staticmethod
    def SearchWeightedGraph(org, dest, graph, permutation):
        """
        Search for route in the weighted graph.

        :param org: route's origin of a certain truck.
        :param dest: destination of a certain truck.
        :param graph: given unweighted graph.
        :param permutation: given permutation for a certain truck.
        :returns: route: found route.
        """

        route = []
        w_graph = EmbedSearch.EmbedWeights(org, graph, permutation)
        route.append(org)
        while dest not in route:
            adj_nodes = {n:w_graph.nodes[n]['weight'] for n in w_graph[org]}

            intersection = list(set(adj_nodes.keys()) & set(route))

            if intersection is not None:
                [adj_nodes.pop(e) for e in intersection]

            if adj_nodes == {}:
                w_graph.remove_node(route[-1])
                route.pop(-1)
                org = route[-1]
                continue

            org = min(adj_nodes, key=adj_nodes.get)
            route.append(org)

        return route

#search_algorithms/naive_solution.py

class NaiveSolution:
    """
    Naive Solution implementation.
    """

    @staticmethod
    def NaiveBuildRoute(org, dest, graph, permutation):
        """
        construct the route of the vehicle.

        :param origin: given origin.
        :param origin: given destination.
        :param graph: the network graph.
        :param permutation: given permutation of a certain truck.
        :returns: route.
        """
        route = []
        current_node = org
        current_permutation = permutation[:]
        current_permutation.remove(current_node)
        route.append(current_node)
        while dest not in route:
            index = len(permutation)
            for node in list(graph[current_node]):
                if node not in route:
                    if node in current_permutation:
                        index = min(index, current_permutation.index(node))
            if index < len(permutation):
                route.append(current_permutation[index])
                current_node = route[-1]
            else:
                route.remove(current_node)
                current_permutation.remove(current_node)
                current_node = route[-1]

        return route

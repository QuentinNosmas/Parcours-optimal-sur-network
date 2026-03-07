"""
This is the graph module. It contains the classes Graph and GraphImplicit
"""
import heapq


class Graph:
    """
    A minimal class for directed weighted graph represented as adjacency list. 
    
    Attributes: 
    -----------
    edges: dict
        A dictionary that contains the list of neighbors of each node with its weight.
        Ex: edges = {v0: [(v1, 21), (v2, 12)], 
                     v1: [(v0, 74), (v2, 32)], 
                     ...}

    Methods: 
    --------
    neighbours(self, node): 
        Returns the list of all neighbors of a node
    """

    def __init__(self, edges):
        self._edges = edges

    def neighbours(self, node):
        if node not in self._edges:
            return []
        return self._edges[node]
    
    def shortest_path(self,vs):
        """
        Renvoie tous les plus courts chemins ainsi que les distances
        correspondantes pour un graphe orienté à poids poisitifs
        sans fatigue. C'est un Dijkstra.
        """
        file_prio = [(0,vs)]
        d = {vs: 0}
        predecesseurs = {vs: None}

        while file_prio:
            dist_a,u_actuel = heapq.heappop(file_prio)

            if dist_a > d[u_actuel]:
                continue

            for u, poids in self.neighbours(u_actuel):
                if u not in d:
                    d[u] = float("inf")
                    predecesseurs[u] = None

                nouvelle_distance = d[u_actuel] + poids
                if nouvelle_distance < d[u]:
                    d[u] = nouvelle_distance
                    predecesseurs[u] = u_actuel
                    heapq.heappush(file_prio,(d[u],u))

        return d,predecesseurs








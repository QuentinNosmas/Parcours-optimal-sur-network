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
    
    def shortest_path(self,start_node):
        P=[(0,start_node)]
        nodes = list(self._edges.keys())
        d = {node : float('inf') for node in nodes}
        d[start_node] = 0
        predecesseurs = {node: None for node in nodes}
        while len(P)!=0 :
            dist_a, u_actuel = heapq.heappop(P)

            if dist_a > d[u_actuel]:
                continue

            for u , weight in self.neighbours( u_actuel ):
                if d[u]>d[u_actuel]+weight:
                    d[u]=d[u_actuel]+weight
                    predecesseurs[u] = u_actuel
                    heapq.heappush(P, (d[u], u))

        return d,predecesseurs




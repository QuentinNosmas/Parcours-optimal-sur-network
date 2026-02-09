import heapq
from network import Network
import os


class Graph:

    def __init__(self, edges):
        self._edges = edges

    def neighbours(self, node):
        if node not in self._edges:
            return []
        return self._edges[node]

    def shortest_path(self,start_node):
        P=[(0,start_node)]
        nodes = list(self._edges.keys())
        d = {node: float('inf') for node in nodes}
        d[start_node] = 0
        predecesseurs = {node: None for node in nodes}
        while len(P)!=0 :
            dist_a, u_actuel = heapq.heappop(P)

            if dist_a > d[u_actuel]:
                continue

            for weight , u in self.neighbours( u_actuel ):
                if d[u]>d[u_actuel]+weight:
                    d[u]=d[u_actuel]+weight
                    predecesseurs[u] = u_actuel
                    heapq.heappush(P, (d[u], u))

        return d,predecesseurs


4


    



    


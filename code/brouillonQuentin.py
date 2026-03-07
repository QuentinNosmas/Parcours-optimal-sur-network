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

#Le graphe étant à poids positifs on peut implémenter l'algorithme de Djikstra pour
#trouver le chemin de longueur minimal 

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
    
    def shortest_path(self,vs):
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

 


graph_test = Network.from_file(r"D:\Ensae\1A\S2\Projet_prog\ensae-prog26\examples\medium-nofatigue.txt")
assert graph_test.start == "v0"
assert graph_test.end == "v99"

graph_test = graph_test.build_simple_graph()
res = graph_test.shortest_path("v0")
print(res[1]) #C'est bon l'algorithme de dijkstra est correct






    



    


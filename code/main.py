from network import *
from graph import Graph

# Load the network
network_file = "examples/small.txt"
network = Network.from_file(network_file)

class GraphImplicit(Graph):
    """
    Cette classe se sert du network pour redéfinir
    la méthode neighbours ensuite utilisée par shortest_path
    """

    def __init__(self, network : Network):
        self.network = network
        n = len(network._roads)
        fatigues = [voisin[2] for sommet in network._roads for voisin in network._roads[sommet]]
        self.Fmax = (n-1)*max(fatigues) if fatigues else 0
    
    def neighbours(self, node):
        res = []
        sommet, f = node
        for voisin in self.network._roads[sommet]:
            F = voisin[2]
            if f + F <= self.Fmax :
                res.append(((voisin[0], f + F), (1 + f)*voisin[1]))
        return res


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

def chemin(vs, vt, pred):
    if vt == vs:
        return [vs]
    else:
        return chemin(vs, pred[vt], pred) + [vt]

def chemin_le_plus_court(g : Network, vs, vt):
    g_extend_implicit = GraphImplicit(g)
    d, pred = g_extend_implicit.shortest_path((vs, 0))
    arrivees = []
    
    for etat in d.keys():
        if etat[0] == vt:
            arrivees.append((etat, d[etat]))
    
    if not arrivees:
        return None, float("inf")
    
    meilleur_etat, meilleur_d = min(arrivees, key = lambda x : x[1])
    chemin_etendu = chemin((vs, 0), meilleur_etat, pred)
    return [sommet for sommet, _ in chemin_etendu], meilleur_d


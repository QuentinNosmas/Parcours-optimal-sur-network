from graph import *

class Network:
    """
    Class for a network that represents the environment (with length and fatigue on roads). 
    """

    def __init__(self, roads={}, start=None, end=None):
        """
        Initializes the network from a dictionary roads. 

        Parameters: 
        -----------
        roads: dict
            A dictionary of the roads as an adjacency list, that is 
            roads[u] = list of (v, length, fatigue)
            Ex: roads = {v0: [(v1, 21, 2), (v2, 12, 4)], 
                        v1: [(v0, 74, 2), (v2, 32, 1)], 
                        ...}
        start, end: 
            Start and end nodes added as attributes
        """
        self._roads = roads
        self.start = start
        self.end = end

    def __str__(self): 
        """
        Prints the network as text.
        """
        output = f"A network with {len(self._roads)} nodes and the following adjacency list:\n"
        return output+self._roads.__str__()

    @classmethod
    def from_file(cls, filename: str):
        """
        Creates a Network from an environment file.

        File format: one edge per line (start end length fatigue).
        """
        # Initialize adjacency list
        roads = {}

        with open(filename, "r") as testcase:
            nb, start, end = testcase.readline().strip().split()
            for _ in range(int(nb)):
                i, j, l, f = testcase.readline().strip().split()
                l, f = int(l), int(f)
                roads.setdefault(i, []).append((j, l, f))
                roads.setdefault(j, [])

        return cls(roads=roads, start=start, end=end)

    def build_simple_graph(self, inverse=False) -> Graph:
        """
        Construit un graphe simple depuis le network.
        Si inverse=True, les arêtes sont inversées — utilisé pour précalculer h dans A*.
        """
        sans_fatigue = {}
        for node, neighbours_list in self._roads.items():
            if not inverse:
                sans_fatigue.setdefault(node, []) #ajoute le neoud s'il n'existe pas déjà
                for voisin, longueur, _ in neighbours_list:
                    sans_fatigue[node].append((voisin, longueur)) #Construit les arêtes sans la fatigue
                    sans_fatigue.setdefault(voisin, [])
            else:
                for voisin, longueur, _ in neighbours_list:
                    sans_fatigue.setdefault(voisin, []).append((node, longueur)) #Construit les arêtes à l'envers
                    sans_fatigue.setdefault(node, [])
        return Graph(sans_fatigue)
    
    def build_extended_graph(self) -> Graph:
        """
        Construit un graphe étendu à partir de g. Les sommets sont les
        (u,F) où u est sommet de g et F est une fatigue entre 0 et une 
        fatigue maximum Fmax. Les arêtes sont les (u,F) -> (v,F+f) 
        de poids (1+F)*poids(u->v), quand u->v a une fatigue f dans g, 
        pour toute F telle que F+f <= Fmax.
        """
        n = len(self._roads)
        fatigues = [voisin[2] for sommet in self._roads for voisin in self._roads[sommet]] #on récupère toutes les fatigues
        Fmax = (n-1)*max(fatigues) if fatigues else 0  # fatigue maximale d'un chemin optimal puisque pour parcourir un graphe à n noeuds il faut n-1 arrêtes 
        edges = {}
    
        for sommet in self._roads:  #Ajoute tous les sommets (u,F) où u est dans g et F < Fmax + 1
            for f in range(Fmax + 1):
                edges[(sommet, f)] = []
    
        for sommet in self._roads:  #Construit les arêtes (u,F) -> (v,F+f) de poids (1+F)*poids(u->v)
            for voisin in self._roads[sommet]:
                F = voisin[2]
                for f in range(Fmax + 1):
                    if f + F <= Fmax:
                        edges[(sommet, f)].append(((voisin[0], f + F), (1 + f)*voisin[1]))
    
        return Graph(edges)
    
class GraphImplicit(Graph):
    """
    Cette classe se sert du network pour redéfinir
    la méthode neighbours ensuite utilisée par shortest_path.
    Les arêtes ne sont pas stockées, mais calculées à la demande
    par neighbours.

    Permet de ne pas construire le graphe étendu entièrement.
    """

    def __init__(self, network : Network):
        self.network = network
        n = len(network._roads)
        fatigues = [voisin[2] for sommet in network._roads for voisin in network._roads[sommet]]
        self.Fmax = (n-1)*max(fatigues) if fatigues else 0 #Fatigue maximale d'un chemin optimal.
    
    def neighbours(self, node):
        """
        Construit les voisins de node dans le graphe étendu, de la 
        même manière que dans build_extended_graph.
        """
        sommet, f = node
        if sommet not in self.network._roads:
            return []
        res = []
        for voisin in self.network._roads[sommet]: #On crée tous les voisins du sommet (sommet, f)
            F = voisin[2]
            if f + F <= self.Fmax :
                res.append(((voisin[0], f + F), (1 + f)*voisin[1]))
        return res




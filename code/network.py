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

    def build_simple_graph(self):
        """
        Builds an object of type Graph from the network, by ignoring the fatigue coefficient. 
        """
        sans_fatigue = {}
        for node , neighbours_list in self._roads.items():
            simple_neighbours = [(neighbour[0], neighbour[1]) for neighbour in neighbours_list]
            sans_fatigue[node]= simple_neighbours 
        
        return Graph(sans_fatigue)
    
    def build_extended_graph(self) -> Graph:
        """
        Construit un graphe étendu à partir de g. Les sommets sont les
        (u,F) où u est sommet de g et F est une fatigue entre 0 et une 
        fatigue maximum Fmax. Les arêtes sont les (u,F) -> (v,F+f) 
        de poids (1+F)*poids(u->v), quand u->v a une fatigue f dans g, 
        pour toute F telle que F+f <= f_max.
        """
        n = len(self._roads)
        fatigues = [voisin[2] for sommet in self._roads for voisin in self._roads[sommet]]
        Fmax = (n-1)*max(fatigues) if fatigues else 0   
        edges = {}
    
        for sommet in self._roads:  #Ajoute tous les sommet (u,F) où u est dans g et F < Fmax + 1
            for f in range(Fmax + 1):
                edges[(sommet, f)] = []
    
        for sommet in self._roads:  #Construit les arêtes (u,F) -> (v,F+f) de poids (1+F)*poids(u->v)
            for voisin in self._roads[sommet]:
                F = voisin[2]
                for f in range(Fmax + 1):
                    if f + F <= Fmax:
                        edges[(sommet, f)].append(((voisin[0], f + F), (1 + f)*voisin[1]))
    
        return Graph(edges)



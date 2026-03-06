from graph import Graph 
from network import Network

def build_extended_graph(g : Network) -> Graph:
    """
    Construit un graphe étendu à partir de g. Les sommets sont les
    (u,F) où u est sommet de g et F est une fatigue entre 0 et une 
    fatigue maximum Fmax. Les arêtes sont les (u,F) -> (v,F+f) 
    de poids (1+F)*poids(u->v), quand u->v a une fatigue f dans g, 
    pour toute F telle que F+f <= f_max.
    """
    n = len(g._roads)
    fatigues = [voisin[2] for sommet in g._roads for voisin in g._roads[sommet]]
    Fmax = (n-1)*max(fatigues) if fatigues else 0   
    edges = {}
    
    for sommet in g._roads:  #Ajoute tous les sommet (u,F) où u est dans g et F < Fmax + 1
        for f in range(Fmax + 1):
            edges[(sommet, f)] = []
    
    for sommet in g._roads:  #Construit les arêtes (u,F) -> (v,F+f) de poids (1+F)*poids(u->v)
        for voisin in g._roads[sommet]:
            F = voisin[2]
            for f in range(Fmax + 1):
                if f + F <= Fmax:
                    edges[(sommet, f)].append(((voisin[0], f + F), (1 + f) * voisin[1]))
    
    return Graph(edges)
        
            
            









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

    def __init__(self, edges={}):
        self._edges = edges

    def neighbours(self, node):
        if node not in self._edges:
            return []
        return self._edges[node]
    
    def distances_depuis(self, source) -> dict:
        """
        Retourne le dictionnaire des distances minimales depuis source
        vers tous les noeuds atteignables. Utilisé pour précalculer h dans A*. 
        C'est un Dijkstra.
        """
        file_prio = [(0, source)]  
        d = {source: 0}

        while file_prio:  
            dist_a, u_actuel = heapq.heappop(file_prio)

            if dist_a > d[u_actuel]:  #Si le sommet retiré est obsolète on l'ignore
                continue

            for u, poids in self.neighbours(u_actuel):
                if u not in d:
                    d[u] = float("inf")
                nouvelle_distance = d[u_actuel] + poids
                if nouvelle_distance < d[u]: #Si on a trouvé un meilleur chemin à la source, on actualise le dictionnaire des distances
                    d[u] = nouvelle_distance
                    heapq.heappush(file_prio, (d[u], u))

        return d

    def shortest_path(self, vs, vt, is_target=None, pruning=False, heuristique=None):
        """
        Retourne le chemin le plus court de vs à vt.
        Implémente Dijkstra (cas particulier de A* avec h=0) et A* avec heuristique.

        Paramètres:
        -----------
        vs : nœud source
        vt : nœud cible
        is_target : fonction qui dit si un nœud est la cible.
                Si None, on compare directement u_actuel == vt.
        pruning : si True, active le Pareto pruning.
        heuristique : fonction h(node) -> estimation du temps restant.
                  Si None, h=0 partout (Dijkstra classique).

        Retourne:
        ---------
        (chemin, distance) : liste des nœuds et distance totale,
                         ou (None, inf) si vt est inatteignable.
        """
        if is_target is None:
            is_target = lambda node: node == vt

        h = heuristique if heuristique is not None else lambda node: 0 #Si aucune heuristique n'est donnée, on prend h = 0

        file_prio = [(0, 0, vs)]  # (f = g + ditance approximée par l'heuristique, g = distance à la source, noeud)
        d = {vs: 0}
        predecesseurs = {vs: None}        
        u_actuel = None
        pareto = {} #Dictionnaire permettant de mémoriser les sommets avec la fatigue et la distance avec lesquelles on les a rencontré
        compteur_prune = 0 #Enregistre le nombre de sommets éliminés par prunning.

        while file_prio: 
            _, dist_a, u_actuel = heapq.heappop(file_prio)

            if dist_a > d[u_actuel]: #Noeud extrait obsolète
                continue

            if pruning: 
                sommet, f = u_actuel
                if sommet in pareto and any(t <= dist_a and fa <= f for t, fa in pareto[sommet]): #sommet déjà rencontré avec distance et fatigue plus faible
                    compteur_prune += 1
                    continue  #on l'ignore
                pareto.setdefault(sommet, []).append((dist_a, f)) #Sinon on le mémorise 

            if is_target(u_actuel): #Condition d'arrêt : on est arrivé à destination
                break

            for u, poids in self.neighbours(u_actuel): #même boucle que Dijsktra, modulée de l'heuristique
                if u not in d:
                    d[u] = float("inf")
                    predecesseurs[u] = None
                nouvelle_distance = d[u_actuel] + poids
                if nouvelle_distance < d[u]:
                    d[u] = nouvelle_distance
                    predecesseurs[u] = u_actuel
                    heapq.heappush(file_prio, (d[u] + h(u), d[u], u)) #La priorité donnée dépend de l'heuristique

        if not is_target(u_actuel): #Aucun chemin ne mène à vt
            return None, float("inf")

        chemin = []    # Reconstruction du chemin
        noeud = u_actuel
        while noeud is not None:
            chemin.append(noeud)
            noeud = predecesseurs[noeud]
        chemin.reverse()

        if pruning:
            print(f"Noeuds prunés : {compteur_prune}")

        return chemin, d[u_actuel]
    
    
    








from network import *
from graph import Graph

### Test 1.1 : Test de buil_simple_graph et shortest_path

graph_test = Network.from_file(r"examples\medium-nofatigue.txt")
assert graph_test.start == "v0"
assert graph_test.end == "v99"

graph_test = graph_test.build_simple_graph()
d, pred = graph_test.shortest_path("v0")
assert d["v99"] == 1771 #C'est bon l'algorithme de dijkstra est correct

### Test 1.2 : Test de shortest_path sur une graph étendu

graph_test = Network.from_file(r"examples\medium-smallfatigue.txt")
graph_test = graph_test.build_extended_graph()
d, pred = graph_test.shortest_path(("v0", 0))
arrivees = []
for etat in d.keys():
    if etat[0] == "v99":
        arrivees.append((etat, d[etat]))  
meilleur_etat, meilleur_d = min(arrivees, key = lambda x : x[1]) # On prend l'état ("v99", F) de distance minimale
assert meilleur_d == 29934

### Test 1.3 : Test de chemin_le_plus_court

graph_test = Network.from_file(r"examples\medium-smallfatigue.txt")
chemin, d = graph_test.chemin_le_plus_court()
assert d == 29934

print("Tous les tests ont réussi.")


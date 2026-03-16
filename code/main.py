from network import *
from graph import Graph

### Test 1.2 : Test de shortest_path sur une graph étendu

graph_test = Network.from_file(r"examples\medium-smallfatigue.txt")
graph_test = graph_test.build_extended_graph()
d, path = graph_test.shortest_path(("v0", 0), "v99")
assert d == 29934

### Test 1.3 : Test de chemin_le_plus_court

graph_test = Network.from_file(r"examples\medium-smallfatigue.txt")
graph_test = GraphImplicit(graph_test)
d, path = graph_test.shortest_path(("v0", 0), "v99")
assert d == 29934

print("Tous les tests ont réussi.")

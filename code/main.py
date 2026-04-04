from network import *
from graph import Graph

### Test 1.1 : Test de shortest_path sur un graphe simple (sans fatigue)
network_test = Network.from_file(r"examples\medium-smallfatigue.txt")
graph_simple = network_test.build_simple_graph()
chemin, dist = graph_simple.shortest_path(network_test.start, network_test.end)
print(f"Test 1.1 — distance : {dist}, chemin : {chemin}")

### Test 1.2 : Test de shortest_path sur un graphe étendu
network_test = Network.from_file(r"examples\medium-smallfatigue.txt")
graph_etendu = network_test.build_extended_graph()
chemin, dist = graph_etendu.shortest_path(
    vs=(network_test.start, 0),
    vt=network_test.end,
    is_target=lambda node: node[0] == network_test.end
)
assert dist == 29934, f"Attendu 29934, obtenu {dist}"
print(dist)

### Test 1.3 : Test de shortest_path sur GraphImplicit
network_test = Network.from_file(r"examples\medium-smallfatigue.txt")
graph_implicit = GraphImplicit(network_test)
chemin, dist = graph_implicit.shortest_path(
    vs=(network_test.start, 0),
    vt=network_test.end,
    is_target=lambda node: node[0] == network_test.end
)
assert dist == 29934, f"Attendu 29934, obtenu {dist}"
print(dist)




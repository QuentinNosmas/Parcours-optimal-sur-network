from network import *
from graph import Graph
import time

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

print("medium-smallfatigue.txt")
network_test = Network.from_file(r"examples\medium-smallfatigue.txt")
graph_implicit = GraphImplicit(network_test)

print("Sans pruning")
debut = time.time()
chemin, dist = graph_implicit.shortest_path(
    vs=(network_test.start, 0),
    vt=network_test.end,
    is_target=lambda node: node[0] == network_test.end
)
print(f"Distance : {dist}, temps : {time.time() - debut:.4f}s")

print("--- Avec pruning ---")
debut = time.time()
chemin, dist = graph_implicit.shortest_path(
    vs=(network_test.start, 0),
    vt=network_test.end,
    is_target=lambda node: node[0] == network_test.end,
    pruning=True
)
print(f"Distance : {dist}, temps : {time.time() - debut:.4f}s")

#%%
from network import *
from graph import Graph
import time

print("large-largefatigue.txt")
network_test = Network.from_file(r"examples\large-largefatigue.txt")
graph_implicit = GraphImplicit(network_test)

'''
print("Sans pruning")
debut = time.time()
chemin, dist = graph_implicit.shortest_path(
    vs=(network_test.start, 0),
    vt=network_test.end,
    is_target=lambda node: node[0] == network_test.end
)
print(f"Distance : {dist}, temps : {time.time() - debut:.4f}s")

Crash car beaucoup trop long?
'''

print("Avec pruning")
debut = time.time()
chemin, dist = graph_implicit.shortest_path(
    vs=(network_test.start, 0),
    vt=network_test.end,
    is_target=lambda node: node[0] == network_test.end,
    pruning=True
)
print(f"Distance : {dist}, temps : {time.time() - debut:.4f}s")
'329s et 8338974 noeuds prunés énorme !'

print("large-smallfatigue.txt")
network_test = Network.from_file(r"examples\large-smallfatigue.txt")
graph_implicit = GraphImplicit(network_test)

print("Sans pruning")
debut = time.time()
chemin, dist = graph_implicit.shortest_path(
    vs=(network_test.start, 0),
    vt=network_test.end,
    is_target=lambda node: node[0] == network_test.end
)
print(f"Distance : {dist}, temps : {time.time() - debut:.4f}s")
337s

print("Avec pruning")
debut = time.time()
chemin, dist = graph_implicit.shortest_path(
    vs=(network_test.start, 0),
    vt=network_test.end,
    is_target=lambda node: node[0] == network_test.end,
    pruning=True
)
print(f"Distance : {dist}, temps : {time.time() - debut:.4f}s")
"""
558048 prunés, 15s
"""
#%%
from network import *
from graph import Graph
import time

network_test = Network.from_file(r"examples\medium-smallfatigue.txt")

# on choisit pour heuristique la distance entre le noeud d'arrivé et le noeud actuel,
#Cette heuristique est admissible car on prend une fatigue = 0
# alors que la fatigue augmente le coût des arrêtes!
graph_inverse = network_test.build_simple_graph(inverse=True)
h = graph_inverse.distances_depuis(network_test.end)
heuristique = lambda node: h.get(node[0], float("inf"))

graph_implicit = GraphImplicit(network_test)
print("---Comparaison pruning et heuristique---")
for pruning, avec_h in [(False, False), (True, False), (False, True), (True, True)]:
    label = f"pruning={pruning}, A*={avec_h}"
    debut = time.time()
    chemin, dist = graph_implicit.shortest_path(
        vs=(network_test.start, 0),
        vt=network_test.end,
        is_target=lambda node: node[0] == network_test.end,
        pruning=pruning,
        heuristique=heuristique if avec_h else None
    )
    print(f"{label} — distance : {dist}, temps : {time.time() - debut:.4f}s")

"""
---Comparaison pruning et heuristique---
pruning=False, A*=False — distance : 29934, temps : 0.0440s
Noeuds prunés : 982
pruning=True, A*=False — distance : 29934, temps : 0.0073s
pruning=False, A*=True — distance : 29934, temps : 0.0506s
Noeuds prunés : 969
pruning=True, A*=True — distance : 29934, temps : 0.0078s
"""
#%%
from network import *
from graph import Graph
import time

network_test = Network.from_file(r"examples\large-smallfatigue.txt")

"""
on choisit pour heuristique la distance entre le noeud d'arrivé et le noeud actue dans un graphe simple,
multipliée par la 1+la fatigue du noeud courant.
Cette heuristique est admissible car les fatigues sont toujours >= 0, donc un chemin partant du noeud 
courant est toujours plus long que si la fatigue était restée constante à partir du noeud courant.
alors que la fatigue augmente le coût des arrêtes!
"""
graph_inverse = network_test.build_simple_graph(inverse=True)
h = graph_inverse.distances_depuis(network_test.end)
heuristique = lambda node: (1+node[1])*h.get(node[0], float("inf"))

graph_implicit = GraphImplicit(network_test)
print("---Comparaison pruning et heuristique 2---")
for pruning, avec_h in [(True, False), (True, True)]:
    label = f"pruning={pruning}, A*={avec_h}"
    debut = time.time()
    chemin, dist = graph_implicit.shortest_path(
        vs=(network_test.start, 0),
        vt=network_test.end,
        is_target=lambda node: node[0] == network_test.end,
        pruning=pruning,
        heuristique=heuristique if avec_h else None
    )
    print(f"{label} — distance : {dist}, temps : {time.time() - debut:.4f}s")


"""
---Comparaison pruning et heuristique 2--- avec heuristique distance simple graph
Noeuds prunés : 558048
pruning=True, A*=False — distance : 2000993, temps : 16.2147s
Noeuds prunés : 557876
pruning=True, A*=True — distance : 2000993, temps : 16.0221s
PS C:/Users/qnosm/OneDrive/Bureau/ENSAE/info 1A/ensae-prog26>

---Comparaison pruning et heuristique 2---  avec heuristique (1+f)*distance simple graph
Noeuds prunés : 558048
pruning=True, A*=False — distance : 2000993, temps : 21.4233s
Noeuds prunés : 410710
pruning=True, A*=True — distance : 2000993, temps : 17.6870s
(fait sur l'ordinateur de maxime)
"""

#%%
from network import *
from graph import Graph
import time

"""Test de shortest_path_mission"""
network = Network.from_file(r"examples\medium-smallfatigue.txt")

graph = GraphImplicit(network)

# Définir des missions arbitraires (choisis des sommets qui existent dans le fichier)
missions = [(v8, v16), (v16, v50), (v50, v60)]


temps = graph.shortest_path_mission(missions)
print(f"Temps total : {temps}")

# Vérification de cohérence : comparer avec deux shortest_path indépendants
_, t1 = graph.shortest_path(v8, v16, pruning=True)
_, t2 = graph.shortest_path(v16, v50, pruning=True)
_, t3 = graph.shortest_path(v50, v60)
print(f"Somme naïve : {t1 + t2 + t3}") 
# %%

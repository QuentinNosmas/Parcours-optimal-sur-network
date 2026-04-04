import sys
sys.path.append("code")  # pour trouver graph.py et network.py

from network import *
from graph import Graph

def test_shortest_path_simple():
    g = Graph({
        'A': [('B', 10), ('C', 3)],
        'B': [('D', 2)],
        'C': [('B', 4), ('D', 8)],
        'D': []
    })
    chemin, dist = g.shortest_path('A', 'D')
    assert dist == 9
    assert chemin == ['A', 'C', 'B', 'D']

def test_shortest_path_etendu():
    network_main = Network(
        roads={'A': [('B', 2, 1)], 'B': [('C', 3, 2)], 'C': []},
        start='A', end='C'
    )
    graph_etendu = network_main.build_extended_graph()
    chemin, dist = graph_etendu.shortest_path(
        vs=('A', 0), vt='C',
        is_target=lambda node: node[0] == 'C'
    )
    assert dist == 8
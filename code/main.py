from network import *
from graph import Graph

# Load the network
network_file = "examples/small.txt"
network = Network.from_file(network_file)

g= network.build_simple_graph()
g.shortest_path()


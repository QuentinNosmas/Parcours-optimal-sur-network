class Graph:

    def __init__(self, edges):
        self._edges = edges

    def neighbours(self, node):
        if node not in self._edges:
            return []
        return self._edges[node]

    def find(self, P,d):
    a=P[0]
    for i in P:
        if d[i]<d[a]:
            a=i            
    return a 

    def shortest_path(self,start_node):
    P=[start_node]
    nodes = list(self._edges.keys())
    d = {node: float('inf') for node in nodes}
    d[start_node] = 0
    while len(P)!=0 :
        a = self.find(P,d)
        P.remove(a)
        for u , weight in self.neighbours(a):
            if d[u]>d[a]+weight:
                d[u]=d[a]+weight
            if u not in P:
                P.append(u)
    return d





    



    


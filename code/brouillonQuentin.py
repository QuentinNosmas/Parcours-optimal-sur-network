import numpy as pd

def find(P,d):
    a=P[0]
    for i in P:
        if d[i]<d[a]:
            a=i
    return a 

    
def shortest_path(g,s):
    P=[s]
    n=len(g)
    d=[int('inf') for i in range(n)]
    d[s]=0
    while len(P)!=0 :
        a = find(P,d)
        P.remove(a)
        for u in neighbours(a):
            if u not in P:
                P.append(u)
                if d[u]>d[a]+g[u][a]:
                    d[u]=d[a]+g[u][a]cg 
    return d
        


    


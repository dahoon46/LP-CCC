from tokenize import cookie_re
from graph import Graph
from algorithm.util import most_frequent_color, shuffled
from random import randrange, sample


def greedy_vote(graph: Graph, epsilon = 0.55, n=10):
    clustering = []
    is_clustered = dict((i, False) for i in graph.nodes())
    unclustered_edges = list(graph.edges())
    while unclustered_edges:

        edge_candidates = []
        while unclustered_edges and len(edge_candidates) <= n:
            i = randrange(len(unclustered_edges))
            u, v = unclustered_edges[i]
            if is_clustered[u] or is_clustered[v]:
                unclustered_edges[i], unclustered_edges[-1] = unclustered_edges[-1], unclustered_edges[i]
                unclustered_edges.pop()
                continue
            edge_candidates.append([u,v])
        if len(edge_candidates) == 0: continue
        def calculate(a, b):
            color = graph.color_of(a, b)
            comm = 1
            exclu = 1
            for node in graph.neighbors(a):
                if is_clustered[node]: continue
                if graph.has_edge(node, b):
                    comm += (color == graph.color_of(node, b) and color == graph.color_of(node, a))
                exclu += 1
            for node in graph.neighbors(b):
                if is_clustered[node]: continue
                if graph.has_edge(node, a):
                    continue
                else:
                    exclu += 1
            return exclu / comm

        candidate = min(edge_candidates, key= lambda pair: calculate(pair[0], pair[1]))
        u = candidate[0]
        v = candidate[1]
        edge_color = graph.edges[(u,v)]['color']
        cluster = []
        candidates = [u, v]
        edge_connectivity = {u: 0, v: 0}

        def add_node(node):
            candidates.remove(node)
            cluster.append(node)
            for neig in graph.neighbors(node):
                if is_clustered[neig]: continue
                edge_connectivity[neig] = edge_connectivity.get(neig, 0) + 0.5 + 0.5*(graph.color_of(neig, node)==edge_color)
                if neig not in cluster and neig not in candidates:
                    candidates.append(neig)
          
        add_node(u)
        add_node(v)
        while candidates:
            candidate = max(candidates, key = lambda candidate: edge_connectivity[candidate])
            if edge_connectivity[candidate] / len(cluster) < epsilon:
                break
            add_node(candidate)
        
        for node in cluster: 
            is_clustered[node] = True
        clustering.append((cluster, most_frequent_color(graph, cluster)))
        #clustering.append((cluster, edge_color))
        
    for node in graph.nodes():
        if is_clustered[node] == False:
            clustering.append(([node], 0))

    return clustering

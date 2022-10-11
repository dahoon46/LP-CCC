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

# 将选择边改为选择顶点对（理由：类内顶点间也可能不存在边）  可能存在的问题：如果取样的点对过少，可能会导致得到的最优点对的质量不高（远远比不上存在边的点对）
def greedy_vote_v2(graph: Graph, epsilon = 0.55, n=10):
    clustering = []
    is_clustered = dict((i, False) for i in graph.nodes())
    unclustered_nodes = list(graph.nodes())
    while len(unclustered_nodes) > 1:
        pairs_candidates = []
        pairs_max_info = {}
        # 对于每对顶点，对每种颜色计算系数，返回最大值和对应的颜色
        def calculate_pair(u, v):
            colors_com = {0: 0}
            neighs = 0
            for node in graph.neighbors(u):
                if is_clustered[node]: continue
                if graph.has_edge(node, v) and graph.color_of(u, node) == graph.color_of(v,node):
                    colors_com[graph.color_of(u, node)] = colors_com.get(graph.color_of(u, node), 0) + 1
                neighs += 1
            for node in graph.neighbors(v):
                if is_clustered[node]: continue
                if graph.has_edge(node, u):
                    continue
                else:
                    neighs += 1
            color = max(colors_com.keys(), key=lambda color_com: colors_com[color_com])
            return [(colors_com[color]+1)/(neighs+1), color]
        # 选出n个顶点对
        while len(unclustered_nodes) > 1 and len(pairs_candidates) < n:
            u_idx, v_idx = sample(range(len(unclustered_nodes)), 2)
            u, v = unclustered_nodes[u_idx], unclustered_nodes[v_idx]
            if is_clustered[u]:
                unclustered_nodes[u_idx] = unclustered_nodes[-1]
                unclustered_nodes.pop()
                continue
            if is_clustered[v]:
                unclustered_nodes[v_idx] = unclustered_nodes[-1]
                unclustered_nodes.pop()
                continue
            pairs_candidates.append([u, v])
            pairs_max_info[(u, v)] = calculate_pair(u, v)
        
        # 返回所有点对中系数最大的以及对应的颜色
        if len(pairs_max_info.keys()) == 0: continue
        (u, v) = max(pairs_max_info.keys(), key=lambda pair: pairs_max_info[pair][0])
        color = pairs_max_info[(u,v)][1]

        # 以该点对和颜色进行扩张
        cluster = []
        candidates = [u, v]
        edge_connectivity = {u: 0, v: 0}

        def add_node(node):
            candidates.remove(node)
            cluster.append(node)
            for neig in graph.neighbors(node):
                if is_clustered[neig]: continue
                edge_connectivity[neig] = edge_connectivity.get(neig, 0) + 0.5 + 0.5*(graph.color_of(neig, node)==color)
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
    for node in unclustered_nodes:
        if is_clustered[node]: continue
        clustering.append(([node], 0))
    return clustering

from random import shuffle, random, choices, randrange
from graph import Graph
from algorithm.util import most_frequent_color, shuffled
import queue as Q
from typing import List, Dict
import gurobipy as gp
from gurobipy import GRB

#temporal package
from dataset import read_dataset

def solve_lp(graph: Graph): # solve the LP relaxation
    # Solve the LP relaxation
    model = gp.Model("CCC")
    
    colors = list(graph.colors())
    
    print("Adding variables...")
    v = model.addVars(graph.nodes(), colors, lb=0, ub=1, name="v")
    e = model.addVars(graph.node_pairs(), colors, lb=0, ub=1, name="e")
    
    print("Variables added.")
    L = len(colors)
     
    # objective function
    print("Adding objective function...")
    model.setObjective(gp.quicksum((e[a,b, graph.color_of(a,b)] if graph.has_edge(a,b)
                                   else gp.quicksum(1 - e[a,b, l] for l in colors))
                                   for a, b in graph.node_pairs()), GRB.MINIMIZE)
    
    print("Objective function added.")
    # boundary constraints
    print("Adding chromatic constraints...")
    model.addConstrs((gp.quicksum(v[a,l] for l in colors) == L-1
                      for a in graph.nodes()),
                     "chromatic")
    
    print("Adding edge-node constraints...")
    model.addConstrs((e[a,b,l] >= v[a, l]
                      for l in colors
                      for a, b in graph.node_pairs()
                      ),
                     "ev_1")
    model.addConstrs((e[a,b,l] >= v[b, l]
                      for l in colors
                      for a, b in graph.node_pairs()
                      ),
                     "ev_2")
    
    print("Adding triangle constraints...")
    model.addConstrs((e[b,c,l] + e[a,c,l] >= e[a,b, l]
                      for l in colors for a in graph.nodes()
                      for b in graph.nodes() if a<b
                      for c in graph.nodes() if b<c
                      ),
                     "triangle_1")
    model.addConstrs((e[a,b,l] + e[a,c,l] >= e[b,c, l]
                      for l in colors for a in graph.nodes()
                      for b in graph.nodes() if a<b
                      for c in graph.nodes() if b<c
                      ),
                     "triangle_2")
    model.addConstrs((e[a,b,l] + e[b,c,l] >= e[a,c, l]
                      for l in colors for a in graph.nodes()
                      for b in graph.nodes() if a<b
                      for c in graph.nodes() if b<c
                      ),
                     "triangle_3")
    
    print("Constraints added.")
    # solve the problem
    
    model.Params.Method = 2
    # model.Params.TimeLimit = 60
    
    model.optimize()
    print(v)
    
    status = model.status
    
    return model, status, v, e

def f(x,s):
  if s==2:
    if x<0.40:
      return 0
    elif x<0.495:
      return 0.78
    else:
      return min(1,0.348*(x-0.5)+0.85)
  elif s==1:
    a=0.19
    b=0.5095
    if x<a:
      return 0
    elif x>b:
      return 1
    else:
      return ((x-a)/(b-a))**2
  else:
      return x
  
def pivot_lp(graph: Graph, model: gp.Model, status: int, v: dict, e: dict): # 2.15-Approximation
    # model, status, v, e = solve_lp(graph)
    if status != GRB.OPTIMAL:
        print("No optimal solution found")
        return []
    print("Optimal solution found")
    print("Objective value:", model.ObjVal)
    
    colors = list(graph.colors())
    L = len(colors)
    partition = dict((color, []) for color in colors)

    clustering = []
    is_clustered = dict((i, False) for i in graph.nodes())

    for a in graph.nodes():
        has_color = False
        for color in colors:
            if v[a, color].X < 0.5:
                has_color = True
                partition[color].append(a)
                break
        if not has_color:
            is_clustered[a] = True
            clustering.append(([a], choices(colors, k=1)[0]))

    for color in colors:
        for center in shuffled(partition[color]):
            if is_clustered[center]: continue
            cluster = [center]
            is_clustered[center] = True
            for a in partition[color]:
                if is_clustered[a]: continue
                u1 = center
                u2 = a
                if u1 > u2:
                    u1, u2 = u2, u1
                prob = e[u1, u2, color].X
                sign = None
                if not graph.has_edge(u1, u2):
                    sign = 0
                elif graph.color_of(u1, u2) == color:
                    sign = 1
                else:
                    sign = 2
                prob = f(prob, sign)
                if random() < 1-prob:
                    is_clustered[a] = True
                    cluster.append(a)
            clustering.append((cluster, color))
    return clustering
        
def test(dataset_name):
    dataset = read_dataset(dataset_name)
    for graph_number, graph in enumerate(dataset):
        print(f'part {graph_number}')
        clustering = lp(graph.subgraph(range(0, 100)))
        if not graph.is_valid_clustering(clustering):
            print("Invalid clustering")
            continue
        print("Valid clustering")
        print("Clustering:", clustering)
        print("Error:", graph.error_of(clustering))
        print("Number of clusters:", len(clustering))
    
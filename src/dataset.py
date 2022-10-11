from graph import Graph
import os
from os.path import isfile, join
import networkx as nx


def read_dataset(name: str):
    if name in ['facebook1', 'facebook2', 'twitter', 'microsoft_academic', 'lastfm_asia', 'string1']:
        return map(remove_self_loops, read_edgelist_dataset(name))
    data_dict = {
        'string2': (lambda : read_legacy('STRING_ALL.csv')),
        'dblp': (lambda : read_legacy('DBLP_ALL.csv')),
        'dawn': (lambda : read_hyperedge('DAWN_majority.csv')),
        'cook': (lambda : read_hyperedge('Cooking_majority.csv'))
    }
    if name not in data_dict:
        raise Exception('Unknown Dataset')
    return map(remove_self_loops, data_dict[name]())

def remove_self_loops(graph):
    for node in graph.nodes():
        if graph.has_edge(node, node):
            graph.remove_edge(node, node)
    return graph

def read_hyperedge(filename):
    def read_graph(path):
        graph = Graph()
        with open(path) as file:
            line = file.readline()
            while line:
                elems = [int(x) for x in line.strip().split(',')]
                u = elems[0]
                v = elems[1]
                graph.add_edge(u, v)
                graph[u][v]['color'] = elems[2]
                line = file.readline()
        return graph

    path = '../data/hyperedge/' + filename
    return [read_graph(path)]

def read_legacy(filename):
    def read_graph(path):
        return nx.read_edgelist(path, comments='#', delimiter=' ', create_using=Graph, nodetype =int, data=[('color', int)])

    directory = '../data/legacy'
    return [read_graph(os.path.join(directory, filename))]

def read_edgelist_dataset(filename):
    def read_graph(path):
        return Graph(nx.read_edgelist(path, comments='#', delimiter=' ', nodetype=int, data=[('color', int)]))

    directory = '../data/edgelist_datasets'
    return [read_graph(os.path.join(directory, filename+'.edgelist'))]

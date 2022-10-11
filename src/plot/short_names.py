def remove_alg_prefix(alg):
    return alg.split('.', maxsplit = 1)[1] if len(alg.split('.')) > 1 else alg

algorithm_short_names = {
    'pivot(graph)': 'Pivot',
    'reduce_and_cluster(graph)': 'RC',
    'deep_cluster(graph)': 'DC',
    'chromatic_balls(graph)': 'CB',
    'greedy_expansion(graph)': 'GE',
    'greedy_expansion(graph.primary_edge_graph())': 'GER',
    'greedy_vote(graph)': 'GV',

    'primary_edge_graph':'primary_edge_graph',  # logs time required to delete secondary edges
}

dataset_short_names = {
    'facebook_1': 'Facebook1', 
    'facebook_2': 'Facebook2',
    'twitter': 'Twitter', 
    'microsoft_academic': 'MAG',
    #'string1': 'String1',
    'plinks': 'String1',
    #'string2': 'String2',
    'string': 'String2',
    'dawn': 'DAWN',
    'dblp': 'DBLP',
    'lastfm_asia': 'Lastfm',
    'cook': 'Cook',
}

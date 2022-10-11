import numpy as np
import pandas as pd
import ast
import matplotlib.pyplot as plt
import textwrap
from statistics import mean
from scipy.stats import mannwhitneyu
from short_names import algorithm_short_names, dataset_short_names, remove_alg_prefix
import locale
import csv
from matplotlib.backends.backend_pdf import PdfPages

locale.setlocale(locale.LC_ALL, 'en_us')

def read_log(filename, dataset_name):
    df = pd.read_csv(filename)
    df['approx_errors'] = df['approx_errors'].apply(lambda array: ast.literal_eval(array))
    return df.loc[df['dataset'] == dataset_name].loc[df['algorithm'].apply(lambda a: a in algorithm_short_names.keys())].sort_values(by = 'mean_approx_error')

def table_string(filename, dataset_names, algorithms, runtime = False):
    primary_graph_algorithms = set(['RC', 'DC', 'GER'])
    entries = {}
    df = pd.read_csv(filename)
    df['wall_clock_times'] = df['wall_clock_times'].apply(lambda array: ast.literal_eval(array))
    for name in dataset_names:
        errors = {}
        for _, row in df.loc[df['dataset'] == name].iterrows():
            alg = row['algorithm']
            if alg not in algorithm_short_names: continue
            alg_name = algorithm_short_names[alg]
            if alg_name in errors:
                raise Exception(f'Watch out! Multiple entries with name {alg} on {name}')
            if runtime:
                errors[alg_name] = round(mean(row['wall_clock_times']), 2)
            else:
                errors[alg_name] = round(row['mean_approx_error'])
        entries[name] = errors
    
    table = "dataset & " + " & ".join(algorithms) + "\\\\\n"
    def adapted_entry(name, alg):
        value = entries[name][alg]
        if runtime and alg in primary_graph_algorithms:
            value += entries[name]['primary_edge_graph']
        string = locale.format_string(f"%.{0 if not runtime else 2}f", value, grouping=True)
        if not runtime and value == min([entries[name][a] for a in algorithms]):
            string = '\\textbf{' + string + '}'
        return string

    for name in dataset_names:
        table += f'{dataset_short_names[name]} & ' + " & ".join([adapted_entry(name, alg) for alg in algorithms]) + "\\\\\n"
    return table

def table_to_csv(my_table, file_name):
    lines = my_table.split('\\\\\n')
    with open(file_name, 'w+') as pf:
        csvfile = csv.writer(pf)
        for i in range(0, len(lines)):
            csvfile.writerow(lines[i].split(' & '))


def table_single(filename, runtime=False):
    algorithms = ['Pivot', 'RC', 'DC', 'CB', 'GER', 'GE', 'GV']
    dataset_names = ['facebook1', 'facebook2', 'lastfm_asia', 'dawn', 'string1', 'string2', 'dblp', 'twitter', 'microsoft_academic']
    my_table = table_string(filename, dataset_names, algorithms, runtime=runtime)
    print(my_table)
    if runtime:
        table_to_csv(my_table, '../../measurements/wall_clock_times_single.csv')
    else:
        table_to_csv(my_table, '../../measurements/mean_approx_errors_single.csv')


filename ='../../measurements/log.csv'
plt.rcParams.update({
    'font.size': 16,
    })


table_single(filename, runtime = False)
table_single(filename, runtime = True)


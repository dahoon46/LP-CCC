# Requirements
- networkx
- matplotlib

# Intro
## Files

- `data`  
This folder contains the datasets used for the experiments, which are preprocessed. Each line of the datafile is like

node1 node2 color

- `src`  
    - `algorithm`  
    This folder contains all algorithms we test.
    - `plot`  
    This folder is used to evaluate the results, which are displayed in the form of two tables.
    - other files

## How to run  
You can execute ``experiment.py`` from the path `./src/` to get the results, which will be put in `./measurements/log.csv`. Note that it may spend a long time on this script, while you can reduce the number of runs for shorter tests.

After getting results file `log.csv`, it can be evaluated running ``plotting.py`` from the path `./src/plot/`.

# Acknowledgement

The data sets belong to their respective owners. They do not belong to us and are only included for better reproducability. The owners are explained in the publication. Please cite them accordingly when using these data sets.

Some code files are from https://github.com/arthurz0/3-approx-for-ccc-and-heuristics and we use them for performance evaluation.

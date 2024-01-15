#!/bin/bash

targ="Fe"

./run_gibuu.py -mode farm -seed 0 -targ ${targ} -run1 1 -run2 200 -lambdadec 1 -expt clas6 -kt 0.44
./run_gibuu.py -mode farm -seed 0 -targ ${targ} -run1 1 -run2 200 -lambdadec 1 -expt clas6 -kt 0.50
./run_gibuu.py -mode farm -seed 0 -targ ${targ} -run1 1 -run2 200 -lambdadec 1 -expt clas6 -kt 0.60
./run_gibuu.py -mode farm -seed 0 -targ ${targ} -run1 1 -run2 200 -lambdadec 1 -expt clas6 -kt 0.70
./run_gibuu.py -mode farm -seed 0 -targ ${targ} -run1 1 -run2 200 -lambdadec 1 -expt clas6 -kt 0.80
./run_gibuu.py -mode farm -seed 0 -targ ${targ} -run1 1 -run2 200 -lambdadec 1 -expt clas6 -kt 0.85
./run_gibuu.py -mode farm -seed 0 -targ ${targ} -run1 1 -run2 200 -lambdadec 1 -expt clas6 -kt 0.90
./run_gibuu.py -mode farm -seed 0 -targ ${targ} -run1 1 -run2 200 -lambdadec 1 -expt clas6 -kt 0.95
./run_gibuu.py -mode farm -seed 0 -targ ${targ} -run1 1 -run2 200 -lambdadec 1 -expt clas6 -kt 1.0

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 11:51:10 2020

@author: wkg
"""

import json
import os

os.chdir("/home/wkg/complex_mapping")

with open("complexes_multiple_copies.json", "r") as handle:
    complexes = json.load(handle)
    
with open("complexes_repeated_distinct_prop.json", "r") as handle:
    complexes_prop_repeated = json.load(handle)

with open("complexes_total_peptide_counts.json", "r") as handle:
    complexes_total_pep_counts = json.load(handle)

planarity = {}
with open("planarity_results.csv", "r") as handle:
    for line in handle:
        line = line.strip("\n").split(",")
        planarity[line[0]] = line[1]

planars = [complexes[comp] for comp in planarity if planarity[comp] == "planar"]
nonplanars = [complexes[comp] for comp in planarity if planarity[comp] == "nonplanar"]

with open("num_repeats_by_planarity.csv", "w") as out:
    out.write("planars,nonplanars")
    out.write("\n")
    for idx, num in enumerate(planars):
        try:
            out.write(",".join([str(num), str(nonplanars[idx])]))
            out.write("\n")
        except IndexError:
            out.write(",".join([str(num), "NA"]))
            out.write("\n")
######################################
planars = [complexes_prop_repeated[comp] for comp in planarity if planarity[comp] == "planar"]
nonplanars = [complexes_prop_repeated[comp] for comp in planarity if planarity[comp] == "nonplanar"]

with open("prop_repeats_by_planarity.csv", "w") as out:
    out.write("planars,nonplanars")
    out.write("\n")
    for idx, num in enumerate(planars):
        try:
            out.write(",".join([str(num), str(nonplanars[idx])]))
            out.write("\n")
        except IndexError:
            out.write(",".join([str(num), "NA"]))
            out.write("\n")
##########################################



#################################
complexes_w_repeats = [c for c in complexes if complexes[c] > 0]
planarity_of_complexes_w_repeats = [planarity[c] for c in complexes if complexes[c] > 0]
pct_planar = len([c for c in planarity_of_complexes_w_repeats if c=='planar'])/len(planarity_of_complexes_w_repeats)

planarity_of_complexes_wo_repeats = [planarity[c] for c in complexes if complexes[c] == 0]
pct_planar = len([c for c in planarity_of_complexes_wo_repeats if c=='planar'])/len(planarity_of_complexes_wo_repeats)




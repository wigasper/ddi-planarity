#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

os.chdir("/home/wkg/complex_mapping")

with open("complex_secondary_structs.json", "r") as handle:
    complexes = json.load(handle)
    
unique_pcts = {}

#for key in complexes:
#    elements = complexes[key]
#    unique_elements = list(dict.fromkeys(elements))
#    unique_pcts[key] = len(unique_elements) / len(elements)

planarity = {}
with open("planarity_results.csv", "r") as handle:
    for line in handle:
        line = line.strip("\n").split(",")
        planarity[line[0]] = line[1]

planars_helices = []
planars_strands = []
nonplanars_helices = []
nonplanars_strands = []
for comp in planarity:
    if planarity[comp] == "planar":
        planars_helices.append(complexes[comp]["helices"])
        planars_strands.append(complexes[comp]["strands"])
    else:
        nonplanars_helices.append(complexes[comp]["helices"])
        nonplanars_strands.append(complexes[comp]["strands"])

sum(nonplanars_helices) / len(nonplanars_helices)
sum(planars_helices) / len(planars_helices)

sum(nonplanars_strands) / len(nonplanars_strands)
sum(planars_strands) / len(planars_strands)

with open("helix_data.csv", "w") as out:
    out.write("planars,nonplanars")
    out.write("\n")
    for idx, num in enumerate(planars_helices):
        try:
            out.write(",".join([str(num), str(nonplanars_helices[idx])]))
            out.write("\n")
        except IndexError:
            out.write(",".join([str(num), "NA"]))
            out.write("\n")
            
with open("strand_data.csv", "w") as out:
    out.write("planars,nonplanars")
    out.write("\n")
    for idx, num in enumerate(planars_strands):
        try:
            out.write(",".join([str(num), str(nonplanars_strands[idx])]))
            out.write("\n")
        except IndexError:
            out.write(",".join([str(num), "NA"]))
            out.write("\n")
############################################
            ################################
            ################################
# some data work to get everything good for statistical tests
with open("complex_secondary_struct_residue_counts.json", "r") as handle:
    complexes = json.load(handle)

with open("complex_total_residue_counts.json", "r") as handle:
    complexes_residue_counts = json.load(handle)
    
planarity = {}
with open("planarity_results.csv", "r") as handle:
    for line in handle:
        line = line.strip("\n").split(",")
        if line[0] != "5H7I":
            planarity[line[0]] = line[1]

planars_helices = []
planars_strands = []
nonplanars_helices = []
nonplanars_strands = []
for comp in planarity:
    helices_prop = complexes[comp]["helix_residues"] / complexes_residue_counts[comp]
    strands_prop = complexes[comp]["strand_residues"] / complexes_residue_counts[comp]
    if planarity[comp] == "planar":
        planars_helices.append(helices_prop)
        planars_strands.append(strands_prop)
    else:
        nonplanars_helices.append(helices_prop)
        nonplanars_strands.append(strands_prop)

sum(nonplanars_helices) / len(nonplanars_helices)
sum(planars_helices) / len(planars_helices)

sum(nonplanars_strands) / len(nonplanars_strands)
sum(planars_strands) / len(planars_strands)

with open("helix_residue_prop_data.csv", "w") as out:
    out.write("planars,nonplanars")
    out.write("\n")
    for idx, num in enumerate(planars_helices):
        try:
            out.write(",".join([str(num), str(nonplanars_helices[idx])]))
            out.write("\n")
        except IndexError:
            out.write(",".join([str(num), "NA"]))
            out.write("\n")
            
with open("strand_residue_prop_data.csv", "w") as out:
    out.write("planars,nonplanars")
    out.write("\n")
    for idx, num in enumerate(planars_strands):
        try:
            out.write(",".join([str(num), str(nonplanars_strands[idx])]))
            out.write("\n")
        except IndexError:
            out.write(",".join([str(num), "NA"]))
            out.write("\n")
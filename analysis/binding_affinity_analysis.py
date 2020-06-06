#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os

#os.chdir("/home/wkg/complex_mapping")

binding_affs = {}
with open("binding_affinity_data.csv", "r") as handle:
    for line in handle:
        if not line.startswith("pdb_id"):
            line = line.strip("\n").split(",")
            if line[12] != "na":
                binding_affs[line[0]] = line[12]
    
planarity = {}
with open("../planarity_results.csv", "r") as handle:
    for line in handle:
        line = line.strip("\n").split(",")
        planarity[line[0]] = line[1]

planars = [binding_affs[comp] for comp in binding_affs if planarity[comp.upper()] == "planar"]
nonplanars = [binding_affs[comp] for comp in binding_affs if planarity[comp.upper()] == "nonplanar"]

with open("binding_aff_by_planarity.csv", "w") as out:
    out.write("planars,nonplanars\n")
    for idx, num in enumerate(planars):
        try:
            out.write(",".join([str(num), str(nonplanars[idx])]))
            out.write("\n")
        except IndexError:
            out.write(",".join([str(num), "NA"]))
            out.write("\n")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 12:35:54 2020

@author: wkg
"""
import json

planarity = {}
with open("../planarity_results.csv", "r") as handle:
    for line in handle:
        line = line.strip("\n").split(",")
        planarity[line[0]] = line[1]
        
planars = [k for k, v in planarity.items() if planarity[k] == "planar"]
nonplanars = [k for k, v in planarity.items() if planarity[k] == "nonplanar"]
   
with open("../pdb_complex_map_uids.json", "r") as handle:
    complex_uids = json.load(handle)

with open("../planars", "w") as out:
    for comp in planars:
        try:
            for uid in complex_uids[comp]:
                out.write(f"{uid}\n")
        except KeyError:
            print(f"keyerror: {comp}")

with open("../nonplanars", "w") as out:
    for comp in nonplanars:
        try:
            for uid in complex_uids[comp]:
                out.write(f"{uid}\n")
        except KeyError:
            print(f"keyerror: {comp}")



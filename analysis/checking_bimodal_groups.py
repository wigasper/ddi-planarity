#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar  7 12:35:54 2020

@author: wkg
"""
import json

with open("complexes_repeated_distinct_prop.json", "r") as handle:
    complexes_prop_repeated = json.load(handle)
    
planarity = {}
with open("planarity_results.csv", "r") as handle:
    for line in handle:
        line = line.strip("\n").split(",")
        planarity[line[0]] = line[1]
        
planar_prop_repeated = {k:v for k,v in complexes_prop_repeated.items() if planarity[k] == "planar"}

upper = [key.lower() for key in planar_prop_repeated if planar_prop_repeated[key] > .5]
lower = [key.lower() for key in planar_prop_repeated if planar_prop_repeated[key] <= .5]

b_affs = {}
with open("binding_affinity/binding_affinity_data.csv", "r") as handle:
    for line in handle:
        if not line.startswith("pdb_id"):
            line = line.split(",")
            if line[12] != "na":
                if planarity[line[0].upper()] == "planar": 
                    b_affs[line[0]] = line[12]

upper_affs = [k for k in b_affs if float(b_affs[k]) > -200]
lower_affs = [k for k in b_affs if float(b_affs[k]) <= -200]

uppers_in_both = [i for i in upper if i in upper_affs]
lowers_in_both = [i for i in lower if i in lower_affs]

test0 = [i for i in upper if i in lower_affs]
test1 = [i for i in lower if i in upper_affs]

with open("pdb_complex_map_uids.json", "r") as handle:
    complex_uids = json.load(handle)
    
with open("upper_affs_list", "w") as out:
    for it in upper_affs:
        try:
            for uid in complex_uids[it.upper()]:
                out.write(f"{uid}\n")
        except KeyError:
            print(f"keyerror: {it}")

with open("lower_affs_list", "w") as out:
    for it in lower_affs:
        try:
            for uid in complex_uids[it.upper()]:
                out.write(f"{uid}\n")
        except KeyError:
            print(f"keyerror: {it}")
            
with open("upper_repeats_list", "w") as out:
    for it in upper:
        try:
            for uid in complex_uids[it.upper()]:
                out.write(f"{uid}\n")
        except KeyError:
            print(f"keyerror: {it}")

with open("lower_repeats_list", "w") as out:
    for it in lower:
        try:
            for uid in complex_uids[it.upper()]:
                out.write(f"{uid}\n")
        except KeyError:
            print(f"keyerror: {it}")
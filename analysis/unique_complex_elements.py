import json
import os

os.chdir("/home/wkg/complex_mapping")

with open("pdb_complex_map_uids.json", "r") as handle:
    complexes = json.load(handle)
    
unique_pcts = {}

for key in complexes:
    elements = complexes[key]
    unique_elements = list(dict.fromkeys(elements))
    unique_pcts[key] = len(unique_elements) / len(elements)

planarity = {}
with open("planarity_results.csv", "r") as handle:
    for line in handle:
        line = line.strip("\n").split(",")
        planarity[line[0]] = line[1]

repeated_elements = {}
for key in complexes:
    repeated = complexes[key]
    unique_elements = list(dict.fromkeys(repeated))
    for element in unique_elements:
        repeated.remove(element)
    for element in list(dict.fromkeys(repeated)):
        repeated.append(element)
    repeated.sort()
    repeated_elements[key] = repeated
    
complexes_w_repeats = []
for comp in repeated_elements:
    if len(repeated_elements[comp]) > 0:
        complexes_w_repeats.append(comp)
        
rpt_comps_planarity = [planarity[comp] for comp in complexes_w_repeats]
pct_planar = len([c for c in rpt_comps_planarity if c == 'planar']) / len(rpt_comps_planarity)


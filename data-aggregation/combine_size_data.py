#!/usr/bin/env python3

import os
import json

complex_fps = os.listdir("complexes")

complex_unique_domains = {}
complex_edge_counts = {}
for comp in complex_fps:
    with open(f"complexes/{comp}", "r") as handle:
        comp = comp.split(".")[0]
        unique_domains = []
        num_edges = 0
        for line in handle:
            num_edges += 1
            line = line.split()
            unique_domains.append(line[0])
            unique_domains.append(line[1])
        complex_edge_counts[comp] = num_edges
        
        complex_unique_domains[comp] = len(list(dict.fromkeys(unique_domains)))
    
with open("complex_total_residue_counts.json", "r") as handle:
    complex_residues = json.load(handle)

planarity = {}
with open("planarity_results.csv", "r") as handle:
    for line in handle:
        line = line.strip("\n").split(",")
        #if line[0] != "5H7I":
        planarity[line[0]] = line[1]
            
with open("complex_size_domains_edges.csv", "w") as out:
    out.write(",".join(["pdb_id", "size_in_residues", "num_unique_domains", 
                        "num_interactions", "planarity"]))
    out.write("\n")
    for comp in complex_residues:
        out.write(",".join([comp, str(complex_residues[comp]), str(complex_unique_domains[comp]),
                            str(complex_edge_counts[comp]), planarity[comp]]))
        out.write("\n")
    

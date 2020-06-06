#!/usr/bin/env python3
import os

def get_sorted_prop_list_1(hash_map):
    counts = {v: 0 for k, v in hash_map.items()}
    for gene_id in hash_map:
        counts[hash_map[gene_id]] += 1
    
    props = [[k, v / len(hash_map)] for k, v in counts.items()]
    props = sorted(props, key=lambda props: props[1], reverse=True)

    return props 

def get_sorted_prop_list(hash_map):
    counts = {}
    for item_list in hash_map:
        for item in hash_map[item_list]:
            if item in counts.keys():
                counts[item] += 1
            else:
                counts[item] = 1
    
    term_props = [[k, v / len(hash_map)] for k, v, in counts.items()]
    term_props = sorted(term_props, key=lambda term_props: term_props[1], 
                        reverse=True)
    
    return term_props
    
if __name__ == "__main__":
    os.chdir("/home/wkg/complex_mapping")
    
    planar_gos = {}
    with open("panther_planars", "r") as handle:
        for line in handle:
            line = line.split("\t")
            gene_id = line[1]
            go_terms = line[7].split(";")
            go_terms = [t.strip("\n") for t in go_terms]
            planar_gos[gene_id] = go_terms
    
    planar_go_term_props = get_sorted_prop_list(planar_gos)
    
    nonplanar_gos = {}
    with open("panther_nonplanars", "r") as handle:
        for line in handle:
            line = line.split("\t")
            gene_id = line[1]
            go_terms = line[7].split(";")
            go_terms = [t.strip("\n") for t in go_terms]
            nonplanar_gos[gene_id] = go_terms
    
    nonplanar_go_term_props = get_sorted_prop_list(nonplanar_gos)
    keys = ["DNA binding(GO:0003677)", "metal ion binding(GO:0046872)", 
            "RNA binding(GO:0003723)", "hydrolase activity(GO:0016787)",
            "transferase activity(GO:0016740)"]
    
    temp_nonplanar_map = {i[0]: i[1] for i in nonplanar_go_term_props if i[0] in keys}
    temp_planar_map = {i[0]: i[1] for i in planar_go_term_props if i[0] in keys}
    
    with open("bar_chart_data/mf", "w") as out:
        for key in keys:
            out.write(",".join([key, str(temp_nonplanar_map[key]), "nonplanar\n"]))
            out.write(",".join([key, str(temp_planar_map[key]), "planar\n"]))
######
    planar_pcs = {}
    with open("panther_planars", "r") as handle:
        for line in handle:
            line = line.split("\t")
            gene_id = line[1]
            panther_fam = line[4]
            planar_pcs[gene_id] = panther_fam
    
    planar_pcs_props = get_sorted_prop_list_1(planar_pcs)
    
    nonplanar_pcs = {}
    with open("panther_nonplanars", "r") as handle:
        for line in handle:
            line = line.split("\t")
            gene_id = line[1]
            panther_fam = line[4]
            nonplanar_pcs[gene_id] = panther_fam
    
    nonplanar_pcs_props = get_sorted_prop_list_1(nonplanar_pcs)
    
    keys = ["ribosomal protein(PC00202)", "RNA splicing factor(PC00148)",
            "ATP synthase(PC00002)", "general transcription factor(PC00259)",
            "oxidase(PC00175)"]
    temp_nonplanar_map = {i[0]: i[1] for i in nonplanar_pcs_props if i[0] in keys}
    temp_planar_map = {i[0]: i[1] for i in planar_pcs_props if i[0] in keys}
    
    with open("bar_chart_data/prot_class", "w") as out:
        for key in keys:
            out.write(",".join([key, str(temp_nonplanar_map[key]), "nonplanar\n"]))
            out.write(",".join([key, str(temp_planar_map[key]), "planar\n"]))
######
    planar_gos_bp = {}
    with open("panther_planars_bp", "r") as handle:
        for line in handle:
            line = line.split("\t")
            gene_id = line[1]
            go_terms = line[3].split(";")
            go_terms = [t.strip("\n") for t in go_terms]
            planar_gos_bp[gene_id] = go_terms
    
    planar_go_bp_props = get_sorted_prop_list(planar_gos_bp)
    
    nonplanar_gos_bp = {}
    with open("panther_nonplanars_bp", "r") as handle:
        for line in handle:
            line = line.split("\t")
            gene_id = line[1]
            go_terms = line[3].split(";")
            go_terms = [t.strip("\n") for t in go_terms]
            nonplanar_gos_bp[gene_id] = go_terms
    
    nonplanar_go_bp_props = get_sorted_prop_list(nonplanar_gos_bp)

    keys = ["mRNA processing(GO:0006397)", "ion transport(GO:0006811)",
            "DNA repair(GO:0006281)", "RNA splicing(GO:0008380)",
            "protein transport(GO:0015031)"]
    
    temp_nonplanar_map = {i[0]: i[1] for i in nonplanar_go_bp_props if i[0] in keys}
    temp_planar_map = {i[0]: i[1] for i in planar_go_bp_props if i[0] in keys}
    
    with open("bar_chart_data/bp", "w") as out:
        for key in keys:
            out.write(",".join([key, str(temp_nonplanar_map[key]), "nonplanar\n"]))
            out.write(",".join([key, str(temp_planar_map[key]), "planar\n"]))
###############################################
# not using GO slim
    planar_gos_slim = {}
    with open("panther_planars", "r") as handle:
        for line in handle:
            line = line.split("\t")
            gene_id = line[1]
            go_terms = line[6].split(";")
            planar_gos_slim[gene_id] = go_terms
            
    planar_go_slim_props = get_sorted_prop_list(planar_gos)
    
    nonplanar_gos = {}
    with open("panther_nonplanars", "r") as handle:
        for line in handle:
            line = line.split("\t")
            gene_id = line[1]
            go_terms = line[6].split(";")
            nonplanar_gos[gene_id] = go_terms
    
    nonplanar_go_slim_props = get_sorted_prop_list(nonplanar_gos)

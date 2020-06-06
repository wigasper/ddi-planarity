import json
import re

if __name__ == "__main__":
    with open("complex_disorder_by_uids.json", "r") as handle:
        comps = json.load(handle)

    mean_dcs = {}
    
    for comp in comps:
        if len(comps[comp]) > 0:
            mean_dc = sum([float(i) for i in comps[comp]]) / len(comps[comp])
        else:
            mean_dc = 0
        mean_dcs[comp] = mean_dc
        
    planarity = {}
    with open("planarity_results.csv", "r") as handle:
        for line in handle:
            line = line.strip("\n").split(",")
            if line[0] != "5H7I":
                planarity[line[0]] = line[1]

    planars = [mean_dcs[comp] for comp in planarity if planarity[comp] == "planar"]
    nonplanars = [mean_dcs[comp] for comp in planarity if planarity[comp] == "nonplanar"]
    
    pct_highly_disordered = {}
    
    for comp in comps:
        threshold = 0.5
        
        if len(comps[comp]) > 0:
            pct = len([p for p in comps[comp] if float(p) > threshold]) / len(comps[comp])
        else:
            pct = 0
        pct_highly_disordered[comp] = pct

    planars = [pct_highly_disordered[comp] for comp in planarity if planarity[comp] == "planar"]
    nonplanars = [pct_highly_disordered[comp] for comp in planarity if planarity[comp] == "nonplanar"]
    sum(planars) / len(planars)
    sum(nonplanars) / len(nonplanars)

    with open("pdb_complex_map_uids.json", "r") as handle:
        complex_uids = json.load(handle)
    
    all_uids = []
    
    for comp in complex_uids:
        all_uids.extend(complex_uids[comp])
        
    all_uids_set = list(dict.fromkeys(all_uids))
        
    unknown_dcs = []
    with open("get_complex_disorder.log", "r") as handle:
        for line in handle:
            line = line.strip("\n")
            match = re.search(r"Unknown dc for (\w+)$", line)
            if match:
                unknown_dcs.append(match.group(1))
    
    unknown_dcs = list(dict.fromkeys(unknown_dcs))
    
    raw_count_unknowns = 0
    unk_dcs_set = set(unknown_dcs)
    for uid in all_uids:
        if uid in unk_dcs_set:
            raw_count_unknowns += 1
    
    raw_count_unknowns / len(all_uids)
    # 101 UIDs out of 866 unique have unknown DCs
    # 41% of the raw counts have are missing DC data
    
#    with open("hydrophobicity_by_planarity.csv", "w") as out:
#        out.write("planars,nonplanars")
#        out.write("\n")
#        for idx, num in enumerate(planars):
#            try:
#                out.write(",".join([str(num), str(nonplanars[idx])]))
#                out.write("\n")
#            except IndexError:
#                out.write(",".join([str(num), "NA"]))
#                out.write("\n")


import json

if __name__ == "__main__":
    with open("complex_ddi_residues.json", "r") as handle:
        complex_residues = json.load(handle)

    hydrophobicity = {'A':.41,'R':-.14,'N':-.28,'D':-.55,'C':.49,'E':-.31,
                      'Q':-.1,'G':0,'H':0.08,'I':.99,'L':.97,'K':-.23,'M':.74,
                      'F':1.0,'P':-.46,'S':-.05,'T':.13,'W':.97,'Y':.63,'V':.76}

    avg_rel_hyd = {}
    
    for comp in complex_residues:
        vals = [hydrophobicity[aa] for aa in complex_residues[comp]]
        mean = sum(vals) / len(vals)
        avg_rel_hyd[comp.upper()] = mean
        
    planarity = {}
    with open("planarity_results.csv", "r") as handle:
        for line in handle:
            line = line.strip("\n").split(",")
            if line[0] != "5H7I":
                planarity[line[0]] = line[1]

    planars = [avg_rel_hyd[comp] for comp in planarity if planarity[comp] == "planar"]
    nonplanars = [avg_rel_hyd[comp] for comp in planarity if planarity[comp] == "nonplanar"]
    

    with open("hydrophobicity_by_planarity.csv", "w") as out:
        out.write("planars,nonplanars")
        out.write("\n")
        for idx, num in enumerate(planars):
            try:
                out.write(",".join([str(num), str(nonplanars[idx])]))
                out.write("\n")
            except IndexError:
                out.write(",".join([str(num), "NA"]))
                out.write("\n")


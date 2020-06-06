import json

if __name__ == "__main__":
    with open("pdb_complex_map_genes.json", "r") as handle:
        complex_map = json.load(handle)

    essentiality = {}
    with open("s_cerevisiae.csv", "r") as handle:
        for line in handle:
            line = line.strip("\n").split(",")
            essentiality[line[1]] = line[4]
            
    planarity = {}
    with open("planarity_results.csv", "r") as handle:
        for line in handle:
            line = line.strip("\n").split(",")
            if line[0] != "5H7I":
                planarity[line[0]] = line[1]
            
    pct_map = {}
    for key in complex_map:
        ess_vals = []
        for gene in complex_map[key]:
            if gene in essentiality.keys():
                    ess_vals.append(essentiality[gene])
            num_e = len([it for it in ess_vals if it == "E"])
            num_ne = len([it for it in ess_vals if it == "NE"])
            if (num_e + num_ne) == 0:
                pct_map[key] = 0
            else:
                pct_map[key] = num_e / (num_e + num_ne)

    planars = [pct_map[comp] for comp in pct_map if planarity[comp] == "planar"]
    nonplanars = [pct_map[comp] for comp in pct_map if planarity[comp] == "nonplanar"]
    

    with open("pct_essentiality_by_planarity.csv", "w") as out:
        out.write("planars,nonplanars")
        out.write("\n")
        for idx, num in enumerate(planars):
            try:
                out.write(",".join([str(num), str(nonplanars[idx])]))
                out.write("\n")
            except IndexError:
                out.write(",".join([str(num), "NA"]))
                out.write("\n")

    with open("complex_essentiality_pcts", "w") as out:
        for key in pct_map:
            out.write(":".join([key, str(pct_map[key])]))
            out.write("\n")

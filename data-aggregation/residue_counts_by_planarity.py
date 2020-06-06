import json

if __name__ == "__main__":
    with open("complex_total_residue_counts.json", "r") as handle:
        complex_residues = json.load(handle)
        
    planarity = {}
    with open("planarity_results.csv", "r") as handle:
        for line in handle:
            line = line.strip("\n").split(",")
            if line[0] != "5H7I":
                planarity[line[0]] = line[1]

    planars = [complex_residues[comp] for comp in planarity if planarity[comp] == "planar"]
    nonplanars = [complex_residues[comp] for comp in planarity if planarity[comp] == "nonplanar"]
    

    with open("residue_counts_by_planarity.csv", "w") as out:
        out.write("planars,nonplanars")
        out.write("\n")
        for idx, num in enumerate(planars):
            try:
                out.write(",".join([str(num), str(nonplanars[idx])]))
                out.write("\n")
            except IndexError:
                out.write(",".join([str(num), "NA"]))
                out.write("\n")


import os
import json

from tqdm import tqdm

def parse_interaction(interaction):
    dom_a_residues = {}
    dom_b_residues = {}

    for line in interaction:
        line = line.split()
        dom_a_residues[line[2]] = line[0]
        dom_b_residues[line[3]] = line[1]

    out = [val for val in dom_a_residues.values()]
    for val in dom_b_residues.values():
        out.append(val)

    return out

def parse_entry(entry, comp_interactions):
    out = {pdbid:[] for pdbid in comp_interactions.keys()}
    relevant_interaction = False
    interaction = []
    pdb_id = ""

    for line in entry:
        if relevant_interaction and not line.startswith("#=3D"):
            interaction.append(line)
        if line.startswith("#=3D"):
            if interaction:
                residues = parse_interaction(interaction)
                #out[pdb_id] = residues
                out[pdb_id].extend(residues)
                interaction = []
            line = line.strip("\n").split()
            pdb_id = line[1]

            relevant_interaction = False
            if pdb_id in comp_interactions.keys():
                relevant_interaction = True
   
    if interaction:
        residues = parse_interaction(interaction)
        out[pdb_id].extend(residues)

    return out

if __name__ == "__main__":
    pdb_ids = os.listdir("/home/wkg/complex_mapping/complexes")
    pdb_ids = [item.split(".")[0] for item in pdb_ids]
    
    # this is what we want, format {pdb_id: [a, e, r, v, k ...], etc}
    interacting_residues = {pdb_id.lower():[] for pdb_id in pdb_ids}

    comp_interactions = {}
    all_interactions = []

    for pdb_id in pdb_ids:
        with open(f"/home/wkg/complex_mapping/complexes/{pdb_id}.txt", "r") as handle:
            interactions = []
            for line in handle:
                line = line.strip("\n").split()
                interactions.append((line[0], line[1]))
                all_interactions.append((line[0], line[1]))
                all_interactions.append((line[1], line[0]))
            comp_interactions[pdb_id.lower()] = interactions

    all_interactions = set(all_interactions)

    with open("/home/wkg/complex_mapping/3did_flat", "r") as handle:
        relevant_interaction = False
        entry = []
        for line in tqdm(handle):
            if relevant_interaction and not line.startswith("//") and not line.startswith("#=ID"):
                entry.append(line)
            if line.startswith("#=ID"):
                # reset here
                if entry:
                    result = parse_entry(entry, comp_interactions)
                    # add result to master dict
                    for pdb_id in result.keys():
                        interacting_residues[pdb_id].extend(result[pdb_id])
                    entry = []
                relevant_interaction = False
                line = line.strip("\n").split()
                if (line[3][1:], line[4][:-1]) in all_interactions:
                    relevant_interaction = True
        if entry:
            result = parse_entry(entry, comp_interactions)
            for pdb_id in result.keys():
                interacting_residues[pdb_id].extend(result[pdb_id])
    with open("complex_ddi_residues.1.json", "w") as out:
        json.dump(interacting_residues, out)

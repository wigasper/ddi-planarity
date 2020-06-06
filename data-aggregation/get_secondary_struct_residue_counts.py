#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import requests
import json
import logging

from tqdm import tqdm

last_pdb_req = time.perf_counter()

def pdbe_request(pdbe_id):
    global last_pdb_req
    out = ""
    
    req_url = f"https://www.ebi.ac.uk/pdbe/api/pdb/entry/secondary_structure/{pdbe_id}"
    if (time.perf_counter() - last_pdb_req) < .2:
        time.sleep(.2 - (time.perf_counter() - last_pdb_req))
    last_pdb_req = time.perf_counter()
    #result = requests.get(req_url, headers={"Accept": "application/xml"})
    result = requests.get(req_url)
    if result.ok:
        out = result.text
    else:
        logger.info(f"pdbe_request - bad request: {pdbe_id}")

    return out

def secondary_structures(pdbe_id):
    num_helix_residues = 0
    num_strand_residues = 0
    req_result = pdbe_request(pdbe_id)
    if req_result:
        complex_data = json.loads(req_result)
        
        for entity in complex_data[list(complex_data.keys())[0]]["molecules"]:
            for chain in entity["chains"]:
                if "helices" in chain["secondary_structure"].keys():
                    for helix in chain["secondary_structure"]["helices"]:
                        start = helix["start"]["residue_number"]
                        end = helix["end"]["residue_number"]
                        num_helix_residues += (end - start)
                if "strands" in chain["secondary_structure"].keys():
                    for strand in chain["secondary_structure"]["strands"]:
                        start = strand["start"]["residue_number"]
                        end = strand["end"]["residue_number"]
                        num_strand_residues += (end - start)
                    
    return (num_helix_residues, num_strand_residues)
    
if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("check_repeated_entities.log")
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    complex_structs = {}

    pdbe_ids = os.listdir("/home/wkg/complex_mapping/complexes")
    pdbe_ids = [item.split(".")[0] for item in pdbe_ids]
    
    for pdbe_id in tqdm(pdbe_ids):
        helices, strands = secondary_structures(pdbe_id)
        complex_structs[pdbe_id] = {"helix_residues": helices, "strand_residues": strands}

    with open("complex_secondary_struct_residue_counts.json", "w") as out:
        json.dump(complex_structs, out)


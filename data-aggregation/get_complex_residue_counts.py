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
    
    req_url = f"https://www.ebi.ac.uk/pdbe/api/pdb/entry/residue_listing/{pdbe_id}"
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

def residues(pdbe_id):
    total_residues = 0
    
    req_result = pdbe_request(pdbe_id)
    if req_result:
        complex_data = json.loads(req_result)
        
        for entity in complex_data[list(complex_data.keys())[0]]["molecules"]:
            for chain in entity["chains"]:
                if len(chain["residues"]) > 1:
                    total_residues += len(chain["residues"])
                    
    return total_residues
    
if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("check_repeated_entities.log")
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    complex_residues = {}

    pdbe_ids = os.listdir("/home/wkg/complex_mapping/complexes")
    pdbe_ids = [item.split(".")[0] for item in pdbe_ids]
    
    for pdbe_id in tqdm(pdbe_ids):
        num_residues = residues(pdbe_id)
        complex_residues[pdbe_id] = num_residues

    with open("complex_total_residue_counts.json", "w") as out:
        json.dump(complex_residues, out)


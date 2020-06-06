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
    
    req_url = f"https://www.ebi.ac.uk/pdbe/api/pdb/entry/assembly/{pdbe_id}"
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

def check_repeated_entities(pdbe_id):
    num_unique_entities = 0
    num_repeated_entities = 0
    num_total_entities = 0
    req_result = pdbe_request(pdbe_id)
    if req_result:
        complex_data = json.loads(req_result)
        for assembly in complex_data[list(complex_data.keys())[0]]:
            if assembly["assembly_id"] == "1":
                for entity in complex_data[list(complex_data.keys())[0]][0]["entities"]:
                    if entity["molecule_type"].startswith("polypeptide"):
                        num_total_entities += entity["number_of_copies"]
                        num_unique_entities += 1
                        if entity["number_of_copies"] > 1:
                            num_repeated_entities += 1
    
    if num_unique_entities > 0:
        prop_repeated = num_repeated_entities / num_unique_entities
    else:
        prop_repeated = 0
        logger.info(f"{pdbe_id} reported 0 unique entities!")
        
    return num_repeated_entities, prop_repeated, num_total_entities
    
if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("check_repeated_entities.log")
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    complexes_multiple_copies = {}
    complexes_prop_repeated = {}
    complexes_total_pep_counts = {}

    pdbe_ids = os.listdir("/home/wkg/complex_mapping/complexes")
    pdbe_ids = [item.split(".")[0] for item in pdbe_ids]
    
    for pdbe_id in tqdm(pdbe_ids):
        count_repeated, prop_repeated, total_count = check_repeated_entities(pdbe_id)
        complexes_multiple_copies[pdbe_id] = count_repeated
        complexes_prop_repeated[pdbe_id] = prop_repeated
        complexes_total_pep_counts[pdbe_id] = total_count
        
    with open("complexes_multiple_copies.json", "w") as out:
        json.dump(complexes_multiple_copies, out)
    
    with open("complexes_repeated_distinct_prop.json", "w") as out:
        json.dump(complexes_prop_repeated, out)

    with open("complexes_total_peptide_counts.json", "w") as out:
        json.dump(complexes_total_pep_counts, out)
            

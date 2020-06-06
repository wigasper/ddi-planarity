import os
import re
#import sys
#import json
import time
import logging
#import requests
from pathlib import Path
from subprocess import Popen, PIPE

from tqdm import tqdm

last_pdb_req = time.perf_counter()

# TODO this needs to use regexes
def parse_aff_data(res, pdb_id):
    result = " ".join([line for line in res.split("\n") if line.startswith("[+")])
    if re.search("Structure contains gaps", res):
        logger.info(f"Gaps found in {pdb_id}")
    chains = "na"
    residues = "na"
    intermol_contacts = "na"
    ch_ch_contacts = "na"
    ch_po_contacts = "na"
    ch_apo_contacts = "na"
    po_po_contacts = "na"
    apo_po_contacts = "na" 
    apo_apo_contacts = "na" 
    pct_apo_nis_res = "na"
    pct_ch_nis_res = "na"
    pred_bind_aff = "na"
    pred_diss_const = "na"
    
    match = re.search(r"(\d+) chains, (\d+) residues", result)
    if match:
        chains = match.group(1)
        residues = match.group(2)
    # intermolecular contacts
    match = re.search(r"intermolecular contacts: (\d*)", result)
    if match:
        intermol_contacts = match.group(1)
    # charged-charged contacts
    match = re.search(r"charged-charged contacts: (\d*)", result)
    if match:
        ch_ch_contacts = match.group(1)
    # charged-polar contacts
    match = re.search(r"charged-polar contacts: (\d*)", result)
    if match:
        ch_po_contacts = match.group(1)
    # charged-apolar contacts
    match = re.search(r"charged-apolar contacts: (\d*)", result)
    if match:
        ch_apo_contacts = match.group(1)
    # polar-polar contacts
    match = re.search(r"polar-polar contacts: (\d*)", result)
    if match:
        po_po_contacts = match.group(1)
    # apolar-polar contacts
    match = re.search(r"apolar-polar contacts: (\d*)", result)
    if match:
        apo_po_contacts = match.group(1)
    # apolar-apolar contacts
    match = re.search(r"apolar-apolar contacts: (\d*)", result)
    if match:
        apo_apo_contacts = match.group(1)
    # pct apolar NIS residues
    match = re.search(r"Percentage of apolar NIS residues: ((\d*)(\.\d*)*)", result)
    if match:
        pct_apo_nis_res = match.group(1)
    # pct charged nis residues
    match = re.search(r"Percentage of charged NIS residues: ((\d*)(\.\d*)*)", result)
    if match:
        pct_ch_nis_res = match.group(1)
    # predicting binding affinity kcal.mol-1
    match = re.search(r"Predicted binding affinity \(kcal.mol-1\):\s*(-*(\d*)(\.\d*)*)\s+\[", result)
    if match:
        pred_bind_aff = match.group(1)
    # pred dissociation constant at 25C
    match = re.search("Predicted dissociation constant \(M\) at .*:\s*(\S*)", result)
    if match:
        pred_diss_const = match.group(1)
    
    out = [pdb_id, chains, residues, intermol_contacts, ch_ch_contacts, ch_po_contacts, 
           ch_apo_contacts, po_po_contacts, apo_po_contacts, apo_apo_contacts, 
           pct_apo_nis_res, pct_ch_nis_res, pred_bind_aff, pred_diss_const]
    
    return out
    
def get_binding_affinity_data(pdb_id):
    out = []
    
    fp = f"/home/wkg/complex_mapping/binding_affinity/pdb_parsed/{pdb_id}.pdb"
    command = f"python3 /media/storage/binding_affinity/predict_IC.py {fp}"
    with Popen(command, stdout=PIPE, stderr=PIPE, shell=True) as proc:
        results, errs = proc.communicate()
    
    results = results.decode("utf-8")
    
    if "Traceback" in results:
        logger.info("Error at get_binding_affinity_data for pdb_id {pdb_id}")
    else:
        out = parse_aff_data(results, pdb_id)
        
    return out

def parse_pdb(pdb_id, invalid_molecules):
    with open(f"/home/wkg/complex_mapping/binding_affinity/pdb/{pdb_id}.pdb", "r") as handle:
        with open(f"/home/wkg/complex_mapping/binding_affinity/pdb_parsed/{pdb_id}.pdb", "w") as out:
            for line in handle:
                if line.startswith("ATOM"):
                    if line.split()[3] not in invalid_molecules:
                        out.write(line)
                else:
                    out.write(line)

def pdb_request(pdb_id):
    global last_pdb_req
    
    putative_file = Path(f"/home/wkg/complex_mapping/binding_affinity/pdb/{pdb_id}.pdb")
    if not putative_file.exists():
        req_url = f"https://files.rcsb.org/download/{pdb_id}.pdb.gz"
        if (time.perf_counter() - last_pdb_req) < .2:
            time.sleep(.2 - (time.perf_counter() - last_pdb_req))
        last_pdb_req = time.perf_counter()
        
        with Popen(f"wget {req_url}", stdout=PIPE, stderr=PIPE, shell=True) as proc:
            results, errs = proc.communicate()

            if b'ERROR 404' in errs:
                logger.info("Error 404 for pdb_id {pdb_id}")
            
        with Popen(f"gunzip {pdb_id}.pdb.gz", stdout=PIPE, stderr=PIPE, shell=True) as proc:
            results, errs = proc.communicate()

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("get_and_parse_pdb.log")
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    invalid_molecules = {"DA", "DC", "DG", "DT", "DI", "A", "C", "G", "U", "I"}
    
    pdb_ids = os.listdir("/home/wkg/complex_mapping/complexes")
    pdb_ids = [item.split(".")[0] for item in pdb_ids]

    os.chdir("/home/wkg/complex_mapping/binding_affinity/pdb")
    
    binding_aff_results = []
    
    for pdb_id in tqdm(pdb_ids):
        pdb_id = pdb_id.lower()
        pdb_request(pdb_id)
        parse_pdb(pdb_id, invalid_molecules)
        result = get_binding_affinity_data(pdb_id)
        if result:
            binding_aff_results.append(result)

    with open("binding_affinity_data.csv", "w") as out:
        out.write("pdb_id,chains,residues,intermol_contacts,ch_ch_contacts,ch_po_contacts," \
           "ch_apo_contacts,po_po_contacts,apo_po_contacts,apo_apo_contacts," \
           "pct_apo_nis_res,pct_ch_nis_res,pred_bind_aff,pred_diss_const\n")
        for result in binding_aff_results:
            out.write(",".join(result))
            out.write("\n")

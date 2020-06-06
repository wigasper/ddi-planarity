import os
import re
import sys
import json
import time
import logging
import requests
from pathlib import Path

from tqdm import tqdm

last_uniprot_req = time.perf_counter()
last_pdb_req = time.perf_counter()

def parse_uniprot_xml(xml):
    symbol = ""
    match = re.search(r'<gene>\s*<name type="primary".*>(\w*)</name>', xml)
    if match:
        symbol = match.group(1)

    return symbol

def uniprot_uid_req(uniprot_id):
    global last_uniprot_req
    out = ""

    req_url = f"https://uniprot.org/uniprot/{uniprot_id}.xml"
    if (time.perf_counter() - last_uniprot_req) < .2:
        time.sleep(.2 - (time.perf_counter() - last_uniprot_req))   
    last_uniprot_req = time.perf_counter()
    result = requests.get(req_url)
    if result.ok:
        out = result.text
    else:
        logger.info(f"uniprot_uid_req - bad request: {uniprot_id}")
    
    return out

def request_or_load_uniprot(uniprot_id):
    out = ""
    putative_file = Path(f"./xmls/{uniprot_id}.xml")
    if putative_file.exists():
        with open(putative_file, "r") as handle:
            out = handle.read()
    else:
        out = uniprot_uid_req(uniprot_id)
        with open(f"./xmls/{uniprot_id}.xml", "w") as out_handle:
            out_handle.write(out)

    return out

def get_gene_symbol(uniprot_id, unique_name):
    gene_symbol = ""
    if unique_name.split("_")[1] == "YEAST":
        req_result = request_or_load_uniprot(uniprot_id)
        if req_result:
            parse_result = parse_uniprot_xml(req_result)
            if parse_result:
                gene_symbol = parse_result
    else:
        pass
        # TODO: figure this out. 
        # like for P84233, is it acceptable to use H3_YEAST?? or
        # H3.2 for a different yeast?
        #additional verification needed

    return gene_symbol

def parse_struct_ref(struct_ref):
    gene_symbol = ""
    uniprot_id = ""
    if re.search(r"<PDBx:db_name.*>UNP</PDBx:db_name>", struct_ref):
        unique_name = ""
        name_match = re.search(r"<PDBx:db_code>(.*)</PDBx:db_code>", struct_ref)
        if name_match:
            unique_name = name_match.group(1)
        uid_match = re.search("<PDBx:pdbx_db_accession>(.+)</PDBx:pdbx_db_accession>", struct_ref)
        if uid_match:
            uniprot_id = uid_match.group(1)
        
        if uid_match:
            gene_symbol = get_gene_symbol(uniprot_id, unique_name)
            if not gene_symbol:
                logger.info(f"error at parse_struct_ref getting symbol for UID {uniprot_id}")
    
    return (gene_symbol, uniprot_id)

def parse_pdb_result(xml):
    prot_components_genes = []
    prot_components_uids = []

    xml = xml.split("\n")
    index = 0

    while index < len(xml):
        line = xml[index]
        if line.strip().startswith("<PDBx:struct_refCategory>"):
            while not line.strip().startswith("</PDBx:struct_refCategory>"):
                if line.strip().startswith("<PDBx:struct_ref id="):
                    struct_ref_element = []
                    while not line.strip().startswith("</PDBx:struct_ref>"):
                        struct_ref_element.append(line.strip())
                        index += 1
                        line = xml[index]
                    struct_ref_element = "".join(struct_ref_element)
                    parse_result = parse_struct_ref(struct_ref_element)
                    if parse_result[0]:
                        prot_components_genes.append(parse_result[0])
                    if parse_result[1]:
                        prot_components_uids.append(parse_result[1])
                index += 1
                line = xml[index]
        index += 1
        
    return (prot_components_genes, prot_components_uids)

def pdb_request(pdb_id):
    global last_pdb_req
    out = ""
    
    req_url = f"https://files.rcsb.org/download/{pdb_id}-noatom.xml"
    if (time.perf_counter() - last_pdb_req) < .2:
        time.sleep(.2 - (time.perf_counter() - last_pdb_req))
    last_pdb_req = time.perf_counter()
    result = requests.get(req_url, headers={"Accept": "application/xml"})
    if result.ok:
        out = result.text
    else:
        logger.info(f"pdb_request - bad request: {pdb_id}")

    return out

def request_or_load_pdb(pdb_id):
    out = ""
    putative_file = Path(f"./xmls/{pdb_id}.xml")
    if putative_file.exists():
        with open(putative_file, "r") as handle:
            out = handle.read()
    else:
        out = pdb_request(pdb_id)
        with open(f"./xmls/{pdb_id}.xml", "w") as out_handle:
            out_handle.write(out)
    return out

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("get_complex_components.log")
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    complex_prots_genes = {}
    complex_prots_uids = {}

    pdb_ids = os.listdir("/home/wkg/complex_mapping/complexes")
    pdb_ids = [item.split(".")[0] for item in pdb_ids]

    for pdb_id in tqdm(pdb_ids):
        # TODO: timing in here????
        pdb_xml = request_or_load_pdb(pdb_id)
        if pdb_xml:
            parse_result = parse_pdb_result(pdb_xml)
            if parse_result[0]:
                complex_prots_genes[pdb_id] = parse_result[0]
            if parse_result[1]:
                complex_prots_uids[pdb_id] = parse_result[1]
        else:
            logger.info(f"request_or_load_pdb failed: {pdb_id}")
        #start_time = time.perf_counter()
        #req_url = f"https://files.rcsb.org/download/{pdb_id}-noatom.xml"
        #result = requests.get(req_url, headers={"Accept": "application/xml"})
        #if result.ok:
        #    complex_prots[pdb_id] = parse_pdb_result(result.text)
        #else:
        #    logger.info(f"error with id: {pdb_id}")

        #if time.perf_counter() - start_time < .2:
        #    time.sleep(.1 - (time.perf_counter() - start_time))

    with open("pdb_complex_map_genes.json", "w") as out:
        json.dump(complex_prots_genes, out)

    with open("pdb_complex_map_uids.json", "w") as out:
        json.dump(complex_prots_uids, out)

    with open("pdb_complex_map_genes", "w") as out:
        for key in complex_prots_genes:
            out.write(key)
            out.write(":")
            out.write(",".join(complex_prots_genes[key]))
            out.write("\n")

    with open("pdb_complex_map_uids", "w") as out:
        for key in complex_prots_uids:
            out.write(key)
            out.write(":")
            out.write(",".join(complex_prots_uids[key]))
            out.write("\n")

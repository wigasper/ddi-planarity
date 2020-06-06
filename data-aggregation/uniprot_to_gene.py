import re
import json
import requests
import logging
import time

from tqdm import tqdm

def parse_result(xml):
    symbol = "error"

    match = re.search(r'<gene>\s*<name type="primary".*>(\w*)</name>', xml)
    if match:
        symbol = match.group(1)

    return symbol

def get_gene_symbol(uniprot_id, key):
    req_url = f"https://www.uniprot.org/uniprot/{uniprot_id}.xml"
    result = requests.get(req_url)
    gene_symbol = ""
    if result.ok:
        gene_symbol = parse_result(result.text)
    else:
        logger.info(f"error with id: {uniprot_id}")
    
    if gene_symbol == "error":
        logger.info(f"bad parse, key:{key} uniprot:{uniprot_id}")
        gene_symbol = ""

    return gene_symbol

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("uniprot_to_gene.log")
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    with open("pdb_complex_map.json", "r") as handle:
        complex_prots = json.load(handle)

    complex_prots_out = {}

    for key in tqdm(complex_prots.keys()):
        gene_symbols = []
        for uniprot_id in complex_prots[key]:
            if uniprot_id != key:
                start_time = time.perf_counter()
                gene_symbols.append(get_gene_symbol(uniprot_id, key))
                if time.perf_counter() - start_time < .1:
                    time.sleep(.1 - (time.perf_counter() - start_time))
        
        gene_symbols = [sym for sym in gene_symbols if sym]
        complex_prots_out[key] = gene_symbols

    with open("pdb_complex_map_genes.json", "w") as out:
        json.dump(complex_prots_out, out)

    with open("pdb_complex_map_genes", "w") as out:
        for key in complex_prots_out:
            out.write(key)
            out.write(":")
            out.write(",".join(complex_prots_out[key]))
            out.write("\n")


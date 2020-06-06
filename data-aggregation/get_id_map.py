import os
import re
import sys
import time
import logging
import requests

from tqdm import tqdm

if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("id_mapping.log")
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    id_map = {}
    
    gene_regex = re.compile(r'<gene><name type="primary">(\w*)</name>.*</gene>')
    pdb_ids = os.listdir("/home/wkg/complex_essentiality/complexes")
    pdb_ids = [item.split(".")[0] for item in pdb_ids]

    for pdb_id in tqdm(pdb_ids):
        start_time = time.perf_counter()
        req_url = f"https://www.ebi.ac.uk/proteins/api/proteins/PDB:{pdb_id}?offset=0&size=100"
        result = requests.get(req_url, headers={"Accept": "application/xml"})
        if result.ok:
            match = gene_regex.search(result.text)
            if match:
                id_map[pdb_id] = match.group(1)
            else:
                logger.info(f"no match for: {pdb_id}")
        else:
            logger.info(f"error with id: {pdb_id}")

        if time.perf_counter() - start_time < .2:
            time.sleep(.1 - (time.perf_counter() - start_time))

    with open("pdb_id_map", "w") as out:
        for key in id_map:
            out.write(",".join([key, id_map[key]]))
            out.write("\n")

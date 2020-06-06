#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import time
import requests
import json
import traceback
import logging

from tqdm import tqdm

last_mobi_req = time.perf_counter()

def mobi_request(uniprot_id):
    out = ""
    try:
        global last_mobi_req
        
        req_url = f"https://mobidb.bio.unipd.it/ws/{uniprot_id}/consensus"
        if (time.perf_counter() - last_mobi_req) < .2:
            time.sleep(.2 - (time.perf_counter() - last_mobi_req))
        last_mobi_req = time.perf_counter()
        #result = requests.get(req_url, headers={"Accept": "application/xml"})
        result = requests.get(req_url)
        if result.ok:
            out = result.text
        else:
            logger.info(f"mobi_request - bad request: {uniprot_id}")
    
        out = json.loads(out)
    except Exception as e:
        trace = traceback.format_exc()
        logger.error(repr(e))
        logger.critical(trace)
        logger.critical(f"uid: {uniprot_id}")
        
    return out

def get_dc(uniprot_id):    
    dc = ""
    req_result = mobi_request(uniprot_id)

    if req_result:
        if "full" in req_result['mobidb_consensus']['disorder'].keys():
           dc = str(req_result['mobidb_consensus']['disorder']['full'][0]['dc'])[0:5]
        else:
            logger.info(f"Unknown dc for {uniprot_id}")
                    
    return dc
    
if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("get_complex_disorder.log")
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    with open("pdb_complex_map_uids.json", "r") as handle:
        complex_pdb_ids = json.load(handle)
    
    disorder_content = {}
    # memoization to avoid redundant calls
    dc_map = {}
    
    for comp in tqdm(complex_pdb_ids.keys()):
        dcs = []
        for uid in complex_pdb_ids[comp]:
            if uid in dc_map.keys():
                dc = dc_map[uid]
            else:
                dc = get_dc(uid)
                dc_map[uid] = dc
            if dc:
                dcs.append(dc)
        disorder_content[comp] = dcs
        
    with open("complex_disorder_by_uids.json", "w") as out:
        json.dump(disorder_content, out)


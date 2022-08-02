import os 
import sys 
import re 

from tqdm import tqdm

import json 
import ndjson

def make_proof_dict(path): 
    with open(path) as f: 
        proofs = f.read()

    pf_list = proofs.split("Proof of ")

    pf_dict = {re.search("\".*?\"", x).group()[1:-1]: 
            x[x.index("\n"):].rstrip("\n") for x in pf_list[1:-1]}

    return pf_dict

def replace_proof_of_key(key, new_proof, set_mm): 
    match_obj = re.search(key + " ", set_mm)
    sep = match_obj.span()[1]+1 

    rest = set_mm[sep:]
    rest = re.sub(r"\$=.*?\$\.", "$=\n\t\t" + new_proof.replace("\n", "\n\t\t") + "$.\n", 
            rest, count=1)

    set_mm = set_mm[:sep] + rest 

    return set_mm


def main():
    proof_dict = make_proof_dict("proofs.txt")

    with open("metamath-0.198/set.mm") as f: 
        set_mm = f.read()

    set_mm = set_mm[:1000]

    for key in tqdm(proof_dict): 
        set_mm = replace_proof_of_key(key, proof_dict[key], set_mm)


if __name__=="__main__": 
    main()

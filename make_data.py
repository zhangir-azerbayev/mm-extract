import os 
import sys 
import re 

from tqdm import tqdm

import json 
import ndjson

def make_proof_dict(path): 
    with open(path) as f: 
        proofs = f.read()

    proofs = proofs.replace("MM> EXIT", "")

    pf_list = proofs.split("Proof of ")

    pf_dict = {re.search("\".*?\"", x).group()[1:-1]: 
            x[x.index("\n"):].rstrip("\n") for x in pf_list[1:]}

    return pf_dict

def replace_proof_of_key(key, new_proof, set_mm): 
    match_obj = re.search(key + r" \$p", set_mm)

    if match_obj: 
        sep = match_obj.span()[1]+1 

        rest = set_mm[sep:]
        pattern = re.compile(r"\$=.*?\$\.", re.DOTALL)
        #print("GROUP: ", re.search(pattern, rest).group())
        rest = re.sub(pattern, "$=" + " "*6 + new_proof.replace("\n", "\n" + " "*6) + " $.", 
                rest, count=1)
        #print("REST:\n", rest[:1000])

        set_mm = set_mm[:sep] + rest 

    return set_mm


def main():
    proof_dict = make_proof_dict("proofs.txt")

    with open("metamath-0.198/set.mm") as f: 
        set_mm = f.read()

    
    # I know this for loop is horrible but I only need to run it once 
    for key in tqdm(proof_dict): 
        set_mm = replace_proof_of_key(key, proof_dict[key], set_mm)

    with open("human-readable.mm", "w") as f: 
        f.write(set_mm)

if __name__=="__main__": 
    main()

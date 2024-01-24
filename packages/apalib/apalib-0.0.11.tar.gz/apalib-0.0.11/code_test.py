import apalib


num_to_generate = 1000 #@param {type: "integer"}

import urllib.request
import os
import random

# if "pdbcodes.txt" not in os.listdir():
#   urllib.request.urlretrieve(r"https://raw.githubusercontent.com/cathepsin/PublicData/main/All_PDB_Codes_Jan_12_2024.txt", "pdbcodes.txt")
# with open("pdbcodes.txt", "r") as fp:
#   codes = fp.readlines()
# code_set = random.sample(codes, num_to_generate)
# for code in code_set:
#   print(code.strip())
#   pdb = apalib.PDB()
#   pdb.Fetch(code)


pdb = apalib.PDB()
pdb.Fetch('4YQR')



print("Stop")

#7E93 is missing an alpha carbon at chain E, ASN 169
# %%
import json
from time import time
import re

# %%
input_path = "./json/BERGEY’S_MANUAL_sample.json"
keyward_list =  ["L-Fructose", "D-tagatose", "Pyruvate", "Catechol", "Succinate"]
with open(input_path, "r") as f:
    str_dict = json.load(f)

# %%
start = time()
for i, page in str_dict.items():
    found_words = []
    for keyward in keyward_list:
        # N = len(re.findall(keyward.lower(), outfp.getvalue().lower()))
        N = page.lower().count(keyward.lower())
        # N = 0
        # for x in [x.lower() for x in page.split("\n") if x != " " and len(keyward) <= len(x)]:
        #     N += x.count(keyward.lower())
        if N > 0:
            found_words.append(f"「{keyward}」: {N} found")
    if len(found_words) > 0:
        print(i)
        [print(x) for x in found_words]
        print("#"*40)
end = time()

print("SIZE :", len(str_dict))
print("TIME :", end - start)

# %%

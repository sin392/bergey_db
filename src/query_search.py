# %%
import json
from time import time
import re
from io import StringIO

# %%
input_path = "./json/BERGEY’S_MANUAL_sample.json"
keyward_list =  ["L-Fructose", "D-tagatose", "Pyruvate", "Catechol", "Succinate"]
with open(input_path, "r") as f:
    str_dict = json.load(f)

# %%
start = time()
log = StringIO()
print(f"query : {keyward_list}\n", file=log)

for i, page in str_dict.items():
    found_words = []
    for keyward in keyward_list:
        # N = len(re.findall(keyward.lower(), outfp.getvalue().lower()))
        # N = page.lower().count(keyward.lower())
        query = keyward.lower()
        match_idx_list = [m.start() for m in re.finditer(query, page.lower())]
        N = len(match_idx_list)

        if N > 0:
            found_words.append(f"「{keyward}」: {N} found")
            for j in range(N):
                idx = match_idx_list[j]
                string = page[idx-30:idx+30].replace("\n", " ").strip()
                found_words.append(f"{j} : {string}")
    if len(found_words) > 0:
        print(str(i), file=log)
        [print(x, file=log) for x in found_words]
        print("#"*80, file=log)
end = time()

print("SIZE :", len(str_dict), file=log)
print("TIME :", end - start, file=log)

print(log.getvalue())

with open("log.txt", "w") as f:
    f.write(log.getvalue())

log.close()
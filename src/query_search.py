# %%
import json
from time import time
import re
from io import StringIO

# %%
input_path = "./json/BERGEY’S_MANUAL-Betaproteobacteria.json"
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
        query = keyward
        # 検索キーワードとマッチした個所のインデックスをとる
        match_idx_list = [m.start() for m in re.finditer(query, page)]
        N = len(match_idx_list)

        if N > 0:
            found_words.append(f"「{keyward}」: {N} found")
            for j in range(N):
                idx = match_idx_list[j]

                try:
                    h_idx = idx - (1 + re.search(r"[A-Z] \.", page[:idx:-1]).start())
                except:
                    # h_idx = idx - (1 + page[:idx].rfind("\n"))
                    h_idx = 0
                try:
                    t_idx = idx + re.search(r"\. [A-Z]", page[idx:]).end()
                except:
                    # t_idx = idx + page[idx:].find("\n")
                    t_idx = -1
                string = page[h_idx:t_idx].replace("\n", " ").strip()

                # string = page[idx-30:idx+30].replace("\n", " ").strip()
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

# %%

# %%
import json
from time import time
import re
import sys
from io import StringIO
sys.path.append("src")
from utils import make_html
import numpy as np

# %%
input_path = "./json/BERGEY’S_MANUAL-Betaproteobacteria.json"
# keyward_list =  ["L-Fructose", "D-tagatose", "Pyruvate", "Catechol", "Succinate"]
with open(input_path, "r") as f:
    str_dict = json.load(f)
# %%
def invalid_re(word):
    return word.replace("[",r"\[").replace("]",r"\]").replace("(",r"\(").replace(")",r"\)").replace("-", r"\-")

with open("search-dictionary_single.txt", "r") as f:
    keyward_list = list(map(invalid_re, [x.replace("\n","") for x in f.readlines() if len(x.replace("\n","")) > 2]))
    keyward_list = np.unique(np.array(keyward_list))
print(len(keyward_list))

# %%
with open("verb-list.txt", "r") as f:
    verb_list = f.read().split("\n")

with open("log.html", "w") as f:
    f.write("")
# %%
def split_text(text, end_idxs):
    text_list = []
    head_idx = 0
    for end_idx in end_idxs:
        text_list.append(text[head_idx:end_idx])
        head_idx = end_idx + 1
    return text_list

all_doc = ""
split_locs = []
pages = []
for i, page in str_dict.items():
    if len(split_locs) > 0:
        end_idx = split_locs[-1] + (len(page) - 1)
    else:
        end_idx = (len(page) - 1)
    split_locs.append(end_idx)
    pages.append(i)
    all_doc += page
for i, text in enumerate(split_text(all_doc, split_locs)[:3]):
    print("-"*60)
    print(text)

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
                    # 何も見つからないとNoneになりstart()でエラー
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

                used_verbs = [x for x in verb_list if x in string]
                if len(string) > 0:
                    make_html(string, keyward, idx, used_verbs, None)

                found_words.append(f"{j} : {string}")
                found_words.append(f"used_verbs : {used_verbs}")
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

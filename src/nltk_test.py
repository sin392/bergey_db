# %%
import nltk
import numpy as np
import json
import os
import re
import sys
sys.path.append("src")
from utils import make_html
from time import time
# %%
with open("json/BERGEY’S_MANUAL-Betaproteobacteria.json", "r") as f:
    str_dict = json.load(f)
page = " ".join([x for x in str_dict.values()])
print(page[:100])

# %%
morph = nltk.word_tokenize(page)
print(morph)
# %%
len(morph)
# %%
pos = nltk.pos_tag(morph)
print(pos)

# %%
T = nltk.text.Text(morph)
T.concordance("on the basis")
T.similar("on the basis")
# %%
T.common_contexts(("this volume", "volume"))

# %%
# 既知のバグが存在するらしい
# T.collocations()
print('; '.join(T.collocation_list(num=-1)))
print(len(T.collocation_list(num=-1)))
# %%
with open("collocations.txt", "w") as f:
    [print(x, file=f) for x in T.collocation_list(num=-1)]

# %%
page = page.replace("( ","(").replace(" )", ")")
with open("keyward_list.txt", "r") as f:
    keywards = f.read()
    print(keywards)
keyward_list = [x.strip().split() for x in keywards.split(", ") if len(x.strip()) > 2]
# %%
with open("search-dictionary_single.txt", "r") as f:
    keyward_list = [x.replace("\n","").strip().split() for x in f.readlines() if len(x.replace("\n","")) > 2]
# %%
# 単語中にカンマを含むものもあるので注意
keyward_list = np.unique(np.array(keyward_list))
keyward_list = list(map(tuple, keyward_list))
print(keyward_list[:100])
# %%
from nltk.tokenize import MWETokenizer
tokenizer = MWETokenizer(keyward_list)

# %%
morph = nltk.word_tokenize(page.lower())
from nltk.corpus import stopwords
stopset = set(stopwords.words('english'))
morph = [x for x in morph if x not in stopset]

morph = tokenizer.tokenize(morph)
T = nltk.text.Text(morph)
# %%
with open("tokens.txt", "w") as f:
    [print(x, file=f) for x in T.tokens]
# %%
print(len(page), len(keyward_list))
# %%
found_keywords = []
with open("found_words.txt", "w") as f:
    start = time()
    for keyword in ["_".join(x) for x in keyward_list]:
        N = T.count(keyword.lower())
        if N > 0:
            print(keyword, N)
            print(keyword, N, file=f)
            found_keywords.append((keyward, N))
    end = time()
print("TIME :", end - start)
# %%
print(found_keywords)
# %%
print(len(found_keywords))
print(sum([x[1] for x in found_keywords]))
# %%

import nltk
import re
import pandas as pd
import json
import numpy as np
from tqdm import tqdm

# def invalid_re(word):
#     return word.replace("[",r"\[").replace("]",r"\]").replace("(",r"\(").replace(")",r"\)").replace("-", r"\-")

with open("../json/splited_sentence.json") as f:
    sentences_dict = json.load(f)
with open("../txt/search-dictionary_single.txt", "r") as f:
    keywords = [x.strip() for x in f.readlines() if len(x.strip()) > 2]
with open("../csv/verb-list.csv", "r") as f:
    verbs_labels = [x.strip().split(",") for x in f.readlines()]

# 分類情報
with open("../csv/microbes.csv", "r") as f:
    # print(np.array([x.strip().split(",") for x in f.readlines()]).shape)
    c_o, c_f, c_g, c_m = np.array([x.strip().split(",") for x in f.readlines()]).transpose(1,0)
    print(c_o, c_f, c_g, c_m)
    columns = pd.MultiIndex.from_arrays([c_o, c_f, c_g, c_m])

# df = pd.DataFrame(index=keywords, columns=sentences_dict.keys())
df = pd.DataFrame(index=keywords, columns=columns)

for microbe, sentence in tqdm(sentences_dict.items()):
    for raw_keyword in keywords:
        keyword = raw_keyword.replace("[",r"\[").replace("]",r"\]").replace("(",r"\(").replace(")",r"\)").replace("-", r"\-")
        # keyword = raw_keyword
        # 検索キーワードとマッチした個所のインデックスをとる
        # 単語の後にスペース入れてもいいんじゃないか
        match_idx_list = [m for m in re.finditer(keyword, sentence)]
        labels = []
        if len(match_idx_list) > 0:
            # print(keyword, len(match_idx_list))
            verb_in = False
            for m in match_idx_list:
                start = m.start()
                end = m.end()
                # [:start:-1]がうまくいかなくなった？
                try:
                    h_idx = start - (re.search(r"[A-Z] \.", sentence[:start][::-1]).start() + 1)
                except:
                    h_idx = 0
                try:
                    t_idx = end + (re.search(r"\. [A-Z]", sentence[end:]).end() - 1)
                except:
                    t_idx = -1
                string = sentence[h_idx:t_idx]
                # print(string)
                for verb, label in verbs_labels:
                    if verb in string:
                        labels.append(label)
                        verb_in = True
                if not verb_in:
                    splited_string = string.lower().split()
                    if "no" in splited_string or "not" in splited_string or "unable" in splited_string \
                        or "none" in splited_string or "fail" in splited_string or "fail" in splited_string:
                        labels.append(0)
                    else:
                        labels.append(0)

        label = np.argmax(np.bincount(labels)) if len(labels) > 0 else -1
        if label != -1:
            symbol = "-" if label == 0 else "+"
            df.at[raw_keyword, microbe] = symbol
            # print(df.at[raw_keyword, microbe], label, labels)
            # print(microbe, raw_keyword, label)
        # break

df.to_csv("../csv/output.csv")

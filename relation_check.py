import nltk
import re
import pandas as pd
import json
import numpy as np
from tqdm import tqdm

# def invalid_re(word):
#     return word.replace("[",r"\[").replace("]",r"\]").replace("(",r"\(").replace(")",r"\)").replace("-", r"\-")

with open("splited_sentence.json") as f:
    sentences_dict = json.load(f)
with open("search-dictionary_single.txt", "r") as f:
    # keywords = list(map(invalid_re, [x.strip() for x in f.readlines() if len(x.strip()) > 2]))
    keywords = [x.strip() for x in f.readlines() if len(x.strip()) > 2]
    keywords = set(keywords)
with open("verb-list.csv", "r") as f:
    verbs_labels = [x.strip().split(",") for x in f.readlines()]

df = pd.DataFrame(index=keywords, columns=sentences_dict.keys())

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

        label = np.argmax(np.bincount(labels)) if len(labels) > 0 else -1
        if label != -1:
            symbol = "-" if label == 0 else "+"
            df.at[raw_keyword, microbe] = symbol
            print(df.at[raw_keyword, microbe], label, labels)
            print(microbe, raw_keyword, label)
        # break

df.to_csv("output.csv")

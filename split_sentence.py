import re
import json

with open("pages.txt", "r") as f:
    doc = f.read()
with open("microbes_mo.txt", "r") as f:
    microbes = [x.strip() for x in f.readlines()]

sentences = doc.replace("-\n", "").split("\n")
sentences = " ".join(sentences)

sentences_dict = {}
# 次のキーワードを検索してから前のキーワードを辞書に追加
for i, microbe in enumerate(microbes):
    keyword = r"\<" + microbe.strip() + r"\>"
    m_keyword = re.search(keyword, sentences)
    if m_keyword != None:
        m_end = re.search(r"\<end\>", sentences[m_keyword.end():])

        start_idx = m_keyword.end()
        end_idx = m_end.start() + m_keyword.end()
        sentence = sentences[start_idx:end_idx]
        sentences_dict[microbe] = sentence
    # break

# for k, t in sentences_dict.items():
#     print(k)
#     print(t)

with open("splited_sentence.json", "w") as f:
    json.dump(sentences_dict, f)
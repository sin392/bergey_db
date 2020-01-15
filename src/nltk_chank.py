import nltk
import json

input_path = "./json/BERGEY’S_MANUAL-Betaproteobacteria.json"
with open(input_path, "r") as f:
    str_dict = json.load(f)

count = 0
for i, page in str_dict.items():
    # print(page)

    count += 1
    if count > 0:
        break


# nltk process
text = nltk.word_tokenize(page)
tag = nltk.pos_tag(text)
print(tag)

tag_freq = nltk.FreqDist(tag for (word, tag) in tag)
print(tag_freq.items())
# tag_freq.plot(cumulative=True)

print([word + "/" + tag for (word, tag) in nltk.FreqDist(tag) if tag.startswith("V")])
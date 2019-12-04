# %%
import numpy as np
# %%
with open("kegg-reactant.txt", "rt") as f:
    kegg_reactant = f.read()

print(kegg_reactant)
# %%
# 空白の削除
keyward_list = kegg_reactant.split("\n")
keyward_list = [x.strip("\s*| ||\"|\'").lower() for x in keyward_list if x != " " and x != ""]
keyward_list.remove('')
print(keyward_list)
# %%
keyward_list = np.array(keyward_list)
# %%
print(keyward_list[:10])
# 0, 1 に空文字？が残る原因がわからない
print(np.unique(keyward_list)[0:2])

# %%
with open("keyward_list.txt", "w") as f:
    f.write(", ".join(keyward_list))
# %%
unique_keyward_list = np.unique(keyward_list)
np.save("unique_keyward_list.npy", unique_keyward_list[2:])
# %%

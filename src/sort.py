import pandas as pd
import numpy as np

df = pd.read_csv("../csv/output.csv", converters={'col_name_a':str, 'col_name_b':str})
# df = df.replace({"+":1, "-":0})
print(len(df.index))
is_nan_list = np.array([True if df.iloc[i,1:].isnull().all() else False for i in range(len(df.index))])
print(np.argsort(is_nan_list))
sorted_idxs = np.argsort(is_nan_list)
print(df.iloc[sorted_idxs[1],:].values)
# df["key"] = sorted_idxs
df["key"] = is_nan_list
print(df["key"].values)
print(len(sorted_idxs))
df = df.sort_values("key")
df = df.drop("key", axis=1)
# df = df.replace({1:"+", 0:"-"})
df.to_csv("../csv/output_sorted.csv", index=None)

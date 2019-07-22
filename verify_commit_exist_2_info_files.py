import pandas as pd

# path to files that share the same column
info_file_path_a = r"D:\capstone\data\missing.csv"
info_file_path_b = r"D:\capstone\data\demma_commits.csv"

# read csv files as dataframes
df_info_file_a = pd.read_csv(info_file_path_a)
df_info_file_b = pd.read_csv(info_file_path_b)


col_a = df_info_file_a['commit_hashes']
col_b = df_info_file_b["full_commit_hash"]

# convert to list to apply list comprehension
list_a = col_a.tolist()
list_b = col_b.tolist()

list_result = [element for element in list_a if element in list_b]

# Output results
print(list_result)
print(len(list_result))


# https://github.com/git/git/tree/5ab72271e16ac23c269f5019a74a7b1d65170e47 this deemas commits doesn't exist




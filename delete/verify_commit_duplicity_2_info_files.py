import pandas as pd

# path to files that share the same column
info_file_path_a = r"D:\capstone\data\demma_commits.csv"
info_file_path_b = r"D:\capstone\data\all_commits.csv"

# read csv files as dataframes
df_info_file_a = pd.read_csv(info_file_path_a)
df_info_file_b = pd.read_csv(info_file_path_b)

column_name_to_compare = 'full_commit_hash'

col_a = df_info_file_a[column_name_to_compare]
col_b = df_info_file_b[column_name_to_compare]

# convert to list to apply list comprehension
list_a = col_a.tolist()
list_b = col_b.tolist()

list_result = [element for element in list_a if element not in list_b]

# Output results
print(list_result)
print(len(list_result))





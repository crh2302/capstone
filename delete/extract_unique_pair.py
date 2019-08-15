import pandas as pd

source_path = r"D:\capstone\data\no_zeros_2.csv"
target_path = r"D:\capstone\data\deema_unique_pairs.csv"
headers = ["Commit A", "Commit B"]

df = pd.read_csv(source_path)
df["combination"] = tuple(zip(df["Commit A"], df["Commit B"]))
unique_combinations = df["combination"].unique()
df_unique = pd.DataFrame(data=list(unique_combinations), columns=headers)
df_unique.to_csv(target_path, mode='w', index=False,
                 header=True, line_terminator='\n', sep=',',
                 encoding='utf-8')

print(len(df.index))
print(len(df_unique.index))

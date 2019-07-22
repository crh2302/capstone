import pandas as pd

source_path = r"D:\capstone\data\no_zeros_2.csv"
target_path = r"D:\capstone\data\deema_count_pairs.csv"
df = pd.read_csv(source_path)

df["Commit A Count"] = df["Commit A"].str.len()
df["Commit B Count"] = df["Commit B"].str.len()
df[["Commit A", "Commit B", "Commit A Count", "Commit B Count"]].to_csv(target_path, mode='w', index=False,
                 header=True, line_terminator='\n', sep=',',
                 encoding='utf-8')
print(df)
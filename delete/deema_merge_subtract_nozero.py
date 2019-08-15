import pandas as pd

df_no_zero = pd.read_csv(r"D:\capstone\data\no_zeros_2.csv")
df_subtraction = pd.read_csv(r"D:\capstone\data\deema_subtraction.csv")

df_no_zero.set_index(["Commit A", "Commit B"])
df_subtraction.set_index(["Commit A", "Commit B"])
merge = df_no_zero.merge(df_subtraction, on=["Commit A", "Commit B"], how='inner')
merge.to_csv(r"D:\capstone\data\deema_merge_subtraction_nozero.csv", mode='w', index = False, line_terminator='\n',sep=',', encoding='utf-8')

import pandas as pd

no_zeros_2 = pd.read_csv(r"D:\capstone\data\no_zeros_2.csv")

single_column = no_zeros_2["Commit A"].append(no_zeros_2["Commit B"])
unique_values = pd.DataFrame(single_column.unique(), columns=["commit_hash"])
print(unique_values)

unique_values.to_csv(r"D:\\capstone\\data\\demma.csv", mode='a', index=False, header=True,
                     line_terminator='\n',sep=',', encoding='utf-8')

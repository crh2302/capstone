import pandas as pd

file_sum = pd.read_csv(r"D:\capstone\metrics_deema\file_sum.csv")
file_max = pd.read_csv(r"D:\capstone\metrics_deema\file_max.csv")
file_avg = pd.read_csv(r"D:\capstone\metrics_deema\file_avg.csv")
file_fun = pd.read_csv(r"D:\capstone\metrics_deema\file_fun.csv")
file_info = pd.read_csv("D:\capstone\data\demma_commits.csv")[["commit_hashes","commit"]]

merge0 = pd.merge(file_info, file_sum, on="commit")

merge1 = pd.merge(merge0, file_max, on="commit")
merge2 = pd.merge(merge1, file_avg, on="commit")
merge3 = pd.merge(merge2, file_fun, on="commit")


merge3.to_csv(r"D:\capstone\metrics_deema\merged.csv", mode='a', index = False, line_terminator='\n',sep=',', encoding='utf-8')

import os

import my_functions
import pandas as pd
import pathlib

target_dir = r'D:\capstone\metrics3'
my_functions.make_working_dir(target_dir)
f = open(os.path.join(target_dir, "file.csv"), "w+")

file_full_path = r"D:\capstone\metrics2\0a0dd632aa9c9bcdb1b79a7fc4cf6dc161760020.csv"

(_, _, file_names) = next(os.walk(r'D:\capstone\metrics2'))
file_full_paths = [ 'D:\capstone\metrics2' + "\\" + filename for filename in file_names]


for file_full_path in file_names:
    csv = pd.read_csv(r"D:\capstone\metrics2\\" + file_full_path)
    commit_name = pathlib.Path(file_full_path).stem
    print(commit_name)
    csv["commit"] = commit_name
    csv_files = csv[csv["Kind"] == "Function"]# Apply filter here
    csv_files.to_csv(f, mode='a', header=False, index = False, line_terminator='\n',sep=',', encoding='utf-8')
f.close()


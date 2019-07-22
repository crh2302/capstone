
import subprocess
import pandas as pd

commit_hashes = pd.read_csv(r"D:\capstone\data\commit_hashes.csv")

commits = []
full_commit_hash = []
date_ci = []
date_ct = []


headers = ["commit_hash", "full_commit_hash", "time_stamp", "unix_time_stamp"]
headers_dict = {headers[i]: i for i in range(0, len(headers))}
for index, row in commit_hashes.iterrows():
    commit = row[0]
    output = subprocess.check_output(f"git show -s --format=%h|%H|%cI|%ct {commit}",
                                     cwd=r'D:\capstone\git').decode("utf-8").rstrip("\n\r")

    split_output = output.split("|")
    commits.append(split_output[headers_dict["commit_hash"]])
    full_commit_hash.append(split_output[headers_dict["full_commit_hash"]])
    date_ci.append(split_output[headers_dict["time_stamp"]])
    date_ct.append(split_output[headers_dict["unix_time_stamp"]])
    print(index)

df = pd.DataFrame(list(zip(commits, full_commit_hash, date_ci, date_ct)),
               columns=headers)

df.to_csv("D:\\capstone\\data\\all_commits.csv", mode='a', header=True,
          index=False, line_terminator='\n', sep=',', encoding='utf-8')




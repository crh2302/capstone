import csv
import os
import generate_metrics as gm

root_dir = os.path.dirname(os.path.realpath(__file__))

with open(file="commits.csv", mode='r', newline='') as cvs_file:
    print(csv.list_dialects())
    commit_collection = csv.reader(cvs_file)
    header = next(commit_collection, None)  # skip the headers
    commit_collection = list(commit_collection)
    gm.generate_metric_all_commits(commit_collection,
                                   os.path.join(root_dir, "git"),
                                   os.path.join(root_dir, "metrics"))

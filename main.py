import csv
import os
import generate_metrics as gm
import my_functions


root_dir = os.path.dirname(os.path.realpath(__file__))

with open(file="data/list_of_commits.csv", mode='r', newline='') as cvs_file:
    complete_commit_collection = list(list(zip(*csv.reader(cvs_file)))[0][1:])
    previously_collected = my_functions.get_file_names_in_path(os.path.join(root_dir, "metrics01"))
    commit_collection_to_go = [commit for commit in complete_commit_collection
                               if commit not in previously_collected]

    gm.generate_metric_all_commits(commit_collection_to_go,
                                   os.path.join(root_dir, "git"),
                                   os.path.join(root_dir, "metrics01"))



import my_functions as mf


print("================================================")
print("From the no_zero file, what commits are empty?:")
info_file_path_a = r"D:\capstone\data\missing.csv"
info_file_path_b = r"D:\capstone\data\demma_commits.csv"

mf.verify_duplicate_csv_diff_files(info_file_path_a, 'commit_hashes',
                                   info_file_path_b, "commit")
print("================================================")


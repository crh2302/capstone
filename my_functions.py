import pathlib
import os
import shutil
import pandas as pd
import subprocess


def get_file_names_in_path(mypath):
    make_working_dir(mypath)
    (_, _, file_names) = next(os.walk(mypath))
    return [pathlib.Path(filename).stem for filename in file_names]


def get_files_in_path(mypath):
    (_, _, file_names) = next(os.walk(mypath))
    return [pathlib.Path(filename).stem for filename in file_names]


def make_working_dir(working_dir):
    """
    Verifies if the specified working directory exist. If it does not exist it will created.
    It does not change  permission.

    :param working_dir: The specified directory where the work of this module will be done
    :type working_dir: basestring
    :return: None
    :rtype: None
    """
    if not os.path.isdir(working_dir):
        os.makedirs(working_dir)


def verify_duplicate_csv_diff_files(info_file_path_a, header_a,
                                    info_file_path_b, header_b):
    # read csv files as data_frames
    df_info_file_a = pd.read_csv(info_file_path_a)
    df_info_file_b = pd.read_csv(info_file_path_b)

    col_a = df_info_file_a[header_a]
    col_b = df_info_file_b[header_b]

    # convert to list to apply list comprehension
    list_a = col_a.tolist()
    list_b = col_b.tolist()

    list_result = [element for element in list_a if element in list_b]

    print("Duplicate list: ")
    print(list_result)
    print("Amount of duplicates: " + str(len(list_result)))


def export_unique_from_no_zero(source_no_zero, target_path):
    print("Creating unique file at " + target_path)

    # if os.path.exists(target_path):
    #     os.remove(target_path)

    no_zeros_2 = pd.read_csv(source_no_zero)
    single_column = no_zeros_2["Commit A"].append(no_zeros_2["Commit B"])
    unique_values = pd.DataFrame(single_column.unique(), columns=["commit_hashes"])
    unique_values.to_csv(target_path, mode='w', index=False, header=True,
                         line_terminator='\n', sep=',', encoding='utf-8')


def convert_to_full_hash(my_column_names, my_file_name ):
    def read_data(file_name, column_names):
        data = pd.read_csv(file_name)
        df = pd.DataFrame(data)
        df.columns = column_names
        return df

    def select_unique_data(my_data, column_names):
        df_unique = my_data.groupby(column_names).size().reset_index().rename(columns={0: 'count'})
        del df_unique['count']
        return df_unique

    def add_hash(data_frame, commit_hashes_df):
        dict_prev_found = {}
        data_frame["hash"] = ""

        for index, row in data_frame.iterrows():
            row_list = row[0:1]
            counter = 0
            for row_i in row_list:
                if row_i in dict_prev_found:
                    value = dict_prev_found[row_i]
                    data_frame["hash"][index] = value[0][0]
                else:
                    value = commit_hashes_df[commit_hashes_df.commit_hashes.str.startswith(row_i)].values
                    if value.size == 0:
                        print(f"index:{index}")
                        print("value.size == 0:")
                        print(f"row_i{row_i}")
                        print(f"Value:{value}")
                    else:
                        dict_prev_found[row_i] = value
                        data_frame["hash"][index] = 0 if value.size == 0 else value[0][0]
                counter = counter + 1
        return data_frame

    # my_column_names = ["commit_hashes"]
    # my_file_name = r'D:\capstone\data\demma.csv'
    data = read_data(my_file_name, my_column_names)
    data = select_unique_data(data, my_column_names)
    commit_hashes_df = read_data(my_file_name, my_column_names)
    commit_hashes_df = select_unique_data(commit_hashes_df, my_column_names)
    data = add_hash(data, commit_hashes_df)
    data.loc[:, data.columns == 'hash'].to_csv("data.csv", index=None)


def count_commit_pairs_no_zero(source_path, target_path):
    df = pd.read_csv(source_path)

    df["Commit A Count"] = df["Commit A"].str.len()
    df["Commit B Count"] = df["Commit B"].str.len()
    df[["Commit A", "Commit B", "Commit A Count", "Commit B Count"]].to_csv(target_path, mode='w', index=False,
                                                                            header=True, line_terminator='\n', sep=',',
                                                                            encoding='utf-8')


def merge_generated_metrics():
    file_sum = pd.read_csv(r"metrics_deema/file_sum.csv")
    file_max = pd.read_csv(r"metrics_deema/file_max.csv")
    file_avg = pd.read_csv(r"metrics_deema/file_avg.csv")
    # file_fun = pd.read_csv(r"metrics_deema/file_fun.csv")
    file_info = pd.read_csv("data/deema_commits.csv")[["abv_commit", "commit"]]

    merge0 = pd.merge(file_info, file_sum, on="commit")

    merge1 = pd.merge(merge0, file_max, on="commit")
    merge2 = pd.merge(merge1, file_avg, on="commit")
    # merge3 = pd.merge(merge2, file_fun, on="commit")

    merge2.to_csv(r"metrics_deema/merged.csv", mode='a', index=False, line_terminator='\n', sep=',',
                  encoding='utf-8')


def substract_metrics():
    print("substract_metrics")
    unique_pairs_path = r"data/deema_unique_pairs.csv"
    # no_zero_path = r"data/no_zeros_2.csv"
    merged_metrics_path = r"metrics_deema/merged.csv"

    #print("1")
    df_unique_pairs = pd.read_csv(unique_pairs_path)
    # df_no_zero = pd.read_csv(no_zero_path)
    df_metrics = pd.read_csv(merged_metrics_path)
    #print("2")

    # headers = ["Commit A", "Commit B"] + df_metrics.columns.tolist()[2:]
    metrics_headers = df_metrics.columns.tolist()[2:]
    metric_count = len(metrics_headers)
    #print("3")

    data = []
    commit_length = len(df_metrics["abv_commit"].loc[0])
    #print("4")
    for commits_index, com_a, com_b in df_unique_pairs.itertuples():
        commit_a = com_a[:commit_length]
        commit_b = com_b[:commit_length]
        try:
            metrics_a = df_metrics[df_metrics["abv_commit"] == commit_a].iloc[0][2:]
        except IndexError:
            print((commits_index, commit_a, commit_b))
            metrics_a = pd.Series(data=["0"] * metric_count,
                                  index=metrics_headers)
        try:
            metrics_b = df_metrics[df_metrics["abv_commit"] == commit_b].iloc[0][2:]
        except IndexError:
            print((commits_index, commit_a, commit_b))
            metrics_b = pd.Series(data=[0] * metric_count,
                                  index=metrics_headers)

        # metrics_a = metrics_a.apply(lambda z: float(z))
        # metrics_b = metrics_b.apply(lambda z: float(z))
        try:
            subtraction = metrics_a - metrics_b
            data.append((commits_index, subtraction.transpose()))
        except Exception as e:
            print(f"error as commits_index: {commits_index}.Error: {e}" )
            # print(metrics_a)
            # print("=========================================================")
            # print(metrics_b)


    df_subtraction = pd.DataFrame(dict(data))
    df_subtraction_t = df_subtraction.transpose()

    df_result = df_unique_pairs.join(df_subtraction_t, how='outer')

    df_result.to_csv(r"data/deema_subtraction", mode='w',
                     header=True, index=False, line_terminator='\n', sep=',', encoding='utf-8')
    #print("5")


def merge_substracted_with_no_zero():
    df_no_zero = pd.read_csv(r"data/no_zeros_2.csv")
    df_subtraction = pd.read_csv(r"data/deema_subtraction.csv")

    df_no_zero.set_index(["Commit A", "Commit B"])
    df_subtraction.set_index(["Commit A", "Commit B"])
    merge = df_no_zero.merge(df_subtraction, on=["Commit A", "Commit B"], how='inner')
    merge.to_csv(r"data/finaloutput.csv", mode='w', index=False, line_terminator='\n',
                 sep=',', encoding='utf-8')


def extract_unique_pairs():
    source_path = r"data/no_zeros_2.csv"
    target_path = r"data/deema_unique_pairs.csv"
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


def create_commit_info(source, target):
    print("Creating commit info file at " + target)
    commit_hashes = pd.read_csv(source)["commit_hashes"].tolist()
    commits = []
    full_commit_hash = []
    date_ci = []
    date_ct = []

    headers = ["abv_commit", "commit", "time_stamp", "unix_time_stamp"]
    headers_dict = {headers[i]: i for i in range(0, len(headers))}
    for index, commit in enumerate(commit_hashes):
        output = subprocess.check_output(f"git show -s --format=%h|%H|%cI|%ct {commit}",
                                         cwd=r'git').decode("utf-8").rstrip("\n\r")
        split_output = output.split("|")
        commits.append(split_output[headers_dict["abv_commit"]])
        full_commit_hash.append(split_output[headers_dict["commit"]])
        date_ci.append(split_output[headers_dict["time_stamp"]])
        date_ct.append(split_output[headers_dict["unix_time_stamp"]])

    df = pd.DataFrame(list(zip(commits, full_commit_hash, date_ci, date_ct)),
                      columns=headers)

    df.to_csv(target, mode='w', header=True,
              index=False, line_terminator='\n', sep=',', encoding='utf-8')

import pandas


"""
The purpose of this file was to convert small commit hashes into full commit hashes.
This module does not take part in the collection of metrics
"""


def read_data(file_name, column_names):
    data = pandas.read_csv(file_name)
    df = pandas.DataFrame(data)
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


def convert_to_full_hash():
    my_column_names = ["commit_hashes"]
    my_file_name = r'D:\capstone\data\demma.csv'
    data = read_data(my_file_name, my_column_names)
    data = select_unique_data(data, my_column_names)
    my_column_names = ["commit_hashes"]
    my_file_name = 'commit_full_hash_demma.csv'
    commit_hashes_df = read_data(my_file_name, my_column_names)
    commit_hashes_df = select_unique_data(commit_hashes_df, my_column_names)
    data = add_hash(data, commit_hashes_df)
    data.loc[:, data.columns == 'hash'].to_csv("data.csv", index=None)



import pandas as pd

unique_pairs_path = r"D:\capstone\data\deema_unique_pairs.csv"
no_zero_path = r"D:\capstone\data\no_zeros_2.csv"
merged_metrics_path = r"D:\capstone\metrics_deema\merged.csv"

df_unique_pairs = pd.read_csv(unique_pairs_path)
df_no_zero = pd.read_csv(no_zero_path)
df_metrics = pd.read_csv(merged_metrics_path)

headers = ["Commit A", "Commit B"] + df_metrics.columns.tolist()[2:]
metrics_headers = df_metrics.columns.tolist()[2:]
metric_count = len(metrics_headers)

data = []
commit_length = len(df_metrics["commit_hashes"].loc[0])

for commits_index, com_a, com_b in df_unique_pairs.itertuples():
    commit_a = com_a[:commit_length]
    commit_b = com_b[:commit_length]
    try:
        metrics_a = df_metrics[df_metrics["commit_hashes"] == commit_a].iloc[0][2:]
    except IndexError:
        print((commits_index, commit_a, commit_b))
        metrics_a = pd.Series(data=["0"] * metric_count,
                              index=metrics_headers)
    try:
        metrics_b = df_metrics[df_metrics["commit_hashes"] == commit_b].iloc[0][2:]
    except IndexError:
        print((commits_index, commit_a, commit_b))
        metrics_b = pd.Series(data=[0] * metric_count,
                              index=metrics_headers)
    subtraction = metrics_a - metrics_b
    data.append((commits_index, subtraction.transpose()))

df_subtraction = pd.DataFrame(dict(data))
df_subtraction_t = df_subtraction.transpose()

df_result = df_unique_pairs.join(df_subtraction_t, how='outer')

df_result.to_csv(r"D:\capstone\data\deema_subtraction", mode='w',
                 header=True, index = False, line_terminator='\n',sep=',', encoding='utf-8')


import os

import my_functions
import pandas as pd
import pathlib
import sys
import logging


LOG_FILENAME = 'log.log'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG,
                    format='{asctime} - {name} - {message}', style='{')


log = logging.getLogger(__name__)


headers = [ 'Kind',
            'Name',
            'File',
            'AltAvgLineBlank',
            'AltAvgLineCode',
            'AltAvgLineComment',
            'AltCountLineBlank',
            'AltCountLineCode',
            'AltCountLineComment',
            'AvgCyclomatic',
            'AvgCyclomaticModified',
            'AvgCyclomaticStrict',
            'AvgEssential',
            'AvgLine',
            'AvgLineBlank',
            'AvgLineCode',
            'AvgLineComment',
            'CountClassBase',
            'CountClassCoupled',
            'CountClassDerived',
            'CountDeclClass',
            'CountDeclClassMethod',
            'CountDeclClassVariable',
            'CountDeclFile',
            'CountDeclFileCode',
            'CountDeclFileHeader',
            'CountDeclFunction',
            'CountDeclInstanceMethod',
            'CountDeclInstanceVariable',
            'CountDeclInstanceVariablePrivate',
            'CountDeclInstanceVariableProtected',
            'CountDeclInstanceVariablePublic',
            'CountDeclMethod',
            'CountDeclMethodAll',
            'CountDeclMethodConst',
            'CountDeclMethodFriend',
            'CountDeclMethodPrivate',
            'CountDeclMethodProtected',
            'CountDeclMethodPublic',
            'CountInput',
            'CountLine',
            'CountLineBlank',
            'CountLineCode',
            'CountLineCodeDecl',
            'CountLineCodeExe',
            'CountLineComment',
            'CountLineInactive',
            'CountLinePreprocessor',
            'CountOutput',
            'CountPath',
            'CountPathLog',
            'CountSemicolon',
            'CountStmt',
            'CountStmtDecl',
            'CountStmtEmpty',
            'CountStmtExe',
            'Cyclomatic',
            'CyclomaticModified',
            'CyclomaticStrict',
            'Essential',
            'Knots',
            'MaxCyclomatic',
            'MaxCyclomaticModified',
            'MaxCyclomaticStrict',
            'MaxEssential',
            'MaxEssentialKnots',
            'MaxInheritanceTree',
            'MaxNesting',
            'MinEssentialKnots',
            'PercentLackOfCohesion',
            'RatioCommentToCode',
            'SumCyclomatic',
            'SumCyclomaticModified',
            'SumCyclomaticStrict',
            'SumEssential', "commit"]

filter_col_sum = [col for col in headers if col.startswith("CountLine") or col.startswith("CountS") or  col.startswith("Sum") or col.startswith("AltCount")]
filter_col_sum.append("commit")
filter_col_max = [col for col in headers if col.startswith("MaxCyclo")]
filter_col_max.append("MaxNesting")
filter_col_max.append("commit")
filter_col_avg = [col for col in headers if col.startswith("AltAvg") or col.startswith("Avg")]
filter_col_avg.append("commit")

filter_col_cyclo = [col for col in headers if col.startswith("Cyclo")]
filter_col_cyclo.append("commit")

target_dir = r'D:\capstone\metrics5'

# f = open(os.path.join(target_dir, "file_sum.csv"), "w+")
fsum = open(os.path.join(target_dir, "file_sum.csv"), "w+")
fmax = open(os.path.join(target_dir, "file_max.csv"), "w+")
favg = open(os.path.join(target_dir, "file_avg.csv"), "w+")
ffun = open(os.path.join(target_dir, "file_fun.csv"), "w+")

source_dir = r'D:\capstone\metrics01\\'

(_, _, file_names) = next(os.walk(source_dir))
file_full_paths = [source_dir + "\\" + filename for filename in file_names]


for file_full_path in file_names:

    csv = pd.read_csv(source_dir + file_full_path)
    commit_name = pathlib.Path(file_full_path).stem
    print(commit_name)
    csv["commit"] = commit_name
    csv_files = csv[csv["Kind"] == "File"]# Apply filter here
    csv_files_sum = csv_files
    csv_files_max = csv_files.copy()
    csv_files_avg = csv_files.copy()
    csv_files_fun = csv[csv["Kind"] == "Function"]
    try:
        csv_files_sum = csv_files_sum[filter_col_sum].groupby(["commit"]).sum()
        csv_files_max = csv_files_max[filter_col_max].groupby(["commit"]).max()
        csv_files_avg = csv_files_avg[filter_col_avg].groupby(["commit"]).mean()
        csv_files_fun = csv_files_fun[filter_col_cyclo].groupby(["commit"]).mean()

        csv_files_sum.to_csv(fsum, mode='a', index=True, header=False, line_terminator='\n',sep=',', encoding='utf-8')
        csv_files_max.to_csv(fmax, mode='a', index=True, header=False, line_terminator='\n',sep=',', encoding='utf-8')
        csv_files_avg.to_csv(favg, mode='a', index=True, header=False, line_terminator='\n',sep=',', encoding='utf-8')
        csv_files_fun.to_csv(ffun, mode='a', index=True, header=False, line_terminator='\n',sep=',', encoding='utf-8')
    except Exception as e:
        log.debug(commit_name + " " + repr(e))




fsum.close()
fmax.close()
favg.close()
ffun.close()


print(filter_col_sum)
print(filter_col_max)
print(filter_col_avg)
print(filter_col_cyclo)

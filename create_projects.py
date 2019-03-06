import sh
import os
import csv

#https://scitools.com/documents/manuals/html/understand/wwhelp/wwhimpl/js/html/wwhelp.htm


'''
Clone repository
Begin
'''
#
# git_repository_url = "https://github.com/git/git.git"
#
# try:
#     print("Cloning git project from ",git_repository_url)
#     sh.git("clone", git_repository_url, _out=True)
# except sh.ErrorReturnCode_128 as e:
#     print("Destination path 'git' already exists and is not an empty directory")
# except Exception as e:
#     print(e)
#     exit(1)

'''
Clone repository
End
'''

'''
Create settings file 
Begin
'''
#-metricmetricsAdd MaxInheritanceTree PercentLackOfCohesion CountClassCoupled CountClassDerived CountDeclMethodAll SumCyclomatic
settings_file_content = \
"""-metricmetricsAdd all
-MetricFileNameDisplayMode RelativePath
-MetricDeclaredInFileDisplayMode RelativePath
-MetricShowDeclaredInFile on
-MetricShowFunctionParameterTypes on
"""

settings_file_name = 'settings.txt'
f = open(settings_file_name, 'w')
f.write(settings_file_content)
f.close()

'''
Create settings file 
End
'''

'''
Calculate metrics 
Begin
'''

root_dir = "/home/test-generators/PycharmProjects/research/"
repository_dir = os.path.join(root_dir, "git")
#current_commit = "f0ac6e39433c1d7e9339207aa4d01e9bf7a05b8a"

project_languages = "c++"

# Create a folder to hold metrics /Begin
# THIS FUNCTION IS DANGEROUS. IF YOU DO NOT CONFIGURE THIS CORRECTLY YOU COULD DELETE THAT YOU DID NOT INTENT TO.
metrics_folder_name = "metrics"
metrics_folder_dir = os.path.join(root_dir, metrics_folder_name)
if os.path.isdir(metrics_folder_dir):
    for root, dirs, files in os.walk(metrics_folder_dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(metrics_folder_dir)
    os.mkdir(metrics_folder_dir)
else:
    os.mkdir(metrics_folder_dir)
# Create a folder to hold metrics /End


commits_to_analyse_file_name = "commits.csv"
with open(commits_to_analyse_file_name, 'r') as cvs_file:
    array_of_commits = csv.reader(cvs_file)
    header = next(array_of_commits, None)  # skip the headers
    for count, row in enumerate(array_of_commits):
        current_commit = row[0]
        if current_commit == "":
            continue
        else:

            udb_commit_file_name = f"{current_commit}.udb"
            # Gather metrics /Begin
            git_dir = os.path.join(repository_dir, ".git")
            while True:
                try:
                    print("---------------------------------------", "Commit", count, "---------------------------------------")
                    # sh.git(f"--git-dir={git_dir}",
                    #              f"--work-tree={repository_dir}",
                    #              "reset", "--hard", current_commit,  _out=True)

                    sh.git(f"--git-dir={git_dir}", f"--work-tree={repository_dir}",
                           "checkout", current_commit, _out=True)
                    print(f"Creating udb database for commit: {current_commit}")
                    sh.und.create("-db", udb_commit_file_name, "-languages", project_languages)

                    print(f"Adding files to commit: {current_commit}")
                    sh.und.add("-db", udb_commit_file_name, repository_dir)

                    print(f"Running Analysis for commit: {current_commit} ...")
                    sh.und.analyze("-db", udb_commit_file_name)

                    print(f"Adding metrics to commit: {current_commit}")
                    sh.und.settings(f"@{settings_file_name}", udb_commit_file_name)

                    print("Calculating metrics and creating csv")
                    sh.und.metrics(udb_commit_file_name)

                    print(f"Removing {udb_commit_file_name}")
                    os.remove(udb_commit_file_name)

                    print(f"Moving {current_commit}.csv to metric folder")
                    os.rename(os.path.join(root_dir, f"{current_commit}.csv"),os.path.join(metrics_folder_dir, f"{current_commit}.csv"))
                    break
                except sh.SignalException_SIGSEGV:
                    print(f"ERROR: An sh.SignalException_SIGSEGV error occurred on commit {count}")
            #Gather metrics /End


'''
Calculate metrics 
End
'''
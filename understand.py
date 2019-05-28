import os
import subprocess
import logging

log = logging.getLogger(__name__)


def und_make_working_dir(root_path):
    if not os.path.isdir(root_path):
        os.makedirs(root_path)


def und_create_db(udb_commit_file_name, project_languages):
    subprocess.call(f"und create -db {udb_commit_file_name} -languages {project_languages}", shell=True)


def und_add_files_to_db(udb_commit_file_name, repository_dir):
    subprocess.call(f"und add -db {udb_commit_file_name} {repository_dir}")


def und_setup_setting(settings_file_name, udb_commit_file_name):
    subprocess.call(f"und settings @{settings_file_name} {udb_commit_file_name}")


def und_generate_metrics(udb_commit_file_name):
    log.info(f"Running Analysis for commit: {udb_commit_file_name} ...")
    subprocess.call(f"und analyze -db {udb_commit_file_name}")
    log.info("Calculating metrics and creating csv")
    subprocess.call(f"und metrics {udb_commit_file_name}")


def und_move_to_path(source, target, current_commit):
    os.rename(os.path.join(source, f"{current_commit}.csv"),
              os.path.join(target, f"{current_commit}.csv"))


def und_clean_up(udb_commit_file_name):
    os.remove(udb_commit_file_name)


def generate_metrics_by_commit_understand(current_commit, project_languages,
                                          repository_dir,
                                          settings_file_name,
                                          metrics_folder_dir,
                                          root_path=r"./temp/"):
    und_make_working_dir(root_path)
    udb_commit_file_name = f"{root_path + current_commit}.udb"
    log.info(f"Creating udb database for commit: {current_commit}")
    und_create_db(udb_commit_file_name, project_languages)
    log.info(f"Adding files to commit: {current_commit}")
    und_add_files_to_db(udb_commit_file_name, repository_dir)
    log.info(f"Adding metrics to commit: {current_commit}")
    und_setup_setting(settings_file_name, udb_commit_file_name)
    und_generate_metrics(udb_commit_file_name)
    log.info(f"Moving {current_commit}.csv to metric folder")
    und_move_to_path(root_path, metrics_folder_dir, current_commit)
    log.info(f"Removing {udb_commit_file_name}")
    und_clean_up(udb_commit_file_name)

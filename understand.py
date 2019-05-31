import os
import subprocess
import logging

log = logging.getLogger(__name__)


def und_make_working_dir(working_dir):
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


def und_create_db(udb_file, project_languages="c++"):
    """
    Wrapper for und create shell command for creating the an understand database.
    The understand database allow for Files to be added and analyzed.

    :param udb_file: Name of the database
    :type udb_file: basestring
    :param project_languages: Languages that can be analysed.
    :type project_languages: basestring
    :return: None
    :rtype: None
    """
    subprocess.call(f"und create -db {udb_file} -languages {project_languages}", shell=True)


def und_add_files_to_db(udb_file, repository_dir):
    """
    Wrapper for und add shell command. This command adds the files in the repository_dir
    to the udb file.

    :param udb_file: Name of the understand database
    :type udb_file: basestring
    :param repository_dir: Directory where the files to analyse are located
    :type repository_dir: basestring
    :return: None
    :rtype: None
    """
    subprocess.call(f"und add -db {udb_file} {repository_dir}")


def und_setup_setting(udb_file, settings_file_path):
    """
    Wrapper for und settings. This command specifies the path for the setting of the udb files

    :param settings_file_path: The path to the settings file
    :type settings_file_path: basestring
    :param udb_file: Name of the understand database
    :type udb_file: basestring
    :return:
    :rtype:
    """
    subprocess.call(f"und settings @{settings_file_path} {udb_file}")


def und_generate_metrics(udb_file):
    """
    Wrapper for und analyze and und metrics. This command analyses the
    files that were added to the database and generates the metrics in a
    csv file
    :param udb_file: Name of the understand database
    :type udb_file: basestring
    :return: None
    :rtype: None
    """
    log.info(f"Running Analysis for commit: {udb_file} ...")
    subprocess.call(f"und analyze -db {udb_file}")
    log.info("Calculating metrics and creating csv")
    subprocess.call(f"und metrics {udb_file}")


def und_move_to_path(source, target, current_commit):
    os.rename(os.path.join(source, f"{current_commit}.csv"),
              os.path.join(target, f"{current_commit}.csv"))


def und_clean_up(udb_file):
    os.remove(udb_file)


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
    und_setup_setting(udb_commit_file_name, settings_file_name)
    und_generate_metrics(udb_commit_file_name)
    log.info(f"Moving {current_commit}.csv to metric folder")
    und_move_to_path(root_path, metrics_folder_dir, current_commit)
    log.info(f"Removing {udb_commit_file_name}")
    und_clean_up(udb_commit_file_name)

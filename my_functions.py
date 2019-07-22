import pathlib
import os
import shutil


def get_file_names_in_path(mypath):
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
    if os.path.isdir(working_dir):
        shutil.rmtree(working_dir)

    os.makedirs(working_dir)

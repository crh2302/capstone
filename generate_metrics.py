import os
import understand
import git
import logging
import sys
import re


logging.basicConfig(stream=sys.stderr, level=logging.DEBUG,
                    format='{asctime} - {name} - {message}', style='{')
log = logging.getLogger(__name__)


def generate_metrics_by_commit(commit_hash, git_dir, metric_folder, languages ='c++', settings = None):

    """
    Generates metrics for files in a commit and saves it in a specified folder

    :param commit_hash: Commit number to analyse
    :type commit_hash: basestring
    :param git_dir: Directory containing the files that are going to be analyse
    :type git_dir: basestring

    :param metric_folder: Target directory
    :type metric_folder: basestring

    :param languages: Language to analyse (this an Understand™ restriction)
    :type languages: basestring

    :param settings: Source directory of the configurations files (this is an Understand™ restriction)
    :type settings: basestring

    :return: None
    :rtype: None
    """

    while True:  # Todo there is a better way
        '''
        
        '''
        try:
            # Todo The existence of the .git folder should be validated before reaching this point
            git.checkout(os.path.join(git_dir, ".git"), git_dir, commit_hash)
            understand.generate_metrics_by_commit_understand(commit_hash, "c++",
                                                             git_dir,
                                                             'data/settings.txt',
                                                             metric_folder)
            break
        except OSError as e:
            log.error(f"ERROR: An OS error occurred on commit: {e}")


def validate_commit_hash(commit_hash):
    """
    Validates the commit hash. This function checks if the string is :
    1 - Exactly 40 char long
    2 - Is lowercase alphanumeric ( With the exception of the  underscore)

    :param commit_hash: Commit number to analyse
    :type commit_hash: basestring
    :return: True if valid False otherwise
    :rtype: bool
    """
    return True if re.search(r'^[a-z0-9]{40}$', commit_hash) else False


def generate_metric_all_commits(commit_collection, git_dir, metric_folder):
    """

    :param commit_collection: Iterable with collection of commit hashes.
    :type commit_collection: Iterable

    :param git_dir: Directory containing the files that are going to be analyse
    :type git_dir: basestring

    :param metric_folder: Target directory
    :type metric_folder: basestring

    :return: None
    :rtype: None
    """

    for count, current_commit in enumerate(commit_collection):
        log.info("------------------------------- Commit" + str(count) + " --------------------------------")
        #if validate_commit_hash(current_commit):
        generate_metrics_by_commit(current_commit, git_dir, metric_folder)







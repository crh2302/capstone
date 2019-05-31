import subprocess
import logging

log = logging.getLogger(__name__)

# git_repository_url = "https://github.com/git/git.git"


def clone(git_repository_url):
    """
    Wrapper for the git clone shell command. Clones repository if its not already cloned.
    :param git_repository_url: Url of the git repository to clone
    :type git_repository_url: basestring
    :return: None
    :rtype: None
    """
    log.info("Cloning git project from ", git_repository_url)
    output = subprocess.getoutput(f"git clone {git_repository_url}")
    if output == "fatal: destination path 'git' already exists and is not an empty directory.":
        print("destination path 'git' already exists and is not an empty directory.")
    else:
        print(output)


def checkout(git_dir, work_tree, commit):
    """
    Updates files in the working tree to match the version in the index or the specified tree.
    If no paths are given, git checkout will also update HEAD to set the specified branch as the current branch.
    https://git-scm.com/docs/git-checkout
    """
    subprocess.call(f"git --git-dir={git_dir} --work-tree={work_tree} checkout -f {commit}")

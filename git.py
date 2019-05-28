import subprocess
import logging

log = logging.getLogger(__name__)

# git_repository_url = "https://github.com/git/git.git"


def clone(git_repository_url):
    log.info("Cloning git project from ", git_repository_url)
    output = subprocess.getoutput(f"git clone {git_repository_url}")
    if output == "fatal: destination path 'git' already exists and is not an empty directory.":
        print("destination path 'git' already exists and is not an empty directory.")
    else:
        print(output)


def checkout(git_dir, work_tree, commit):
    subprocess.call(f"git --git-dir={git_dir} --work-tree={work_tree} checkout -f {commit}")

import ast
import logging
import os
import shlex
import site
import subprocess
from importlib.util import find_spec
from os.path import join

from setuptools import find_packages

log = logging.getLogger()

HERE = os.path.dirname(__file__)


def normpath(path):
    """ return normalised path """
    return path.replace("\\", "/")


def subprocess_run(cmd, verbose=True):
    """ subprocess_run command string and return output """
    if verbose:
        log.info(cmd)
    if isinstance(cmd, str):
        cmd = shlex.split(cmd)
    result = subprocess.run(cmd, text=True, check=True, capture_output=True)
    return result.stdout


def import2pypi(imports):
    """ return dict of import2pypi name """
    f = open(f"{HERE}/import2pypi.txt")
    rows = [l.lower().split(":") for l in f.read().splitlines()]
    import2pypi = {k: v for k, v in rows}
    pypi = [import2pypi.get(i, i).lower() for i in imports]
    return sorted(pypi)


def git2docker():
    """ add .gitignore to .dockerignore """
    # get gitignore including global
    git = subprocess.getoutput(["git", "status", "--porcelain", "--ignored"])
    git = [r.split()[1] for r in git.splitlines()]

    # add abs path
    root = subprocess.getoutput(["git", "rev-parse", "--show-toplevel"])
    git = ["!" + join(root, r[1:]) if r.startswith("!") else join(root, r) for r in git]

    # get dockerignore up to ####
    docker = []
    if os.path.exists(".dockerignore"):
        with open(".dockerignore") as f:
            for row in f.readlines():
                if row.startswith("####"):
                    break
                docker.append(row.strip("\r\n"))
    docker.append("#### Below added from files ignored by git")
    docker.append(".dockerignore")
    docker.extend(git)
    with open(".dockerignore", "w") as f:
        f.write("\n".join(docker))
